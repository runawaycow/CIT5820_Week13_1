from web3 import Web3
from eth_account.messages import encode_defunct
import random

def gettoken():
    

    infura_url = 'https://api.avax-test.network/ext/bc/C/rpc'
    w3 = Web3(Web3.HTTPProvider(infura_url))

    if w3.isConnected():
        print("Connected to Ethereum network")
    else:
        print("Not connected")
        exit()

    private_key = 'bff1e88a649e5125d96928f35efc4f29a0b0785f3c05452c656fd79f49fe1dbd'
    account = w3.eth.account.privateKeyToAccount(private_key)
    contract_abi = 'NFT.abi'
    contract_address = w3.toChecksumAddress('0x85ac2e065d4526FBeE6a2253389669a12318A412')

    nft_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    nonce = random.randint(1, 2**256 - 1)

    transaction_data = nft_contract.functions.claim(nonce).buildTransaction({
        'from': account.address,
        'gas': w3.eth.estimateGas({'to': contract_address, 'from': account.address, 'data': nft_contract.encodeABI(fn_name='claim', args=[nonce])}),
        'gasPrice': w3.eth.gasPrice,
        'nonce': w3.eth.getTransactionCount(account.address),
    })

    signed_txn = w3.eth.account.signTransaction(transaction_data, private_key)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)


def signChallenge( challenge ):

    w3 = Web3()
    gettoken()
    #This is the only line you need to modify
    sk = 'bff1e88a649e5125d96928f35efc4f29a0b0785f3c05452c656fd79f49fe1dbd'
    

    acct = w3.eth.account.from_key(sk)

    signed_message = w3.eth.account.sign_message( challenge, private_key = acct._private_key )

    return acct.address, signed_message.signature


def verifySig():
    """
        This is essentially the code that the autograder will use to test signChallenge
        We've added it here for testing 
    """

    challenge_bytes = random.randbytes(32)

    challenge = encode_defunct(challenge_bytes)
    address, sig = signChallenge( challenge )

    w3 = Web3()

    return w3.eth.account.recover_message( challenge , signature=sig ) == address

if __name__ == '__main__':
    """
        Test your function
    """
    if verifySig():
        print( f"You passed the challenge!" )
    else:
        print( f"You failed the challenge!" )
