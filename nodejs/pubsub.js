require('dotenv').config()
const {google} = require('googleapis')
const {PubSub} = require('@google-cloud/pubsub');
const request = require('request');



// TODO start
const GOOGLE_APPLICATION_CREDENTIALS = process.env.GOOGLE_APPLICATION_CREDENTIALS;

project_id      = 'dotted-marking-327507'
topic_id        = 'Testbot'
subscription_id = 'Testbot'

const credentials = new google.auth.GoogleAuth({
    keyFile: GOOGLE_APPLICATION_CREDENTIALS,
    scopes: ['https://www.googleapis.com/auth/chat.bot'],
})
// TODO end



function itElse(obj, key, alt = null) {
    if (obj instanceof Array) {
        return (obj.length >= key + 1) ? obj[key] : alt
    } else if (obj instanceof Object) {
        return (obj.hasOwnProperty(key)) ? obj[key] : alt
    } else {
        return alt
    }
}


function isKey(obj, key) {
    if (obj instanceof Array) {
        return (obj.length >= key + 1)
    } else if (obj instanceof Object) {
        return obj.hasOwnProperty(key)
    } else {
        return false
    }
}



const pubSubClient = new PubSub();

function listenForMessages() {
    const subscription = pubSubClient.subscription(subscription_id)


    function respond(reply, verbose = true) {
        const data = {
            headers: {'content-type': 'application/json'},
            url:     'http://localhost:7007',
            body:    JSON.stringify(reply)
        }
        
        let response = ''

        request.post(data, function(error, response, body) {
            if (error) {
                console.error(`Error:\n${error}`)
            } else if (verbose && body) {
                console.log(`Reply:\n${body}`)
                console.log('\n' + '='.repeat(80) + '\n')
            }
        })

        return response
    }
  

    const callback = (msg) => {
        const data = JSON.parse(msg.data)

        const type = itElse(data, 'type', 'NONE').toUpperCase()

        const time = itElse(data, 'eventTime', 0)

        const message = itElse(data, 'message', {})
        const message_name            = itElse(message, 'name', '')
        const message_text            = itElse(message, 'text', '')
        const message_cards           = itElse(message, 'cards', [])
        const message_attachments     = itElse(message, 'attachment', [])
        const message_attachment      = itElse(message, 'attachment', [{}])[0]
        const message_attachment_type = itElse(message_attachment, 'contentType', '')

        const user = itElse(data, 'user', {})
        const user_name    = itElse(user, 'name', '')
        const user_display = itElse(user, 'displayName', 'User')
        const user_avatar  = itElse(user, 'avatarUrl', '')
        const user_email   = itElse(user, 'email', '')
        const user_type    = itElse(user, 'type', '')

        const space = itElse(data, 'space', null)
        const space_name   = itElse(space, 'name', '')
        const space_type   = itElse(space, 'type', '')
        const space_single = itElse(space, 'singleUserBotDm', false)

        const thread = itElse(message, 'thread', {})
        const thread_name = itElse(thread, 'name', null)

        console.log(`Message:\n${JSON.stringify(data)}`)

        msg.ack()
        console.log()


        reply = {}
        reply_text  = ''
        reply_image = ''
        reply_cards = []


        if (type == 'ADDED_TO_SPACE') {
            if (space_single) {
                reply = `Hey ${user_display.split()[0]}, thanks for adding me!`
            } else {
                reply = 'Hey everyone, thanks for adding me!'
            }
        } else if (type == 'MESSAGE') {
            reply_text = `_You said:_\n${message_text}`
        } else if (type == 'CARD_CLICKED') {
            reply = 'CARD_CLICKED'
        } else if (type == 'REMOVED_FROM_SPACE') {
            reply = 'This should not appear'
        } else {
            reply = type
        }

        if (reply_text) {
            reply['text'] = reply_text
        } if (reply_image) {
            reply['image'] = reply_image
        } if (reply_cards) {
            reply['cards'] = reply_cards
        }
        
        if (reply && space_name) {
            reply['recipient'] = space_name.split('/')[1]
        } else {
            return
        }
        

        const bot_response = respond(reply)

        if (space_name != 'spaces/7gV80IAAAAE') {
            let feedback = {}
            feedback['recipient'] = '7gV80IAAAAE'

            feedback['text'] = `*Replied in _${space_name}_ to _${user_name}_ (_${user_display}_)*\n\n`

            if (message_text) {
                feedback['text'] += message_text + '\n\n- - - - -\n\n'
            }
            
            feedback['text'] += reply_text + '\n\n= = = = = = = =\n\n'

            respond(feedback, false)
        }

    }
    
    subscription.on('message', callback)
}
  
listenForMessages()