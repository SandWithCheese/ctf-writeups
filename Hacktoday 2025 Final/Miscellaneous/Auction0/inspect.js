// scripts/inspect.js
const { ethers } = require("ethers")
require("dotenv").config()

const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL, {
  name: "hacktoday",
  chainId: 31337,
})
const setupAddr = process.env.SETUP_CONTRACT_ADDR

async function main() {
  if (!setupAddr) {
    console.error("set SETUP_CONTRACT_ADDR in .env")
    process.exit(1)
  }
  console.log("Setup address:", setupAddr)

  // get code at setup
  const setupCode = await provider.getCode(setupAddr)
  console.log("setup bytecode length (bytes):", (setupCode.length - 2) / 2)

  // read public auction, nft, tokenId via ABI minimal
  const setupAbi = [
    "function auction() view returns (address)",
    "function nft() view returns (address)",
    "function tokenId() view returns (uint256)",
    "function isSolved() view returns (bool)",
  ]
  const setup = new ethers.Contract(setupAddr, setupAbi, provider)

  const auctionAddr = await setup.auction()
  const nftAddr = await setup.nft()
  const tokenId = await setup.tokenId()

  console.log("auction:", auctionAddr)
  console.log("nft:", nftAddr)
  console.log("tokenId:", tokenId.toString())

  // Check auction code length
  const auctionCode = await provider.getCode(auctionAddr)
  console.log("auction bytecode length (bytes):", (auctionCode.length - 2) / 2)

  // balances
  const pSetupBal = await provider.getBalance(setupAddr)
  const pAuctionBal = await provider.getBalance(auctionAddr)
  const pWalletBal = await provider.getBalance(process.env.WALLET_ADDR)

  console.log("balance - setup (wei):", pSetupBal.toString())
  console.log("balance - auction (wei):", pAuctionBal.toString())
  console.log("balance - your wallet (wei):", pWalletBal.toString())

  // call auction.Balance() view via minimal ABI to check consistency
  const auctionAbi = [
    "function Balance() view returns (uint256)",
    "function targetAmount() view returns (uint256)",
  ]
  const auction = new ethers.Contract(auctionAddr, auctionAbi, provider)
  try {
    const balView = await auction.Balance()
    console.log("auction.Balance() =>", balView.toString())
  } catch (e) {
    console.log("auction.Balance() call failed:", e.message)
  }

  console.log(
    "isSolved() =>",
    await setup.isSolved().catch((e) => "reverted: " + e.message)
  )

  // print owner of token (try)
  const erc721abi = ["function ownerOf(uint256) view returns (address)"]
  const nft = new ethers.Contract(nftAddr, erc721abi, provider)
  try {
    const owner = await nft.ownerOf(tokenId)
    console.log("nft.ownerOf(tokenId) =>", owner)
  } catch (e) {
    console.log("ownerOf() failed:", e.message)
  }

  console.log("\nDONE")
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
