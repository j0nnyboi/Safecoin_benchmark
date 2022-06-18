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
ThreadAmount = 19 #amount of threads to use(only 19 hard coded wallets)
sendamount = 10000000 #amount in lamports to send to start with

sender_secret_key = b'\xbf\xcf\xb4\xf1\x90\x0c \x9bR\xd7|\x0e\x01\x8f\x05\xfe/\x9c+c\xa3\xa0\xa20k\x88\xd2\x17\xab\xab\xd0\xf1JQ\x1c\x0c~7\xcb\xfd\r\xb0[\xc1]\xbf\xc4\r\xd5\x99\xca:\xf8\xe1\nXA\x98\xb1GV\xe2L2'
sender_public_key = "616uPrX31oL55PPLqm1SY4x72BCHRvab7Lon3vgavpf3"

sender_public_key_List = ['6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt',
                         '8pM1DN3RiT8vbom5u1sNryaNT1nyL8CTTW3b5PwWXRBH','HPYVwAQmskwT1qEEeRzhoomyfyupJGASQQtCXSNG8XS2',
                         'J3qYF7YJMKCqQke47UQwiHizgFUXapHxRxKmxbkar89x','J66fMDgSVVcdRgKucj1D5ssXAcQvg35JopvHNQo6cGY6',
                         'DAiJNXqRaLoixp41pNW2MovKG93QvrjM2d5Lq1eMpjpp','5EUjf4oPLzrA7w7M9EC9fDEyBBjkAVS4QgqrZhRx3G9s',
                         'DoavDC9XjHnBmsPyadzgrGZTskZKRXGsdT8JzrQFbZBF','FucziRiZGfB6iZCUxBxrRn8Mh5PyxjKZApKu8HtyQnRg',
                         '6YqXjX1oAD9nndCZBp7m68nFgoPFHxB41J42cTtmikUY','5Z9UDgBHm5AEjQbvvkgicKwEuFAdx35TE95KozK1iyVL',
                         '2EmfMLLtBz9tkBoEwyiaBwqWzhiJn7UW2XJq7V9D5LjP','4xEy4xQzGrbTXiiuZ9yLJzBWLfo28Tqb52Mdd7oQba4N',
                         'AhwM3wt1gvoCxq9jKLSLrgR6kXGSQ2f4Urfx9Ffz9RNt','7xMJ1iUN8iDqn9yXq8ML4x4gCAq93vXyjUYyrL619MrM',
                         'DTpAAnGm1NGtGy177mVN5zzDqUkADEFGmyp22HAuTSGx','6L2fW53tcYXcqaGBHLfVxE5DfdtKtCEvbccVR7Wdetb1',
                         '8AAJvL1nUXNVfhTGjr4wz4tVvRZXp3du1raUHWJBX6gK','FYPRpYc4YdYhqH24AgM1tPtxkTJwcgb9KG31R4WZXYDJ']

