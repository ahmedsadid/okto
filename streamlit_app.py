import streamlit as st
from datetime import datetime
import pytz
import requests
from streamlit_geolocation import streamlit_geolocation



def fetch_prayer_times(loc, method, asr_calc):
    date = datetime.now().strftime("%d-%m-%Y")
    url = f"https://api.aladhan.com/v1/timingsByAddress/{date}"
    params = {
            "address": loc,
            "method": method,
            "school": asr_calc
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
        
    if data["code"] == 200:
        return data["data"]["timings"]
    else:
        st.error("Error fetching prayer times")
        return None


def get_calculation_method_number(method_name):
    """Convert method name to API method number"""
    method_map = {
        "Muslim World League": 3,
        "Islamic Society of North America": 2,
        "Egyptian General Authority of Survey": 5,
        "Umm Al-Qura University, Makkah": 4,
        "University of Islamic Sciences, Karachi": 1,
        "Institute of Geophysics, University of Tehran": 7,
        "Shia Ithna-Ashari, Leva Institute, Qum": 0
    }
    return method_map.get(method_name)  


def main():
    st.title("okto")
    st.title("Prayer Times For Today")
    
    
    # col1, col2, col3 = st.columns([1, 2, 1])
    # with col2:
        # st.markdown("<h3 style='text-align: center;'>Current time in </h3>", unsafe_allow_html=True)
        # time_placeholder = st.empty()
        # Example of how to update the time:
        # time_placeholder.markdown("<h2 style='text-align: center;'>12:00:00</h2>", unsafe_allow_html=True)
    

    col1, col2 = st.columns([3, 1])
    with col1:
        location_search = st.text_input("Search for a location (City, Country)")
    with col2:
        st.write("")  # Add some spacing to align with text input
        search_button = st.button("Search")


    col1, col2 = st.columns(2)
    
    with col1:
        calculation_method = st.selectbox(
            "Method",
            options=[
                "Muslim World League",
                "Islamic Society of North America",
                "Egyptian General Authority of Survey",
                "Umm Al-Qura University, Makkah",
                "University of Islamic Sciences, Karachi",
                "Institute of Geophysics, University of Tehran",
                "Shia Ithna-Ashari, Leva Institute, Qum"
            ]
        )
    
    with col2:
        asr_calculation = st.selectbox(
            "Asr Calculation",
            options=[
                "Standard",
                "Hanafi"
            ]
        )

    search_button = st.button("Search")





    st.markdown("### Prayer Times")
    
    prayer_times = {
        "Fajr": st.container(),
        "Sunrise": st.container(),
        "Duhr": st.container(),
        "Asr": st.container(),
        "Maghrib": st.container(),
        "Dusk": st.container(),
        "Isha": st.container(),
        "Midnight": st.container()
    }
    
    prayer_time_style = """
        <div style="
            padding: 10px;
            background-color: #f0f2f6;
            border-radius: 5px;
            margin: 5px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span>{prayer_name}</span>
            <span>{time}</span>
        </div>
    """
    
    for prayer_name, container in prayer_times.items():
        with container:
            # Example of how to populate with actual times:
            # time_value = "04:30"  # This would come from your API
            time_value = "--:--"  # Placeholder
            st.markdown(
                prayer_time_style.format(
                    prayer_name=prayer_name,
                    time=time_value
                ),
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()