from eth_utils import address
from web3 import Web3
import os
from solc import compile_standard, install_solc
from dotenv import load_dotenv
import json

def compile_contract():
    with open("./smart_contract.sol", "r") as file:
        simple_storage_file = file.read()
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"./smart_contract.sol": {"content": simple_storage_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                        }
                    }
                },
            },
            # solc_version="0.6.0",
        )

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

def get_contract_details():
    with open('compiled_code.json', 'r') as file:
        data = file.read()
        json_data = json.loads(data)
        get_abi = json.loads(json_data['contracts']['./smart_contract.sol']["SimpleStorage"]["metadata"])["output"]["abi"]
        # print(get_abi)
        get_byte_code = json_data["contracts"]["./smart_contract.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
        return get_abi ,get_byte_code

def connect_ganache():
    # set up connection
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    chain_id = 1337
    my_address = "0x771A6956987D4F6A7d1E26B078cbEBE783628b8b"
    #private_key = os.getenv("PRIVATE_KEY")
    private_key = "172375032d0adc123d2c7b3f6ca9eb67ff8825981a87ac85b5cd27facbecf5f8"
    # initialize contract
    abi, bytecode = get_contract_details()
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(my_address)
    # set up transaction from constructor which executes when firstly
    transaction = SimpleStorage.constructor().buildTransaction( {
    "gasPrice": w3.eth.gas_price, 
    "chainId": chain_id, 
    "from": my_address, 
    "nonce": nonce, 
})
    signed_tx = w3.eth.account.signTransaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

if __name__ =='__main__':
    connect_ganache()