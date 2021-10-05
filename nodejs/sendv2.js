const {google} = require('googleapis');



// TODO start
const GOOGLE_APPLICATION_CREDENTIALS = 'nodejs/dotted-marking-327507-277d58834909.json'

project_id      = 'dotted-marking-327507'
topic_id        = 'Testbot'
subscription_id = 'Testbot'

const credentials = new google.auth.GoogleAuth({
    keyFile: GOOGLE_APPLICATION_CREDENTIALS,
    scopes: ['https://www.googleapis.com/auth/chat.bot'],
})

const chat = google.chat({
    version: 'v1',
    auth: credentials
})

spaces = {
    'CR': '7gV80IAAAAE', // Chris Rahmé
    'GS': 'i9uCMIAAAAE', // Ge||ge Salloum
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



function cook(message) {
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
            console.log(section)
            return
        }

        let new_section = {}
        let new_widgets = []

        let label   = itElse(section, 'label', null)
        let content = itElse(section, 'content', null)
        let image   = itElse(section, 'image', null)
        let buttons = []

        itElse(section, 'buttons', []).forEach((button) => {
            let url  = itElse(button, 'url', '//')
            let text = itElse(button, 'text', url)

            let new_button = {
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
        'space': "spaces/" + message['recipient']
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
            parent: 'spaces/7gV80IAAAAE',
            requestBody: body
        }).then((response) => {
            console.log('Response:', response.data);
        }).catch((error) => {
            console.error('Error:', error);
        })
    }
}



let message = {
    "recipient": "7gV80IAAAAE",
    "text": "This is a custom message sent from Node with a small card",

    "title": "Card title",
    "subtitle": "Card subtitle",
    "icon": "https://i.picsum.photos/id/315/200/200.jpg?hmac=cE5OEQSh9gvXqkP0fkrmaSbqLfc_KQdDPtH7yBbeuiQ"
}

message = {
    "recipient": "7gV80IAAAAE",
    "text": "This is a custom message sent from Node with a big card",

    "title": "Card title",
    "subtitle": "Card subtitle",
    "icon": "https://i.picsum.photos/id/315/200/200.jpg?hmac=cE5OEQSh9gvXqkP0fkrmaSbqLfc_KQdDPtH7yBbeuiQ",
    
    "sections": [
        {
            "label": "Label 1",
            "content": "Content 1"
        },
        {
            "label": "Label 2",
            "content": "Content 2",
            "image": "https://i.picsum.photos/id/315/200/200.jpg?hmac=cE5OEQSh9gvXqkP0fkrmaSbqLfc_KQdDPtH7yBbeuiQ"
        },
        {
            "label": "Label 3",
            "buttons": [
                {
                    "text": "Google",
                    "url": "www.google.com"
                },
                {
                    "text": "DuckDuckGo",
                    "url": "www.duckduckgo.com"
                }
            ]
        }
    ]
}

send(cook(message))