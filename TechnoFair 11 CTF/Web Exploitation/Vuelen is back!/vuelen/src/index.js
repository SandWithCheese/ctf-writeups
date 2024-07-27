//Same for all javascritp template tengines
const express = require('express')
var bodyParser = require('body-parser');
const app = express()
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
const port = 1329

require('./vuelen')(app, "/");

app.listen(port, (err) => {
    if (err) {

        return console.log('something bad happened', err)
    }

    console.log(`server is listening on ${port}`)
})