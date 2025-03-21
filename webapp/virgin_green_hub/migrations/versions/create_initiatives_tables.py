"""create initiatives tables

Revision ID: create_initiatives_tables
Revises: previous_migration
Create Date: 2024-02-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'create_initiatives_tables'
down_revision = 'previous_migration'  # Replace with the actual previous migration ID
branch_labels = None
depends_on = None

def upgrade():
    # Create companies table
    op.create_table('companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('logo_url', sa.String(length=255), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )

    # Create company_initiatives table
    op.create_table('company_initiatives',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('goals', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, default='planned'),
        sa.Column('current_progress', sa.Integer(), nullable=False, default=0),
        sa.Column('target_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create initiative_metrics table
    op.create_table('initiative_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('initiative_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('value', sa.Float(), nullable=False, default=0),
        sa.Column('target', sa.Float(), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.ForeignKeyConstraint(['initiative_id'], ['company_initiatives.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create initiative_participants table
    op.create_table('initiative_participants',
        sa.Column('initiative_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False, default='participant'),
        sa.Column('joined_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['initiative_id'], ['company_initiatives.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('initiative_id', 'user_id')
    )

    # Create call_to_actions table
    op.create_table('call_to_actions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('initiative_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=255), nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.ForeignKeyConstraint(['initiative_id'], ['company_initiatives.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create feedback table
    op.create_table('feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('initiative_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.ForeignKeyConstraint(['initiative_id'], ['company_initiatives.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop tables in reverse order
    op.drop_table('feedback')
    op.drop_table('call_to_actions')
    op.drop_table('initiative_participants')
    op.drop_table('initiative_metrics')
    op.drop_table('company_initiatives')
    op.drop_table('companies') 