"""Add email digest preference on users."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003_user_email_prefs"
down_revision: Union[str, None] = "002_billing_fields"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("email_digest_enabled", sa.Boolean(), server_default="true", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("users", "email_digest_enabled")
