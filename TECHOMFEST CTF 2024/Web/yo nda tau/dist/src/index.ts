import express from "express";
import { runInNewContext } from "vm"

const app = express()

app.get("/", async (req, res) => {
    const run = req.query?.run
    if (!run) return res.sendfile("index.html")
    if (!(typeof run === "string")) return res.send("wrong")
    try {
        const code = runInNewContext(run, { query: req.query })
        return res.send(await code?.toString())
    } catch (e) {
        console.error(e)
        return res.send(e?.toString())
    }
})

app.listen(8080)
