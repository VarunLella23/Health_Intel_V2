import pytz
from datetime import datetime

def datetimeformat(value, format='%d-%m-%Y %H:%M:%S %Z'):
    try:
        # Handle both datetime objects and nanosecond timestamps
        if isinstance(value, datetime):
            dt = value.astimezone(pytz.timezone('Asia/Kolkata'))
        else:
            # Convert nanoseconds to seconds
            timestamp = int(value) / 1e9
            utc_time = datetime.utcfromtimestamp(timestamp)
            dt = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
            
        return dt.strftime(format)
    except:
        return 'N/A'