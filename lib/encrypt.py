from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
from hashlib import sha256
import json

class Encrypt:
    def __init__(self,key,*,data=None,from_db_path=None,to_db_path=None):
        self.key=key
        self.data=data
        self.from_db_path=from_db_path
        self.to_db_path=to_db_path

    def encrypt_file(self):
        # 读取数据
        with open(self.from_db_path,'rb') as file:
            data=file.read()
        # 检查编码
        if isinstance(data,str):
            data=data.encode()
        if isinstance(self.key,str):
            self.key=self.key.encode()
        # 获得 key 的哈希值
        key=sha256(self.key).digest()
        # 生成 iv
        iv=os.urandom(16)
        # 生成加密对象
        cipher=AES.new(key,AES.MODE_CBC,iv)
        # 加密
        ciphertext=cipher.encrypt(pad(data,AES.block_size))

        # 写入数据文件
        with open(self.to_db_path,'wb') as file:
            file.write(iv+ciphertext)

    def encrypt_data(self):
        # 检查编码
        if isinstance(self.data,str):
            self.data=self.data.encode()
        if isinstance(self.data,list):
            self.data=json.dumps(self.data,ensure_ascii=False).encode('utf-8')
        if isinstance(self.key,str):
            self.key=self.key.encode()
        # 获得 key 的哈希值
        key=sha256(self.key).digest()
        # 生成 iv
        iv=os.urandom(16)
        # 生成加密对象
        cipher=AES.new(key,AES.MODE_CBC,iv)
        # 加密
        ciphertext=cipher.encrypt(pad(self.data,AES.block_size))

        # 写入数据文件
        with open(self.to_db_path,'wb') as file:
            file.write(iv+ciphertext)
