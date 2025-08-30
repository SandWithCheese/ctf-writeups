const { ethers } = require("ethers")

const RPC_URL =
  process.env.RPC_URL ||
  "http://103.160.212.3:24376/9a0a3ff6-0fca-4a85-87e9-184f15194e10"
const PRIVKEY =
  process.env.PRIVKEY ||
  "26d7870a11e5389e61c635a96a982bc417cdc23868a939cd79934fbb70fd14a1"
const SETUP_CONTRACT_ADDR =
  process.env.SETUP_CONTRACT_ADDR ||
  "0xb1675b999243515221A8a58B5eF6588Ad659fb0E"

async function main() {
  console.log("RPC:", RPC_URL)
  console.log("Setup addr:", SETUP_CONTRACT_ADDR)

  const provider = new ethers.providers.JsonRpcProvider(RPC_URL)
  const wallet = new ethers.Wallet(PRIVKEY, provider)

  const setupAbi = [
    "function warmup() view returns (address)",
    "function isSolved() view returns (bool)",
  ]

  const warmupAbi = [
    "function solve(uint256 a, uint256 b) external",
    "function solved() view returns (bool)",
  ]

  const setup = new ethers.Contract(SETUP_CONTRACT_ADDR, setupAbi, wallet)

  // read warmup address
  const warmupAddr = await setup.warmup()
  console.log("Warmup contract address:", warmupAddr)

  // optional: print runtime code (useful for debugging)
  const code = await provider.getCode(warmupAddr)
  console.log("Warmup runtime code length:", (code.length - 2) / 2, "bytes")

  const warmup = new ethers.Contract(warmupAddr, warmupAbi, wallet)

  // sanity: check solved before
  const before = await warmup.solved()
  console.log("solved before:", before)

  // the runtime requires a == 0x0aa289 (decimal 697097)
  const requiredA = ethers.BigNumber.from("0x0aa289") // 697097
  const b = 0

  console.log(`Calling solve(${requiredA.toString()}, ${b})...`)
  try {
    const tx = await warmup.solve(requiredA, b, { gasLimit: 200000 })
    console.log("tx hash:", tx.hash)
    const receipt = await tx.wait()
    console.log(
      "tx mined. status:",
      receipt.status === 1 ? "success" : "fail",
      "gasUsed:",
      receipt.gasUsed.toString()
    )
  } catch (err) {
    console.error("Transaction failed:", err)
    process.exit(1)
  }

  const after = await warmup.solved()
  console.log("solved after:", after)

  const setupSolved = await setup.isSolved()
  console.log("setup.isSolved():", setupSolved)

  if (after || setupSolved) {
    console.log(
      "🎉 Contract solved. Visit the CTF platform UI (or flag endpoint) to collect the flag."
    )
  } else {
    console.log(
      "Not solved — something still wrong. Inspect tx and bytecode above."
    )
  }
}

main().catch((e) => {
  console.error("Fatal error:", e)
  process.exit(1)
})
