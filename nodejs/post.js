const express = require('express')
const bodyParser = require('body-parser')



const app = express()

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

app.post('/', (request, result) => {
    console.log('Got body:', request.body)
    console.log(request)
    result.send(request.body)
})

app.listen(7007, () => {
    console.log('Started server at http://localhost:7007')
})