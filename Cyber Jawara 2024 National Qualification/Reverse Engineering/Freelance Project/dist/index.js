const express = require("express")
const { createHash } = require("crypto")
const app = express()

const ozE9HYybjMGimCWK = function (req, res, next) {
  console.log(req) // debug request
  next()
}

app.use(ozE9HYybjMGimCWK)

app.get("/", (req, res) => {
  res.send("Hello World!")
})

app.get("/ping", (req, res) => {
  res.send("Pong!")
})

app.get("/calc", function (req, res) {
  var inp = req.query.text
  res.send("Results: " + eval(inp))
})

app.get("/flag", function (req, res) {
  var inp = req.query.text
  var hsh = createHash("sha256").update(inp).digest("base64")
  var test = "coNj4PU1ygx/vsnU1zLSkAI6nyXg1CG/wEGIQmJ2nqE="
  // -------- code here ----------

  if (hsh == test) {
    res.send("Wow")
  } else {
    res.send("Lol")
  }
})

app.listen(3001)
