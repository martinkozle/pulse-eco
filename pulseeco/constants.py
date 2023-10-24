import datetime

PULSE_ECO_BASE_URL = "https://{city_name}.pulse.eco/rest/{end_point}"
DATA_RAW_MAX_SPAN = datetime.timedelta(days=7)
AVG_DATA_MAX_SPAN = datetime.timedelta(days=365)
