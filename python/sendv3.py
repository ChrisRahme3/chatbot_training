from apiclient.discovery import build # pip install google-api-python-client
from concurrent import futures
import datetime
from flask import Flask, request
from google.cloud import pubsub_v1
from httplib2 import Http
import json
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2
import os



# TODO start
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'python/dotted-marking-327507-277d58834909.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dotted-marking-327507-277d58834909.json'

project_id      = 'dotted-marking-327507'
topic_id        = 'Testbot'
subscription_id = 'Testbot'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    'https://www.googleapis.com/auth/chat.bot'
).authorize(Http())

chat = build(
    serviceName = 'chat',
    version = 'v1',
    http = credentials
)

spaces = {
    'CR': '7gV80IAAAAE', # Chris Rahmé
    'GS': 'i9uCMIAAAAE', # George Salloum
}

myspace = spaces['CR']
# TODO end



def itElse(obj, key, alt = None):
    if isinstance(obj, dict):
        return obj[key] if (key in obj) else alt
    return alt

def isKey(obj, key):
    if isinstance(obj, dict):
        return key in obj
    elif isinstance(obj, list):
        return len(obj) >= key + 1



def cook(message):
    # Header
    header = {}

    if isKey(message, 'title') or isKey(message, 'subtitle') or isKey(message, 'image'):
        if isKey(message, 'title'):
            header['title'] = message['title']

        if isKey(message, 'subtitle'):
            header['subtitle'] = message['subtitle']

        if isKey(message, 'icon'):
            header['imageUrl'] = message['icon']
            header['imageStyle'] = "AVATAR"


    # Sections
    sections = []

    for section in itElse(message, 'sections', []):
        if len(section) == 0:
            break

        new_section = {}
        new_widgets = []

        label   = itElse(section, 'label', None)
        content = itElse(section, 'content', None)
        image   = itElse(section, 'image', None)
        buttons = []

        for button in itElse(section, 'buttons', []):
            url  = itElse(button, 'url', '#')
            text = itElse(button, 'text', url)

            new_button = {
                "textButton": {
                    "text": text,
                    "onClick": {
                        "openLink": {
                            "url": url
                        }
                    }
                }
            }

            buttons.append(new_button)

        if label or content:
            new_widget = {'keyValue': {}}

            if label:
                new_widget['keyValue']['topLabel'] = label
                
            if label and (not content):
                new_widget['keyValue']['content'] = ' '
            elif content:
                new_widget['keyValue']['content'] = content

            new_widgets.append(new_widget)

        if image:
            new_widget = {'image': {}}

            new_widget['image']['imageUrl'] = section['image']
            
            new_widgets.append(new_widget)

        if buttons:
            new_widget = {'buttons': []}

            new_widget['buttons'] = buttons

            new_widgets.append(new_widget)

        new_section['widgets'] = new_widgets
        sections.append(new_section)


    # Card
    card = {}

    if header:
        card['header'] = header

    if sections:
        card['sections'] = sections


    # Data
    data = {
        'space': "spaces/" + message['recipient']
    }

    if isKey(message, 'text'):
        data['text'] = message['text']

    if isKey(card, 'header') or itElse(card, 'sections'):
        data['cards'] = [card]

    if isKey(data, 'space') and (isKey(data, 'text') or isKey(data, 'cards')):
        return data
    else:
        return {}


def send(data):
    parent = itElse(data, 'space', None)
    body = {}

    text    = itElse(data, 'text', None)
    cards   = itElse(data, 'cards', None)

    if text:
        body['text'] = text

    if cards:
        body['cards'] = cards

    if parent and body:
        response = chat.spaces().messages().create(
            parent = parent,
            body = body
        ).execute()



###############################################################################



app = Flask(__name__)

@app.route('/', methods=['POST'])
def on_event():
    data = request.get_json()
    cooked = cook(data)

    print(data)
    send(cooked)

    return cooked

if __name__ == '__main__':
    app.run(port=9009, debug=True)
