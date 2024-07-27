const ex = process.argv[2].trim();
const { Parser } = require("expr-eval");

console.log(new Parser().evaluate(ex));
