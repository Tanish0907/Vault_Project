from sys import exception
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import binascii
import os
import hashlib
import random
import json
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import base64
from ipfs import IPFS
global storage
ipfs_api_url = os.getenv("IPFS_API_URL", "http://localhost:10002")

storage=IPFS(ipfs_api_url)
def key_gen(seed):
    seed=bytes(seed,"utf-8")
    seed_hash=hashlib.sha256()
    seed_hash.update(seed)
    return str(seed_hash.hexdigest())
def random_key_gen():
    char_lst=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0","!","@","#","$","%","^","&","*"]
    seed=""
    min_len=8
    max_len=10
    rnd_len=random.randint(min_len,max_len)
    for i in range(rnd_len):
        rand_char=char_lst[random.randint(0,i)]
        seed=seed+rand_char
    seed=key_gen(seed)
    return seed
def decrypt_file(input_file, seed_token):
    # Generate a key from the seed token
    key = seed_token.ljust(32)[:32].encode('utf-8')  # Ensure key is 32 bytes long

    # Read the hex data from the input file
    hex_data =input_file 

    # Convert the hex data back to binary
    encrypted_data_with_iv = binascii.unhexlify(hex_data)

    # Extract the IV and the encrypted data
    iv = encrypted_data_with_iv[:16]
    encrypted_data = encrypted_data_with_iv[16:]

    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    print(f"Decrypted data")
    return data    
    
def encrypt(input_file,seed_token):
    # Generate a key from the seed token
    key = seed_token.ljust(32)[:32].encode('utf-8')  # Ensure key is 32 bytes long
    iv = os.urandom(16)  # Initialization vector

    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Read the binary file
    data = input_file

    # Pad the data to make it a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Convert to hex
    hex_data = binascii.hexlify(iv + encrypted_data).decode('utf-8')
    
    return hex_data

def divide_file(path:str,parts:int)->list:
    file=[]
    chunk_size=int(int(os.path.getsize(path))/parts)
    CHUNK_SIZE = chunk_size  # in bytes
    with open(path, 'rb') as f:  # open in binary read mode
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            file.append(chunk) 
            chunk = f.read(CHUNK_SIZE)
    return file

class block:
    def __init__(self,block_hash:str=None,prev_hash:str=None,data:str=None,thumbnail:str=None) ->None:
        self.hash=block_hash
        self.prev_hash=prev_hash
        self.data=data

