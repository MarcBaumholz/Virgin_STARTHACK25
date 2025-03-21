from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime
from ..models import db, CompanyInitiative, Company, InitiativeMetric, InitiativeParticipant, CallToAction, Feedback
from ..utils.decorators import admin_required

bp = Blueprint('initiatives', __name__)

@bp.route('/initiatives')
def list_initiatives():
    """Display the list of all initiatives."""
    # Get filter parameters
    company_id = request.args.get('company_id', type=int)
    category = request.args.get('category')
    status = request.args.get('status')
    search = request.args.get('search', '').strip()

    # Build query
    query = CompanyInitiative.query

    # Apply filters
    if company_id:
        query = query.filter_by(company_id=company_id)
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                CompanyInitiative.title.ilike(search_term),
                CompanyInitiative.description.ilike(search_term)
            )
        )

    # Get all initiatives
    initiatives = query.order_by(CompanyInitiative.created_at.desc()).all()

    # Get all companies for the filter dropdown
    companies = Company.query.all()

    # Get unique categories for the filter dropdown
    categories = db.session.query(CompanyInitiative.category).distinct().all()
    categories = [cat[0] for cat in categories]

    return render_template('initiatives.html',
                         initiatives=initiatives,
                         companies=companies,
                         categories=categories)

@bp.route('/initiatives/<int:initiative_id>')
def initiative_details(initiative_id):
    """Display detailed information about a specific initiative."""
    initiative = CompanyInitiative.query.get_or_404(initiative_id)
    return render_template('initiative_details.html', initiative=initiative)

@bp.route('/initiatives/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_initiative():
    """Create a new initiative."""
    if request.method == 'POST':
        # Get form data
        company_id = request.form.get('company_id', type=int)
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        goals = request.form.get('goals')
        target_date = datetime.strptime(request.form.get('target_date'), '%Y-%m-%d')

        # Validate required fields
        if not all([company_id, title, description, category, target_date]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('initiatives.create_initiative'))

        # Create new initiative
        initiative = CompanyInitiative(
            company_id=company_id,
            title=title,
            description=description,
            category=category,
            goals=goals,
            target_date=target_date,
            status='planned',
            current_progress=0
        )

        try:
            db.session.add(initiative)
            db.session.commit()
            flash('Initiative created successfully!', 'success')
            return redirect(url_for('initiatives.initiative_details', initiative_id=initiative.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating initiative: {str(e)}")
            flash('An error occurred while creating the initiative.', 'error')
            return redirect(url_for('initiatives.create_initiative'))

    # Get companies for the form
    companies = Company.query.all()
    return render_template('create_initiative.html', companies=companies)

@bp.route('/initiatives/<int:initiative_id>/participate', methods=['POST'])
@login_required
def participate_initiative(initiative_id):
    """Allow a user to participate in an initiative."""
    initiative = CompanyInitiative.query.get_or_404(initiative_id)

    # Check if user is already participating
    if current_user in initiative.participants:
        return jsonify({'error': 'Already participating in this initiative'}), 400

    # Create participant record
    participant = InitiativeParticipant(
        initiative_id=initiative_id,
        user_id=current_user.id,
        role='participant'
    )

    try:
        db.session.add(participant)
        # Award green points for participation
        current_user.add_green_points(10)
        db.session.commit()
        return jsonify({'message': 'Successfully joined the initiative'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error joining initiative: {str(e)}")
        return jsonify({'error': 'Failed to join initiative'}), 500

@bp.route('/initiatives/<int:initiative_id>/feedback', methods=['POST'])
@login_required
def submit_feedback(initiative_id):
    """Submit feedback for an initiative."""
    initiative = CompanyInitiative.query.get_or_404(initiative_id)
    
    # Get form data
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')

    # Validate input
    if not rating or rating < 1 or rating > 5:
        return jsonify({'error': 'Invalid rating'}), 400
    if not comment:
        return jsonify({'error': 'Comment is required'}), 400

    # Create feedback
    feedback = Feedback(
        initiative_id=initiative_id,
        user_id=current_user.id,
        rating=rating,
        comment=comment
    )

    try:
        db.session.add(feedback)
        # Award green points for feedback
        current_user.add_green_points(5)
        db.session.commit()
        return jsonify({
            'message': 'Feedback submitted successfully',
            'feedback': {
                'user': {
                    'username': current_user.username,
                    'avatar_url': current_user.avatar_url
                },
                'rating': rating,
                'comment': comment,
                'created_at': datetime.utcnow().isoformat()
            }
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting feedback: {str(e)}")
        return jsonify({'error': 'Failed to submit feedback'}), 500

@bp.route('/api/initiatives')
def api_initiatives():
    """API endpoint to get filtered initiatives."""
    # Get filter parameters
    company_id = request.args.get('company_id', type=int)
    category = request.args.get('category')
    status = request.args.get('status')
    search = request.args.get('search', '').strip()

    # Build query
    query = CompanyInitiative.query

    # Apply filters
    if company_id:
        query = query.filter_by(company_id=company_id)
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                CompanyInitiative.title.ilike(search_term),
                CompanyInitiative.description.ilike(search_term)
            )
        )

    # Get initiatives
    initiatives = query.order_by(CompanyInitiative.created_at.desc()).all()

    # Format response
    return jsonify([{
        'id': i.id,
        'title': i.title,
        'description': i.description,
        'category': i.category,
        'status': i.status,
        'progress': i.current_progress,
        'participants': len(i.participants),
        'company': {
            'id': i.company.id,
            'name': i.company.name,
            'logo_url': i.company.logo_url
        }
    } for i in initiatives])

@bp.route('/api/initiatives/<int:initiative_id>/metrics')
def api_initiative_metrics(initiative_id):
    """API endpoint to get metrics for a specific initiative."""
    initiative = CompanyInitiative.query.get_or_404(initiative_id)
    
    return jsonify([{
        'name': m.name,
        'value': m.value,
        'target': m.target,
        'unit': m.unit
    } for m in initiative.metrics]) 