from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import random
import google.generativeai as genai
import json

genai.configure(api_key="GEMINI_API_KEY")
gemini = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

model = joblib.load('model.pkl')
enc_content = joblib.load('encoder_cont.pkl')
enc_label = joblib.load('encoder_label.pkl')

PALETTE = {
    # DI LAM

    ("trang", "di_lam"): [
        ["trang", "den", "xam"],
        ["den", "nau", "trang"],
        ["trang", "xam", "be"],
        ["kem", "den", "xam"],
        ["trang","xanh","den"],
        ["trang","den","nau"]
    ],

    ("vang", "di_lam"): [
        ["den", "xam", "trang"],
        ["kem", "trang", "den"],
        ["trang", "den", "be"],
        ["den", "nau", "xam"],
        ["kem","xanh","nau"]
    ],

    ("ngam", "di_lam"): [
        ["trang", "xam", "den"],
        ["vang", "trang", "xam"],
        ["kem", "xam", "trang"],
        ["trang", "nau", "den"],
        ["trang","xanh","xam"],
        ["kem","trang","nau"]
    ],

    #DI HOC
    ("trang", "di_hoc"): [
        ["trang", "xanh", "nau"],
        ["hong",  "trang", "xam"],
        ["vang",  "nau", "den"],
        ["den", "xam",   "trang"],
        ["xanhla",  "trang", "den"],
        ["vang","trang","nau"]
    ],

    ("vang", "di_hoc"): [
        ["do", "trang",   "den"],
        ["kem",   "xanh",  "nau"],
        ["vang",  "trang", "den"],
        ["trang", "nau",   "xanh"],
        ["den",   "trang", "nau"],
    ],

    ("ngam", "di_hoc"): [
        ["hong", "trang",  "den"],
        ["vang",  "den",  "trang"],
        ["xanh", "trang", "den"],
        ["do",   "trang","nau"],
        ["xanh",  "den",  "trang"],
    ],
    # -------- ĐI CHƠI --------

    ("trang", "di_choi"): [
        ["do", "kem",   "den"],  
        ["hong",  "xam",  "trang"], 
        ["kem",   "nau",  "be"],    
        ["xanhla", "den", "trang"], 
        ["xanh",  "den",  "xam"],
        ["xanh","trang","nau"]   
    ],

    ("vang", "di_choi"): [
        ["trang", "kem",  "xanh"], 
        ["xanh",   "nau",  "xam"],   
        ["trang", "xanh", "den"],   
        ["den",  "nau",  "xam"],   
        ["den", "trang",  "be"],
        ["trang","den","nau"]    
    ],

    ("ngam", "di_choi"): [
        ["do", "kem",  "den"],
        ["kem",   "nau",  "xanh"], 
        ["vang",  "do",   "trang"],   
        ["den", "trang",  "xanh"],  
        ["kem",   "xam",  "den"],
        ["kem","trang","nau"]   
    ]
}

class TextInput(BaseModel):
    text : str

class DataInput(BaseModel):
    skin : str
    season : str
    sex : str
    situation : str
    style : str

@app.post("/predict_text")
def predict_text(data: TextInput):
    promt = f"""
        Từ câu này : "{data.text}"
        Trích xuất thộng tin và trả về JSON :
        {{
            "skin" : "trang/vang/ngam hoặc null",
            "season" : "nong/mat/lanh hoặc null",
            "sex" : "nam/nu hoặc null",
            "situation" : "di_lam/di_hoc/di_choi hoặc null",
            "style" : "toi_gian/lich_su/streetwear/sporty/han_quoc/vintage hoặc null"
        }}
        Chỉ trả về JSON, không giải thích gì thêm.
    """

    try :
        response = gemini.generate_content(promt)
        print("GEMINI RAW:", response.text, flush=True)

        text = response.text.strip()
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        print("SAU CLEAN:", text, flush=True)
        extracted = json.loads(text)
    except Exception as e:
        return {"error": str(e)}
        
    defaults = {
        "skin" : "trang",
        "season" : "mat",
        "sex" : "nam",
        "situation" : "di_choi",
        "style" : "toi_gian"
    }

    for key in defaults :
        if not extracted.get(key) or extracted.get(key) == "null" :
            extracted[key] = defaults[key]

    input_data = DataInput(
        skin = extracted["skin"],
        season    = extracted["season"],
        sex       = extracted["sex"],
        situation = extracted["situation"],
        style     = extracted["style"]
    )
    return predict(input_data)

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

    for pc in current_list :
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
