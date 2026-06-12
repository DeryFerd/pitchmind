"""Add Stripe subscription id and site audit usage counter."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_billing_fields"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("subscriptions", sa.Column("stripe_subscription_id", sa.String(255)))
    op.add_column(
        "subscriptions",
        sa.Column("site_audits_used_this_period", sa.Integer(), server_default="0", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("subscriptions", "site_audits_used_this_period")
    op.drop_column("subscriptions", "stripe_subscription_id")
