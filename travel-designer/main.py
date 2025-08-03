from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import asyncio
import os

load_dotenv()  

@function_tool
def get_flights(name: str, country: str) -> str:
    """
    Suggested flight: {name} country: {country}.
    """
    return f"Suggested flight: {name} country: {country}."

@function_tool
def suggest_hotels(name: str, country: str) -> str:
    """
    Suggested hotel: {name} Country: {country}.
    """
    return f"Suggested hotel: {name} Country: {country}."

async def main():
    DestinationAgent = Agent(
        name="DestinationAgent",
        instructions=(
            "You are the destination agent. Based on the user's interest (e.g. 'beaches', "
            "or 'food trips'), recommend *one* travel destination (city and country). "
            "Do not call any tool. Let the user confirm the destination."
        )
    )

    BookingAgent = Agent(
        name="BookingAgent",
        instructions=(
            "You are the booking agent. Once the user says 'Yes' and confirms a destination "
            "(country and city), simulate booking by calling get_flights(name, country) "
            "and then suggest_hotels(name, country). Return exactly the tool outputs."
        ),
        tools=[get_flights, suggest_hotels]
    )

    DistributionAgent = Agent(
        name="DistributionAgent",
        instructions="You distribute the user's request to sub-agents.",
        handoffs=[DestinationAgent, BookingAgent]
    )

    while True:
        user_input = input("How can I help you? ")
        if user_input.strip().lower() in {"exit", "break"}:
            print("Goodbye!")
            return
        result = await Runner.run(DistributionAgent, user_input)
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
