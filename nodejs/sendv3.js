const express    = require('express')
const {google}   = require('googleapis')




// TODO start
const GOOGLE_APPLICATION_CREDENTIALS = 'nodejs/dotted-marking-327507-277d58834909.json'
// const GOOGLE_APPLICATION_CREDENTIALS = 'dotted-marking-327507-277d58834909.json'

project_id      = 'dotted-marking-327507'
topic_id        = 'Testbot'
subscription_id = 'Testbot'

const credentials = new google.auth.GoogleAuth({
    keyFile: GOOGLE_APPLICATION_CREDENTIALS,
    scopes: ['https://www.googleapis.com/auth/chat.bot'],
})

const chat = google.chat({
    serviceName: 'chat',
    version: 'v1',
    auth: credentials
})

spaces = {
    'CR': '7gV80IAAAAE', // Chris Rahmé
    'GS': 'i9uCMIAAAAE', // George Salloum
}

myspace = spaces['CR']
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



function translate(message) {
    // Header
    header = {}

    if (isKey(message, 'title') || isKey(message, 'subtitle') || isKey(message, 'image')) {
        if (isKey(message, 'title')) {
            header['title'] = message['title']
        }

        if (isKey(message, 'subtitle')) {
            header['subtitle'] = message['subtitle']
        }

        if (isKey(message, 'icon')) {
            header['imageUrl'] = message['icon']
            header['imageStyle'] = "AVATAR"
        }
    }


    // Sections
    sections = []

    itElse(message, 'sections', []).forEach((section) => {
        if (section.length == 0) {
            return
        }

        let new_section = {}
        let new_widgets = []

        let label   = itElse(section, 'label', null)
        let content = itElse(section, 'content', null)
        let image   = itElse(section, 'image', null)
        let buttons = []

        // Buttons
        itElse(section, 'buttons', []).forEach((button) => {
            let new_button = {}
            let on_click   = {}

            let text   = itElse(button, 'text', 'Click')
            let url    = itElse(button, 'url')
            let action = itElse(button, 'action')

            if (url) {
                on_click['openLink'] =  {
                    "url": url
                }
            } else if (action) {
                let new_action = {}

                let action_name = isKey(action, 'name')
                let action_parameters = isKey(action, 'parameters')

                if (action_name) {
                    new_action['actionMethodName'] = action['name']

                    if ((action_parameters instanceof Array) && (action_parameters.length > 0)) {
                        new_parameters = []

                        action_parameters.forEach((parameter) => {
                            if (isKey(parameter, 'key') && isKey(parameter, 'value')) {
                                new_parameter = {
                                    "key": parameter['key'],
                                    "value": parameter['value']
                                }

                                new_parameters.push(new_parameter)
                            }
                        })

                        new_action['parameters'] = new_parameters
                    }

                    on_click['action'] = new_action
                }
            }

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

            buttons.push(new_button)
        })

        if (label || content) {
            let new_widget = {'keyValue': {}}

            if (label) {
                new_widget['keyValue']['topLabel'] = label
            }
                
            if (label && (!content)) {
                new_widget['keyValue']['content'] = ' '
            } else if (content) {
                new_widget['keyValue']['content'] = content
            }

            new_widgets.push(new_widget)
        }

        if (image) {
            new_widget = {'image': {}}
            new_widget['image']['imageUrl'] = section['image']
            new_widgets.push(new_widget)
        }

        if (buttons) {
            new_widget = {'buttons': []}
            new_widget['buttons'] = buttons
            new_widgets.push(new_widget)
        }

        new_section['widgets'] = new_widgets
        sections.push(new_section)
    })


    // Card
    let card = {}

    if (header) {
        card['header'] = header
    }

    if (sections) {
        card['sections'] = sections
    }


    // Data
    let data = {
        "space": "spaces/" + message['recipient']
    }

    if (isKey(message, 'text')) {
        data['text'] = message['text']
    }

    if (isKey(card, 'header') || itElse(card, 'sections')) {
        data['cards'] = [card]
    }

    if (isKey(data, 'space') && (isKey(data, 'text') || isKey(data, 'cards'))) {
        return data
    } else {
        return {}
    }

}


function send(data) {
    const parent = itElse(data, 'space', null)
    const body   = {}
    
    text  = itElse(data, 'text', null)
    cards = itElse(data, 'cards', null)
    
    if (text) {
        body['text'] = text
    }
    
    if (cards) {
        body['cards'] = cards
    }
    
    if (parent && body) {
        const response = chat.spaces.messages.create({
            parent: parent,
            requestBody: body
        }).then((response) => {
            // console.log('Response:', response.data)
        }).catch((error) => {
            console.error('Error:', error)
        })
    }
}



///////////////////////////////////////////////////////////////////////////////



const app = express()

app.use(express.json())

app.post('/', (request, result) => {
    const data = request.body
    const translated = translate(data)

    console.log(data)
    send(translated)

    result.json(translated)
})

app.listen(7007, () => {
    console.log('Started server at http://localhost:7007')
})