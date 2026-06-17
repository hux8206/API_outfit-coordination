from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import random
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini = genai.GenerativeModel("gemini-3.5-flash")

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
    Bạn là AI phân tích yêu cầu phối đồ.

    Nhiệm vụ:
    Đọc mô tả của người dùng và chuyển thành JSON đúng format bên dưới.

    QUY TẮC:
    - Chỉ trả về JSON hợp lệ.
    - Không giải thích.
    - Không thêm markdown.
    - Nếu người dùng dùng tiếng Anh hoặc từ đồng nghĩa thì tự hiểu và chuyển về format chuẩn.
    - Nếu thiếu thông tin thì điền null.

    Các giá trị hợp lệ:

    skin:
    - trang
    - vang
    - ngam

    season:
    - nong
    - mat
    - lanh

    sex:
    - nam
    - nu

    situation:
    - di_hoc
    - di_choi
    - di_lam

    style:
    - toi_gian
    - lich_su
    - streetwear
    - sporty
    - han_quoc
    - vintage

    Ví dụ:

    Input:
    "male, dark skin, sporty style, hot weather, go to school"

    Output:
    {{
        "skin": "ngam",
        "season": "nong",
        "sex": "nam",
        "situation": "di_hoc",
        "style": "sporty"
    }}

    Input:
    "Tôi là nam da vàng đi chơi trời mát thích phong cách Hàn Quốc"

    Output:
    {{
        "skin": "vang",
        "season": "mat",
        "sex": "nam",
        "situation": "di_choi",
        "style": "han_quoc"
    }}

    Phân tích câu sau:

    "{data.text}"
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
    
    seen = set()
    outfits = []
    pallete_key = (data.skin.strip(), data.situation.strip())
    pallete_list = PALETTE.get(pallete_key, [["trang","den","xam"]])

    for pc in style_list:
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

        # Tăng lên top3 để đa dạng hơn
        top3_aotrong = sorted(zip(categories[0], probas[0][0]), key=lambda x: x[1], reverse=True)[:3]
        top3_aokhoac = sorted(zip(categories[1], probas[1][0]), key=lambda x: x[1], reverse=True)[:3]
        top3_quan    = sorted(zip(categories[2], probas[2][0]), key=lambda x: x[1], reverse=True)[:3]

        # Đảm bảo phong cách này góp được ít nhất 1 outfit (lấy top1 trước)
        best_outfit_for_pc = None

        for ao_trong, p1 in top3_aotrong:
            for ao_khoac, p2 in top3_aokhoac:
                for quan, p3 in top3_quan:
                    if data.situation == "di_lam" and ao_trong in ["tank_top", "crop_top"]:
                        continue

                    outfit_key = (ao_trong, ao_khoac, quan)
                    
                    color = random.choice(pallete_list).copy()
                    if ao_khoac == "khong_co":
                        color[1] = "khong_co"

                    decrease = 1.0 if pc == data.style.strip() else 0.85
                    score = (((p1 + p2 + p3) / 3) ** 0.35) * 100 * decrease

                    candidate = {
                        "phong_cach":   pc,
                        "ao_trong":     ao_trong,
                        "ao_khoac":     ao_khoac,
                        "quan":         quan,
                        "mau_ao_trong": color[0],
                        "mau_ao_khoac": color[1],
                        "mau_quan":     color[2],
                        "compatibility": round(score, 2)
                    }

                    # Lưu lại outfit tốt nhất của phong cách này (dù trùng vẫn lưu tạm)
                    if best_outfit_for_pc is None or score > best_outfit_for_pc["compatibility"]:
                        best_outfit_for_pc = candidate

                    # Nếu chưa trùng thì thêm vào danh sách chính
                    if outfit_key not in seen:
                        seen.add(outfit_key)
                        outfits.append(candidate)

        # Đảm bảo MỖI phong cách có ít nhất 1 outfit đại diện trong kết quả cuối
        if best_outfit_for_pc:
            key = (best_outfit_for_pc["ao_trong"], best_outfit_for_pc["ao_khoac"], best_outfit_for_pc["quan"])
            if key not in seen:
                seen.add(key)
                outfits.append(best_outfit_for_pc)

    outfits.sort(key=lambda x: x["compatibility"], reverse=True)

    # Lấy outfit đa dạng — ưu tiên không lặp ao_trong liên tiếp
    final_outfits = []
    used_ao_trong = []
    
    for outfit in outfits:
        if len(final_outfits) >= 6:
            break
        # Ưu tiên outfit có ao_trong khác với 2 outfit gần nhất
        recent_ao_trong = used_ao_trong[-2:]
        if outfit["ao_trong"] not in recent_ao_trong or len(final_outfits) < 2:
            final_outfits.append(outfit)
            used_ao_trong.append(outfit["ao_trong"])

    # Nếu chưa đủ 6 thì bổ sung từ outfits còn lại
    if len(final_outfits) < 6:
        for outfit in outfits:
            if outfit not in final_outfits:
                final_outfits.append(outfit)
            if len(final_outfits) >= 6:
                break

    return {"outfits": final_outfits[:6]}
