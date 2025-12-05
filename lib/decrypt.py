from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256
import json

class Decrypt:
    def __init__(self,key,*,from_db_path=None,data=None):
        self.key=key
        self.from_db_path=from_db_path
        self.data=data

    def decrypt_file(self):
        # 读取数据
        with open(self.from_db_path,'rb') as file:
            data=file.read()
        # 获得 iv 和加密的数据
        iv=data[:16]
        ciphertext=data[16:]
        # 检查编码
        if isinstance(self.key,str):
            self.key=self.key.encode()
        # 获得 key 的哈希值
        key=sha256(self.key).digest()
        # 生成解密对象
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # 解密
        try:
            plainbytes=unpad(cipher.decrypt(ciphertext), AES.block_size)
            # 解码和逆序列化
            plaintext=plainbytes.decode('utf-8')
            self.plaintext=json.loads(plaintext)
            # 用于伪解锁软件
            self.decrypt_success_flag=True
        except Exception:
            self.decrypt_success_flag=False

    def decrypt_data(self):
        # 获得 iv 和加密的数据
        iv=self.data[:16]
        ciphertext=self.data[16:]
        # 检查编码
        if isinstance(self.key,str):
            self.key=self.key.encode()
        # 获得 key 的哈希值
        key=sha256(self.key).digest()
        # 生成解密对象
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # 解密
        try:
            plainbytes=unpad(cipher.decrypt(ciphertext), AES.block_size)
            # 解码和逆序列化
            plaintext=plainbytes.decode('utf-8')
            self.plaintext=json.loads(plaintext)
            # 用于伪解锁软件
            self.decrypt_success_flag=True
        except Exception:
            self.decrypt_success_flag=False
