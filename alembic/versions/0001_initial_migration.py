"""initial migration

Revision ID: 0001
Revises: 
Create Date: 2026-07-22 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('jobs',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('reference_image_url', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'failed', name='jobstatus'), nullable=False),
    sa.Column('generated_prompt', sa.Text(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('jobs')
    op.execute("DROP TYPE jobstatus;")
