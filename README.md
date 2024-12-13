# 🖐️ Gesture-Controlled Action Triggering System

A Python-based application to recognize hand gestures and trigger actions like launching apps, zooming, scrolling, and volume control! This project combines **MediaPipe** for gesture recognition, a SQLite database for gesture-action mapping, and **OpenCV** for camera input, making it a powerful tool for gesture-based interaction.

---

## 🎯 Features

- **Hand Gesture Recognition**: Detect gestures like `fist_closed`, `fist_opened`, `one_finger_up`, and `one_finger_down`.
- **Customizable Actions**: Assign gestures to actions via a database.
- **Actions Supported**:
    - Open applications
    - Adjust volume
    - Zoom in/out
    - Scroll up/down
- **Debug Logs**: Displays a log of recognized gestures with timestamps in real-time alongside the camera feed.

---

## 📦 Prerequisites

- Python 3.7 or newer
- A webcam or laptop camera

---

## 🚀 Setup Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/gesture-control-app.git
cd gesture-control-app
```

### 2️⃣ Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3️⃣ Activate the Virtual Environment

- On **Linux/macOS**:
    
    ```bash
    source venv/bin/activate
    ```
    
- On **Windows**:
    
    ```bash
    venv\Scripts\activate
    ```
    

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Initialize the Database

Run the provided gesture configuration script to initialize the SQLite database:

```bash
python gesture_config_app.py
```

---

## 🖥️ How to Use

### Step 1: Configure Gestures

Run the `gesture_config_app.py` script to assign gestures to actions:

```bash
python gesture_config_app.py
```

- Choose a gesture.
- Select an action type (`Open App` or `Accessibility Option`).
- Assign an action (e.g., `/usr/bin/firefox` or `Volume Up`).
- Save your configuration.

### Step 2: Start the Gesture Detection

Run the `gesture_detection.py` script to start detecting gestures and triggering actions:

```bash
python gesture_detection.py
```

### Step 3: Quit the Program

Press `q` in the camera feed window to exit.

---

## 🛠️ Project Structure

- **`gesture_config_app.py`**: A GUI tool to configure gestures and save them to the database.
- **`gesture_detection.py`**: The main program to detect gestures using the webcam and trigger the assigned actions.
- **`gestures.db`**: SQLite database storing gesture-action mappings.
- **`requirements.txt`**: Lists all the Python dependencies for the project.

---

## 📋 Requirements

This project uses the following Python libraries:

- **OpenCV**: For video capture and display
- **MediaPipe**: For hand gesture recognition
- **PyAutoGUI**: To control keyboard and mouse
- **SQLite**: For gesture-action mapping
- **Subprocess**: For launching applications

---

## 📸 Screenshots

| Gesture Recognition |                |
| ------------------- | -------------- |
| ![Screenshot](/SRCS/SCRS1.png) | ![Screenshot](/SRCS/SCRS3.png) |
| ![Screenshot](/SRCS/SCRS2.png) | ![Screenshot](/SRCS/SCRS4.png) |
