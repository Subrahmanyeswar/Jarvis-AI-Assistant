# C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\main.py

import cv2
import os
import numpy as np
import face_recognition
from ultralytics import YOLO
import torch
# Your original torch imports are preserved for compatibility
from ultralytics.nn.tasks import DetectionModel
from torch.nn.modules.container import Sequential
from torch.nn.modules import Module
import pickle
from deepface import DeepFace
import datetime
import logging
import sqlite3
import smtplib
from email.mime.text import MIMEText
import threading

# --- UPGRADE 1: IMPORT JARVIS'S VOICE ---
# We replace the old 'playsound' import with our new, intelligent voice module.
from ai_core.voice_output import speak

# This is your custom logger, which is preserved. Ensure 'logger.py' exists.
from logger import log_message
log_message("DETECT", "Logger working ✅")
log_message("AI_CORE", "Voice assistant online.")
log_message("PROD", "No pending reminders.")
log_message("AUTO", "Listening for automation commands...")
log_message("EXTRAS", "Battery health: Good")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# --- GPU DEVICE SETUP ---
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"--- System Info ---")
print(f"PyTorch is using device: {DEVICE}")
try:
    import tensorflow as tf
    gpu_devices = tf.config.list_physical_devices('GPU')
    if gpu_devices:
        print(f"TensorFlow is using device: {gpu_devices[0].name}")
    else:
        print("TensorFlow is using device: CPU")
except Exception as e:
    print(f"Could not check TensorFlow device: {e}")
print(f"--------------------")

