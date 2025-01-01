import streamlit as st
from datetime import datetime
import requests

def fetch_prayer_times(loc, method, asr_calc=0):
    try:
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
    except requests.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        return None

def get_calculation_method_number(method_name):
    """Convert method name to API method number"""
    method_map = {
        "Muslim World League": 3,
        "Islamic Society of North America": 2,
        "Egyptian General Authority of Survey": 5,
        "Umm Al-Qura University, Makkah": 4,
        "University of Islamic Sciences, Karachi": 1,
    }
    return method_map.get(method_name)  

def main():
    st.title("okto")
    st.title("Prayer Times For Today")
    
    # Initialize session state variables
    if 'prayer_times' not in st.session_state:
        st.session_state.prayer_times = None
    if 'location_search' not in st.session_state:
        st.session_state.location_search = ""
    if 'calculation_method' not in st.session_state:
        st.session_state.calculation_method = "Muslim World League"
    if 'asr_calculation' not in st.session_state:
        st.session_state.asr_calculation = "Standard"
    
    # Method selection
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
            ],
            key="calculation_method"
        )
    
    with col2:
        asr_calculation = st.selectbox(
            "Asr Calculation",
            options=[
                "Standard",
                "Hanafi"
            ],
            key="asr_calculation"
        )

    # Location search
    col1, col2 = st.columns([3, 1])
    with col1:
        location_search = st.text_input(
            "Search for a location (City, Country)",
            key="location_search"
        )
    with col2:
        st.write("") 
        search_button = st.button("Search")

    # Handle search
    if search_button:
        try:
            method_number = get_calculation_method_number(calculation_method)
            asr_calc = {"Standard": 0, "Hanafi": 1}.get(asr_calculation)
            
            prayer_times = fetch_prayer_times(location_search, method_number, asr_calc)
            
            if prayer_times:
                st.session_state.prayer_times = prayer_times
                st.success(f"Prayer times fetched for {location_search}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Prayer times display
    st.markdown("### Prayer Times")
    
    prayer_names = [
        "Fajr",
        "Sunrise",
        "Dhuhr",
        "Asr",
        "Maghrib",
        "Isha",
        "Midnight"
    ]
    
    prayer_time_style = """
        <div style="
            padding: 10px;
            background-color: var(secondary);
            color: var(--st-color-text);
            border-color: var(--st-color-text);
            border-style: solid;
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
    
    # Display prayer times
    for name in prayer_names:
        time_value = "--:--"
        if st.session_state.prayer_times and name in st.session_state.prayer_times:
            time_value = st.session_state.prayer_times[name]
        
        st.markdown(
            prayer_time_style.format(
                prayer_name=name,
                time=time_value
            ),
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()