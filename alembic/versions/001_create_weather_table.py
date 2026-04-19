"""create weather table

Revision ID: 001
Revises:
Create Date: 19.04.2026
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "weather",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("location_name", sa.String(100)),
        sa.Column("last_updated", sa.DateTime),
        sa.Column("wind_kph", sa.Float),
        sa.Column("wind_degree", sa.Integer),
        sa.Column(
            "wind_direction",
            sa.Enum(
                "N","NNE","NE","ENE","E","ESE","SE","SSE",
                "S","SSW","SW","WSW","W","WNW","NW","NNW",
                name="wind_direction_enum"
            )
        ),
        sa.Column("sunrise", sa.String(20)),
        sa.Column("air_quality_Carbon_Monoxide", sa.Float),
        sa.Column("air_quality_Ozone", sa.Float),
        sa.Column("air_quality_Nitrogen_dioxide", sa.Float),
        sa.Column("air_quality_Sulphur_dioxide", sa.Float),
        sa.Column("air_quality_PM25", sa.Float),
        sa.Column("air_quality_PM10", sa.Float),
        sa.Column("air_quality_us_epa_index", sa.Integer),
        sa.Column("air_quality_gb_defra_index", sa.Integer),
    )


def downgrade():
    op.drop_table("weather")
    sa.Enum(name="wind_direction_enum").drop(op.get_bind())