from agents import Agent, Runner
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def agent_function():
    Student_Agent = Agent(
        name="Smart Student Agent",
        instructions="You are a study agent. You will guide the user for study-related topics and nothing else.",
    )

    while True:
        user_input = input("How can i help you :")
        result = await Runner.run(Student_Agent, user_input)
        print(result.final_output)
        if "break" in user_input or "exit" in user_input:
            break 


asyncio.run(agent_function())




    