sender_secret_key_List = [b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01L\xb5\xab\xf6\xady\xfb\xf5\xab\xbc\xca\xfc\xc2i\xd8\\\xd2e\x1e\xd4\xb8\x85\xb5\x86\x9f$\x1a\xed\xf0\xa5\xba)',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02t"\xb9\x88u\x98\x06\x8e2\xc4D\x8a\x94\x9a\xdb)\r\x0fN5\xb9\xe0\x1b\x0e\xe5\xf1\xa1\xe6\x00\xfe&t',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xf3\x81bnA\xe7\x02~\xa41\xbf\xe3\x00\x9e\x94\xbd\xd2Ztk\xee\xc4h\x94\x8dl<|]\xc9\xa5K',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\xfdP\xb8\xe3\xb1D\xea$O\xbfw7\xf5P\xbc\x8d\xd0\xc2e\x0b\xbc\x1a\xad\xa83\xca\x17\xff\x8d\xbf2\x9b',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xfd\xe4\xfb\xa00\xad\x00/|/}L3\x1fI\xd1?\xb0\xect~\xce\xeb\xeccO\x1f\xf4\xcb\xca\x9d\xef',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\xb4\xc9*\xfb;\xa5\x7f:\xb9Y\xff\xe6\xd3\x19\xc9\x84\x84\xa2\x15Z\x0fLe\xb2\xc3p\x11\xff\xd1\x97\xb0u',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07>\xe2\xa8\xa7(<\xb2\xfdr\x89C\xda\xa1\'\xef\t\xe4\x83\x07\x1a\x8bK\xc6\x99\xbaE"\xf0\x9b\x14\xcf\xde',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xbe;O\x95\xd1\xd8u\xd7\x1d\xd2\xfa\xcfl^M\xa5|\x1a,y\xde\xad\x9e\x1f\xc5\xc3\xb5\xc1\xdeT\xc0"',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\xdd~\x84\xd0\x10\xae\xd2\x8aAn\x92\x8fP\xc4\xc0\x9a\xc0\xf9J\x8f[4eH\x16\x8b\xdd\xb6\x1c\xdbrc',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\nRrP\x08\x1b\xdc\xdc.\x81\x01\xec\xbdOn56\xe7\r\x14\xbe\x91\xf4QRs&\xb9}\r\xe2\x0eQ',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0bC\xaa\xe8\xeb\xbd\xed\xb9iA]\x02\x0b\x01!\x11\x80"r*WwX\xc5\xfa\x88\xdc\xd9\xd8\xa2\x11e3',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x12b\xbcmT\x08\xa3\xc4\xe0%\xaa\x0c\x15\xe6Oi\x19|\xdb8\x91\x1b\xe5\xad4J\x94\x97y\xdf=\xa6',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r:\xb9\xcc&\xe2\xe4\x14.\x80\rb\x94#d/Ip\x8b \xf8\xf4\xeb6\x81\x95\xb8N\xfcd\x92\x8ag',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x905\xdd\x13\xc4\xc9\xeb=\x8fq\xad\xf9\xcf\xd6)\xab\xbc\xb6\x84\x9aM\x8e\xc9\xedw)\x96\xaa\xea\xb8\xfae',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0fgT\x03\x042\x88\xcc|\xd1\x10\xc6\xa4\xa7\x0e\xca\x13{n\xba[\xb8\xcf\xc0\x08\xa4\x0c\xdf\xb3\xe4S\xc2\x9e',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\xb9*\xaa|\x8d\xb2\x119\xaa}~\xc0\xda\xa8\xd7\xe6%\x19\xd6\xeeF\xa4SN\x07dLh:\x00\x83\x91',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11O*Y\xed\xc86}\xeb@\x04|\xe8>\xe7\xf5\xceq\x1aW\xd9:\xbb\xda\x9d\x1c\xe8X\x8cV\xa3\xce\x88',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12jZ\x8f\xbaHD^\xdd4D\xf6T\xf8 \xbdq\xf1~l9Fi3\x9c\x8a\x00\x04\xbaN\xd2\xc3\xcc',
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\xd8\r\xfb<8\xa4l\xd0\x19#\x03}\xa6\x0c\xb5IM\x03\x11\x9f%X1,x\x15\x00\x18-\x03n\xb5']
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


def WalletConnect(api_endpoint,Wallet_Address,Wallet_Address2,topup,topupamount,x,sender_secret_key_List,ThreadAmount):
    client = Client(api_endpoint)   
    if(client.is_connected()):
    
        sender = Keypair.from_secret_key(sender_secret_key)
        #print(sender.secret_key)
        #print(sender.public_key)
        if(ThreadAmount > 19):
          receiver = Keypair.from_secret_key(sender_secret_key_List[x])
        else:
          receiver = Keypair.from_secret_key(bytes(PublicKey(x)))
        #print(receiver.secret_key)
        #print(receiver.public_key)
        spre = 0
        
        txnonce = Transaction().add(transfer(TransferParams(from_pubkey=sender.public_key, to_pubkey=receiver.public_key, lamports=sendamount)))
        client.send_transaction(txnonce, sender) 
        time.sleep(10)           
        txn = Transaction().add(transfer(TransferParams(from_pubkey=sender.public_key, to_pubkey=receiver.public_key, lamports=1000)))
        rxn = Transaction().add(transfer(TransferParams(from_pubkey=receiver.public_key, to_pubkey=sender.public_key, lamports=1000)))


        
        for x in range(120):
            #try:
                if(client.is_connected()):
                    s = time.strftime("%S", time.gmtime())
                    while(s == spre):
                        s = time.strftime("%S", time.gmtime())
                        client.send_transaction(txn, sender)
                        client.send_transaction(rxn, receiver)
                        #print("Pass")
                    else:
                        spre = s
                        client.send_transaction(txn, sender)
                        client.send_transaction(rxn, receiver)
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
            


for y in range(ThreadAmount):
        x = threading.Thread(target=WalletConnect, args=(api_endpoint,Wallet_Address1,Wallet_Address2,topup,topupamount,y,sender_secret_key_List,ThreadAmount,))
        threads.append(x)
        x.start()


print("done")
