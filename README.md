# 🖐️ AI Hand Gesture Controller dengan ESP32 menggunakan Computer Vision

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-red?logo=espressif)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-green)
![OpenGL](https://img.shields.io/badge/OpenGL-3D-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

### **Sistem Kendali LED ESP32 Menggunakan Pengenalan Gestur Tangan Berbasis Artificial Intelligence (Computer Vision)**

</div>

---

# 📖 Deskripsi Proyek

Proyek ini merupakan implementasi **Artificial Intelligence (AI)** berbasis **Computer Vision** yang mampu mengenali gestur tangan secara *real-time* menggunakan **MediaPipe**, kemudian mengirimkan perintah ke **ESP32** melalui komunikasi **Serial USB**.

Selain mengendalikan perangkat keras (LED pada ESP32), aplikasi juga menampilkan **visualisasi partikel 3D interaktif menggunakan OpenGL**, sehingga setiap gestur tangan menghasilkan bentuk animasi yang berbeda.

Proyek ini menggabungkan beberapa teknologi modern dalam satu sistem, yaitu:

* Artificial Intelligence (Computer Vision)
* MediaPipe Hand Tracking
* OpenGL 3D Visualization
* Komunikasi Serial Python ↔ ESP32
* Embedded System menggunakan ESP32

---

# ✨ Fitur Utama

✅ Deteksi tangan secara **real-time**

✅ Pengenalan berbagai gestur tangan

✅ Visualisasi partikel 3D menggunakan OpenGL

✅ Komunikasi Serial Python ke ESP32

✅ Kontrol LED bawaan ESP32

✅ Mode simulasi apabila ESP32 tidak terhubung

✅ Latensi komunikasi sangat rendah

---

# 🏗️ Arsitektur Sistem

```
                Webcam
                   │
                   ▼
        MediaPipe Hand Tracking
                   │
                   ▼
          Deteksi Gestur Tangan
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
Visualisasi OpenGL      Serial Communication
      3D                      (USB)
                                │
                                ▼
                             ESP32
                                │
                                ▼
                          LED Built-in
```

---

# 🛠️ Kebutuhan Perangkat Keras

* ESP32 DevKit
* Kabel USB Data
* Laptop / PC
* Webcam

### Opsional

* Breadboard
* LED Eksternal
* Resistor 220Ω

---

# 💻 Kebutuhan Perangkat Lunak

## Arduino IDE

Install:

* Arduino IDE versi terbaru
* ESP32 Board Package
* Driver USB (CP210x / CH340)

---

## Python

Versi yang direkomendasikan

```
Python 3.10 atau lebih baru
```

---

# 📦 Instalasi Library Python

Install seluruh library berikut

```bash
pip install opencv-python
pip install mediapipe
pip install pygame
pip install PyOpenGL
pip install numpy
pip install pyserial
```

Atau menggunakan

```bash
pip install -r requirements.txt
```

Isi `requirements.txt`

```txt
opencv-python
mediapipe
pygame
PyOpenGL
numpy
pyserial
```

---

# ⚙️ Konfigurasi ESP32

Buka file

```
ESP32_LED_Controller.ino
```

Upload ke board ESP32 menggunakan Arduino IDE.

Program ESP32 bertugas menerima karakter dari Python melalui komunikasi serial.

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

# ⚙️ Konfigurasi Program Python

Pada file Python terdapat konfigurasi berikut

```python
SERIAL_PORT = "COM3"
```

Sesuaikan dengan port ESP32 Anda.

### Contoh

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
/ dev/cu.usbserial
```

Pastikan baudrate sama

```python
115200
```

---

# ▶️ Cara Menjalankan Program

## 1. Hubungkan ESP32

Hubungkan board ESP32 ke komputer menggunakan kabel USB.

---

## 2. Upload Program Arduino

Upload file

```
ESP32_LED_Controller.ino
```

hingga berhasil.

---

## 3. Install Library Python

```bash
pip install -r requirements.txt
```

---

## 4. Jalankan Program

```bash
python main.py
```

Apabila seluruh konfigurasi benar maka akan muncul:

* Kamera aktif
* Visualisasi 3D
* Status koneksi ESP32
* Deteksi gestur tangan

---

# ✋ Daftar Gestur Tangan

| Gestur         | Mode   | Visualisasi       | ESP32  |
| -------------- | ------ | ----------------- | ------ |
| Tangan Terbuka | Mode 1 | Partikel Kosmos   | OFF    |
| Telunjuk       | Mode 2 | Planet Saturnus   | OFF    |
| Peace (✌)      | Mode 3 | Tulisan C.R.E.S.T | OFF    |
| Genggam        | Mode 4 | Bentuk Hati       | OFF    |
| Tiga Jari      | Mode 5 | Logo Berwarna     | OFF    |
| Empat Jari     | Mode 6 | Hardware Mode     | LED ON |

---

# 🔌 Protokol Komunikasi Serial

Program Python hanya mengirim **1 karakter** ke ESP32.

### Menyalakan LED

```
1
```

Python

```python
esp32.write(b'1')
```

ESP32

```cpp
char command = Serial.read();
```

---

### Mematikan LED

```
0
```

Python

```python
esp32.write(b'0')
```

ESP32

```cpp
char command = Serial.read();
```

Pengiriman hanya satu karakter membuat komunikasi menjadi sangat cepat dan efisien.

---

# 🧠 Alur Kerja Sistem

```
Webcam
    │
    ▼
MediaPipe AI
    │
    ▼
Deteksi Landmark Tangan
    │
    ▼
Analisis Posisi Jari
    │
    ▼
Klasifikasi Gestur
    │
    ├────────► Visualisasi OpenGL
    │
    ▼
Komunikasi Serial
    │
    ▼
ESP32
    │
    ▼
LED Built-in
```

---

# 🖥️ Tampilan Program

Program menampilkan dua jendela utama.

### 1. OpenCV

Menampilkan:

* Kamera
* Skeleton tangan
* Nama mode gestur
* Status koneksi ESP32

### 2. OpenGL

Menampilkan animasi partikel 3D sesuai gestur tangan.

---

# ⚡ Performa

Estimasi performa pada komputer dengan spesifikasi menengah.

| Komponen          | Performa  |
| ----------------- | --------- |
| Kamera            | ±30 FPS   |
| OpenGL            | ±60 FPS   |
| MediaPipe         | Real-Time |
| Komunikasi Serial | <10 ms    |

---

# 🔍 Troubleshooting

## ESP32 Tidak Terdeteksi

Periksa:

* Kabel USB
* Driver USB
* Port COM
* Board ESP32

---

## Kamera Tidak Menyala

Pastikan

```python
cv2.VideoCapture(0)
```

Apabila gagal coba

```python
cv2.VideoCapture(1)
```

---

## LED Tidak Menyala

Pastikan

* Port COM benar
* Baudrate 115200
* Program berhasil di-upload
* LED bawaan menggunakan GPIO2

---

## Modul Python Tidak Ditemukan

Install ulang seluruh library

```bash
pip install -r requirements.txt
```

---

# 🚀 Pengembangan Selanjutnya

Beberapa fitur yang dapat ditambahkan:

* MQTT Communication
* Kontrol ESP32 melalui WiFi
* Integrasi Node-RED
* Dashboard Monitoring IoT
* TensorFlow Gesture Recognition
* YOLO Object Detection
* OLED Display ESP32
* Smart Home Automation
* Kendali Robot menggunakan Gestur Tangan

---

# 👨‍💻 Pengembang

**Habibullah Naja Alfatih Wibowo**

**Bidang Keahlian**

* Artificial Intelligence
* Internet of Things (IoT)
* Embedded Systems
* Computer Vision
* Software Development

GitHub

```
https://github.com/alfatih2025
```

---

# 📄 Lisensi

Proyek ini menggunakan lisensi **MIT License**.

Silakan menggunakan, mempelajari, mengembangkan, maupun memodifikasi proyek ini untuk keperluan pendidikan, penelitian, maupun pengembangan teknologi.

---

<div align="center">

⭐ Apabila proyek ini bermanfaat, jangan lupa berikan **Star** pada repository GitHub.

</div>
