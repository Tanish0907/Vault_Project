'''from PIL import Image
import io
import base64
import requests
data=requests.get("http://localhost:8000/file/1/p?k=qwerty").json()
data=data["img"]
img_data = base64.b64decode(data)
img = Image.open(io.BytesIO(img_data))
img.show()'''
from Vault import block_chain
chain=block_chain()
print(f"####################################{len(chain.chain)}##########################################")
chain.test()
