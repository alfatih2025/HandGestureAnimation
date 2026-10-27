import cv2
import mediapipe as mp
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import threading
import time
import os
import serial  


WIDTH, HEIGHT = 1000, 700
NUM_PARTICLES = 5000  


SERIAL_PORT = 'COM6'
BAUD_RATE = 115200

try:
    esp32 = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"BERHASIL: Terhubung ke ESP32 di port {SERIAL_PORT}")
except Exception as e:
    esp32 = None
    print(f"PERINGATAN: ESP32 tidak ditemukan di {SERIAL_PORT} atau port sedang dipakai.")
    print("Mode simulasi aktif (Program tetap berjalan tanpa ESP32).")

lock = threading.Lock()
shared_data = {
    "mode": 1,
    "target_x": 0.0,
    "target_y": 0.0,
    "target_z": -12.0,
    "frame": None,
    "running": True
}


pos_space = np.random.uniform(-4.0, 4.0, (NUM_PARTICLES, 3))


pos_planet = np.zeros((NUM_PARTICLES, 3))
NUM_SPHERE = 1500  
for i in range(NUM_SPHERE):
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    r = 1.3  
    pos_planet[i, 0] = r * np.sin(theta) * np.cos(phi)
    pos_planet[i, 1] = r * np.sin(theta) * np.sin(phi)
    pos_planet[i, 2] = r * np.cos(theta)

for i in range(NUM_SPHERE, NUM_PARTICLES):
    theta = np.random.uniform(0, 2 * np.pi)
    r = np.random.uniform(1.8, 3.8)  
    pos_planet[i, 0] = r * np.cos(theta)
    pos_planet[i, 1] = np.random.uniform(-0.05, 0.05)  
    pos_planet[i, 2] = r * np.sin(theta)


text_img = np.zeros((200, 800), dtype=np.uint8)
cv2.putText(text_img, "C.R.E.S.T", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 3.5, 255, 12, cv2.LINE_AA)
y_indices, x_indices = np.where(text_img > 0)
x_text = (x_indices - 400) / 70.0
y_text = -(y_indices - 100) / 70.0 
z_text = np.random.uniform(-0.1, 0.1, len(x_text))
pos_text = np.zeros((NUM_PARTICLES, 3))
text_points = np.stack((x_text, y_text, z_text), axis=-1)
chosen_indices = np.random.choice(len(text_points), NUM_PARTICLES)
pos_text = text_points[chosen_indices]


pos_heart = np.zeros((NUM_PARTICLES, 3))
for i in range(NUM_PARTICLES):
    t = np.random.uniform(-np.pi, np.pi)
    p = np.random.uniform(-np.pi, np.pi)
    x = 2.0 * (np.sin(t) ** 3)
    y = 2.0 * np.cos(t) - 0.7 * np.cos(2*t) - 0.3 * np.cos(3*t) - 0.1 * np.cos(4*t)
    z = np.sin(p) * 0.4  
    pos_heart[i, 0] = x * 0.85
    pos_heart[i, 1] = (y * 0.85) + 0.5  
    pos_heart[i, 2] = z

# Mode 5: Logo Realistis Berwarna
pos_logo = np.zeros((NUM_PARTICLES, 3))
color_logo = np.zeros((NUM_PARTICLES, 3)) 
logo_path = 'WhatsApp Image 2026-07-15 at 08.27.52.jpeg' 

if os.path.exists(logo_path):
    logo_img = cv2.imread(logo_path, cv2.IMREAD_COLOR)
    logo_img = cv2.resize(logo_img, (300, 300)) 
    logo_img_rgb = cv2.cvtColor(logo_img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(logo_img_rgb, cv2.COLOR_RGB2GRAY)
    y_indices_logo, x_indices_logo = np.where(gray > 15)
    
    if len(x_indices_logo) > 0:
        x_logo = (x_indices_logo - 150) / 45.0
        y_logo = -(y_indices_logo - 150) / 45.0 
        z_logo = np.random.uniform(-0.02, 0.02, len(x_logo)) 
        
        logo_points = np.stack((x_logo, y_logo, z_logo), axis=-1)
        logo_colors = logo_img_rgb[y_indices_logo, x_indices_logo] / 255.0
        
        chosen_indices_logo = np.random.choice(len(logo_points), NUM_PARTICLES, replace=True)
        pos_logo = logo_points[chosen_indices_logo]
        color_logo = logo_colors[chosen_indices_logo]
else:
    print(f"PERINGATAN: Gambar '{logo_path}' tidak ditemukan di folder yang sama!")
    pos_logo = np.random.uniform(-2.0, 2.0, (NUM_PARTICLES, 3))
    color_logo = np.ones((NUM_PARTICLES, 3)) 

current_pos = np.copy(pos_space)
target_pos = np.copy(pos_space)

# ==========================================
# FUNGSI LOGIKA DETEKSI GESTUR
# ==========================================
def hitung_mode_gestur(hand_landmarks):
    tips = [8, 12, 16, 20]  
    pips = [6, 10, 14, 18]
    jari_berdiri = [hand_landmarks.landmark[t].y < hand_landmarks.landmark[p].y for t, p in zip(tips, pips)]
    
    total_jari = sum(jari_berdiri)
    
    if total_jari == 0: 
        return 4  # Genggam -> Hati
    if jari_berdiri[0] and not any(jari_berdiri[1:]):
        return 2  # Telunjuk -> Saturnus
    if jari_berdiri[0] and jari_berdiri[1] and not jari_berdiri[2] and not jari_berdiri[3]:
        return 3  # Peace -> Teks C.R.E.S.T
    if total_jari == 3:
        return 5  # 3 Jari -> Logo Realistis
    if total_jari == 4:
        return 6  # 4 Jari -> ESP32 LED ON (Mode Hardware)
        
    return 1  # 5 Jari / Default -> Kosmos

# ==========================================
# THREAD BACKGROUND: PROSES KAMERA, AI & ESP32
# ==========================================
def camera_thread_func():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)   
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    last_esp_state = False # Track status LED agar tidak spam data ke ESP32

    while shared_data["running"]:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.01)
            continue

        frame = cv2.flip(frame, 1)  
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        local_mode = 1
        local_x, local_y, local_z = 0.0, 0.0, -12.0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                local_mode = hitung_mode_gestur(hand_landmarks)
                
                wrist = hand_landmarks.landmark[0]
                local_x = (wrist.x - 0.5) * 10.0 
                local_y = -(wrist.y - 0.5) * 7.0 
                
                pinky_mcp = hand_landmarks.landmark[17]
                distance = math.sqrt((wrist.x - pinky_mcp.x)**2 + (wrist.y - pinky_mcp.y)**2)
                local_z = -10.0 - (1.0 / (distance + 0.01)) * 0.2
        
        # Kirim sinyal ke ESP32 HANYA ketika status berubah
        if local_mode == 6 and not last_esp_state:
            if esp32: 
                esp32.write(b'1')
            last_esp_state = True
        elif local_mode != 6 and last_esp_state:
            if esp32: 
                esp32.write(b'0')
            last_esp_state = False

        with lock:
            shared_data["mode"] = local_mode
            shared_data["target_x"] = local_x
            shared_data["target_y"] = local_y
            shared_data["target_z"] = local_z
            shared_data["frame"] = frame

    cap.release()
    if esp32: # Matikan LED saat program keluar
        esp32.write(b'0')
        esp32.close()

