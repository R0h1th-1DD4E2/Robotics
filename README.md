# Gesture-Controlled Robot using ESP8266 and OpenCV

![Gesture-Controlled Robot]()

This repository contains the code and resources for building a **gesture-controlled robot** using an **ESP8266** microcontroller, which will later transition to an **ESP32**, and **Python** with **OpenCV** for image processing.

## Overview
The goal of this project is to create a robot that responds to hand gestures, allowing you to control its movement. We'll use computer vision techniques to detect hand gestures and translate them into commands for the robot.

## Features
- **Gesture Detection**: The robot will recognize specific hand gestures to perform different actions.
- **Wireless Communication**: The ESP8266 (and later, ESP32) will communicate wirelessly with the robot.
- **OpenCV Integration**: We'll use OpenCV for hand tracking and gesture recognition.
- **Expandability**: The codebase is designed to be extensible, allowing you to add more gestures or features.

## Getting Started
1. **Hardware Setup**:
    - Assemble your robot hardware, including motors, wheels, and the ESP8266.
    - Connect the necessary components (motor drivers, sensors, etc.).

2. **Software Setup**:
    - Install the Arduino IDE and set up the ESP8266 board support.
    - Upload the provided Arduino sketch (`Boty.ino`) to your ESP8266.

3. **Gesture Detection**:
    - Use OpenCV to detect hand gestures. Refer to the `Handtracker.py` script for details.

4. **Robot Control**:
    - Implement the logic for translating detected gestures into robot movements.
    - Modify the `Boty.ino` sketch to handle these commands.


## Usage
1. Install the reqired libraries using the command `pip install -r requirements.txt`
2. Run the `Handtracker.py` script on your computer (acting as the client).
3. The robot will act as the server, receiving gesture commands from the client.
4. The following gestures are assigned for robot movement:
    - Halt
    - Forward movement
    - Left turn
    - Right turn
    - Move backward
    - To quit the program, press the **'q'** key.

## Future Improvements
- Transition to the ESP32 for better performance and additional features.
- Enhance gesture recognition accuracy.
- Add more gestures or custom commands.

Feel free to contribute, report issues, or suggest improvements! 🤖👋
