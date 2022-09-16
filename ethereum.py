from web3 import Web3, EthereumTesterProvider


if __name__ == '__main__':
    w3 = Web3(EthereumTesterProvider())
    print(w3.isConnected())