class block_chain:
    def __init__(self,chain_tocken:str,file:str):
        self.file=file
        self.chain_tocken=chain_tocken
        self.chain=[]
        lf=open(f"./{file}","x")
        with open(f"./{file}","r") as lf:
            lf=lf.readlines()
            
        if not lf:
            with open(f"./{file}","w") as f:
                lst=[]
                json.dump(lst,f)
                f.close()
        else:
            self.load()
            self.validate_chain()

    def create_chain(self,enc_tocken:str,files:list)->None:

        enc_tocken=key_gen(enc_tocken)
        self.file_list=files
        for i in files:
            self.chain.append([])
        print("chain initaiaized")
        for i in files:
            file_idx=files.index(i)
            file=divide_file(i,5)
            file_chain=[]
            for x in file:   
                block=self.create_block(x,enc_tocken)
                file_chain.append(block)
                for block_idx in range(len(file_chain)):
                    #try:
                        #file_chain[block_idx].next_block=file_chain[block_idx+1]
                    #except IndexError as e:
                        #pass
                    try:
                        #file_chain[block_idx].prev_block=file_chain[block_idx-1]
                        file_chain[block_idx].prev_hash=file_chain[block_idx-1].hash
                    except IndexError as e:
                        pass
            self.chain[file_idx]=file_chain
            print(f"appended {i} to chain")
        self.save()
        self.load()
        self.validate_chain()
    #debug
    '''
        for i in self.chain[0]:
            print(f"###########################{self.chain[0].index(i)}###############################")
            #print(f"data:{i.data}")
            print(f"prev_hash:{i.prev_hash}")
            print(f"block_hash:{i.block_hash}")
    '''


    def create_block(self,file_chunk:bytes,enc_tocken:str):
        new_block=block()
        data=encrypt(file_chunk,enc_tocken)
        with open("./temp.txt","x") as file:
            file.write(data)
        id_hash=storage.upload_ipfs("./temp.txt")
        os.remove("./temp.txt")
        new_block.data=id_hash
        new_block.hash=key_gen(new_block.data)
        return new_block
    
    def validate_block(self,blk:dict)->bool:
        if key_gen(blk["data"]) == blk["hash"] :
            return True
        return False
    def validate_chain(self):
        print(len(self.chain))
        for i in self.chain:
            for block_idx in range(len(i)):
                if self.validate_block(i[block_idx]) and i[block_idx]["prev_hash"]==i[block_idx-1]["hash"]:
                    continue
                else:
                    print("chain not valid")
                    return False
        print("chain is valid")
        return True


    def save(self,if_del:bool=False):  
        # print(self.chain)
        if not self.chain and if_del:
            with open(f"./{self.file}","w") as file:
                json.dump(self.chain, file, indent=4)
                return ("sucess")
        elif not if_del:
            with open(f"./{self.file}","r") as file:
                logs=json.load(file)
                file.close()
                for i in range(len(self.chain)):
                    file_data=[]
                    for block in self.chain[i]:
                        try:
                            block_data={}
                            block_data["hash"]=block.hash
                            block_data["prev_hash"]=block.prev_hash
                            block_data["data"]=block.data
                        except Exception as e:
                            block_data={}
                            block_data["hash"]=block["hash"]
                            block_data["prev_hash"]=block["prev_hash"]
                            block_data["data"]=block["data"]
                        file_data.append(block_data)
                    if file_data not in logs:
                        logs.append(file_data)

            with open(f"./{self.file}","w") as file:
                json.dump(logs, file, indent=4)
                return ("sucess")
        elif if_del:
            with open(f"./{self.file}","w") as file:
                json.dump(self.chain, file, indent=4)
                return ("sucess")


    
    def load(self):
        with open(f"./{self.file}","r") as file:
            logs=json.load(file)
            self.chain=logs
            for i in self.chain:
                if len(i)==0:
                    self.chain.pop(self.chain.index(i))
            file.close()

    def open_file(self,file_idx:int,enc_tocken:str):
        img_data=b''
        key=key_gen(enc_tocken)
        file=self.chain[file_idx]
        for i in file:
            img_data=img_data+decrypt_file(i["data"],key)
            #print("prev:",i["prev_hash"],"\n","hash:",i["hash"])
        img=Image.open(BytesIO(img_data))
        plt.imshow(img)
        plt.show()

    def return_img_str(self,file_idx:int,enc_tocken:str):
        img_data=b''
        key=key_gen(enc_tocken)
        file=self.chain[file_idx]
        for i in file:
            byt_data=storage.get_ipfs(i["data"])
            img_data=img_data+decrypt_file(byt_data,key)
            #print("prev:",i["prev_hash"],"\n","hash:",i["hash"])
        #image_string = base64.b64encode(img_data)
        img_data=base64.b64encode(img_data).decode("utf-8")
        return {"img":img_data}
    
    def delete_img(self,file_idx:int,enc_tocken:str):
        #print(self.chain)
        key=key_gen(enc_tocken)
        file=self.chain[file_idx]
        for i in file:
            log=storage.delete_ipfs(i["data"])
            
            # self.chain[file_idx].pop(self.chain[file_idx].index(i))
            # self.chain.pop(file_idx)
            print(log)
        self.chain.remove(self.chain[file_idx])
        self.save(if_del=True)
        self.load()
        self.validate_chain()
            
    def test(self):
        for i in self.chain:
            print(len(i))
            for x in i:
                print(x["hash"])

          

'''           
if __name__=="__main__":
   file_lst=os.listdir("./imp")
   files=[]
   for i in range(len(file_lst)):
       files.append(f"./imp/{file_lst[i]}")
   chain=block_chain()
   chain.create_chain("1234",files)
   chain.open_file(1,"1234")
    

 '''  
