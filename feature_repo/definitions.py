from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float32, String
from datetime import timedelta

feature_source = FileSource(
    path="../data/features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

ticker = Entity(name="ticker", value_type=ValueType.STRING, description="Stock Ticker Symbol")

technical_indicators_view = FeatureView(
    name="technical_indicators",
    entities=[ticker],
    ttl=timedelta(days=3650), # How far back do we look?
    schema=[
        Field(name="rsi_14", dtype=Float32),
        Field(name="macd_line", dtype=Float32),
        Field(name="macd_signal", dtype=Float32),
        Field(name="volatility_24h", dtype=Float32),
    ],
    online=True, 
    source=feature_source,
    tags={"team": "quant_research", "layer": "technical"},
)