# ==========================================
# MAIN THREAD: RENDERING GRAFIS 3D 
# ==========================================
camera_thread = threading.Thread(target=camera_thread_func, daemon=True)
camera_thread.start()

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Space Gesture Controller + ESP32")

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)

clock = pygame.time.Clock()
rotation_angle = 0.0
hand_x, hand_y, hand_z = 0.0, 0.0, -12.0

while shared_data["running"]:
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            shared_data["running"] = False

    with lock:
        current_mode = shared_data["mode"]
        target_hand_x = shared_data["target_x"]
        target_hand_y = shared_data["target_y"]
        target_hand_z = shared_data["target_z"]
        frame = shared_data["frame"]

    if frame is not None:
        mode_labels = {
            1: "ROTASI KOSMOS (Terbuka)", 
            2: "SATURNUS 3D (Satu Jari)", 
            3: "TEKS C.R.E.S.T (Peace)", 
            4: "BENTUK HATI / LOVE (Kepal)",
            5: "LOGO REALISTIS (3 Jari)",
            6: "ESP32 LED ON (4 Jari)"
        }
        cv2.putText(frame, f"MODE: {mode_labels.get(current_mode, 'UNKNOWN')}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Tampilkan status koneksi ESP32 di layar OpenCV
        esp_status = "Tersambung" if esp32 is not None else "Tidak Terhubung"
        cv2.putText(frame, f"ESP32: {esp_status}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255) if esp32 else (0, 0, 255), 2)
        
        cv2.imshow("Hand Sensor Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            shared_data["running"] = False

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    hand_x += (target_hand_x - hand_x) * 0.25
    hand_y += (target_hand_y - hand_y) * 0.25
    hand_z += (target_hand_z - hand_z) * 0.25

    if current_mode == 1:
        target_pos = pos_space
        rotation_angle += 0.5 
    elif current_mode == 2:
        target_pos = pos_planet
        rotation_angle += 2.0 
    elif current_mode == 3:
        target_pos = pos_text
        rotation_angle = 0.0  
    elif current_mode == 4:
        target_pos = pos_heart
        rotation_angle += 1.5  
    elif current_mode == 5:
        target_pos = pos_logo
        rotation_angle = 0.0
    elif current_mode == 6:
        # Gunakan pos_space (Kosmos) sebagai basis untuk Mode 6 (Indikator ESP32 aktif)
        target_pos = pos_space
        rotation_angle += 1.5

    current_pos += (target_pos - current_pos) * 0.15

    if current_mode in [2, 3, 4, 5, 6]:
        glTranslatef(hand_x, hand_y, hand_z)
        if current_mode == 2:
            glRotatef(25, 1.0, 0.0, 0.5)
    else:
        glTranslatef(0.0, 0.0, -12.0)
    
    glRotatef(rotation_angle, 0.0, 1.0, 0.0)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPointSize(3.5)  
    
    glBegin(GL_POINTS)
    for i in range(NUM_PARTICLES):
        if current_mode == 3:
            glColor4f(0.0, 0.8, 1.0, 0.9)  
        elif current_mode == 5:
            glColor4f(color_logo[i, 0], color_logo[i, 1], color_logo[i, 2], 1.0)
        elif current_mode == 4:
            glColor4f(1.0, 0.1, 0.4, 0.95) 
        elif current_mode == 2 and i >= NUM_SPHERE:
            glColor4f(1.0, 0.7, 0.3, 0.6)  
        elif current_mode == 2 and i < NUM_SPHERE:
            glColor4f(1.0, 0.5, 0.0, 0.85) 
        elif current_mode == 6:
            # Mode Hardware Aktif: Partikel menyala warna Hijau Matrix terang
            glColor4f(0.0, 1.0, 0.2, 0.9)
        else:
            glColor4f(0.1, 0.5, 1.0, 0.8)  
            
        glVertex3f(current_pos[i, 0], current_pos[i, 1], current_pos[i, 2])
    glEnd()

    pygame.display.flip()
    clock.tick(60)

cv2.destroyAllWindows()
pygame.quit()
