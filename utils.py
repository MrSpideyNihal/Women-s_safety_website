from models import Alert
from datetime import datetime, timedelta

def get_nearby_alerts(lat, lng, radius_km=5):
    """Get alerts within radius_km kilometers of the given coordinates"""
    if not lat or not lng:
        return []
    
    # Basic proximity calculation
    lat_range = radius_km / 111.0  # 1 degree = 111km
    lng_range = radius_km / (111.0 * abs(cos(radians(lat))))
    
    recent = datetime.utcnow() - timedelta(hours=24)
    
    return Alert.query.filter(
        Alert.lat.between(lat - lat_range, lat + lat_range),
        Alert.lng.between(lng - lng_range, lng + lng_range),
        Alert.created_at >= recent
    ).all()
