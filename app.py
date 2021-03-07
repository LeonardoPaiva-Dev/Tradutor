from flask import Flask, request, render_template
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    texto_original = request.form['text']
    idioma_alvo = request.form['language']

    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    path = '/translate?api-version=3.0'

    idioma_alvo_par = '&to=' + idioma_alvo

    url = endpoint + path + idioma_alvo_par

    headers = {'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
        }

    body = [{'text': texto_original}]

    request_tradutor = requests.post(url, headers=headers, json=body)
    response_tradutor = request_tradutor.json()
    texto_traduzido = response_tradutor[0]['translations'][0]['text']

    return render_template('results.html', texto_traduzido=texto_traduzido, texto_original=texto_original, idioma_alvo=idioma_alvo)