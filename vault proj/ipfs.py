import requests

class IPFS:
    def __init__(self,url:str):
    # Define the IPFS node address and port
        self.node = url

    # Upload a file to IPFS
    def upload_ipfs(self,file_path):
        with open(file_path, 'rb') as file:
            response = requests.post(f"{self.node}/api/v0/add", files={'file': file})
            if response.status_code == 200:
                return response.json()['Hash']
            else:
                raise Exception(f"Failed to upload file: {response.text}")

# Retrieve a file from IPFS using its hash
    def get_ipfs(self,file_hash):
        response = requests.post(f"{self.node}/api/v0/cat?arg={file_hash}")
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to retrieve file: {response.text}")
    
    def delete_ipfs(self, file_hash):
        # Step 1: Unpin the file
        response = requests.post(f"{self.node}/api/v0/pin/rm", params={"arg": file_hash})
        if response.status_code == 200:
            print(f"Unpinned file: {file_hash}")
        else:
            raise Exception(f"Failed to unpin file {file_hash}: {response.text}")

        # Step 2: Trigger garbage collection
        gc_response = requests.post(f"{self.node}/api/v0/repo/gc")
        if gc_response.status_code == 200:
            print("Garbage collection completed.")
        else:
            raise Exception(f"Failed to run garbage collection: {gc_response.text}")

        return f"File {file_hash} removed from local node."
