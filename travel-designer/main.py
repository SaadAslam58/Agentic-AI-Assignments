from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import asyncio

load_dotenv()


async def agent_function():

    @function_tool
    def get_flights(name: str, country: str) -> dict:
        """
        Mock tool that simulates booking a flight and provides information
        about destination weather, temperature, and other useful details.

        Args:
            name (str): Name of the traveler.
            country (str): Destination country.

        Returns:
            dict: Mock flight and weather details.
        """

        mock_data = {
            "traveler": name,
            "destination": country,
            "flight": {
                "airline": "SkyJet Airlines",
                "flight_number": "SJ987",
                "departure": "2025-07-22T10:00:00",
                "arrival": "2025-07-22T14:30:00",
                "terminal": "B",
                "gate": "17"
            },
            "weather": {
                "condition": "Sunny",
                "temperature_celsius": 29,
                "humidity_percent": 40
            },
            "note": f"Hi {name}, your flight to {country} is confirmed. Expect sunny weather with moderate temperature. Enjoy your trip!"
        }

        return mock_data
    
    @function_tool
    def suggest_hotels(name: str, country: str) -> dict:
        """
        Mock tool that returns a list of suggested hotels in a given country
        along with amenities and pricing information.

        Args:
            name (str): Name of the traveler.
            country (str): Destination country.

        Returns:
            dict: Suggested hotels with details.
        """

        mock_data = {
            "traveler": name,
            "destination": country,
            "hotels": [
                {
                    "name": "Grand Palace Hotel",
                    "stars": 5,
                    "price_per_night_usd": 220,
                    "amenities": ["Free Wi-Fi", "Spa", "Airport Shuttle", "Breakfast Included"],
                    "rating": 4.8
                },
                {
                    "name": "City Comfort Inn",
                    "stars": 4,
                    "price_per_night_usd": 150,
                    "amenities": ["Free Wi-Fi", "Gym", "Room Service"],
                    "rating": 4.5
                },
                {
                    "name": "Budget Stay Lodge",
                    "stars": 3,
                    "price_per_night_usd": 75,
                    "amenities": ["Wi-Fi", "Air Conditioning", "Shared Kitchen"],
                    "rating": 4.0
                }
            ],
            "note": f"{name}, here are some hotel options in {country} based on your travel preference."
        }

        return mock_data
        



    DestinationAgent = Agent(
        name="DestinationAgent",
        instructions=(
            "You are the destination agent. Based on the user's interest, "
            "recommend a travel destination. Use keywords like 'beach', 'mountain', 'history', or 'adventure' "
            "to make informed suggestions."
        )
    )

    BookingAgent = Agent(
        name="BookingAgent",
        instructions=(
            "You are the booking agent. Once a destination is confirmed, "
            "you simulate booking a flight and suggesting hotels by calling the tools: get_flights() and suggest_hotels()."
        ),
        tools=[get_flights, suggest_hotels]
    )

    ExploreAgent = Agent(
        name="ExploreAgent",
        instructions=(
            "You are the explore agent. Given a destination, suggest popular attractions, food, "
            "local experiences, and must-do activities."
        )
    )

    Handoff_Agent = Agent(
        name="Distribution",
        instructions="You are a distribution agent that will distribute task and give a precise output,",
        handoffs=[DestinationAgent, BookingAgent, ExploreAgent]
    )

    while True:
        user_input = input("How can i help you :")
        result = await Runner.run(Handoff_Agent, user_input)
        print(result.final_output)
        if "break" in user_input or "exit" in user_input:
            break 


asyncio.run(agent_function())