import streamlit as st
import threading
from eyeBlink.blinkCounter import start_eye_detection, stop_eye_detection

def display_eye_complete_message():
    st.write("Eye Monitoring is complete!")

def monitor_eye_thread():
    start_eye_detection(display_eye_complete_message)

def main():
    st.title("WORKFIT: Posture and Eye Blink Detection")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("")
        monitor_posture = st.button("Monitor Posture", key="posture_btn")
        if monitor_posture:
            st.write("Posture monitoring is active!")

    with col2:
        st.sidebar.markdown("## Select a page above", unsafe_allow_html=True)
        st.write("")
        monitor_eye = st.button("Monitor Eye", key="eye_btn")
        if monitor_eye:
            st.write("Eye monitoring is active!")
            eye_thread = threading.Thread(target=monitor_eye_thread)
            eye_thread.start()  # Start the eye detection in a separate thread

if __name__ == "__main__":
    main()

