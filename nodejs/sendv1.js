const {google} = require('googleapis');


const GOOGLE_APPLICATION_CREDENTIALS = 'nodejs/dotted-marking-327507-277d58834909.json'



const chat = google.chat('v1');

const auth = new google.auth.GoogleAuth({
    keyFile: GOOGLE_APPLICATION_CREDENTIALS,
    scopes: ['https://www.googleapis.com/auth/chat.bot'],
})

console.log('Project', auth.getProjectId())

// Acquire an auth client, and bind it to all future calls
const authClient = auth.getClient();
google.options({auth: authClient});

console.log('auth', auth)
console.log('authClient', authClient)

// Build response
const res = chat.spaces.messages.create({
  	// Required. Space resource name, in the form "spaces/x". Example: spaces/AAAAMpdlehY
  	parent: 'spaces/7gV80IAAAAE',

  	// Request body metadata
 	requestBody: {
		"text": "Hello from Node",
		"cards": [],
        // "actionResponse": {},
        // "annotations": [],
        // "argumentText": "my_argumentText",
        // "attachment": [],
        // "createTime": "my_createTime",
        // "fallbackText": "my_fallbackText",
        // "lastUpdateTime": "my_lastUpdateTime",
        // "name": "my_name",
        // "previewText": "my_previewText",
        // "sender": {},
        // "slashCommand": {},
        // "space": {},
        // "thread": {}
    }
})

console.log(res)
console.log(res.data)