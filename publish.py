"""Publishes multiple messages to a Pub/Sub topic with an error handler."""
from concurrent import futures
import datetime
import json
from google.cloud import pubsub_v1
import os



# TODO start
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'testbot-service_dotted-marking-327507-3f09fb404fb7.json'

project_id      = 'dotted-marking-327507'
topic_id        = 'Testbot'
subscription_id = 'Testbot'

imageUrl = "https://lh5.googleusercontent.com/proxy/6tlNKVdkuog5DOJU17puXqZDKPoR3OnVrXhAyFX2zR9Q13dqofsl0DydZpZDA4SZvYgZDIK58VBLBjHXaH-sv0pVFcNBpx9YXNXHi4uTIseBjQMTZlXoAPIV4T7Sg4xJhOoQP7_B4UHuVpakwPaVe4WFg_BiYjRTjjivvzY4592akLl7Dc75Q4QNxp7CJW1BDgrML4e_rjLtPi9o8k4IpHifEjiaGjpLIsn0h6gaxeTkOVxZ_w3jXEqcteWlaOg7y3db2Hv4EWp2L_g6Ss1tfbGJZ8e2emHTYJWu772bB1KoWZgw6FTy6jI"
# TODO end



publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []



def itElse(obj, key, alt = None):
    if isinstance(obj, dict):
        return obj[key] if (key in obj) else alt
    return alt

def isKey(obj, key):
    if isinstance(obj, dict):
        return key in obj
    elif isinstance(obj, list):
        return len(obj) >= key + 1


def get_callback(publish_future: pubsub_v1.publisher.futures.Future, data: str):
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            publish_future.result(timeout=60)
        except futures.TimeoutError:
            print(f"\nPublishing {data} timed out.")

    return callback


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

        label   = itElse(section, 'label')
        content = itElse(section, 'content')
        image   = itElse(section, 'image')
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



    data = {
        "type": "CUSTOM",

        "eventTime": str(datetime.datetime.now()),

        "space": {
            "name": f"spaces/{message['recipient']}"
        }
    }

    if isKey(message, 'text') or card:
        data['message'] = {}

        if isKey(message, 'text'):
            data['message']['text'] = message['text']
            
        if isKey(card, 'header') or isKey(card, 'sections'):
            data['message']['cards'] = [card]

    if isKey(data, 'space') and isKey(data, 'message'):
        return json.dumps(data).encode('UTF-8')
    else:
        return None




data = cook({
    "recipient": "7gV80IAAAAE",
    "text": f'This is a custom message sent at ' + str(datetime.datetime.now()),

    "title": f"Card title",
    "subtitle": f"Card subtitle",
    "icon": imageUrl,
    
    "sections": [
        {
            "label": 'Label 1',
            "content": 'Content 1',
        },
        {
            "label": 'Label 2',
            "content": 'Content 2',
            "image": imageUrl,
        },
        {
            "label": 'Label 3',
            "buttons": [
                {
                    # "text": "Google",
                    "url": "www.google.com"
                },
                {
                    # "text": "DuckDuckGo",
                    "url": "www.duckduckgo.com"
                },
            ]
        }
    ]
})

print(data)
print()

if data:
    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data)

    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)



# Wait for all the publish futures to resolve before exiting.
futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

print(f"\n\nPublished message to {topic_path}.")
