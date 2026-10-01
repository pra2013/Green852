import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Colour Scheme
st.set_page_config(page_title="Green852", page_icon= "🌱", layout="centered")
st.markdown("""
<style>
    .stApp {
        background-color: #f4f9f4;
    }
    h1, h2, h3 {
        color: #1b5e20;
    }
    div.stButton > button {
        background-color: #2e7d32; 
        color: white; 
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

#Sidebar
st.sidebar.title("Green852")
user_input = st.sidebar.radio(
    "Choose a page:", 
    ("Home", "Leaderboard", "Recycling Map", "Redemption Center")
)
st.markdown(f"Welcome to the {user_input} page!")

#Home Page
if user_input == "Home":
    st.title("Green852: Save the planet through your actions")
    st.image("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09", caption="Green852 Carbon Tracker")
    st.write("Welcome to Green852! Track your carbon footprint and compete with your friends to see who can use the least carbon")

    #Electricity Emissions
    electricity_use = st.slider("How much electricity do you use per month (in Kwh)?", min_value=0, max_value=1000, value=500)
    electricity_emissions = electricity_use * 0.39
    st.write(f"Your calculated carbon emissions are: {electricity_emissions} kg Co2 per month.")

    #Transportation Emissions
    car_use = st.slider("How many kilometers do you drive per month?", min_value=0, max_value=1000, value=500)
    public_use = st.slider("How many kilometers do you travel by public transport (MTR, Minibus, Bus) per month?", min_value=0, max_value=1000, value=500)
    car_emissions = car_use * 0.20
    public_emissions = public_use * 0.04
    st.write(f"Your calculated carbon emissions from travel is {car_emissions + public_emissions} kg Co2 per month.")

    #Recycling Emissions
    recycling_use = st.slider("How many kilograms of waste do you recycle per month?", min_value=0, max_value=1000, value=500)
    recycling_emissions = recycling_use * 1.5

    st.write(f"Your calculated carbon offset from recycling is {recycling_emissions} kg Co2 per month.")
    #Total Emissions
    total_emissions = electricity_emissions + car_emissions + public_emissions - recycling_emissions
    st.write(f"Your total calculated carbon emissions per month is {total_emissions} kg Co2 per month.")
    st.session_state["user_co2"] = round(total_emissions, 1)

    recycling_points = recycling_use * 50
    leaderboard_bonus = max(0, int(440 - total_emissions) * 2)
    total_points = recycling_points + leaderboard_bonus
    if "green_points" not in st.session_state:
        st.session_state["green_points"] = total_points
        
    if total_emissions < 440:
        st.write("Congratulations! You are doing a great job in reducing your carbon footprint.")
    else:
        st.write("You can do better! Try to reduce your electricity usage, travel less by car, and recycle more to lower your carbon footprint.")

#Leaderboard Page
elif user_input == "Leaderboard":
    st.title("Leaderboard: Battle your friends to find the strongest EcoWarrior!")
    st.write("Check out the top users with the lowest carbon footprint and see how you rank.")
    user_score = st.session_state.get("user_co2", 440.0)
    leaderboard_data = {
        "Name": ["Alex", "Chloe", "Ryan", "You", "Emma", "Liam", "Sophia", "Noah", "Olivia", "Ethan", "Ava", "Mason", "Isabella", "Logan", "Mia"],
        "Monthly Carbon Footprint(kg Co2)": [300, 250, 460, 350, 280, 400, 320, 480, 340, 420, 290, 380, 310, 450, 330],
        "Status": ["EcoFighter", "Eco Warrior", "Needs Improvement", "EcoFighter", "Eco Warrior", "On Track", "EcoFighter", "Needs Improvement", "EcoFighter", "On Track", "Eco Warrior", "EcoFighter", "EcoFighter", "On Track", "EcoFighter"]
    }
    user_index = leaderboard_data["Name"].index("You")
    leaderboard_data["Monthly Carbon Footprint(kg Co2)"][user_index] = user_score
    if user_score < 300:
        leaderboard_data["Status"][user_index] = "Eco Warrior"
    elif user_score < 400:
        leaderboard_data["Status"][user_index] = "EcoFighter"
    elif user_score <= 450:
        leaderboard_data["Status"][user_index] = "On Track"
    else:
        leaderboard_data["Status"][user_index] = "Needs Improvement"
    df = pd.DataFrame(leaderboard_data)
    df_sorted = df.sort_values(by="Monthly Carbon Footprint(kg Co2)", ascending=True).reset_index(drop=True)
    df_sorted["Rank"] = df_sorted.index + 1
    df_sorted = df_sorted[["Rank", "Name", "Monthly Carbon Footprint(kg Co2)", "Status"]]
    st.dataframe(df_sorted, hide_index=True)

    your_rank = df_sorted[df_sorted["Name"] == "You"]["Rank"].values[0]
    st.info(f"Your current rank is {your_rank} with a {user_score} kg Co2 monthly carbon footprint.")
  
    #Recycling Map Page
elif user_input == "Recycling Map":
    st.title("Recyling Map: Find your nearest recycling center!")
    st.write("Use the map to locate your nearest GREEN@COMMUNITY station to start recycling your waste and offset your carbon footprint.")
    recyling_map = folium.Map (location=[22.3193, 114.1694], zoom_start=11)

    recycling_centers = [
    {
        "name": "GREEN@WAN CHAI",
        "lat": 22.2783,
        "lon": 114.1738,
        "address": "6 Wan Shing Street, Wan Chai"
    },
    {
        "name": "GREEN@KWUN TONG",
        "lat": 22.3218,
        "lon": 114.2104,
        "address": "27 Sheung Yee Road, Kowloon Bay"
    },
    {
        "name": "GREEN@SHA TIN",
        "lat": 22.3880,
        "lon": 114.2078,
        "address": "10 On Ping Street, Shek Mun"
    }
    ]

    for station in recycling_centers:
        folium.Marker(
            location=[station["lat"], station["lon"]],
            popup=f"{station['name']}<br>{station['address']}",
            tooltip=station["name"],
            icon=folium.Icon(color= "green", icon= "recycle", prefix="fa")
        ).add_to(recyling_map)

    st_folium(recyling_map, width=700, height=500)

#Redemption Center Page
elif user_input == "Redemption Center":
    st.title("Redemption Center: Redeem rewards through earning green points for recycling!")
    st.write("Link your GREEN@COMMUNITY account to redeem your rewards and earn green points for recycling.")
    if "green_points" not in st.session_state:
        st.session_state["green_points"] = 250

    st.metric(label="Green Points Balance", value=f"{st.session_state['green_points']} points")
    st.divider()

    rewards = [
        {
            "title": "Eco-Friendly Water Bottle",
            "cost": 4000,
            "description": "A reusable water bottle made from sustainable materials.",
            "code": "GREEN-BOTTLE",
        },
        {
            "title": "$10 MTR Shops E-Voucher",
            "cost": 2000,
            "description": "A $10 e-voucher for participating MTR Shops.",
            "code": "GREEN-MTR10",
        },
        {
            "title": "$10 Red Cross Donation",
            "cost": 2000,
            "description": "Donate $10 to support the Hong Kong Red Cross.",
            "code": "GREEN-RED-CROSS10",
        },
        {
            "title": "1 Free Mrs Field's Cookie/Muffin worth $25",
            "cost": 6000,
            "description": "Redeem a cookie or muffin at a participating Mrs. Fields shop.",
            "code": "GREEN-MF25",
        },
    ]

    #Rendering rewards in columns
    col1, col2 = st.columns(2)
    for index, reward in enumerate(rewards):
        target_col = col1 if index % 2 == 0 else col2
        with target_col:
            st.subheader(reward["title"])
            st.write(f"Cost: {reward['cost']} Points")
            st.caption(reward["description"])
            if st.button(f"Redeem {reward['title']}", key=f"button_{index}"):
                if st.session_state["green_points"] >= reward["cost"]:
                    st.session_state["green_points"] -= reward["cost"]
                    st.success(f"Successfully redeemed! Your code: {reward['code']}")
                    st.rerun()
                else:
                    st.error("Not enough points! Recycle more to earn this reward.")
            st.divider()