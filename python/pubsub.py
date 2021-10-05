from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1 # pip install google google-cloud google-cloud-pubsub
from googleapiclient.discovery import build # pip install google-api-python-client
from httplib2 import Http
import json
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2
import os
from time import sleep
from typing import Any, Dict, Text



# TODO start
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dotted-marking-327507-277d58834909.json'

project_id      = 'dotted-marking-327507' # https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat?project=dotted-marking-327507
topic_id        = 'Testbot'
subscription_id = 'Testbot'

credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'https://www.googleapis.com/auth/chat.bot')
chat = build('chat', 'v1', http = credentials.authorize(Http()))

flow_control = pubsub_v1.types.FlowControl(max_messages = 10)
timeout = 30
# TODO end



def itElse(obj, key: Text, alt: Any):
    if isinstance(obj, dict):
        return obj[key] if (key in obj) else alt
    return alt



publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


with pubsub_v1.SubscriberClient() as subscriber:
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    print(f'Topic:        {topic_path}')
    print(f'Subscription: {subscription_path}\n')


    def respond(text = None, cards = None, space = None, thread = None) -> Dict:
        parent = space
        body = {}

        if text is not None and len(text) > 0:
            body['text'] = text

        if cards is not None and len(cards) > 0:
            body['cards'] = cards

        if thread is not None:
            body['thread'] = {
                'name': thread
            }

        response = chat.spaces().messages().create(
            parent = parent,
            body = body
        ).execute()

        return response

    def typeof(x):
        return type(x)


    def callback(msg: pubsub_v1.subscriber.message.Message) -> None:
        data = None

        try:
            data = json.loads(msg.data.decode('UTF-8'))
        except Exception as e:
            print('[ERROR]', e)
            return

        type = itElse(data, 'type', 'NONE')

        time = itElse(data, 'eventTime', 0)

        message = itElse(data, 'message', {})
        message_name            = itElse(message, 'name', '')
        message_text            = itElse(message, 'text', '')
        message_cards           = itElse(message, 'cards', [])
        message_attachments     = itElse(message, 'attachment', [])
        message_attachment      = itElse(message, 'attachment', [{}])[0]
        message_attachment_type = itElse(message_attachment, 'contentType', '')

        user = itElse(data, 'user', {})
        user_name    = itElse(user, 'name', '')
        user_display = itElse(user, 'displayName', 'User')
        user_avatar  = itElse(user, 'avatarUrl', '')
        user_email   = itElse(user, 'email', '')
        user_type    = itElse(user, 'type', '')

        space = itElse(data, 'space', None)
        space_name   = itElse(space, 'name', '')
        space_type   = itElse(space, 'type', '')
        space_single = itElse(space, 'singleUserBotDm', False)

        thread = itElse(message, 'thread', {})
        thread_name = itElse(thread, 'name', None)

        print(f"Message:\n{data}")
        #print(f"Text:    {message_text}")
        #print(f"Space:   {space_name}")

        msg.ack()
        print()


        reply = ''
        cards = []

        if type == 'ADDED_TO_SPACE':
            if space_single:
                reply = f'Hey {user_display.split()[0]}, thanks for adding me!'

            else:
                reply = 'Hey everyone, thanks for adding me!'

        elif type == 'MESSAGE':
            if message_text.strip(' \n\t') == '@TestbotDC21':
                if not message_attachment_type:
                    if space_single:
                        reply = f'Yes?'
                    else:
                        reply = f'Yes, {user_display.split()[0]}?'

                message_text = ''

            if message_text:
                if space_single:
                    reply = f'_You said:_\n{message_text}'
                else:
                    reply = f'_<{user_name}> said:_\n{message_text}'
                    
            if message_text and message_attachment_type:
                reply += '\n\n'
            
            if message_attachment_type:
                if space_single:
                    reply += f'_You sent an attachment of type:_\n{message_attachment_type}'
                else:
                    reply += f'_<{user_name}> sent an attachment of type:_\n{message_attachment_type}'

        elif type == 'CARD_CLICKED':
            reply = ''

        elif type == 'REMOVED_FROM_SPACE':
            reply = ''

        elif type == 'CUSTOM':
            reply = '*Custom message recieved:*\n' + message_text
            cards = message_cards

            print(cards)
            print()

        if reply.strip(' \n\t') != '':
            bot_response = respond(text = reply, cards = cards, space = space_name, thread = thread_name)
            print(f'Reply:\n{bot_response}')

            if space_name != 'spaces/7gV80IAAAAE':
                feedback = f'*Replied in _{space_name}_ to _{user_name}_ (_{user_display}_)*\n\n'

                if message_text:
                    feedback += message_text + '\n\n- - - - -\n\n'
                
                feedback += reply + '\n\n= = = = = = = =\n\n'

                respond(text = feedback, cards = cards, space = 'spaces/7gV80IAAAAE', thread = None)

        else:
            print(f'No reply from bot after {type}.')


        print('\n' + '='*80 + '\n')
        


    while True:
        pull_future = subscriber.subscribe(
            subscription = subscription_path,
            callback     = callback,
            flow_control = flow_control,
        )

        try:
            print('Listening...\n' + '='*80 + '\n')
            pull_future.result(timeout = None)
        except TimeoutError:
            print(f'Error: TimeoutError')
            pull_future.cancel()  # Trigger the shutdown
            pull_future.result()  # Block until the shutdown is complete
        except Exception as e:
            print(f'Error: {e}')
            print()
            sleep(2)
            