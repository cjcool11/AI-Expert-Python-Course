import pyaudio
import numpy as np
import keyboard

RATE = 44100
CHUNK = 1024

p = pyaudio.PyAudio()

stream_in = p.open(format=pyaudio.paFloat32,
                   channels=1,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)

stream_out = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

def pitch_shift(data, shift):
    fft = np.fft.rfft(data)
    shifted = np.zeros_like(fft)
    s = int(len(fft) * shift)
    if s < len(fft):
        shifted[:s] = fft[:s]
    return np.fft.irfft(shifted)

def robot(data):
    t = np.arange(len(data))
    mod = np.sin(2 * np.pi * 50 * t / RATE)
    return data * mod

def echo(data, buffer, decay):
    buffer[:len(data)] = data + buffer[:len(data)] * decay
    return buffer[:len(data)]

def radio(data):
    fft = np.fft.rfft(data)
    fft[2000:] = 0
    return np.fft.irfft(fft)

echo_buffer = np.zeros(CHUNK)
mode = "pitch"

print("Voice Filter Active")
print("Modes: pitch, robot, echo, radio")
print("Press 1/2/3/4 to switch modes")
print("Press SPACE to stop recording")

running = True

while running:
    if keyboard.is_pressed("space"):
        print("Stopped.")
        running = False
        break

    raw = stream_in.read(CHUNK, exception_on_overflow=False)
    data = np.frombuffer(raw, dtype=np.float32)

    if mode == "pitch":
        out = pitch_shift(data, 0.6)
    elif mode == "robot":
        out = robot(data)
    elif mode == "echo":
        out = echo(data, echo_buffer, decay=0.4)
    elif mode == "radio":
        out = radio(data)
    else:
        out = data

    stream_out.write(out.astype(np.float32).tobytes())

    if keyboard.is_pressed("1"):
        mode = "pitch"
        print("Pitch mode")
    if keyboard.is_pressed("2"):
        mode = "robot"
        print("Robot mode")
    if keyboard.is_pressed("3"):
        mode = "echo"
        print("Echo mode")
    if keyboard.is_pressed("4"):
        mode = "radio"
        print("Radio mode")

stream_in.stop_stream()
stream_in.close()
stream_out.stop_stream()
stream_out.close()
p.terminate()
