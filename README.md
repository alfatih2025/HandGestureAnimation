# 🖐️ AI Hand Gesture Controller with ESP32 LED Communication

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-red?logo=espressif)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-green)
![OpenGL](https://img.shields.io/badge/OpenGL-3D-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

**Real-Time Hand Gesture Recognition using Artificial Intelligence with Computer Vision and Serial Communication to ESP32**

</div>

---

# 📖 Overview

This project demonstrates how Artificial Intelligence (Computer Vision) can control hardware in real-time.

The Python application uses **MediaPipe Hand Tracking** to recognize hand gestures from a webcam. Every detected gesture changes a 3D particle visualization rendered with OpenGL. One specific gesture also sends a serial command to an ESP32, allowing physical hardware (built-in LED) to respond instantly.

The communication protocol between Python and ESP32 is intentionally lightweight by transmitting only a single character through Serial.

```
Webcam
   │
   ▼
MediaPipe AI
   │
   ▼
Gesture Detection
   │
   ├────────► OpenGL Visualization
   │
   ▼
Serial Communication
   │
   ▼
ESP32
   │
   ▼
Built-in LED
```

---

# ✨ Features

- Real-time hand tracking
- AI gesture recognition
- OpenGL 3D particle animation
- Multi-mode visualization
- ESP32 serial communication
- Low latency hardware control
- Automatic LED synchronization
- Simulation mode when ESP32 is disconnected

---

# 📂 Project Structure

```
AI-Hand-Gesture-ESP32/
│
├── Arduino/
│   └── ESP32_LED_Controller.ino
│
├── Python/
│   ├── main.py
│   └── logo.jpg
│
├── requirements.txt
│
├── README.md
│
└── LICENSE
```

---

# 🛠 Hardware Requirements

- ESP32 DevKit
- USB Cable
- Computer
- Webcam

Optional

- External LED
- Breadboard

---

# 💻 Software Requirements

## Arduino IDE

Install:

- ESP32 Board Package
- USB Driver (CP210x / CH340)

---

## Python

Python Version

```
Python 3.10+
```

---

# 📦 Python Libraries

Install all dependencies:

```bash
pip install opencv-python
pip install mediapipe
pip install pygame
pip install PyOpenGL
pip install numpy
pip install pyserial
```

or

```bash
pip install -r requirements.txt
```

Example requirements.txt

```txt
opencv-python
mediapipe
pygame
PyOpenGL
numpy
pyserial
```

---

# ⚙ ESP32 Setup

Open

```
ESP32_LED_Controller.ino
```

Upload to ESP32.

Code:

```cpp
const int ledPin = 2;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void loop() {

  if (Serial.available()) {

    char command = Serial.read();

    if(command=='1')
      digitalWrite(ledPin,HIGH);

    else if(command=='0')
      digitalWrite(ledPin,LOW);
  }
}
```

---

# ⚙ Configure Python

Open

```python
SERIAL_PORT = "COM3"
```

Replace with your own port.

Example

Windows

```python
COM3
```

Linux

```python
/dev/ttyUSB0
```

macOS

```python
/dev/cu.usbserial
```

Baudrate must match the ESP32

```python
115200
```

---

# ▶ Running the Project

## Step 1

Connect ESP32

---

## Step 2

Upload Arduino Sketch

---

## Step 3

Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4

Run

```bash
python main.py
```

---

# 🎮 Gesture Mapping

| Gesture | Mode | Visualization | ESP32 |
|----------|------|--------------|--------|
| Open Hand | 1 | Space | OFF |
| Index Finger | 2 | Saturn | OFF |
| Peace | 3 | C.R.E.S.T Text | OFF |
| Closed Fist | 4 | Heart | OFF |
| Three Fingers | 5 | Logo | OFF |
| Four Fingers | 6 | Hardware Mode | LED ON |

---

# 🔌 Serial Communication

Python only sends one byte.

LED ON

```
1
```

LED OFF

```
0
```

Example

```python
esp32.write(b'1')
```

```python
esp32.write(b'0')
```

ESP32 receives

```cpp
char command = Serial.read();
```

This protocol minimizes communication latency while maintaining reliable synchronization.

---

# 🧠 Gesture Detection Pipeline

```
Webcam

      │

      ▼

MediaPipe

      │

      ▼

21 Hand Landmarks

      │

      ▼

Finger State Analysis

      │

      ▼

Gesture Classification

      │

      ├────────► 3D Visualization

      │

      ▼

Serial Communication

      │

      ▼

ESP32

      │

      ▼

LED
```

---

# 📷 User Interface

The application displays

- Live camera feed
- Hand skeleton
- Current gesture mode
- ESP32 connection status
- Real-time OpenGL particle visualization

---

# ⚡ Performance

Approximate performance on a modern PC

| Component | Performance |
|------------|------------|
| Camera | 30 FPS |
| OpenGL | 60 FPS |
| MediaPipe | Real-Time |
| Serial Delay | <10 ms |

---

# 🔍 Troubleshooting

## ESP32 Not Detected

Check

- USB cable
- COM port
- USB Driver
- Arduino IDE Port

---

## Camera Cannot Open

Verify

```python
cv2.VideoCapture(0)
```

Try

```python
cv2.VideoCapture(1)
```

---

## LED Doesn't Turn On

Verify

- Correct COM port
- Baudrate 115200
- Successful upload
- Built-in LED pin (GPIO2)

---

## Missing Python Modules

Install

```bash
pip install -r requirements.txt
```

---

# 🚀 Future Improvements

- MQTT Communication
- WiFi ESP32 Control
- Multiple ESP32 Devices
- Voice Command
- YOLO Object Detection
- TensorFlow Gesture Recognition
- OLED Display Integration
- Home Automation Support

---

# 👨‍💻 Author

**Habibullah Naja Alfatih Wibowo**

AI • IoT • Embedded Systems • Software Development

GitHub

```
https://github.com/alfatih2025
```

---

# 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this project for educational and research purposes.

---

<div align="center">

⭐ If you find this project useful, consider giving it a star on GitHub.

</div>
