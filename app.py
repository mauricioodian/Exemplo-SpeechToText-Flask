from flask import Flask, render_template, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk

# Carregar as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

text = ''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exemplo')
def exemplo():
    return render_template('exemplo.html')


@app.route('/get_text', methods=['POST'])
def get_text():
    global text
    return jsonify({'valor': text})


@app.route('/clean_text')
def clean_text():
    global text
    text = ''
    return jsonify({'valor': text})


def continuous_transcription():

    # Configurações do Serviço de Fala do Azure
    api_key = os.getenv('API_KEY')
    region = os.getenv('REGION')

    # Define ID e Regiao do Servico no Azure, além da linguagem desejada
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
    speech_config.speech_recognition_language="pt-BR"

    # Define configurações de microfone e reconhecimento de fala
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Aumenta o tempo limite de duração de silêncio no inicio para 30seg e no fim para 10seg
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "30000")
    speech_recognizer.properties.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "10000")

    # Callback de reconhecimento que concatena valores de texto reconhecidos
    def recognized_cb(evt):
        global text
        text += ' ' + evt.result.text
        print("-----------------------------------------------------------------------")
        print(text)
        print("-----------------------------------------------------------------------")

    # Configurando callbacks de eventos de reconhecimento
    speech_recognizer.recognized.connect(recognized_cb)

    # Inicia o reconhecimento contínuo de fala
    speech_recognizer.start_continuous_recognition()

    return speech_recognizer


# Função que inicia a captura e reconhecimento continuo
@app.route('/start_transcription', methods=['POST'])
def start_transcription():
    global recognizer
    recognizer = continuous_transcription()
    return jsonify({'message': 'Captura Contínua Iniciada!'})


# Função que finaliza a captura e reconhecimento
@app.route('/stop_transcription', methods=['POST'])
def stop_transcription():
    global recognizer
    recognizer.stop_continuous_recognition()
    return jsonify({'message': 'Captura Contínua Finalizada!'})


if __name__ == '__main__':
    app.run()
