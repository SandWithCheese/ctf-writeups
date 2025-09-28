// scripts/diagnose.js
require("dotenv").config()
const { ethers } = require("ethers")

const provider = new ethers.providers.StaticJsonRpcProvider(
  { url: process.env.RPC_URL, timeout: 30000 },
  { name: "hacktoday", chainId: 31337 }
)
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider)

async function main() {
  const setupAddr = process.env.SETUP_CONTRACT_ADDR
  const setupAbi = [
    "function auction() view returns (address)",
    "function nft() view returns (address)",
    "function tokenId() view returns (uint256)",
    "function isSolved() view returns (bool)",
  ]
  const auctionAbi = [
    "function bid() external payable",
    "function withdraw() external",
    "function Balance() view returns (uint256)",
    "function ended() view returns (bool)",
    "function bids() view returns (uint256)",
    "function uniqueBidders() view returns (uint256)",
    "function lastBidder() view returns (address)",
    "function targetAmount() view returns (uint256)",
  ]
  const erc721Abi = ["function ownerOf(uint256) view returns (address)"]

  const setup = new ethers.Contract(setupAddr, setupAbi, provider)
  const auctionAddr = await setup.auction()
  const auction = new ethers.Contract(auctionAddr, auctionAbi, provider)
  const nft = new ethers.Contract(await setup.nft(), erc721Abi, provider)
  const tokenId = await setup.tokenId()

  console.log("auction:", auctionAddr)
  console.log("tokenId:", tokenId.toString())

  // State snapshot
  const [bal, ended, bids, uniq, last, tgt] = await Promise.all([
    auction.Balance(),
    auction.ended(),
    auction.bids(),
    auction.uniqueBidders(),
    auction.lastBidder(),
    auction.targetAmount(),
  ])

  console.log("Balance (ETH):", ethers.utils.formatEther(bal))
  console.log("ended:", ended)
  console.log("bids:", bids.toString())
  console.log("uniqueBidders:", uniq.toString())
  console.log("lastBidder:", last)
  console.log("targetAmount (ETH):", ethers.utils.formatEther(tgt))
  console.log("nft.ownerOf(tokenId):", await nft.ownerOf(tokenId))

  // callStatic withdraw to catch revert reason
  const auctionWithSigner = auction.connect(wallet)
  try {
    await auctionWithSigner.callStatic.withdraw({ gasLimit: 500000 })
    console.log("callStatic withdraw: would succeed")
  } catch (e) {
    console.log("callStatic withdraw reverted:")
    console.log("  message:", e.message)
    if (e.error && e.error.data) console.log("  data:", e.error.data)
  }
}

main().catch(console.error)
