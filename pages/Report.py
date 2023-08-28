
import streamlit as st
from pymongo import MongoClient

def fetch_eye_health_report():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['blink_db']
    collection = db['blink_data']

    # Fetch data from the collection
    data = collection.find({}, {'_id': 0})

    formatted_data = []
    for entry in data:
        if 'blink_rate' in entry:
            entry['blink_rate'] = int(entry['blink_rate'])
        if 'avg_distance_from_screen' in entry:
            entry['avg_distance_from_screen'] = format(float(entry['avg_distance_from_screen']), '.2f')
        formatted_data.append(entry)

    return formatted_data

def display_eye_health_report():
    st.title("Eye Health Report")

    data = fetch_eye_health_report()

    if len(data) == 0:
        st.write("No data available.")
    else:
        st.table(data)  # Display the list of dictionaries as a table

def main():
    st.title("Report Page")
    st.write("")
    st.write("Welcome to the report page!")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("")
        if st.button("Posture Report"):
            st.write("Generating Posture Report...")

    with col2:
        st.write("")
        if st.button("Eye Health Report"):
            with st.expander("Eye Health Report", expanded=True):
                display_eye_health_report()

    # Place the eye health and posture report displays below the columns
    st.write("")
    st.write("")

if __name__ == "__main__":
    main()
