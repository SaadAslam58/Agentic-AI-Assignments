from agents import Agent, Runner
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def agent_function():
    CareerAgent = Agent(
        name="Smart Student Agent",
        instructions="You are a career agent you will guide user according to their interest and show them the path with details",
    )
    SkillAgent = Agent(
        name="Skill-Agent",
        instructions="Ypu guide user which skills they need according their field of interest and provide latest ongoing skills in the market"
    )
    JobAgent = Agent(
        name="Job-Agent",
        instructions="You will guide users what jobs they will get according to thier carrer and skills and show the expected salaries and future growths"
    )

    Handoff_Work = Agent(
        name="Handoff-Agent",
        instructions="You will use agents accordingly to guide the user for successfull career path and let them know the final output with precise information.",
        handoffs=[CareerAgent, SkillAgent, JobAgent]
    )

    while True:
        user_input = input("How can i help you :")
        result = await Runner.run(Handoff_Work, user_input)
        print(result.final_output)
        if "break" in user_input or "exit" in user_input:
            break 

asyncio.run(agent_function())