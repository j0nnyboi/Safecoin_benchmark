import argparse
import string
import random
import json
import threading
import time
import base58
from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from safecoin.system_program import TransferParams, transfer
from safecoin.transaction import Transaction
from safecoin.account import Account
from safecoin.publickey import PublicKey

############################################## Config Wallet and or endpoint ################################################

api_endpoint="https://api.testnet.safecoin.org"
Wallet_Address1 = "24n6hzEPP69hX2kg168APr7nWLsWM4sbeY6zS2vYFSh1"#"Wallet Address"
Wallet_Address2 = "9pytm5ZNTG8CG3Szdrq9W5xDVJpAztMXhmf78q211Zqp"#"Wallet Address"
topup = True #True if you want to topup
topupamount = 1000000 # amount to topup

sender_secret_key = b'\xbf\xcf\xb4\xf1\x90\x0c \x9bR\xd7|\x0e\x01\x8f\x05\xfe/\x9c+c\xa3\xa0\xa20k\x88\xd2\x17\xab\xab\xd0\xf1JQ\x1c\x0c~7\xcb\xfd\r\xb0[\xc1]\xbf\xc4\r\xd5\x99\xca:\xf8\xe1\nXA\x98\xb1GV\xe2L2'
sender_public_key = "616uPrX31oL55PPLqm1SY4x72BCHRvab7Lon3vgavpf3"
##############################################################################################################################

def await_full_confirmation(client, txn, max_timeout=60):
    if txn is None:
        return
    elapsed = 0
    while elapsed < max_timeout:
        sleep_time = 1
        time.sleep(sleep_time)
        elapsed += sleep_time
        resp = client.get_confirmed_transaction(txn)
        while 'result' not in resp:
            resp = client.get_confirmed_transaction(txn)
        if resp["result"]:
            print(f"Took {elapsed} seconds to confirm transaction {txn}")
            break


def WalletConnect(api_endpoint,Wallet_Address,Wallet_Address2,topup,topupamount,x):
    #print("Connecting to Safecoin chain")
    client = Client(api_endpoint)
    #print("Connected to %s :" % api_endpoint, client.is_connected())
    #print("")
    #sender = Keypair.from_seed(bytes(PublicKey(x)))
    
    
    sender = Keypair.from_secret_key(sender_secret_key)
    #print(sender.secret_key)
    #print(sender.public_key)
        
    if(client.is_connected()):
    
        #resp = client.get_balance(sender.public_key)
        #print("balance = ", int(resp['result']['value']) / 1000000000)
        receiver = Keypair.from_seed(bytes(PublicKey(x)))
        spre = 0
        txn = Transaction().add(transfer(TransferParams(from_pubkey=sender.public_key, to_pubkey=receiver.public_key, lamports=100000)))
        for x in range(120):
            #try:
                if(client.is_connected()):
                    s = time.strftime("%S", time.gmtime())
                    while(s == spre):
                        s = time.strftime("%S", time.gmtime())
                        #print("Pass")
                    else:
                        spre = s
                        client.send_transaction(txn, sender)
                        #print(client.send_transaction(txn, sender))
                else:
                    client = Client(api_endpoint)
                    print("reconnect")
            #except:
            #    print("Failed")
            #    pass
        
        
    else:
        print("cannot connect to ",api_endpoint)
        
        #resp = api.topup(api_endpoint,Wallet_Address,amount=20)
        #print(resp)





#WalletConnect(api_endpoint,Wallet_Address1,Wallet_Address2,topup,topupamount)
#print("setup, now testing")
threads = list()
client = Client(api_endpoint)
if(client.is_connected()):
        if(topup == True):
            resp = {}
            while 'result' not in resp:
                resp = client.request_airdrop(sender_public_key,topupamount * 10000000)
            txn = resp['result']
            await_full_confirmation(client, txn)
            #print(resp)
            print("Topup complete")
            print("")
            resp = client.get_balance(sender_public_key)
            print("balance = ", int(resp['result']['value']) / 1000000000)
            

for x in range(100):
        x = threading.Thread(target=WalletConnect, args=(api_endpoint,Wallet_Address1,Wallet_Address2,topup,topupamount,x,))
        threads.append(x)
        x.start()


print("done")
