import uvicorn
from fastapi import FastAPI, UploadFile, File
from pydub import AudioSegment
import os
import speech_recognition as sr
import requests

app = FastAPI()

@app.post("/upload_file")
async def upload_mp3_and_convert_to_wav(file: UploadFile):
    if file.content_type != 'audio/mpeg':
        return {"error": "Only MP3 files are allowed."}

    file_path = f"uploads/{file.filename}"

    # Save the uploaded MP3 file
    with open(file_path, "wb") as mp3_file:
        mp3_file.write(file.file.read())

    # Convert MP3 to WAV using pydub
    wav_file_path = f"uploads/{os.path.splitext(file.filename)[0]}.wav"
    audio = AudioSegment.from_mp3(file_path)
    audio.export(wav_file_path, format="wav")

    r = sr.Recognizer()
    r.energy_threshold = 300
    with sr.AudioFile(wav_file_path) as source:
        audio = r.record(source)  # read the entire audio file
        print("user says: " + r.recognize_google(audio))
    message = r.recognize_google(audio)
    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})
    # print("hi")
    bot_message = ""
    for i in r.json():
        # print(i,"checking")
        bot_message = i['text']
        # os.remove(file.filename)
        return {"status": 200,
                "message": bot_message}

    # return {"message": "File uploaded and converted to WAV successfully."}

if __name__ == '__main__':
    # app.run(debug=True)
    uvicorn.run(app, host='172.16.17.42')
    # main()



# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0',
#

#                 ssl_keyfile='C:/Users/MDP/OCR/mpcz.key',
#                 ssl_certfile='C:/Users/MDP/OCR/mpcz.crt')

#
# from fastapi import FastAPI, UploadFile, File
# import uvicorn
#
# app = FastAPI()
#
#
# @app.post("/upload_wav/")
# async def upload_wav_file(wav_file: UploadFile):
#     if not wav_file:
#         return {"error": "No file provided"}
#
#     # Check if the uploaded file is a .wav file
#     if not wav_file.filename.endswith(".wav"):
#         return {"error": "Only .wav files are allowed"}
#
#     # Process the .wav file here, e.g., save it to a directory
#     with open(wav_file.filename, "wb") as f:
#         f.write(wav_file.file.read())
#
#     return {"message": "File uploaded successfully"}
#
# if __name__ == '__main__':
#     # app.run(debug=True)
#     uvicorn.run(app)
