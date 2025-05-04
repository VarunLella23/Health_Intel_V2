import datetime
import pytz
import logging
from datetime import timezone
from typing import Dict, List, Union
# from auth.auth import authenticate_google_fit

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data source configurations
DATA_SOURCES = {
    'steps': 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps',
    'heart_rate': 'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm',
    'distance': 'derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta',
    'calories': 'derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended',
    'activity': 'derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments',
    'glucose': 'derived:com.google.blood_glucose:com.google.android.gms:merge_blood_glucose',
    'blood_pressure': 'derived:com.google.blood_pressure:com.google.android.gms:merge_blood_pressure',
    'nutrition': 'derived:com.google.nutrition:com.google.android.gms:merge_nutrition'
}

ACTIVITY_MAP = {
    0: 'In Vehicle', 1: 'Biking', 2: 'On Foot', 3: 'Still', 4: 'Unknown',
    5: 'Tilting', 7: 'Walking', 8: 'Running', 9: 'Aerobics', 10: 'Badminton',
    11: 'Baseball', 12: 'Basketball', 13: 'Biathlon', 14: 'Handbiking',
    16: 'Crossfit', 17: 'Curling', 19: 'Dancing', 20: 'Elliptical',
    21: 'Ergometer', 22: 'Fencing', 23: 'Football (American)',
    24: 'Football (Australian)', 25: 'Football (Soccer)', 26: 'Frisbee',
    27: 'Gardening', 28: 'Golf', 29: 'Gymnastics', 30: 'Handball',
    31: 'Hiking', 32: 'Hockey', 33: 'Horseback Riding', 34: 'Housework',
    35: 'Ice Skating', 36: 'In Vehicle', 37: 'Jumping Rope', 38: 'Kayaking',
    39: 'Kettlebell Training', 40: 'Kickboxing', 41: 'Kitesurfing',
    42: 'Martial Arts', 43: 'Meditation', 44: 'Mixed Martial Arts',
    45: 'P90X Exercises', 46: 'Paragliding', 47: 'Pilates', 48: 'Polo',
    49: 'Racquetball', 50: 'Rock Climbing', 51: 'Rowing', 52: 'Rowing Machine',
    53: 'Rugby', 54: 'Running', 55: 'Jogging', 56: 'Sailing', 57: 'Scuba Diving',
    58: 'Skateboarding', 59: 'Skating', 60: 'Cross Skating', 61: 'Skiing',
    62: 'Back-Country Skiing', 63: 'Kite Skiing', 64: 'Roller Skiing',
    65: 'Sledding', 66: 'Sleeping', 67: 'Light Sleep', 68: 'Deep Sleep',
    69: 'REM Sleep', 70: 'Awake (during sleep)', 71: 'Snowboarding',
    72: 'Snowmobile', 73: 'Snowshoeing', 74: 'Squash', 75: 'Stair Climbing',
    76: 'Stair-Climbing Machine', 77: 'Stand-up Paddleboarding', 78: 'Strength Training',
    79: 'Surfing', 80: 'Swimming', 81: 'Swimming (open water)', 82: 'Swimming (pool)',
    83: 'Table Tennis', 84: 'Team Sports', 85: 'Tennis', 86: 'Treadmill',
    87: 'Volleyball', 88: 'Volleyball (Beach)', 89: 'Volleyball (Indoor)',
    90: 'Wakeboarding', 91: 'Walking', 92: 'Water Polo', 93: 'Weightlifting',
    94: 'Wheelchair', 95: 'Windsurfing', 96: 'Yoga', 97: 'Zumba', 108: 'Interval Training'
}

def to_nanoseconds(dt: datetime.datetime) -> int:
    """Convert datetime to nanoseconds since epoch"""
    return int(dt.timestamp() * 1e9)

def get_time_range() -> Dict[str, Union[datetime.datetime, int]]:
    """Get IST time range for the current day with validation"""
    try:
        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.datetime.now(tz)
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        return {
            'start_ns': to_nanoseconds(start.astimezone(timezone.utc)),
            'end_ns': to_nanoseconds(now.astimezone(timezone.utc)),
            'start_time': start,
            'end_time': now
        }
    except Exception as e:
        logger.error(f"Time range error: {str(e)}")
        return {
            'start_ns': 0,
            'end_ns': 0,
            'start_time': None,
            'end_time': None
        }

def fetch_dataset(service, data_source: str, start_ns: int, end_ns: int):
    """Generic dataset fetcher with error handling"""
    try:
        return service.users().dataSources().datasets().get(
            userId='me',
            dataSourceId=data_source,
            datasetId=f"{start_ns}-{end_ns}"
        ).execute()
    except Exception as e:
        logger.warning(f"Failed to fetch {data_source}: {str(e)}")
        return {'point': []}

def get_steps(service, time_range: dict) -> int:
    """Get total daily steps with enhanced validation"""
    data = fetch_dataset(service, DATA_SOURCES['steps'], 
                       time_range['start_ns'], time_range['end_ns'])
    total = 0
    
    for point in data.get('point', []):
        try:
            # Validate data point structure
            if not isinstance(point, dict):
                continue
                
            values = point.get('value', [{}])
            if not isinstance(values, list) or len(values) < 1:
                continue
                
            steps = values[0].get('intVal', 0)
            if isinstance(steps, (int, float)) and steps >= 0:
                total += int(steps)
                
        except (KeyError, TypeError, ValueError) as e:
            logger.warning(f"Invalid step data point: {str(e)}")
            continue
            
    logger.info(f"Total steps retrieved: {total}")
    return total

