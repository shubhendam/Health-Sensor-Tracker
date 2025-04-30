import streamlit as st
import time
from database import get_db, update_user_location
from auth import authenticate_user, register_user
from sqlalchemy.orm import Session
from activity_tracker import start_activity_tracking, get_current_activity
from llm_integration import generate_llm_response
from utils import fetch_temperature
from get_sensor_data import get_current_steps

# Streamlit UI for login and signup
def main():
    st.title("Activity Tracker")

    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'location_prompt' not in st.session_state:
        st.session_state.location_prompt = False
    if 'current_activity' not in st.session_state:
        st.session_state.current_activity = "Static"

    # Check session state first
    if st.session_state.user and not st.session_state.location_prompt:
        start_activity_tracking(st.session_state.user)
        dashboard(st.session_state.user)
    elif st.session_state.user and st.session_state.location_prompt:
        ask_for_location()
    else:
        # Only show auth if user not set
        auth_option = st.sidebar.selectbox("Select an option", ("Login", "Signup"))
        if auth_option == "Login":
            login()
        elif auth_option == "Signup":
            signup()

def login():
    st.sidebar.header("Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        db: Session = next(get_db())
        user = authenticate_user(db, username, password)
        if user:
            st.session_state.user = user
            st.session_state.location_prompt = True
            st.sidebar.success(f"Welcome, {user.name}!")
            ask_for_location()
        else:
            st.sidebar.error("Invalid username or password")

def signup():
    st.sidebar.header("Signup")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    name = st.sidebar.text_input("Name")
    age = st.sidebar.number_input("Age", min_value=0, max_value=120)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.sidebar.number_input("Weight (kg)", min_value=0.0)
    location = st.sidebar.text_input("Location")
    daily_step_goal = st.sidebar.number_input("Daily Step Goal", min_value=0)

    if st.sidebar.button("Signup"):
        db: Session = next(get_db())
        user = register_user(db, username, password, name, age, gender, weight, location, daily_step_goal)
        if user:
            st.sidebar.success(f"Welcome, {user.username}! Please login to continue.")
        else:
            st.sidebar.error("Username already exists")

def ask_for_location():
    st.sidebar.header("Update Location")
    location = st.sidebar.text_input("Enter your current location")

    if st.sidebar.button("Submit Location"):
        if location:
            db: Session = next(get_db())
            update_user_location(db, st.session_state.user.id, location)
            st.session_state.user.location = location
            st.session_state.location_prompt = False  # Mark location done
            st.sidebar.success("Location updated successfully!")
            st.rerun()  # Force Streamlit to rerun and go to dashboard
        else:
            st.sidebar.error("Please enter a valid location")

def dashboard(user):
    st.write(f"### Welcome, {user.username}!")
    #st.write(f"**Name:** {user.username}")
    st.write(f"**Age:** {user.age}")
    st.write(f"**Gender:** {user.gender}")
    st.write(f"**Weight:** {user.weight} kg")
    # st.write(f"**Location:** {user.location}")


    st.write("### Activity Tracking")

    # --- Dynamic Refresh Block ---
    current_temp = fetch_temperature(user.location)
    st.write(f"**Current Temperature in {user.location}:** {current_temp}")
    current_steps = get_current_steps()
    st.write(f"**Current Steps/Daily Goal:** {current_steps}/{user.daily_step_goal}")
    st.session_state.current_activity = get_current_activity()
    st.write(f"**Current Activity:** {st.session_state.current_activity}")

    # Debugging: Print the current activity
    print(f"Current Activity: {st.session_state.current_activity}")

    # Generate LLM response
    try:
        # Debugging: Print the current activity
        # print(f"Current Activity in try: {st.session_state.current_activity}")
        # print(f"User object: {user}")
        activity = st.session_state.current_activity
        name = user.username
        llm_response = generate_llm_response(user, current_steps, current_temp, activity)
        st.write(f"**LLM Response:** {llm_response}")
    except Exception as e:
        st.warning(f"LLM error: {e}")

    time.sleep(5)  # Wait for 5 seconds
    st.rerun()     # Force refresh to get updated activity

    # --- Logout ---
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.location_prompt = False
        st.rerun()

if __name__ == "__main__":
    main()
