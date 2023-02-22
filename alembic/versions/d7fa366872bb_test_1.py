"""test 1

Revision ID: d7fa366872bb
Revises: 
Create Date: 2023-02-16 17:24:51.381918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7fa366872bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO public.user_tbl (user_img_url, age, mbti, created_at, created_by) 
        VALUES ('example.com', '1991-01-01', 'INTJ', '2023-01-01', 'JSR')
    """)


def downgrade() -> None:
    pass
