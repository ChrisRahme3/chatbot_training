from apiclient.discovery import build # pip install google-api-python-client
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2
import os



# TODO start
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'testbot-service_dotted-marking-327507-3f09fb404fb7.json'

project_id      = 'dotted-marking-327507'
topic_id        = 'Testbot'
subscription_id = 'Testbot'

credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'https://www.googleapis.com/auth/chat.bot')
chat = build(serviceName = 'chat', version = 'v1', http = credentials.authorize(Http()))

spaces = {
    'CR': '7gV80IAAAAE', # Chris Rahmé
    'GS': 'i9uCMIAAAAE', # George Salloum
}

myspace = spaces['CR']

image_url = 'https://lh5.googleusercontent.com/proxy/6tlNKVdkuog5DOJU17puXqZDKPoR3OnVrXhAyFX2zR9Q13dqofsl0DydZpZDA4SZvYgZDIK58VBLBjHXaH-sv0pVFcNBpx9YXNXHi4uTIseBjQMTZlXoAPIV4T7Sg4xJhOoQP7_B4UHuVpakwPaVe4WFg_BiYjRTjjivvzY4592akLl7Dc75Q4QNxp7CJW1BDgrML4e_rjLtPi9o8k4IpHifEjiaGjpLIsn0h6gaxeTkOVxZ_w3jXEqcteWlaOg7y3db2Hv4EWp2L_g6Ss1tfbGJZ8e2emHTYJWu772bB1KoWZgw6FTy6jI'
# TODO end



cards = [
    {
        "sections": [ {
            "widgets": [
                { "image": { "imageUrl": image_url } },
                { "buttons": [ { "textButton": { "text": "OPEN", "onClick": { "openLink": { "url": "https://www.example.com" } } } } ] }
            ]
        } ]
    }
]

cards = [
    {
        "header": { # optional
            "title": "header title",
            "subtitle": "header subtitle",
            "imageUrl": image_url,
            "imageStyle": "IMAGE" # IMAGE, AVATAR
        },

        "sections": [ # must contain at least 1
            { # section 0
                "widgets": [
                    { # widgets 0
                        "keyValue": {
                            "topLabel": "sections 0 widgets 0 keyValue topLabel",
                            "content": "sections 0 widgets 0 keyValue content"
                        }
                    },
                    { # widgets 1
                        "keyValue": {
                            "topLabel": "sections 0 widgets 1 keyValue topLabel",
                            "content": "sections 0 widgets 1 keyValue content"
                        }
                    }
                ]
            },

            { # section 1
                "header": "sections 1 header",
                "widgets": [
                    { # widgets 0
                        "image": {
                            "imageUrl": image_url
                        }
                    }
                ]
            },

            { # section 2
                "widgets": [
                    { # widgets 0
                        "buttons": [
                            { # buttons 0
                                "textButton": {
                                    "text": "sections 2 widgets 0 buttons 0 textButton text",
                                    "onClick": {
                                        "openLink": {
                                            "url": "https://example.com"
                                        }
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        ] 
    }
  ]

cards = [{
    "header":{
        "title":"Card title",
        "subtitle":"Card subtitle",
        "imageUrl":"https://lh5.googleusercontent.com/proxy/6tlNKVdkuog5DOJU17puXqZDKPoR3OnVrXhAyFX2zR9Q13dqofsl0DydZpZDA4SZvYgZDIK58VBLBjHXaH-sv0pVFcNBpx9YXNXHi4uTIseBjQMTZlXoAPIV4T7Sg4xJhOoQP7_B4UHuVpakwPaVe4WFg_BiYjRTjjivvzY4592akLl7Dc75Q4QNxp7CJW1BDgrML4e_rjLtPi9o8k4IpHifEjiaGjpLIsn0h6gaxeTkOVxZ_w3jXEqcteWlaOg7y3db2Hv4EWp2L_g6Ss1tfbGJZ8e2emHTYJWu772bB1KoWZgw6FTy6jI",
        "imageStyle":"AVATAR"
    },

    "sections": [
        {
            "widgets": [
                {
                    "keyValue":{
                        "topLabel":"Label 1",
                        "content":"Content 1"
                    }
                }
            ]
        },
        {
            "widgets":[
                {
                    "keyValue":{
                        "topLabel":"Label 2",
                        "content":"Content 2"
                    }
                },
                {
                    "image":{
                        "imageUrl":"https://lh5.googleusercontent.com/proxy/6tlNKVdkuog5DOJU17puXqZDKPoR3OnVrXhAyFX2zR9Q13dqofsl0DydZpZDA4SZvYgZDIK58VBLBjHXaH-sv0pVFcNBpx9YXNXHi4uTIseBjQMTZlXoAPIV4T7Sg4xJhOoQP7_B4UHuVpakwPaVe4WFg_BiYjRTjjivvzY4592akLl7Dc75Q4QNxp7CJW1BDgrML4e_rjLtPi9o8k4IpHifEjiaGjpLIsn0h6gaxeTkOVxZ_w3jXEqcteWlaOg7y3db2Hv4EWp2L_g6Ss1tfbGJZ8e2emHTYJWu772bB1KoWZgw6FTy6jI"
                    }
                }
            ]
        },
        {
            "widgets":[
                {
                    "keyValue":{
                        "topLabel":"Label 3",
                        "content": " "
                    }
                },
                {
                    "buttons":[
                        {
                            "textButton":{
                                "text":"Google",
                                "onClick":{
                                    "openLink":{
                                        "url":"www.google.com"
                                    }
                                }
                            }
                        },
                        {
                            "textButton":{
                                "text":"DuckDuckGo",
                                "onClick":{
                                    "openLink":{
                                        "url":"www.duckduckgo.com"
                                    }
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
}]

# https://developers.google.com/chat/reference/rest/v1/spaces.messages#Message
bot_response = chat.spaces().messages().create(
    parent = f'spaces/{myspace}',
    body = {
        'text': 'Test from Python',
        'cards': cards,
#        'thread': {
#            'name': 'spaces/7gV80IAAAAE/threads/LO1eVoppjy0'
#        }
    }
).execute()

print(bot_response)