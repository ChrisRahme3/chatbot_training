const {google} = require('googleapis');

const chat = google.chat('v1');

const auth = new google.auth.GoogleAuth({
    // Scopes can be specified either as an array or as a single, space-delimited string.
    scopes: ['https://www.googleapis.com/auth/chat.bot'],
})

// Acquire an auth client, and bind it to all future calls
const authClient = auth.getClient();
google.options({auth: authClient});

console.log(auth)
console.log(authClient)

// Build response
const res = chat.dms.messages({
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