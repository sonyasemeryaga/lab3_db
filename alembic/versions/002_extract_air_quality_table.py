"""extract air quality table

Revision ID: 002
Revises: 001
Create Date: 19.04.2026
"""
from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "air_quality",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("weather_id", sa.Integer, sa.ForeignKey("weather.id"), nullable=False),
        sa.Column("carbon_monoxide", sa.Float),
        sa.Column("ozone", sa.Float),
        sa.Column("nitrogen_dioxide", sa.Float),
        sa.Column("sulphur_dioxide", sa.Float),
        sa.Column("pm25", sa.Float),
        sa.Column("pm10", sa.Float),
        sa.Column("us_epa_index", sa.Integer),
        sa.Column("gb_defra_index", sa.Integer),
    )

    op.execute("""
        INSERT INTO air_quality (
            weather_id, carbon_monoxide, ozone, nitrogen_dioxide,
            sulphur_dioxide, pm25, pm10, us_epa_index, gb_defra_index
        )
        SELECT
            id,
            "air_quality_Carbon_Monoxide",
            "air_quality_Ozone",
            "air_quality_Nitrogen_dioxide",
            "air_quality_Sulphur_dioxide",
            "air_quality_PM25",
            "air_quality_PM10",
            "air_quality_us_epa_index",
            "air_quality_gb_defra_index"
        FROM weather
    """)

    op.drop_column("weather", "air_quality_Carbon_Monoxide")
    op.drop_column("weather", "air_quality_Ozone")
    op.drop_column("weather", "air_quality_Nitrogen_dioxide")
    op.drop_column("weather", "air_quality_Sulphur_dioxide")
    op.drop_column("weather", "air_quality_PM25")
    op.drop_column("weather", "air_quality_PM10")
    op.drop_column("weather", "air_quality_us_epa_index")
    op.drop_column("weather", "air_quality_gb_defra_index")


def downgrade():
    op.add_column("weather", sa.Column("air_quality_Carbon_Monoxide", sa.Float))
    op.add_column("weather", sa.Column("air_quality_Ozone", sa.Float))
    op.add_column("weather", sa.Column("air_quality_Nitrogen_dioxide", sa.Float))
    op.add_column("weather", sa.Column("air_quality_Sulphur_dioxide", sa.Float))
    op.add_column("weather", sa.Column("air_quality_PM25", sa.Float))
    op.add_column("weather", sa.Column("air_quality_PM10", sa.Float))
    op.add_column("weather", sa.Column("air_quality_us_epa_index", sa.Integer))
    op.add_column("weather", sa.Column("air_quality_gb_defra_index", sa.Integer))

    op.execute("""
        UPDATE weather w
        SET
            "air_quality_Carbon_Monoxide"  = aq.carbon_monoxide,
            "air_quality_Ozone"            = aq.ozone,
            "air_quality_Nitrogen_dioxide" = aq.nitrogen_dioxide,
            "air_quality_Sulphur_dioxide"  = aq.sulphur_dioxide,
            "air_quality_PM25"             = aq.pm25,
            "air_quality_PM10"             = aq.pm10,
            "air_quality_us_epa_index"     = aq.us_epa_index,
            "air_quality_gb_defra_index"   = aq.gb_defra_index
        FROM air_quality aq
        WHERE w.id = aq.weather_id
    """)

    op.drop_table("air_quality")