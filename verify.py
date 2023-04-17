from web3 import Web3
from eth_account.messages import encode_defunct
import random


    print('4444444444444444444444')


def signChallenge( challenge ):

    w3 = Web3()

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
