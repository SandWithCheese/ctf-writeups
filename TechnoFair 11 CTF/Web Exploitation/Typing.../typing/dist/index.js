const app = require("fastify")();
const { promises: fsProm } = require("node:fs");
const { promisify } = require("util");
const exfileAsync = promisify(require("child_process").execFile);
const APP_PORT = process.env.PORT ?? "3000";


app.get("/", async (req, reply) => {
  const html = await fsProm.readFile("index.html");
  return reply.type("text/html; charset=utf-8").send(html);
});

app.post("/setCal", async (req, reply) => {
  const { ex } = req.body;
  try {
    const result = await exfileAsync("node", ["./setCal.js", ex.toString()], {
      timeout: 1000,
    });
    return result.stdout;
  } catch (err) {
    return reply.code(500).send(err.killed ? "Timeout" : err);
  }
});

app.listen({ port: APP_PORT, host: "0.0.0.0" });
