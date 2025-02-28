from models import Alert
from datetime import datetime, timedelta
from math import cos, radians
from datetime import datetime, timedelta

from datetime import datetime, timedelta

def get_nearby_alerts(lat, lng, radius_km=5):
    if not lat or not lng:
        return []
    
    lat_range = radius_km / 111.0
    lng_range = radius_km / (111.0 * abs(cos(radians(lat))))
    
    recent = datetime.utcnow() - timedelta(hours=48)  # Changed from 24 to 48 hours
    
    return Alert.query.filter(
        Alert.lat.between(lat - lat_range, lat + lat_range),
        Alert.lng.between(lng - lng_range, lng + lng_range),
        Alert.created_at >= recent
    ).all()
