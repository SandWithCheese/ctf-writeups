// scripts/ping.js
require("dotenv").config()
const { ethers } = require("ethers")

// Force the chainId we saw via curl: 0x7a69 = 31337
const provider = new ethers.providers.StaticJsonRpcProvider(
  { url: process.env.RPC_URL, timeout: 20000 },
  { name: "hacktoday", chainId: 31337 }
)

;(async () => {
  console.log("RPC_URL =", process.env.RPC_URL)
  const chainIdHex = await provider.send("eth_chainId", [])
  console.log("eth_chainId =", chainIdHex)
  const block = await provider.send("eth_blockNumber", [])
  console.log("eth_blockNumber =", block)
})()
