import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import time
from win10toast import ToastNotifier
import os
from pymongo import MongoClient
import threading

should_stop = False

 # Define the store_blink_data function
def store_blink_data(start_interval, data_interval, blink_count, blink_rate, eye_strain, avg_distance):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['blink_db']
    collection = db['blink_data']
    
    # Generate a timestamp
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    # Create a data document
    data = {
        'timestamp': timestamp,
        'start_interval': start_interval,
        'end_interval': start_interval + data_interval,
        'blink_count': blink_count,
        'blink_rate': blink_rate,
        'eye_strain': '',
        'avg_distance_from_screen': avg_distance
    }

    if data['blink_rate'] < 20:  
        data['eye_strain'] = 'Low'
    elif 20 <= data['blink_rate'] < 30:
        data['eye_strain'] = 'Moderate'
    else:
        data['eye_strain'] = 'High'

    
    # Insert the data document into the collection
    collection.insert_one(data)
    
    # Close the MongoDB connection
    client.close()

def start_eye_detection(callback_func):

    global should_stop 

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['blink_db']
    collection = db['blink_data']

    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector(maxFaces=1)
    plotY = LivePlot(640, 360, [20, 50], invert=True)   

    idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
    ratioListLeft = []
    ratioListRight = []
    blinkCounter = 0
    counter = 0
    color = (255, 0, 255)

    blink_limit = 5             #blink limit
    time_interval = 10          #time interval in seconds
    data_interval = 10          # data storage interval in seconds

    data_time = time.time()
    start_interval = 0
    blink_count = 0

    start_time = time.time()
    end_time = time.time()

    # Create a toast notifier
    toaster = ToastNotifier()

    while not should_stop:
        key = cv2.waitKey(1) & 0xFF  # Wait for key events
        if key == 27:       # Press 'esc' to stop the program
            should_stop = True  # Set the should_stop flag to stop the loop
            callback_func()
            break

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, img = cap.read()
        img = cv2.resize(img, (640, 360))
        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:
            face = faces[0]
            # Calculate the average distance between leftUp and rightUp points as an example
            leftUp = face[159]
            rightUp = face[386]
            avg_distance = detector.findDistance(leftUp, rightUp)[0]  # Distance calculation based on specific points
            avg_distance = round(avg_distance, 2)
            
            for id in idList:
                cv2.circle(img, face[id], 5,color, cv2.FILLED)

            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            lenghtVerLeft, _ = detector.findDistance(leftUp, leftDown)
            lenghtHorLeft, _ = detector.findDistance(leftLeft, leftRight)
            cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
            cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

            ratioLeft = int((lenghtVerLeft / lenghtHorLeft) * 100)
            ratioListLeft.append(ratioLeft)

            rightUp = face[386]
            rightDown = face[374]
            rightLeft = face[362]
            rightRight = face[263]
            lenghtVerRight, _ = detector.findDistance(rightUp, rightDown)
            lenghtHorRight, _ = detector.findDistance(rightLeft, rightRight)
            cv2.line(img, rightUp, rightDown, (0, 200, 0), 3)
            cv2.line(img, rightLeft, rightRight, (0, 200, 0), 3)

            ratioRight = int((lenghtVerRight / lenghtHorRight) * 100)
            ratioListRight.append(ratioRight)   

            if len(ratioListLeft) > 3:
                ratioListLeft.pop(0)
            if len(ratioListRight) > 3:
                ratioListRight.pop(0)

            ratioAvgLeft = sum(ratioListLeft) / len(ratioListLeft)
            ratioAvgRight = sum(ratioListRight) / len(ratioListRight)

            if ratioAvgLeft < 20 and ratioAvgRight < 20 and counter == 0:
                blink_count += 1
                blinkCounter += 1
                color = (0,200,0)
                counter = 1
            if counter != 0:
                counter += 1
                if counter > 10:
                    counter = 0
                    color = (255,0, 255)

            cvzone.putTextRect(img, f'Blink Count: {blinkCounter}', (20, 100),
                            colorR=color)

            imgPlot = plotY.update(ratioAvgLeft, color)
            img = cv2.resize(img, (640, 360))
            imgStack = cvzone.stackImages([img, imgPlot], 2, 1)

        else:
            img = cv2.resize(img, (640, 360))
            imgStack = cvzone.stackImages([img, img], 2, 1)

        cv2.imshow("Image", imgStack)


        # Save blink data with timestamp to MongoDB at regular intervals
        end_data_time = time.time()
        elapsed_data_time = end_data_time - data_time

        if elapsed_data_time >= data_interval:
            store_blink_data(start_interval, data_interval, blink_count, (blink_count / data_interval) * 60, '', avg_distance)
            data_time = time.time()
            start_interval += data_interval
            blink_count = 0  # Reset blink count for the next interval

        # Check if blink limit is exceeded within time interval
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time >= time_interval:
            if blinkCounter < blink_limit:
                prompt_msg = f"Number of eye blinks ({blinkCounter}) is less than the expected count within the time interval!"
                toaster.show_toast("Blink More Often", prompt_msg, duration=1, threaded=True)  # Show Windows pop-up notification

            blinkCounter = 0
            start_time = time.time()

    cap.release()
    cv2.destroyAllWindows()
   


def stop_eye_detection():
    global should_stop
    should_stop = True