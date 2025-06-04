import streamlit as st
import requests

st.set_page_config(page_title="MLB Betting Assistant", layout="wide")

st.title("⚾ MLB Betting Assistant")

oddsapi_key = st.secrets.get("oddsapi_key", "YOUR_API_KEY")
sport = "baseball_mlb"
region = "us"
market = "h2h"

st.sidebar.header("Today's Games")

@st.cache_data(ttl=600)
def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={oddsapi_key}&regions={region}&markets={market}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

odds_data = get_odds()
if not odds_data:
    st.warning("No data available or invalid API key.")
else:
    for game in odds_data:
        teams = game["teams"]
        home_team = game["home_team"]
        commence_time = game["commence_time"].split("T")[0]
        bookmakers = game.get("bookmakers", [])
        st.markdown(f"### {teams[0]} vs {teams[1]} ({commence_time})")
        for bookmaker in bookmakers[:1]:  # show only top bookmaker
            outcomes = bookmaker.get("markets", [])[0].get("outcomes", [])
            for o in outcomes:
                st.write(f"{o['name']}: {o['price']}")
