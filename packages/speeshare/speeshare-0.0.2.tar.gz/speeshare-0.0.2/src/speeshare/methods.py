import requests as r
import json
import os

def load_link(file):
    dict = {'file': open(file, "rb")}
    rol = r.post(url="https://api.share-online.is/upload", files=dict)
    return rol.json()['data']['file']['url']['short']

