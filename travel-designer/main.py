from dotenv import load_dotenv
from agents import Agent, Runner
import asyncio
load_dotenv()



async def agent_function():

    Traveller_Agent = Agent(
        name="Traveller Agent",
        instructions="You are a traveller agent that will guide user for travelling related stuff as well as guide them properly about the current situation of the place and its props and cons"
    )

    while True:
        user_input = input("How can i help you :")
        result = await Runner.run(Traveller_Agent, user_input)
        print(result.final_output)
        if "break" in user_input or "exit" in user_input:
            break 


asyncio.run(agent_function())