

from datetime import datetime, timezone

from zoneinfo import ZoneInfo


async def get_current_time():
    
    try:
        current_time = datetime.now(timezone.utc)
        print("grabbed the current time")
    except Exception as e:
        print("Failed to grab the current time")
        print(f"Exception = {e}")
        
        
    return current_time


def convert_to_user_time(date, zone_name):
    # Convert timestamp integers to datetime
    if isinstance(date, int):
        date = datetime.fromtimestamp(date, tz=timezone.utc)

    # If naive datetime, assume Africa/Nairobi
    if date.tzinfo is None:
        date = date.replace(tzinfo=ZoneInfo("Africa/Nairobi")) #since the first few users joined when date_time columns lacked timezone

    try:
        return date.astimezone(ZoneInfo(zone_name))
    except Exception as e:
        print(f"Exception = {e}")
        return date.astimezone(timezone.utc)