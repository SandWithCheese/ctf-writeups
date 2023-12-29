from web3 import Web3

abi = [
    {
        "inputs": [],
        "name": "getFlag",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    }
]

addr = "0xCE69Ea4901b51d0E24981be690010E48E1C6336c"

w3 = Web3(Web3.EthereumTesterProvider())
w3.eth.default_account = w3.eth.accounts[0]

flag = w3.eth.contract(address=addr, abi=abi)

tx_hash = flag.functions.getFlag().transact()
print(tx_hash.hex())
