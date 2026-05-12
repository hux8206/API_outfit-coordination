from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import random

app = FastAPI()

model = joblib.load('model.pkl')
enc_content = joblib.load('encoder_cont.pkl')
enc_label = joblib.load('encoder_label.pkl')

trang = [
    ['#008B8B', '#C0D6A4', '#D6E8A3'],
    ['#023E64', '#56C7F3', '#0280C0'],
    ['#2E66C0', '#D0E3F0', '#9DC7F3'],
    ['#A8A3C3', '#E0E0E8', '#D2D3E0'],
    ['#019898', '#F0E4B9', '#00CCCC']
]

vang = [
    ['#106B80', '#F3D458', '#F4A177'],
    ['#0B9A97', '#F7B96C', '#F0D6A6'],
    ['#F6E0B6', '#D97A2C', '#E4A84C'],
    ['#6E70AA', '#F3D6A5', '#E8B487'],
    ['#476B8E', '#94B0C0', '#8CA9C0']
]

ngam = [
    ['#F6E0B6', '#D97A2C', '#F0BA6C'],
    ['#019898', '#FBEA05', '#00CCCC'],
    ['#7A706C', '#FF6A00', '#C0C0C5'],
    ['#3375CC', '#D7D7D7', '#2C6AA3'],
    ['#0B9A97', '#E07B39', '#F0D6A6']
]
class DataInput(BaseModel):
    skin : str
    season : str
    sex : str
    situation : str
    style : str

@app.post("/predict")
def predict(data:DataInput):
    dulieu = np.array([[
        data.skin,
        data.season,
        data.sex,
        data.situation,
        data.style
    ]])
    if data.skin == 'trang ':
        color = random.choice(trang)
    elif data.skin == 'vang' :
        color = random.choice(vang)
    else :
        color = random.choice(ngam)

    encode = enc_content.transform(dulieu)

    result = model.predict(encode)

    result_enc = enc_label.inverse_transform(result)[0] #tra ve mang 2 chieu vidu ; arr = [[1,2,3]] nen dung [0] de lay duoc ket qua

    if result_enc[1] == "khong_co":
        color[2] = "khong_co"
    return {
        "ao_trong" : result_enc[0],
        "ao_khoac" : result_enc[1],
        "quan" : result_enc[2],
        "mau_ao_trong" : color[0],
        "mau_quan" : color[1],
        "mau_ao_khoac" : color[2]
    }