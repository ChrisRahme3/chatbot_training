const express = require('express')
const bodyParser = require('body-parser')



const app = express()

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

app.post('/', (request, result) => {
    const data = request.body
    const cooked = cooked(data)

    console.log(data)
    result.send(cooked)
})

app.listen(7007, () => {
    console.log('Started server at http://localhost:7007')
})