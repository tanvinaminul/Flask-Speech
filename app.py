from flask import Flask, render_template
from flask import request as flask_request
from playsound import playsound
import azure.cognitiveservices.speech as speechsdk
import os, uuid, json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    
    speech_config = speechsdk.SpeechConfig(subscription="a9946f8b3d524bcc8da4a19bd4867f14", region="eastus")
    speech_config.speech_synthesis_language = "en-US"
    speech_config.speech_synthesis_voice_name ="en-US-JennyNeural"
    text = flask_request.form['text']
    audio_config = speechsdk.audio.AudioOutputConfig(filename="tune.wav")
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text_async("Getting the response as an in-memory stream.").get()  
    playsound("tune.wav")
    return render_template(
        'results.html'
    )
if __name__== "__main__":
    app.run(debug=False, host= '0.0.0.0')