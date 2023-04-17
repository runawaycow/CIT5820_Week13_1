from web3 import Web3
from eth_account.messages import encode_defunct
import random



def signChallenge( challenge ):

    w3 = Web3()


    # Connect to the Ethereum network
    w3 = Web3(Web3.HTTPProvider('https://api.avax-test.network/ext/bc/C/rpc'))

    # Address of the wallet that claimed the NFT
    wallet_address = '0xd85ac92e6103e1e21f2fa0c771e2fa4d655bd8e8'

    # Transaction hash of the NFT claim transaction
    claim_tx_hash = '0x92a2d47452c6c9eaeb65159068251a69da138a4a219828dc2c871ee4abbce352'

    # Get the transaction receipt for the NFT claim transaction
    tx_receipt = w3.eth.getTransactionReceipt(claim_tx_hash)

    # Get the contract address from the transaction receipt
    contract_address = tx_receipt['0x85ac2e065d4526FBeE6a2253389669a12318A412']

    # Load the NFT contract ABI
    with open('nft_contract_abi.json', 'r') as f:
        nft_contract_abi = json.load(f)

    # Create a contract instance for the NFT contract
    nft_contract = w3.eth.contract(address=contract_address, abi=nft_contract_abi)

    # Get the token ID of the claimed NFT
    token_id = nft_contract.functions.tokenOfOwnerByIndex(wallet_address, 0).call()

    # Get the secret key for the wallet address
    private_key = w3.eth.account.decrypt(keystore_json, 'password')
    #This is the only line you need to modify
    sk = private_key 
    

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
