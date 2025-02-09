# main.py

from flask import Flask, jsonify, request
from dummyDB import get_trains, get_all_trains, get_nearby_stations
from route_finder import find_alternative_routes, format_route_details

app = Flask(__name__)

@app.route("/trains", methods=["GET"])
def trains():
    source = request.args.get("source")
    destination = request.args.get("destination")
    include_alternative_routes = request.args.get("alternative_routes", "false").lower() == "true"
    max_transfers = int(request.args.get("max_transfers", "2"))
    max_wait_time = int(request.args.get("max_wait_time", "120"))
    
    if not source:
        return jsonify({"error": "Source station is required"}), 400
        
    if destination and include_alternative_routes:
        # Get all trains to find possible routes
        all_trains = get_all_trains()
        routes = find_alternative_routes(all_trains, source, destination, max_transfers,)
        
        if not routes:
            # Check for nearby stations if no routes are found
            nearby_stations = get_nearby_stations(source)
            alternative_routes = []
            for station in nearby_stations:
                routes_from_nearby = find_alternative_routes(all_trains, station, destination, max_transfers)
                if routes_from_nearby:
                    alternative_routes.extend(routes_from_nearby)
            
            if not alternative_routes:
                return jsonify({
                    "direct_routes": [],
                    "alternative_routes": [],
                    "message": "No routes found between the specified stations"
                })
            else:
                # Format routes from nearby stations
                return jsonify({
                    "direct_routes": [],
                    "alternative_routes": [format_route_details(route) for route in alternative_routes],
                    "message": "No direct routes found. Showing routes from nearby stations."
                })
            
        # Separate direct and alternative routes
        direct_routes = [route for route in routes if route.transfers == 0]
        alternative_routes = [route for route in routes if route.transfers > 0]
        
        return jsonify({
            "direct_routes": [format_route_details(route) for route in direct_routes],
            "alternative_routes": [format_route_details(route) for route in alternative_routes]
        })
    else:
        # Original functionality for direct trains only
        trains = get_trains(source, destination)
        return jsonify(trains)

@app.route("/all_trains", methods=["GET"])
def all_trains():
    trains = get_all_trains()
    return jsonify(trains)

if __name__ == "__main__":
    app.run(port=5000, debug=True)