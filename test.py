from datetime import datetime, timedelta, UTC
from zoneinfo import ZoneInfo

expired_at = datetime.now(UTC)+ timedelta(days=30)
print(expired_at)