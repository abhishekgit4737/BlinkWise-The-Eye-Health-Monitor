## BlinkWise: Eye Blink Detection and Health Monitoring

**Project Description:**

BlinkWise is a web application built with Python which is designed to monitor user eye health through blink detection and provide relevant eye health information. The application is developed using streamlit library for user interaction, tracks and analyzes user blinking patterns.It gathers data and generates reports on eye health, offering insights into user eye strain and blink rate. The application also provides real-time notifications to encourage users to blink more frequently, helping to alleviate potential eye strain.

### Components and Modules:

1. **blinkCounter.py:**
   This module is responsible for real-time eye blink detection and data collection. It captures video from the user's webcam, detects facial landmarks, calculates blink rates, and stores blink-related data in a MongoDB database.

   - Utilizes OpenCV and cvzone libraries for video processing and facial landmark detection.
   - Implements FaceMeshDetector for identifying facial landmarks and measuring distances.
   - Employs a LivePlot to visualize blink-related data trends over time.
   - Defines functions for storing blink data in MongoDB and generating eye strain levels.
   - Monitors blink counts, rates, and eye strain for data storage and real-time notifications.

2. **Home.py:**
   The Home module serves as the entry point for the WorkFit application. It provides a user interface through streamlit for interacting with posture and eye monitoring functionalities.

   - Includes buttons to initiate posture and eye monitoring.
   - Utilizes threading to run eye monitoring in a separate background thread.
   - Controls the start and stop of eye monitoring using blinkCounter.py.
   - Displays notifications and status messages to the user based on monitoring activities.

3. **Report.py:**
   The Report module handles the display of eye health reports generated from the collected blink data.

   - Connects to the MongoDB database to fetch stored eye health data.
   - Presents the eye health report in a tabular format using streamlit.
   - Provides options to generate posture and eye health reports.

### Usage Instructions:

1. Run the `Home.py` script to launch the WorkFit application interface.
2. Click the "Monitor Eye" button to initiate eye health monitoring.
3. The `blinkCounter.py` module will track user eye blinking patterns in the background.
4. Real-time notifications will remind the user to blink more frequently if necessary.
5. The application generates eye health reports accessible through the "Eye Health Report" button.
6. The `Report.py` module presents eye health data in tabular format for easy analysis.

### Requirements:

- Python 3.x
- Streamlit
- OpenCV
- cvzone
- pymongo
- win10toast (for notifications)
- MongoDB (running on localhost)

**Note:** Ensure MongoDB is running and accessible at `localhost:27017` for proper data storage.

---
 
