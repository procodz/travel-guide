# agent.py

import streamlit as st
import requests
from datetime import datetime, timedelta
from route_finder import format_duration  
from fuzzywuzzy import process
from dummyDB import get_all_trains, get_trains, get_nearby_stations



# Constants
API_BASE_URL = "http://localhost:5000"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

class TrainRouteUI:
    def __init__(self):
        self.setup_page()
        
    def setup_page(self):
        """Initialize the Streamlit page with basic settings"""
        st.set_page_config(
            page_title="Travel Guide",
            page_icon="🚂",
            layout="wide"
        )
        st.title("🚂 Travel Guide")
        
    def correct_station_name(self, station_name):
        """Auto-correct station names using fuzzy matching"""
        all_stations = set(train["source"] for train in get_all_trains()) | set(train["destination"] for train in get_all_trains())
        match, score = process.extractOne(station_name, all_stations)
        return match if score > 80 else station_name  # Adjust threshold as needed

    def fetch_trains(self, params):
        """Fetch train data from the API with travel date filtering"""
        try:
            response = requests.get(f"{API_BASE_URL}/trains", params=params)
            response.raise_for_status()
            trains = response.json()
            
            # Filter trains based on travel date if provided
            if "travel_date" in params:
                travel_date = datetime.strptime(params["travel_date"], "%Y-%m-%d")
                day_of_week = travel_date.strftime("%a")
                trains = [train for train in trains if day_of_week in train["days_available"]]
            
            return trains
        except requests.RequestException as e:
            st.error(f"Error fetching train data: {str(e)}")
            return None

    def get_llm_recommendation(self, query, context):
        """Get recommendations from the LLM with user preferences"""
        prompt = f"""
        You are a smart travel guide assistant. The user's query is "{query}".

        Context:
        - Source Station: {context['source']}
        - Destination Station: {context['destination']}
        - Available Trains: {context['available_trains']}
        - Seat Availability: {context['seat_availability']}
        - Travel Date: {context['travel_date']}

        Provide a detailed response including train options, seat availability, and recommendations.
        Prioritize faster routes if speed is preferred, cheaper routes if cost is preferred, or less crowded routes if comfort is preferred.
        """
        
        try:
            response = requests.post(
                OLLAMA_API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "model": "qwen2.5:3b",
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json().get("response", "Unable to generate recommendation.")
        except requests.RequestException as e:
            return f"Error generating recommendation: {str(e)}"

    def display_route_card(self, route, is_alternative=False):
        """Display a single route in a card format"""
        with st.container():
            route_type = "Alternative Route" if is_alternative else "Direct Route"
            
            # Create columns for route header
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                st.subheader(route_type)
            with col2:
                st.metric("Duration", format_duration(route['total_duration_minutes']))
            with col3:
                if is_alternative:
                    st.metric("Transfers", str(route['number_of_transfers']))

            # Display route details
            for i, leg in enumerate(route['legs'], 1):
                with st.expander(f"Leg {i}: {leg['source']} → {leg['destination']}", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Train:** {leg['train_name']}")
                        st.write(f"**Train ID:** {leg['train_id']}")
                        st.write(f"**Seats Available:** {leg['seats_available']}")
                    with col2:
                        st.write(f"**Departure:** {leg['departure_time']}")
                        st.write(f"**Arrival:** {leg['arrival_time']}")
                        if i > 1 and 'wait_time_at_source' in leg:
                            st.write(f"**Wait Time:** {format_duration(leg['wait_time_at_source'])}")
                        if 'transfer_instructions' in leg:
                            st.write(f"**Transfer Instructions:** {leg['transfer_instructions']}")

    def display_search_results(self, data):
        """Display search results in an organized manner"""
        if not data:
            st.warning("No routes found.")
            return

        # Display direct routes
        if "direct_routes" in data and data["direct_routes"]:
            st.markdown("## 🎯 Direct Routes")
            for route in data["direct_routes"]:
                self.display_route_card(route)

        # Display alternative routes
        if "alternative_routes" in data and data["alternative_routes"]:
            st.markdown("## 🔄 Alternative Routes")
            for route in data["alternative_routes"]:
                self.display_route_card(route, is_alternative=True)

    def show_search_filters(self):
        """Display and handle search filters"""
        with st.expander("🔍 Advanced Search Options", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                max_transfers = st.slider(
                    "Maximum Transfers",
                    min_value=1,
                    max_value=3,
                    value=2,
                    help="Maximum number of train changes allowed"
                )
                max_wait_time = st.slider(
                    "Maximum Wait Time (minutes)",
                    min_value=0,
                    max_value=240,
                    value=120,
                    help="Maximum waiting time at transfer points"
                )
            with col2:
                include_overnight = st.checkbox(
                    "Include Overnight Journeys",
                    value=True,
                    help="Include routes with overnight travel"
                )
                priority = st.radio(
                    "Priority",
                    options=["Speed", "Cost", "Comfort"],
                    index=0,
                    help="Prioritize faster, cheaper, or less crowded routes"
                )
        return max_transfers, max_wait_time, include_overnight, priority

    def run(self):
        """Main UI logic"""
        # Input Section
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                source = st.text_input("🚉 From Station", key="source")
                if source:
                    source = self.correct_station_name(source)
            with col2:
                destination = st.text_input("🏁 To Station", key="destination")
                if destination:
                    destination = self.correct_station_name(destination)

        # Advanced Filters
        max_transfers, max_wait_time, include_overnight, priority = self.show_search_filters()

        # Search Options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Search Routes", use_container_width=True):
                if source and destination:
                    params = {
                        "source": source,
                        "destination": destination,
                        "alternative_routes": "true",
                        "max_transfers": str(max_transfers),
                        "max_wait_time": str(max_wait_time),
                        "include_overnight": str(include_overnight).lower()
                    }
                    data = self.fetch_trains(params)
                    if data:
                        self.display_search_results(data)
                else:
                    st.warning("Please enter both source and destination stations.")

        with col2:
            if st.button("💡 Get Smart Recommendations", use_container_width=True):
                if source and destination:
                    # Prepare context for LLM
                    context = {
                        "source": source,
                        "destination": destination,
                        "available_trains": self.fetch_trains({"source": source}),
                        "seat_availability": "Available",  # This could be more dynamic
                        "travel_date": datetime.now().strftime("%Y-%m-%d"),
                        "priority": priority
                    }
                    
                    with st.spinner("Generating smart recommendations..."):
                        recommendation = self.get_llm_recommendation(
                            f"Find me the best route from {source} to {destination}",
                            context
                        )
                        st.info(recommendation)
                else:
                    st.warning("Please enter both source and destination stations.")

if __name__ == "__main__":
    app = TrainRouteUI()
    app.run()