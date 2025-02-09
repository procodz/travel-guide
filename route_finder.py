# route_finder.py

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Route:
    legs: List[Dict]
    total_duration: int
    total_wait_time: int
    transfers: int

def calculate_duration(departure: str, arrival: str) -> int:
    """Calculate duration in minutes between departure and arrival times."""
    dep = datetime.strptime(departure, "%H:%M")
    arr = datetime.strptime(arrival, "%H:%M")
    duration = arr - dep
    if duration.days < 0:  # Handle overnight journeys
        duration += timedelta(days=1)
    return int(duration.total_seconds() / 60)

def calculate_wait_time(arrival: str, next_departure: str) -> int:
    """Calculate waiting time in minutes between arrival and next departure."""
    arr = datetime.strptime(arrival, "%H:%M")
    dep = datetime.strptime(next_departure, "%H:%M")
    wait = dep - arr
    if wait.days < 0:  # Handle overnight waits
        wait += timedelta(days=1)
    return int(wait.total_seconds() / 60)

def format_duration(minutes: int) -> str:
    """Format duration from minutes to hours and minutes."""
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m" if hours else f"{minutes}m"

def find_alternative_routes(trains: List[Dict], source: str, destination: str, max_transfers: int = 2) -> List[Route]:
    """Find all possible routes between source and destination with up to max_transfers"""
    routes = []
    
    # First check for direct routes
    direct_routes = [train for train in trains if train["source"] == source and train["destination"] == destination]
    for train in direct_routes:
        duration = calculate_duration(train["departure_time"], train["arrival_time"])
        routes.append(Route(
            legs=[train],
            total_duration=duration,
            total_wait_time=0,
            transfers=0
        ))
    
    # If no direct routes or we want to find alternatives, look for multi-leg journeys
    def find_connecting_routes(current_station: str, target: str, visited: set, current_route: List[Dict], transfers: int):
        if transfers > max_transfers:
            return
            
        possible_next_legs = [
            train for train in trains 
            if train["source"] == current_station 
            and train["source"] not in visited
        ]
        
        for next_leg in possible_next_legs:
            if next_leg["destination"] == target:
                # Found a complete route
                total_duration = 0
                total_wait_time = 0
                
                # Calculate total duration and wait times
                for i, leg in enumerate(current_route + [next_leg]):
                    duration = calculate_duration(leg["departure_time"], leg["arrival_time"])
                    total_duration += duration
                    
                    if i > 0:  # Calculate wait time between legs
                        wait_time = calculate_wait_time(
                            current_route[i-1]["arrival_time"],
                            leg["departure_time"]
                        )
                        total_wait_time += wait_time
                        total_duration += wait_time
                
                routes.append(Route(
                    legs=current_route + [next_leg],
                    total_duration=total_duration,
                    total_wait_time=total_wait_time,
                    transfers=len(current_route)
                ))
            else:
                # Continue searching for routes through this leg
                new_visited = visited | {next_leg["source"]}
                find_connecting_routes(
                    next_leg["destination"],
                    target,
                    new_visited,
                    current_route + [next_leg],
                    transfers + 1
                )
    
    if len(routes) == 0 or max_transfers > 0:
        find_connecting_routes(source, destination, {source}, [], 0)
    
    # Sort routes by total duration
    return sorted(routes, key=lambda x: x.total_duration)

def format_route_details(route: Route) -> Dict:
    """Format route details for API response"""
    legs = []
    for i, leg in enumerate(route.legs):
        leg_info = {
            "train_id": leg["train_id"],
            "train_name": leg["train_name"],
            "source": leg["source"],
            "destination": leg["destination"],
            "departure_time": leg["departure_time"],
            "arrival_time": leg["arrival_time"],
            "seats_available": leg["seats_available"]
        }
        if i > 0:
            leg_info["wait_time_at_source"] = calculate_wait_time(
                route.legs[i-1]["arrival_time"],
                leg["departure_time"]
            )
        legs.append(leg_info)
    
    return {
        "legs": legs,
        "total_duration_minutes": route.total_duration,
        "total_wait_time_minutes": route.total_wait_time,
        "number_of_transfers": route.transfers
    }
