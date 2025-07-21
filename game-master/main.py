# 🎲 game.py
import random, re
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()

@function_tool
def roll_dice(sides: int = 6) -> int:
    return random.randint(1, sides)

@function_tool
def generate_event(context: str) -> str:
    events = {
        "battle": ["Goblin ambush!", "Troll appears!", "Bandit attacks!"],
        "treasure": ["You find a magic sword!", "You discover a healing potion!", "You receive 50 gold!"]
    }
    return random.choice(events.get(context, ["Nothing happens."]))

NarratorAgent = Agent(
    name="NarratorAgent",
    instructions="Continue the narrative based on story and recent events."
)

MonsterAgent = Agent(
    name="MonsterAgent",
    instructions="Resolve the combat: roll the dice and describe the result. Use roll_dice and generate_event('battle').",
    tools=[roll_dice, generate_event]
)

ItemAgent = Agent(
    name="ItemAgent",
    instructions="Handle treasure discovery: use generate_event('treasure') and describe the reward.",
    tools=[generate_event]
)

GameAgent = Agent(
    name="GameAgent",
    instructions=(
        "You orchestrate the adventure. "
        "Use NarratorAgent for narration, "
        "MonsterAgent for battles, "
        "ItemAgent for treasure events."
    ),
    handoffs=[NarratorAgent, MonsterAgent, ItemAgent]
)

TITLE = "🌟 My Quest"
TEMPLATE = "A ___ (role) named ___ (name) travels to ___ (place), armed with a ___ (noun)."

st.title(TITLE)
st.write(TEMPLATE)

labels = re.findall(r"___ \((.*?)\)", TEMPLATE)
user_input = {lbl: st.text_input(lbl.capitalize(), "") for lbl in labels}

if st.button("Begin Adventure"):
    if all(user_input.values()):
        story = TEMPLATE
        for lbl, val in user_input.items():
            story = story.replace(f"___ ({lbl})", val, 1)

        result = Runner.run_sync(GameAgent, story)

        st.markdown("### 🗺️ Adventure Log")
        st.write(result.final_output)
    else:
        st.warning("Fill in all fields.")
