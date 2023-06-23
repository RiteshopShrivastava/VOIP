import speech_recognition as sr
import socket
import pyaudio
import wave
import requests
import subprocess
from gtts import gTTS
# from mpyg321.MPyg123Player import MPyg123Player
from playsound import playsound
# import sendfile
# from pyaudio import Stream


# Set up PyAudio object
p = pyaudio.PyAudio()

# Create a socket

# Bind the socket to a specific address and port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
# server_socket.bind(('192.168.78.35', 8000))

# Listen for incoming connections
server_socket.listen(4)  # 4 is no of connections waiting while server is busy

# Wait for a client to connect
print('Waiting for a client to connect...')

client_socket, address = server_socket.accept()
print('Client connected:', address)

while True:
    try:

        # Receive audio data from the client and play it
        # stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, frames_per_buffer=1024, output=True)
        stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, frames_per_buffer=1024, input=True)
        frames = []

        # Store data in chunks for 30 seconds
        for i in range(0, int(44100 / 1024 * 30)):
            audio_data = stream.read(1024)
            # data = client_socket.recv(1024)
            frames.append(audio_data)
        # while True:
        #     data = client_socket.recv(1024)
        #     # audio_data = sr.AudioData(data, 44100, 2)
        #     # frames.append(audio_data)
        #     if not data:
        #         break
        # Play the audio data using PyAudio
        # stream.write(data)

        # Stop and close the PyAudio stream
        # stream.stop_stream()
        # stream.close()
        # p.terminate()

        # Save the recorded data as a WAV file
        channels = 2
        filename = "output.wav"
        sample_format = pyaudio.paInt16  # 16 bits per sample
        fs = 44100  # Record at 44100 samples per second

        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        # transcribe audio file
        AUDIO_FILE = "output.wav"
        # client_socket.close()
        # use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file

            print("user says: " + r.recognize_google(audio))
        message = r.recognize_google(audio)

        r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})
        print("Bot says: ", end=' ')
        for i in r.json():
            bot_message = i['text']
            print(f"{bot_message}")

        # myobj = gTTS(text=bot_message, lang=language, slow=False)
        myobj = gTTS(text=bot_message )
        myobj.save("welcome.mp3")
        # Playing the converted file
        playsound('welcome.mp3')

    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))