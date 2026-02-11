from pipelines.ingest_google_flights import IngestGoogleFlights
from pipelines import checkpoint
from pathlib import Path


"""driver = IngestGoogleFlights()
driver.run_driver()
"""

driver = checkpoint.process_jsonl_incremental(Path("data/bronze/bronze_flights_raw.jsonl"), Path("data/checkpoints/bronze_flights_raw.offset"))