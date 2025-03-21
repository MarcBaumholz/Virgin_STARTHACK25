from datetime import datetime
from .. import db
from .user import User

class Company(db.Model):
    """Model for Virgin companies."""
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(255))
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    initiatives = db.relationship('CompanyInitiative', backref='company', lazy=True)

    def __repr__(self):
        return f'<Company {self.name}>'

class CompanyInitiative(db.Model):
    """Model for company sustainability initiatives."""
    __tablename__ = 'company_initiatives'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    goals = db.Column(db.Text)
    status = db.Column(db.String(20), default='planned')  # planned, active, completed
    current_progress = db.Column(db.Integer, default=0)  # 0-100
    target_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    metrics = db.relationship('InitiativeMetric', backref='initiative', lazy=True, cascade='all, delete-orphan')
    participants = db.relationship('User', secondary='initiative_participants', backref='initiatives')
    call_to_actions = db.relationship('CallToAction', backref='initiative', lazy=True, cascade='all, delete-orphan')
    feedback = db.relationship('Feedback', backref='initiative', lazy=True, cascade='all, delete-orphan')

    @property
    def status_color(self):
        """Return the Bootstrap color class for the initiative status."""
        colors = {
            'planned': 'primary',
            'active': 'success',
            'completed': 'secondary'
        }
        return colors.get(self.status, 'info')

    @property
    def days_remaining(self):
        """Calculate the number of days remaining until the target date."""
        if self.status == 'completed':
            return 0
        delta = self.target_date - datetime.utcnow()
        return max(0, delta.days)

    @property
    def total_points_earned(self):
        """Calculate the total green points earned by all participants."""
        return len(self.participants) * 10  # 10 points per participant

    def __repr__(self):
        return f'<CompanyInitiative {self.title}>'

class InitiativeMetric(db.Model):
    """Model for tracking initiative metrics."""
    __tablename__ = 'initiative_metrics'

    id = db.Column(db.Integer, primary_key=True)
    initiative_id = db.Column(db.Integer, db.ForeignKey('company_initiatives.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, default=0)
    target = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<InitiativeMetric {self.name}>'

# Association table for initiative participants
initiative_participants = db.Table('initiative_participants',
    db.Column('initiative_id', db.Integer, db.ForeignKey('company_initiatives.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role', db.String(20), default='participant'),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

class CallToAction(db.Model):
    """Model for initiative call-to-action buttons."""
    __tablename__ = 'call_to_actions'

    id = db.Column(db.Integer, primary_key=True)
    initiative_id = db.Column(db.Integer, db.ForeignKey('company_initiatives.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50))  # Font Awesome icon name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CallToAction {self.title}>'

class Feedback(db.Model):
    """Model for initiative feedback."""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    initiative_id = db.Column(db.Integer, db.ForeignKey('company_initiatives.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='feedback')

    def __repr__(self):
        return f'<Feedback {self.id}>' 