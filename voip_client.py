import socket
import pyaudio


# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('localhost', 8000))

# Send audio data to the server
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
while True:
    data = stream.read(1024)
    client_socket.sendall(data)

# Close the connection
stream.stop_stream()
stream.close()
p.terminate()
client_socket.close()



######chatgpt code

# import socket
# import pyaudio
#
# # Create a socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # Connect to the server
# client_socket.connect(('localhost', 8000))
#
# # Set up PyAudio object
# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
#
# try:
#     while True:
#         # Read audio data from the microphone or any source
#         data = stream.read(1024)
#
#         # Send the audio data to the server
#         client_socket.sendall(data)
#
# finally:
#     # Close the connection and clean up resources
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#     client_socket.close()
