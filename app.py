import streamlit as st
import json
import pandas as pd
import random
from datetime import datetime

# Load objection data from JSON
with open("objections.json", "r") as f:
    objections = json.load(f)

# Function to log responses
def log_response(agent_name, agent_response, score, objection_text):
    # Log data to CSV file
    with open("logs/response_log.csv", "a") as log_file:
        log_file.write(f"{datetime.now()},{agent_name},{objection_text},{agent_response},{score}\n")

# Streamlit app configuration
st.set_page_config(page_title="Sales Objection Handling Coach", page_icon="💬", layout="centered")
st.title("💬 Sales Objection Handling Coach")

# Agent Information
st.sidebar.header("Agent Information")
agent_name = st.sidebar.text_input("Enter your name")

# Step 1: Select an Objection
st.header("1. Select an Objection")
objection = random.choice(objections)
objection_text = objection["objection"]
st.write(f"**Objection:** {objection_text}")

# Step 2: Respond to the Objection
st.header("2. Respond to the Objection")
agent_response = st.text_area("Type your response here...", height=100)

# Step 3: Submit and Score the Response
if st.button("Submit Response"):
    suggested_response = objection["suggested_response"]
    keywords = objection["keywords"]

    # Score based on keyword presence
    keyword_count = sum(1 for keyword in keywords if keyword.lower() in agent_response.lower())
    score = (keyword_count / len(keywords)) * 100

    # Display feedback
    st.header("3. Feedback")
    st.write(f"**Suggested Response:** {suggested_response}")
    st.write(f"**Your Score:** {score:.0f}%")
    if score == 100:
        st.success("Great job! You used all the key phrases.")
    elif score > 50:
        st.info("Good effort! You included some key phrases, but there's room for improvement.")
    else:
        st.warning("Try again. Consider incorporating more of the suggested phrases.")

    # Detailed feedback
    missing_keywords = [kw for kw in keywords if kw.lower() not in agent_response.lower()]
    if missing_keywords:
        st.write(f"**Consider adding these keywords:** {', '.join(missing_keywords)}")

    # Log response
    if agent_name:
        log_response(agent_name, agent_response, score, objection_text)
    else:
        st.warning("Please enter your name in the sidebar to log your score.")
