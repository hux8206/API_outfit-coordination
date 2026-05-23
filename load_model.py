from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import random

app = FastAPI()

model = joblib.load('model.pkl')
enc_content = joblib.load('encoder_cont.pkl')
enc_label = joblib.load('encoder_label.pkl')

PALETTE = {
    # DI LAM

    ("trang", "di_lam"): [
        ["trang", "den", "xam"],
        ["kem", "nau", "xam"],
        ["trang", "xam", "be"],
        ["kem", "den", "xam"],
    ],

    ("vang", "di_lam"): [
        ["trang", "xam", "xam"],
        ["kem", "nau", "xam"],
        ["trang", "den", "be"],
        ["vang", "nau", "xam"],
    ],

    ("ngam", "di_lam"): [
        ["trang", "xam", "den"],
        ["vang", "nau", "xam"],
        ["be", "xam", "den"],
        ["trang", "nau", "den"],
    ],

    #DI HOC
    ("trang", "di_hoc"): [
        ["trang", "xanh", "den"],
        ["kem", "nau", "xam"],
        ["hong", "xam", "trang"],
        ["trang", "nau", "xanh"],
        ["kem", "den", "xam"],
    ],

    ("vang", "di_hoc"): [
        ["trang", "nau", "den"],
        ["kem", "xanh", "xam"],
        ["vang", "nau", "den"],
        ["trang", "xam", "xanh"],
        ["kem", "den", "xam"],
    ],

    ("ngam", "di_hoc"): [
        ["trang", "den", "xam"],
        ["kem", "nau", "den"],
        ["vang", "xam", "den"],
        ["trang", "nau", "xanh"],
        ["kem", "den", "xam"],
    ],
    # -------- ĐI CHƠI --------

    ("trang", "di_choi"): [
        ["trang", "do",   "den"],  
        ["hong",  "xam",  "trang"], 
        ["kem",   "nau",  "be"],    
        ["trang", "xanh", "trang"], 
        ["vang",  "den",  "xam"],   
    ],

    ("vang", "di_choi"): [
        ["trang", "cam",  "xanh"], 
        ["kem",   "nau",  "xam"],   
        ["trang", "xanh", "den"],   
        ["vang",  "nau",  "xam"],   
        ["trang", "den",  "be"],    
    ],

    ("ngam", "di_choi"): [
        ["trang", "cam",  "den"],
        ["kem",   "nau",  "xanh"], 
        ["vang",  "do",   "xam"],   
        ["trang", "den",  "xanh"],  
        ["kem",   "xam",  "den"],   
    ]
}

class DataInput(BaseModel):
    skin : str
    season : str
    sex : str
    situation : str
    style : str

@app.post("/predict")
def predict(data: DataInput):
    dulieu = np.array([[
        data.skin,
        data.season,
        data.sex,
        data.situation,
        data.style
    ]])

    encode = enc_content.transform(dulieu)
    probas = model.predict_proba(encode) #tinh xs cua tung loai do trong tung loai quan ao, vidu : aotrong(somi,thun,..)no se tinh xac suat cac cai nay
    outfits = []
    categories = enc_label.categories_

    top_ao_trong = sorted(zip(categories[0],probas[0][0]),key=lambda x : x[1], reverse=True)[:2] #sap xep giam dan theo %, x[1] la so sanh probas, :2 lay 2 cai cao nhat
    top_ao_khoac = sorted(zip(categories[1],probas[1][0]),key=lambda x : x[1], reverse=True)[:2]
    top_quan = sorted(zip(categories[2],probas[2][0]), key=lambda x : x[1], reverse=True)[:2]

    pallete_key = (data.skin.strip(),data.situation.strip())
    pallete_list = PALETTE.get(pallete_key,[["trang","den","xam"]]) #neu k tim thay skin va situa phu hop se lay trang,den,xam  

    for ao_trong,p1 in top_ao_trong :
        for ao_khoac,p2 in top_ao_khoac :
            for quan, p3 in top_quan :
                color = random.choice(pallete_list).copy()

                if ao_khoac == "khong_co":
                    color[1] = "khong_co"

                score = (p1*p2*p3)*100

                outfits.append(
                    {
                        "ao_trong" : ao_trong,
                        "ao_khoac" : ao_khoac,
                        "quan" : quan,
                        "mau_ao_trong" : color[0],
                        "mau_ao_khoac" : color[1],
                        "mau_quan" : color[2],
                        "compatibility" : round(score,2)
                    }
                )
    
    outfits = sorted(outfits, key=lambda x : x["compatibility"], reverse=True)

    unique_outfit = []
    seen = set() #luu cac key de tranh trung lap

    for outfit in outfits :
        outfit_key = (
            outfit["ao_trong"],
            outfit["ao_khoac"],
            outfit["quan"]
        )
        if outfit_key not in seen :
            seen.add(outfit_key) 
            unique_outfit.append(outfit)
    
    return{
        "outfits" : unique_outfit[:3]
    }
