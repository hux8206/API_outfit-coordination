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
    style_list = ["toi_gian","han_quoc","lich_su","vintage","sporty","streetwear"]

    current_list = style_list.copy() #tao ban sao de khong thay doi ban goc
    user_style = data.style.strip()
    if user_style in current_list : 
        current_list.append(user_style)
        current_list.append(user_style)

    seen = set()
    outfits = []
    pallete_key = (data.skin.strip(),data.situation.strip())
    pallete_list = PALETTE.get(pallete_key,[["trang","den","xam"]])

    for pc in style_list :
        dulieu = np.array([[
            data.skin,
            data.season,
            data.sex,
            data.situation,
            pc
        ]])

        encode = enc_content.transform(dulieu)
        probas = model.predict_proba(encode)
        categories = enc_label.categories_

        top2_aotrong = sorted(zip(categories[0],probas[0][0]),key=lambda x : x[1],reverse=True)[:2]
        top2_aokhoac = sorted(zip(categories[1],probas[1][0]),key=lambda x : x[1],reverse=True)[:2]
        top2_quan = sorted(zip(categories[2],probas[2][0]),key=lambda x : x[1],reverse=True)[:2]

        for ao_trong, p1 in top2_aotrong:
            for ao_khoac, p2 in top2_aokhoac :
                for quan, p3 in top2_quan :
                    if data.situation == "di_lam" and ao_trong in ["tank_top", "crop_top"]:
                        continue
                    outfit_key = (ao_trong, ao_khoac, quan)
                    if outfit_key not in seen :
                        seen.add(outfit_key)
                        color = random.choice(pallete_list).copy() #copy(): tao ban sao de neu chinh sua se khong thay doi du lieu goc
                        
                        if ao_khoac == "khong_co":
                            color[1] = "khong_co"

                        decrease = 1.0 if pc == data.style.strip() else 0.85
                        score = (((p1+p2+p3)/3)**0.35)*100*decrease
                        outfits.append({
                            "ao_trong":     ao_trong,
                            "ao_khoac":     ao_khoac,
                            "quan":         quan,
                            "mau_ao_trong": color[0],
                            "mau_ao_khoac": color[1],
                            "mau_quan":     color[2],                             
                            "compatibility": round(score, 2)
                        })
        outfits.sort(key=lambda x: x["compatibility"], reverse=True)
    return{
        "outfits" : outfits[:6]
    }