def get_heart_data(service, time_range: dict) -> Dict:
    """Get heart-related data including blood pressure"""
    heart_rates = []
    blood_pressure = []
    
    try:
        # Heart rate data
        rate_data = fetch_dataset(service, DATA_SOURCES['heart_rate'], 
                                time_range['start_ns'], time_range['end_ns'])
        for point in rate_data.get('point', []):
            try:
                heart_rates.append({
                    'time': point['startTimeNanos'],
                    'bpm': round(float(point['value'][0]['fpVal']), 1)
                })
            except (KeyError, IndexError, ValueError):
                continue

        # Blood pressure data
        pressure_data = fetch_dataset(service, DATA_SOURCES['blood_pressure'], 
                                    time_range['start_ns'], time_range['end_ns'])
        for point in pressure_data.get('point', []):
            try:
                blood_pressure.append({
                    'systolic': round(float(point['value'][0]['fpVal']), 1),
                    'diastolic': round(float(point['value'][1]['fpVal']), 1),
                    'time': point['startTimeNanos']
                })
            except (KeyError, IndexError, ValueError):
                continue
    except Exception as e:
        logger.error(f"Heart data error: {str(e)}")

    return {
        'rate': heart_rates,
        'pressure': blood_pressure
    }

def get_distance(service, time_range: dict) -> float:
    """Get total distance in kilometers"""
    data = fetch_dataset(service, DATA_SOURCES['distance'], 
                       time_range['start_ns'], time_range['end_ns'])
    total_meters = 0.0
    for point in data.get('point', []):
        try:
            if 'value' in point and len(point['value']) > 0:
                total_meters += float(point['value'][0].get('fpVal', 0))
        except (KeyError, ValueError, TypeError):
            continue
    return round(total_meters / 1000, 2)

def get_calories(service, time_range: dict) -> float:
    """Get total calories expended"""
    data = fetch_dataset(service, DATA_SOURCES['calories'], 
                       time_range['start_ns'], time_range['end_ns'])
    total = 0.0
    for point in data.get('point', []):
        try:
            if 'value' in point and len(point['value']) > 0:
                total += float(point['value'][0].get('fpVal', 0))
        except (KeyError, ValueError, TypeError):
            continue
    return round(total, 1)

def get_glucose(service, time_range: dict) -> List[Dict]:
    """Get blood glucose measurements"""
    data = fetch_dataset(service, DATA_SOURCES['glucose'], 
                       time_range['start_ns'], time_range['end_ns'])
    readings = []
    for point in data.get('point', []):
        try:
            readings.append({
                'time': point['startTimeNanos'],
                'value': round(float(point['value'][0]['fpVal']), 1),
                'meal_type': point.get('originDataSourceId', '').split(':')[-1]
            })
        except (KeyError, IndexError, ValueError):
            continue
    return readings

def get_nutrition(service, time_range: dict) -> List[Dict]:
    """Get nutritional data"""
    data = fetch_dataset(service, DATA_SOURCES['nutrition'], 
                       time_range['start_ns'], time_range['end_ns'])
    nutrients = []
    for point in data.get('point', []):
        try:
            nutrients.append({
                'name': str(point['value'][0]['stringVal']),
                'value': round(float(point['value'][1]['fpVal']), 1),
                'unit': str(point['value'][2]['stringVal'])
            })
        except (KeyError, IndexError, ValueError):
            continue
    return nutrients

def get_activities(service, time_range: dict) -> List[Dict]:
    """Get physical activity segments with validation"""
    data = fetch_dataset(service, DATA_SOURCES['activity'], 
                       time_range['start_ns'], time_range['end_ns'])
    activities = []
    
    for point in data.get('point', []):
        try:
            start_ns = int(point['startTimeNanos'])
            end_ns = int(point['endTimeNanos'])
            
            if start_ns <= 0 or end_ns <= 0 or (end_ns - start_ns) <= 0:
                continue
                
            activity_code = int(point['value'][0]['intVal'])
            activity_name = ACTIVITY_MAP.get(activity_code, f"Unknown ({activity_code})")
            
            activities.append({
                'start': start_ns,
                'end': end_ns,
                'activity': activity_name,
                'duration': (end_ns - start_ns) / 1e9  # Duration in seconds
            })
        except (KeyError, ValueError, TypeError) as e:
            logger.warning(f"Invalid activity point: {str(e)}")
            continue
            
    return activities

def get_fitness_data() -> Dict:
    """Main function to aggregate all health data"""
    try:
        service = authenticate_google_fit()
        time_range = get_time_range()
        
        return {
            'time_range': time_range,
            'metrics': {
                'steps': get_steps(service, time_range),
                'heart': get_heart_data(service, time_range),
                'distance': get_distance(service, time_range),
                'calories': get_calories(service, time_range),
                'glucose': get_glucose(service, time_range),
                'nutrition': get_nutrition(service, time_range),
                'activities': get_activities(service, time_range)
            },
            'success': True
        }
    except Exception as e:
        logger.error(f"Data fetch failed: {str(e)}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        }