from altair import Then
from dotenv import load_dotenv
from agents import Agent, Runner
import streamlit as st
import re
load_dotenv()

Game_Agent = Agent(
    name="Game-Agent",
    instructions="You are a storytelling assistant. The story has blanks marked by '___'. You will collect user inputs for each blank, then output the completed story.",
)

TITLE = "🌟 My Quest Story"
TEMPLATE ="Once upon a time, a ___ (role) named ___ (name) embarked on a journey to ___ (place). TheyThened a ___ (adjective) dragon and used their ___ (noun) to ___ (verb). The end."


st.title(TITLE)
st.write(TEMPLATE)

labels = re.findall(r"___ \((.*?)\)", TEMPLATE)
user_input = {label: st.text_input(f"Enter a {label}") for label in labels}

if st.button("Complete my story"):
    if all(user_input.values()):
        story = TEMPLATE
        for label, val in user_input.items():
            story = story.replace(f"___ ({label})", val, 1)
        st.markdown("Your complete story")
        st.write(story)
    else:
        st.warning("Please fill in all blanks!")

