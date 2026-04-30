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
    air_quality_table = op.create_table(
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

    bind = op.get_bind()
    meta = sa.MetaData()
    weather_table = sa.Table("weather", meta, autoload_with=bind)

    op.execute(
        sa.insert(air_quality_table).from_select(
            [
                "weather_id",
                "carbon_monoxide",
                "ozone",
                "nitrogen_dioxide",
                "sulphur_dioxide",
                "pm25",
                "pm10",
                "us_epa_index",
                "gb_defra_index",
            ],
            sa.select(
                weather_table.c.id,
                weather_table.c.air_quality_carbon_monoxide,
                weather_table.c.air_quality_ozone,
                weather_table.c.air_quality_nitrogen_dioxide,
                weather_table.c.air_quality_sulphur_dioxide,
                weather_table.c.air_quality_pm25,
                weather_table.c.air_quality_pm10,
                weather_table.c.air_quality_us_epa_index,
                weather_table.c.air_quality_gb_defra_index,
            )
        )
    )

    op.drop_column("weather", "air_quality_carbon_monoxide")
    op.drop_column("weather", "air_quality_ozone")
    op.drop_column("weather", "air_quality_nitrogen_dioxide")
    op.drop_column("weather", "air_quality_sulphur_dioxide")
    op.drop_column("weather", "air_quality_pm25")
    op.drop_column("weather", "air_quality_pm10")
    op.drop_column("weather", "air_quality_us_epa_index")
    op.drop_column("weather", "air_quality_gb_defra_index")


def downgrade():
    op.add_column("weather", sa.Column("air_quality_carbon_monoxide", sa.Float))
    op.add_column("weather", sa.Column("air_quality_ozone", sa.Float))
    op.add_column("weather", sa.Column("air_quality_nitrogen_dioxide", sa.Float))
    op.add_column("weather", sa.Column("air_quality_sulphur_dioxide", sa.Float))
    op.add_column("weather", sa.Column("air_quality_pm25", sa.Float))
    op.add_column("weather", sa.Column("air_quality_pm10", sa.Float))
    op.add_column("weather", sa.Column("air_quality_us_epa_index", sa.Integer))
    op.add_column("weather", sa.Column("air_quality_gb_defra_index", sa.Integer))

    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == 'postgresql':
        op.execute("""
            UPDATE weather w
            SET
                air_quality_carbon_monoxide  = aq.carbon_monoxide,
                air_quality_ozone            = aq.ozone,
                air_quality_nitrogen_dioxide = aq.nitrogen_dioxide,
                air_quality_sulphur_dioxide  = aq.sulphur_dioxide,
                air_quality_pm25             = aq.pm25,
                air_quality_pm10             = aq.pm10,
                air_quality_us_epa_index     = aq.us_epa_index,
                air_quality_gb_defra_index   = aq.gb_defra_index
            FROM air_quality aq
            WHERE w.id = aq.weather_id
        """)
    else:
        op.execute("""
            UPDATE weather w
            JOIN air_quality aq ON w.id = aq.weather_id
            SET
                w.air_quality_carbon_monoxide  = aq.carbon_monoxide,
                w.air_quality_ozone            = aq.ozone,
                w.air_quality_nitrogen_dioxide = aq.nitrogen_dioxide,
                w.air_quality_sulphur_dioxide  = aq.sulphur_dioxide,
                w.air_quality_pm25             = aq.pm25,
                w.air_quality_pm10             = aq.pm10,
                w.air_quality_us_epa_index     = aq.us_epa_index,
                w.air_quality_gb_defra_index   = aq.gb_defra_index
        """)

    op.drop_table("air_quality")