# All your original setup code is preserved
logging.basicConfig(filename="security_log.txt", level=logging.INFO, 
                    format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()

conn = sqlite3.connect("security_events.db")
conn.execute("CREATE TABLE IF NOT EXISTS events (timestamp TEXT, event_type TEXT, details TEXT)")
conn.commit()

def log_to_db(event_type, details):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("INSERT INTO events (timestamp, event_type, details) VALUES (?, ?, ?)",
                 (timestamp, event_type, details))
    conn.commit()

# Define paths
YOLO_MODEL_PATH = "models/yolov8n.pt"
AUTHORIZED_FOLDER = r"C:\Users\SUBBU\Downloads\RealTimeSecuritySystem\data\authorized_faces"
ENCODINGS_CACHE = "authorized_encodings.pkl"
VIDEO_OUTPUT_DIR = "recordings"
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

# --- UPGRADE 2: GPU ACCELERATION ---
print("Loading YOLOv8 model...")
with torch.serialization.safe_globals([DetectionModel, Sequential, Module]):
    yolo_model = YOLO(YOLO_MODEL_PATH)
yolo_model.to(DEVICE) # Explicitly move the model to the GPU
print(f"YOLOv8 model loaded and is running on device: {yolo_model.device}")

# All your original face encoding logic is preserved
AUTHORIZED_NAMES = [name for name in os.listdir(AUTHORIZED_FOLDER) 
                    if os.path.isdir(os.path.join(AUTHORIZED_FOLDER, name))]
UNAUTHORIZED_OBJECTS = ["knife", "gun", "weapon"]
AUTHORIZED_ENCODINGS = {}
try:
    if os.path.exists(ENCODINGS_CACHE):
        print("Loading cached face encodings...")
        with open(ENCODINGS_CACHE, "rb") as f:
            AUTHORIZED_ENCODINGS = pickle.load(f)
        print("✅ Loaded cached encodings")
    else:
        raise FileNotFoundError("Cache file not found")
except (FileNotFoundError, pickle.PickleError, Exception) as e:
    print(f"⚠ Failed to load cached encodings: {e}. Recomputing...")
    print("Preloading authorized face encodings...")
    for name in AUTHORIZED_NAMES:
        authorized_path = os.path.join(AUTHORIZED_FOLDER, name)
        encodings = []
        for img_name in os.listdir(authorized_path):
            if img_name.lower().endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(authorized_path, img_name)
                img = face_recognition.load_image_file(img_path)
                encoding = face_recognition.face_encodings(img)
                if encoding:
                    encodings.append(encoding[0])
                    break 
        if encodings:
            AUTHORIZED_ENCODINGS[name] = encodings[0]
            print(f"✅ Loaded encoding for {name}")
        else:
            print(f"⚠ No valid encodings for {name}")
    try:
        with open(ENCODINGS_CACHE, "wb") as f:
            pickle.dump(AUTHORIZED_ENCODINGS, f)
        print("✅ Saved encodings to cache")
    except Exception as e:
        print(f"⚠ Failed to save encodings to cache: {e}")

# Video recording setup is preserved
recording = False
video_writer = None
recording_start_time = None
RECORD_DURATION = 10

# Email setup is preserved (ensure your credentials are correct)
EMAIL_ADDRESS = "subrahmanyeswarkolluru@gmail.com"
EMAIL_PASSWORD = "jwbrsskuwubmbibz" 
def send_email_alert(subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email alert sent successfully")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

# --- UPGRADE 3: JARVIS VOICE ALERTS ---
# This new function replaces the old 'play_buzzer' function.
def issue_voice_alert(message):
    """Issues a voice alert using JARVIS in a separate thread."""
    threading.Thread(target=speak, args=(message,), daemon=True).start()

# --- Main Frame Processing Logic (Preserved with only alert changes) ---
def process_frame(frame):
    global recording, video_writer, recording_start_time
    unauthorized_detected = False
    status_text = "All Clear"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        recognized, color, min_distance, closest_match, expression = "Unknown", (0, 0, 255), float('inf'), None, "N/A"
        
        print("Distances to authorized persons:")
        for name, auth_encoding in AUTHORIZED_ENCODINGS.items():
            distance = np.linalg.norm(face_encoding - auth_encoding)
            print(f"  - {name}: {distance:.3f}")
            if distance < min_distance:
                min_distance = distance
                closest_match = name
        
        if min_distance < 0.5:
            recognized, color = closest_match, (0, 255, 0)
            print(f"Recognized as {recognized} with distance {min_distance:.3f}")
            logger.info(f"Authorized person detected: {recognized}")
            log_to_db("Authorized Person", recognized)
        else:
            print(f"No match found (min distance {min_distance:.3f} exceeds threshold 0.5)")
            unauthorized_detected, status_text = True, "ALERT: Unauthorized Person"
            logger.info("Unauthorized person detected")
            log_to_db("Unauthorized Person", "Unknown")
            send_email_alert("Security Alert - Unauthorized Person", f"An unauthorized person was detected at {timestamp}.")
            # --- VOICE ALERT REPLACES BUZZER ---
            issue_voice_alert("Warning. Unauthorized person detected.")

        try:
            face_img = frame[top:bottom, left:right]
            result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
            expression = result[0]['dominant_emotion'].capitalize()
            print(f"Facial Expression: {expression}")
        except Exception as e:
            print(f"Failed to detect facial expression: {e}")

        label = f"{recognized} - {expression}"
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, label, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # We pass the device to the model call for certainty
    results = yolo_model(frame, device=DEVICE, verbose=False)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id, confidence = int(box.cls[0]), float(box.conf[0])
            label = result.names[class_id]
            print(f"Detected {label} with confidence {confidence:.2f}")
            
            if label in UNAUTHORIZED_OBJECTS and confidence > 0.5:
                unauthorized_detected, status_text = True, f"ALERT: Unauthorized Object ({label})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f"ALERT: {label}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                logger.info(f"Unauthorized object detected: {label}")
                log_to_db("Unauthorized Object", label)
                send_email_alert("Security Alert - Unauthorized Object", f"An unauthorized object ({label}) was detected at {timestamp}.")
                # --- VOICE ALERT REPLACES BUZZER ---
                issue_voice_alert(f"Alert. Unauthorized object detected: {label}.")
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    status_color = (0, 255, 0) if status_text == "All Clear" else (0, 0, 255)
    cv2.putText(frame, status_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

    if unauthorized_detected and not recording:
        recording, recording_start_time = True, datetime.datetime.now()
        video_filename = os.path.join(VIDEO_OUTPUT_DIR, f"unauthorized_{recording_start_time.strftime('%Y-%m-%d_%H-%M-%S')}.avi")
        video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame.shape[1], frame.shape[0]))
        print(f"Started recording: {video_filename}")

    if recording:
        video_writer.write(frame)
        elapsed_time = (datetime.datetime.now() - recording_start_time).total_seconds()
        if elapsed_time > RECORD_DURATION or not unauthorized_detected:
            recording = False
            video_writer.release()
            video_writer = None
            print("Stopped recording")

    if unauthorized_detected:
        print("🚨 ALERT! Unauthorized person or object detected!")
    
    return frame, status_text # Return status_text for the GUI

# --- CORRECTED MAIN LOOP ---
# The main execution block and cleanup are now safely inside this 'if' statement.
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame, _ = process_frame(frame) # We don't need the status text here
        
        cv2.imshow("Real-Time Security System", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Cleanup
    if recording and video_writer is not None:
        video_writer.release()
    conn.close()
    cap.release()
    cv2.destroyAllWindows()