# dummyDB.py

# Expanded dummy train data with more interconnected routes
trains = [
    # Delhi Hub Routes
    {
        "train_id": "DEL-MUM-01",
        "train_name": "Delhi Mumbai Express",
        "source": "Delhi",
        "destination": "Mumbai",
        "departure_time": "08:00",
        "arrival_time": "20:00",
        "days_available": ["Mon", "Wed", "Fri"],
        "seats_available": 50,
        "popularity": 0.8  # Higher value means more crowded
    },
    {
        "train_id": "DEL-KOL-01",
        "train_name": "Delhi Kolkata Rajdhani",
        "source": "Delhi",
        "destination": "Kolkata",
        "departure_time": "16:30",
        "arrival_time": "08:30",
        "days_available": ["Daily"],
        "seats_available": 45,
        "popularity": 0.7
    },
    {
        "train_id": "DEL-LKO-01",
        "train_name": "Delhi Lucknow Shatabdi",
        "source": "Delhi",
        "destination": "Lucknow",
        "departure_time": "06:10",
        "arrival_time": "12:00",
        "days_available": ["Daily"],
        "seats_available": 60,
        "popularity": 0.6
    },
    
    # Mumbai Hub Routes
    {
        "train_id": "MUM-BLR-01",
        "train_name": "Mumbai Bangalore Express",
        "source": "Mumbai",
        "destination": "Bangalore",
        "departure_time": "14:30",
        "arrival_time": "06:30",
        "days_available": ["Tue", "Thu", "Sat"],
        "seats_available": 55,
        "popularity": 0.75
    },
    {
        "train_id": "MUM-AMD-01",
        "train_name": "Mumbai Ahmedabad Tejas",
        "source": "Mumbai",
        "destination": "Ahmedabad",
        "departure_time": "07:00",
        "arrival_time": "13:30",
        "days_available": ["Daily"],
        "seats_available": 70,
        "popularity": 0.65
    },
    
    # Bangalore Hub Routes
    {
        "train_id": "BLR-CHE-01",
        "train_name": "Bangalore Chennai Shatabdi",
        "source": "Bangalore",
        "destination": "Chennai",
        "departure_time": "06:00",
        "arrival_time": "11:00",
        "days_available": ["Daily"],
        "seats_available": 65,
        "popularity": 0.7
    },
    {
        "train_id": "BLR-HYD-01",
        "train_name": "Bangalore Hyderabad Express",
        "source": "Bangalore",
        "destination": "Hyderabad",
        "departure_time": "20:00",
        "arrival_time": "06:00",
        "days_available": ["Daily"],
        "seats_available": 80,
        "popularity": 0.6
    },
    
    # Chennai Hub Routes
    {
        "train_id": "CHE-KOL-01",
        "train_name": "Chennai Kolkata Express",
        "source": "Chennai",
        "destination": "Kolkata",
        "departure_time": "14:30",
        "arrival_time": "18:30",
        "days_available": ["Wed", "Sat"],
        "seats_available": 40,
        "popularity": 0.5
    },
    {
        "train_id": "CHE-HYD-01",
        "train_name": "Chennai Hyderabad Express",
        "source": "Chennai",
        "destination": "Hyderabad",
        "departure_time": "16:00",
        "arrival_time": "04:00",
        "days_available": ["Daily"],
        "seats_available": 75,
        "popularity": 0.7
    },
    
    # Kolkata Hub Routes
    {
        "train_id": "KOL-GHY-01",
        "train_name": "Kolkata Guwahati Express",
        "source": "Kolkata",
        "destination": "Guwahati",
        "departure_time": "10:00",
        "arrival_time": "04:00",
        "days_available": ["Mon", "Thu", "Sun"],
        "seats_available": 35,
        "popularity": 0.4
    },
    
    # Lucknow Hub Routes
    {
        "train_id": "LKO-PTN-01",
        "train_name": "Lucknow Patna Express",
        "source": "Lucknow",
        "destination": "Patna",
        "departure_time": "14:00",
        "arrival_time": "22:00",
        "days_available": ["Daily"],
        "seats_available": 85,
        "popularity": 0.6
    },
    
    # Ahmedabad Hub Routes
    {
        "train_id": "AMD-JAI-01",
        "train_name": "Ahmedabad Jaipur Express",
        "source": "Ahmedabad",
        "destination": "Jaipur",
        "departure_time": "15:00",
        "arrival_time": "23:00",
        "days_available": ["Daily"],
        "seats_available": 90,
        "popularity": 0.7
    },
    {
        "train_id": "AMD-DEL-01",
        "train_name": "Ahmedabad Delhi Express",
        "source": "Ahmedabad",
        "destination": "Delhi",
        "departure_time": "18:00",
        "arrival_time": "06:00",
        "days_available": ["Daily"],
        "seats_available": 65,
        "popularity": 0.8
    },
    
    # Hyderabad Hub Routes
    {
        "train_id": "HYD-NGP-01",
        "train_name": "Hyderabad Nagpur Express",
        "source": "Hyderabad",
        "destination": "Nagpur",
        "departure_time": "07:30",
        "arrival_time": "16:30",
        "days_available": ["Daily"],
        "seats_available": 70,
        "popularity": 0.6
    },
    
    # Return routes (reverse journeys)
    {
        "train_id": "MUM-DEL-01",
        "train_name": "Mumbai Delhi Express",
        "source": "Mumbai",
        "destination": "Delhi",
        "departure_time": "21:30",
        "arrival_time": "09:30",
        "days_available": ["Tue", "Thu", "Sat"],
        "seats_available": 50,
        "popularity": 0.8
    },
    {
        "train_id": "BLR-MUM-01",
        "train_name": "Bangalore Mumbai Express",
        "source": "Bangalore",
        "destination": "Mumbai",
        "departure_time": "19:30",
        "arrival_time": "11:30",
        "days_available": ["Mon", "Wed", "Fri"],
        "seats_available": 55,
        "popularity": 0.7
    }
]

NEARBY_STATIONS = {
    "Mumbai": ["Thane", "Kalyan"],
    "Delhi": ["Ghaziabad", "Noida"],
    "Bangalore": ["Whitefield", "Kengeri"],
    "Chennai": ["Tambaram", "Avadi"],
    "Kolkata": ["Howrah", "Sealdah"],
    "Hyderabad": ["Secunderabad", "Lingampally"],
    "Ahmedabad": ["Gandhinagar", "Vadodara"],
    "Lucknow": ["Kanpur", "Barabanki"]
}

def get_trains(source, destination=None):
    """Fetch trains by source and optional destination"""
    if destination:
        return [train for train in trains if train["source"] == source and train["destination"] == destination]
    else:
        # Group trains by destination if no destination is provided
        destinations = {}
        for train in trains:
            if train["source"] == source:
                if train["destination"] not in destinations:
                    destinations[train["destination"]] = []
                destinations[train["destination"]].append(train)
        return destinations

def get_all_trains():
    """Fetch all trains"""
    return trains

def get_nearby_stations(station):
    """Get nearby stations for a given station"""
    return NEARBY_STATIONS.get(station, [])