import pickle
import os
from Vault import random_key_gen,block_chain
from ipfs import IPFS
class User:
    def __init__(self,uname:str,auth_tocken:str=''):
        if os.path.exists(f"./{uname}.obj"):
            self.load_user(uname,auth_tocken)
        else:
            self.uname=uname
            self.thumbnail=[]
            auth_tocken=random_key_gen()
            self.chain_obj=block_chain(auth_tocken,f"{uname}.json")

    def auth(self,auth_tocken:str):
        if self.chain_obj.chain_tocken==auth_tocken:
            return True
        else:
            return False

    def save(self):
        try:
            file=open(f"./{self.uname}.obj","x")
        except:
            pass

        with open(f"./{self.uname}.obj","wb" ) as file:
            print(self.chain_obj.chain_tocken)
            pickle.dump(self,file)

    def load_user(self,uname:str,auth_tocken:str):
        with open(f"./{uname}.obj","rb") as file:
            user=pickle.load(file)
        if user.auth(auth_tocken):
            #print("y??")
            self.uname=user.uname
            self.thumbnail=user.thumbnail
            self.chain_obj=user.chain_obj
            self.chain_obj.load()
            return {"uname":user.uname,"thumbnails":list(user.thumbnail)}
        else:
            #print("yep>:")
            return "null"
    def del_thumbnail(self,idx:int):
        self.thumbnail.pop(idx)
        self.save()
    def no_of_files(self):
        return len(self.chain_obj.chain)







