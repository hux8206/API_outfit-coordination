from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import random

app = FastAPI()

model = joblib.load('model.pkl')
enc_content = joblib.load('encoder_cont.pkl')
enc_label = joblib.load('encoder_label.pkl')

# Phân màu theo CẢ 2 — màu da + hoàn cảnh
PALETTE = {
    # ĐI LÀM — tone trung tính, trang trọng
    ("trang", "di_lam"): [
        ['#FFFFFF', '#1A1A1A', '#4A4A4A'],  # áo trắng + khoác đen + quần xám
        ['#F5F0E8', '#8B6F5E', '#4A4A4A'],  # áo be + khoác nâu + quần xám đậm
        ['#FFFFFF', '#1A3A5C', '#E8E0D5'],  # áo trắng + khoác navy + quần be
    ],

    ("vang", "di_lam"): [
        ['#FFFFFF', '#1A3A5C', '#4A4A4A'],  # áo trắng + khoác navy + quần xám
        ['#F5F0E8', '#8B6F5E', '#2F3A44'],  # áo be + khoác nâu + quần jeans đen
        ['#FFFFFF', '#4A4A4A', '#E8E0D5'],  # áo trắng + khoác xám đậm + quần be
        ['#F5DEB3', '#106B80', '#4A4A4A'],  # áo vàng nhạt + khoác teal đậm + quần xám
    ],

    ("ngam", "di_lam"): [
        ['#FFFFFF', '#4A4A4A', '#1A1A1A'],  # áo trắng + khoác xám + quần đen
        ['#F5DEB3', '#8B6F5E', '#2F3A44'],  # áo vàng nhạt + khoác nâu + jeans đen
        ['#E8E0D5', '#1A3A5C', '#4A4A4A'],  # áo be + khoác navy + quần xám
        ['#FFFFFF', '#106B80', '#1A1A1A'],  # áo trắng + khoác teal đậm + quần đen
    ],

        # ĐI HỌC — casual
    ("trang", "di_hoc"): [
        ['#FFFFFF', '#4A90D9', '#355C7D'],  # áo trắng + khoác denim + jeans xanh đậm
        ['#F5F0E8', '#8B6F5E', '#6F8FAF'],  # áo be + khoác nâu + jeans xanh classic
        ['#FFD6E0', '#6C63A8', '#AFCBDA'],  # áo hồng + khoác tím + jeans xanh nhạt
        ['#E3F2FD', '#019898', '#2F3A44'],  # áo xanh nhạt + khoác teal + jeans đen
    ],

    ("vang", "di_hoc"): [
        ['#F5F0E8', '#106B80', '#4A4A4A'],  # áo be + khoác teal + quần xám
        ['#FFFFFF', '#D97A2C', '#8B6F5E'],  # áo trắng + khoác cam đất + quần nâu
        ['#E8CFC1', '#8B6F5E', '#1A1A1A'],  # áo nude + khoác nâu + quần đen
        ['#D6E8A3', '#019898', '#4A4A4A'],  # áo olive nhạt + khoác teal + quần xám
    ],

    ("ngam", "di_hoc"): [
        ['#F5DEB3', '#FF8C00', '#1A1A1A'],  # áo vàng nhạt + khoác cam + quần đen
        ['#FFFFFF', '#106B80', '#1A1A1A'],  # áo trắng + khoác teal + quần đen
        ['#FFD700', '#4A4A4A', '#1A1A1A'],  # áo vàng + khoác xám + quần đen
        ['#E8E0D5', '#4A90D9', '#4A4A4A'],  # áo be + khoác xanh + quần xám 
    ],
\
    # ĐI CHƠI — nổi hơn
    ("trang", "di_choi"): [
        ['#FFFFFF', '#B22222', '#1A1A1A'],  # áo trắng + khoác đỏ đô + quần đen
        ['#FFD6E0', '#C8A2C8', '#E8E0D5'],  # áo hồng + khoác tím pastel + quần be
        ['#F5F0E8', '#019898', '#4A4A4A'],  # áo be + khoác teal + quần xám
        ['#E3F2FD', '#1A3A5C', '#FFFFFF'],  # áo xanh nhạt + khoác navy + quần trắng
    ],

    ("vang", "di_choi"): [
        ['#FFFFFF', '#FF8C00', '#355C7D'],  # áo trắng + khoác cam + jeans xanh đậm
        ['#F5F0E8', '#019898', '#6F8FAF'],  # áo be + khoác teal + jeans classic
        ['#FFFFFF', '#4A90D9', '#2F3A44'],  # áo trắng + khoác xanh + jeans đen
        ['#FFD700', '#8B6F5E', '#7A7A7A'],  # áo vàng + khoác nâu + jeans xám
    ],

    ("ngam", "di_choi"):[
        ['#FFFFFF', '#FF8C00', '#2F3A44'],  # áo trắng + khoác cam + jeans đen
        ['#F5DEB3', '#019898', '#355C7D'],  # áo be + khoác teal + jeans xanh đậm
        ['#FFD700', '#B22222', '#6F8FAF'],  # áo vàng + khoác đỏ đô + jeans xanh vừa
        ['#FFFFFF', '#6C63A8', '#AFCBDA'],  # áo trắng + khoác tím + jeans nhạt
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

    key = (data.skin.strip(), data.situation.strip())
    palette_list = PALETTE.get(key, [['#FFFFFF', '#1A1A1A', '#9E9E9E']])
    color = random.choice(palette_list)

    encode = enc_content.transform(dulieu)
    result = model.predict(encode)
    result_enc = enc_label.inverse_transform(result)[0]

    if result_enc[1] == "khong_co":
        color[1] = "khong_co"

    return {
        "ao_trong":      result_enc[0],
        "ao_khoac":      result_enc[1],
        "quan":          result_enc[2],
        "mau_ao_trong":  color[0],
        "mau_quan":      color[2],
        "mau_ao_khoac":  color[1]
    }