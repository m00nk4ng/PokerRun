"""Update column names to match frontend

Revision ID: 91104b790239
Revises: 3c3fcbfd13b5
Create Date: 2026-01-27 18:21:51.300442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91104b790239'
down_revision: Union[str, Sequence[str], None] = '3c3fcbfd13b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop FK that currently points entries.person_id -> people.id
    op.drop_constraint(
        "entries_person_id_fkey",
        "entries",
        type_="foreignkey",
    )


    # Rename people -> player
    op.rename_table("people", "player")

    op.alter_column("player", "first_name", new_column_name="firstName")
    op.alter_column("player", "last_name", new_column_name="lastName")
    op.alter_column("player", "city", new_column_name="townOrCity")
    op.alter_column("player", "province_or_territory", new_column_name="provinceOrTerritory")
    op.alter_column("player", "postal_code", new_column_name="postalCode")
    op.alter_column("player", "phone_number", new_column_name="phoneNumber")
    op.alter_column("player", "created_at", new_column_name="createdAt")
    op.alter_column("player", "updated_at", new_column_name="updatedAt")

    # Rename entries -> hand
    op.rename_table("entries", "hand")

    op.alter_column("hand", "person_id", new_column_name="playerId")
    op.alter_column("hand", "hands", new_column_name="cards")
    op.alter_column("hand", "created_at", new_column_name="createdAt")
    op.alter_column("hand", "updated_at", new_column_name="updatedAt")


    # Recreate FK: hand.playerId -> player.id
    op.create_foreign_key(
        "hand_playerId_fkey",
        "hand",
        "player",
        ["playerId"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # Drop the FK we created: hand.playerId -> player.id
    op.drop_constraint("hand_playerId_fkey", "hand", type_="foreignkey")

    # Reverse hand column renames
    op.alter_column("hand", "updatedAt", new_column_name="updated_at")
    op.alter_column("hand", "createdAt", new_column_name="created_at")
    op.alter_column("hand", "cards", new_column_name="hands")
    op.alter_column("hand", "playerId", new_column_name="person_id")

    # Rename hand -> entries
    op.rename_table("hand", "entries")

    # Reverse player column renames
    op.alter_column("player", "updatedAt", new_column_name="updated_at")
    op.alter_column("player", "createdAt", new_column_name="created_at")
    op.alter_column("player", "phoneNumber", new_column_name="phone_number")
    op.alter_column("player", "postalCode", new_column_name="postal_code")
    op.alter_column("player", "provinceOrTerritory", new_column_name="province_or_territory")
    op.alter_column("player", "townOrCity", new_column_name="city")
    op.alter_column("player", "lastName", new_column_name="last_name")
    op.alter_column("player", "firstName", new_column_name="first_name")

    # Rename player -> people
    op.rename_table("player", "people")

    # Recreate original FK: entries.person_id -> people.id
    op.create_foreign_key(
        "entries_person_id_fkey",
        "entries",
        "people",
        ["person_id"],
        ["id"],
        ondelete="CASCADE",
    )
