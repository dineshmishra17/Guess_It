import cv2
import time

# ------------------- PATHS -------------------
video_path = r"C:\Users\HP\Desktop\traffic3.mp4"
cascade_path = r"C:\Users\HP\Desktop\haarcascade_car.xml"

# ------------------- LOAD CASCADE -------------------
car_cascade = cv2.CascadeClassifier(cascade_path)
if car_cascade.empty():
    raise IOError(f"Cannot load cascade file at {cascade_path}")

# ------------------- VIDEO CAPTURE -------------------
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError(f"Cannot open video {video_path}")

# ------------------- TRAFFIC LIGHT VARIABLES -------------------
traffic_light_state = "RED"
last_switch = time.time()
red_time = 0
yellow_time = 0
green_time = 0

# ------------------- COLORS -------------------
colors = {"RED": (0, 0, 255), "YELLOW": (0, 255, 255), "GREEN": (0, 255, 0)}

# ------------------- WINDOW -------------------
cv2.namedWindow("Smart Traffic Light Simulation", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Smart Traffic Light Simulation", 1000, 700)

# ------------------- MAIN LOOP -------------------
while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Resize frame to fit window
    frame = cv2.resize(frame, (800, 600))

    # Convert to gray for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 2)
    vehicle_count = len(cars)

    # Update traffic light every 5 seconds
    if time.time() - last_switch > 5:
        if vehicle_count > 3:
            traffic_light_state = "GREEN"
        elif 1 <= vehicle_count <= 3:
            traffic_light_state = "YELLOW"
        else:
            traffic_light_state = "RED"
        last_switch = time.time()

    # Draw vehicle rectangles
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Draw traffic light panel
    cv2.rectangle(frame, (10, 10), (110, 250), (50, 50, 50), -1)
    cv2.circle(frame, (60, 60), 30, colors["RED"] if traffic_light_state == "RED" else (80, 80, 80), -1)
    cv2.circle(frame, (60, 120), 30, colors["YELLOW"] if traffic_light_state == "YELLOW" else (80, 80, 80), -1)
    cv2.circle(frame, (60, 180), 30, colors["GREEN"] if traffic_light_state == "GREEN" else (80, 80, 80), -1)

    # Update timer counts
    if traffic_light_state == "RED":
        red_time += 0.1
    elif traffic_light_state == "YELLOW":
        yellow_time += 0.1
    else:
        green_time += 0.1

    # Display text info
    cv2.putText(frame, f"Traffic Light: {traffic_light_state}", (150, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    info = f"RED: {int(red_time)}s  YELLOW: {int(yellow_time)}s  GREEN: {int(green_time)}s  Vehicles: {vehicle_count}"
    cv2.putText(frame, info, (150, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show frame
    cv2.imshow("Smart Traffic Light Simulation", frame)

    # Exit on ESC key
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()