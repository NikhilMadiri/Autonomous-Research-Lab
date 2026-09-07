"""Add literature records linked to research questions."""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0002_literature"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

literature_status = postgresql.ENUM(
    "not_reviewed",
    "reading",
    "reviewed",
    name="literaturestatus",
    create_type=False,
)


def upgrade():
    bind = op.get_bind()
    literature_status.create(bind, checkfirst=True)

    op.create_table(
        "literature",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "question_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("research_questions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("authors", sa.String(1000)),
        sa.Column("year", sa.Integer()),
        sa.Column("journal", sa.String(500)),
        sa.Column("doi", sa.String(255)),
        sa.Column("url", sa.String(2048)),
        sa.Column("abstract", sa.Text()),
        sa.Column("notes", sa.Text()),
        sa.Column("citation", sa.Text()),
        sa.Column("status", literature_status, nullable=False, server_default="not_reviewed"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )
    op.create_index(
        "ix_literature_question_id",
        "literature",
        ["question_id"],
    )


def downgrade():
    op.drop_index("ix_literature_question_id", table_name="literature")
    op.drop_table("literature")
    literature_status.drop(op.get_bind(), checkfirst=True)
