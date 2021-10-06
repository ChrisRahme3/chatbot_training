# Node/Python Google Chatbot Prototype 

Simple Google Chat API chatbot made with Node and Python.

`node` and `python` folders each contain the same code, but written in JavaScript and Python respectively. They each contain:

- `sendv1`: Sends a message to a given space
- `sendv2`: Reads a custom JSON, translates it to Google Chat format, then sends it
- `sendv3`: Is a server in which we POST a custom JSON, translates it to Google Chat format, then sends it
- `pubsub`: Reads incoming data from conversations with the bot and replies accordingly
  - In the Python version, the reply is sent directly to Google Chat
  - In the Node version, the reply gets sent to Google Chat via `sendv3.js`
