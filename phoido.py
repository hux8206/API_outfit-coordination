import csv
import random

# ==========================
# GIÁ TRỊ INPUT
# ==========================
MAU_DA    = ["trang", "vang", "ngam"]
MUA       = ["nong", "mat", "lanh"]
GIOI_TINH = ["nam", "nu"]

RULES = [
    #---DI LAM---

    #toi gian
    ("di_lam","toi_gian","nu","nong", "so_mi",   "khong_co", "quan_tay"),
    ("di_lam","toi_gian","nu","nong", "ao_thun", "cardigan", "quan_tay"),
    ("di_lam","toi_gian","nu","nong", "polo",    "khong_co", "quan_tay"),
    ("di_lam","toi_gian","nu","nong", "so_mi",   "khong_co", "chan_vay"),

    ("di_lam","toi_gian","nu","mat",  "so_mi",   "blazer",   "quan_tay"),
    ("di_lam","toi_gian","nu","mat",  "ao_thun", "blazer",   "quan_tay"),
    ("di_lam","toi_gian","nu","mat",  "ao_len",  "cardigan", "chan_vay"),
    ("di_lam","toi_gian","nu","mat",  "polo",    "blazer",   "quan_tay"),

    ("di_lam","toi_gian","nu","lanh", "ao_len",  "ao_khoac", "quan_tay"),
    ("di_lam","toi_gian","nu","lanh", "ao_len",  "blazer",   "quan_tay"),
    ("di_lam","toi_gian","nu","lanh", "so_mi",   "ao_khoac", "quan_tay"),
    ("di_lam","toi_gian","nu","lanh", "ao_len",  "ao_khoac", "chan_vay"),

    ("di_lam","toi_gian","nam","nong", "so_mi",   "khong_co", "quan_tay"),
    ("di_lam","toi_gian","nam","nong", "polo",    "khong_co", "kaki"),
    ("di_lam","toi_gian","nam","nong", "ao_thun", "ao_khoac", "kaki"),
    ("di_lam","toi_gian","nam","nong", "so_mi",   "khong_co", "kaki"),

    ("di_lam","toi_gian","nam","mat",  "so_mi",   "blazer",   "quan_tay"),
    ("di_lam","toi_gian","nam","mat",  "polo",    "blazer",   "kaki"),
    ("di_lam","toi_gian","nam","mat",  "ao_thun", "ao_khoac", "kaki"),
    ("di_lam","toi_gian","nam","mat",  "ao_len",  "blazer",   "quan_tay"),

    ("di_lam","toi_gian","nam","lanh", "ao_len",  "ao_khoac", "quan_tay"),
    ("di_lam","toi_gian","nam","lanh", "so_mi",   "ao_khoac", "quan_tay"),
    ("di_lam","toi_gian","nam","lanh", "ao_len",  "blazer",   "kaki"),
    ("di_lam","toi_gian","nam","lanh", "polo",    "ao_khoac", "kaki"),

    #lich su
    ("di_lam","lich_su","nu","nong", "so_mi",   "khong_co", "chan_vay"),
    ("di_lam","lich_su","nu","nong", "so_mi",   "cardigan", "chan_vay"),
    ("di_lam","lich_su","nu","nong", "polo",    "khong_co", "quan_tay"),
    ("di_lam","lich_su","nu","nong", "ao_thun", "blazer",   "quan_tay"),

    ("di_lam","lich_su","nu","mat",  "so_mi",   "blazer",   "chan_vay"),
    ("di_lam","lich_su","nu","mat",  "ao_thun", "blazer",   "quan_tay"),
    ("di_lam","lich_su","nu","mat",  "ao_len",  "blazer",   "chan_vay"),
    ("di_lam","lich_su","nu","mat",  "so_mi",   "cardigan", "quan_tay"),

    ("di_lam","lich_su","nu","lanh", "ao_len",  "blazer",   "quan_tay"),
    ("di_lam","lich_su","nu","lanh", "ao_len",  "ao_khoac", "chan_vay"),
    ("di_lam","lich_su","nu","lanh", "so_mi",   "ao_khoac", "quan_tay"),
    ("di_lam","lich_su","nu","lanh", "ao_len",  "cardigan", "chan_vay"),

    ("di_lam","lich_su","nam","nong", "so_mi",   "khong_co", "quan_tay"),
    ("di_lam","lich_su","nam","nong", "so_mi",   "blazer",   "quan_tay"),
    ("di_lam","lich_su","nam","nong", "polo",    "khong_co", "kaki"),
    ("di_lam","lich_su","nam","nong", "so_mi",   "khong_co", "kaki"),

    ("di_lam","lich_su","nam","mat",  "so_mi",   "blazer",   "quan_tay"),
    ("di_lam","lich_su","nam","mat",  "ao_len",  "blazer",   "quan_tay"),
    ("di_lam","lich_su","nam","mat",  "polo",    "blazer",   "kaki"),
    ("di_lam","lich_su","nam","mat",  "so_mi",   "ao_khoac", "quan_tay"),

    ("di_lam","lich_su","nam","lanh", "ao_len",  "blazer",   "quan_tay"),
    ("di_lam","lich_su","nam","lanh", "so_mi",   "ao_khoac", "quan_tay"),
    ("di_lam","lich_su","nam","lanh", "ao_len",  "ao_khoac", "kaki"),
    ("di_lam","lich_su","nam","lanh", "polo",    "ao_khoac", "quan_tay"),

    #han quoc
    ("di_lam","han_quoc","nu","nong", "so_mi",   "khong_co", "chan_vay"),
    ("di_lam","han_quoc","nu","nong", "ao_thun", "cardigan", "chan_vay"),
    ("di_lam","han_quoc","nu","nong", "polo",    "khong_co", "quan_tay"),

    ("di_lam","han_quoc","nu","mat",  "ao_len",  "blazer",   "chan_vay"),
    ("di_lam","han_quoc","nu","mat",  "so_mi",   "cardigan", "quan_tay"),
    ("di_lam","han_quoc","nu","mat",  "ao_thun", "blazer",   "chan_vay"),

    ("di_lam","han_quoc","nu","lanh", "ao_len",  "ao_khoac", "chan_vay"),
    ("di_lam","han_quoc","nu","lanh", "ao_len",  "blazer",   "quan_tay"),
    ("di_lam","han_quoc","nu","lanh", "so_mi",   "ao_khoac", "chan_vay"),

    ("di_lam","han_quoc","nam","nong", "so_mi",   "khong_co", "quan_tay"),
    ("di_lam","han_quoc","nam","nong", "polo",    "khong_co", "kaki"),
    ("di_lam","han_quoc","nam","nong", "ao_thun", "cardigan", "kaki"),

    ("di_lam","han_quoc","nam","mat",  "ao_len",  "blazer",   "kaki"),
    ("di_lam","han_quoc","nam","mat",  "so_mi",   "cardigan", "quan_tay"),
    ("di_lam","han_quoc","nam","mat",  "ao_thun", "blazer",   "kaki"),

    ("di_lam","han_quoc","nam","lanh", "ao_len",  "ao_khoac", "kaki"),
    ("di_lam","han_quoc","nam","lanh", "ao_len",  "blazer",   "quan_tay"),
    ("di_lam","han_quoc","nam","lanh", "so_mi",   "ao_khoac", "kaki"),

    # -------- ĐI HỌC --------

    # tối giản - nữ
    ("di_hoc","toi_gian","nu","nong", "ao_thun", "khong_co",       "quan_ni"),
    ("di_hoc","toi_gian","nu","nong", "ao_thun", "ao_chong_nang",  "quan_ni"),
    ("di_hoc","toi_gian","nu","nong", "polo",    "khong_co",       "jeans"),
    ("di_hoc","toi_gian","nu","nong", "so_mi",   "khong_co",       "quan_tay"),

    ("di_hoc","toi_gian","nu","mat",  "ao_thun", "hoodie",         "quan_ni"),
    ("di_hoc","toi_gian","nu","mat",  "polo",    "cardigan",       "jeans"),
    ("di_hoc","toi_gian","nu","mat",  "so_mi",   "ao_khoac",       "quan_tay"),
    ("di_hoc","toi_gian","nu","mat",  "ao_len",  "cardigan",       "quan_ong_suong"),

    ("di_hoc","toi_gian","nu","lanh", "ao_len",  "ao_khoac",       "quan_ni"),
    ("di_hoc","toi_gian","nu","lanh", "ao_len",  "hoodie",         "jeans"),
    ("di_hoc","toi_gian","nu","lanh", "so_mi",   "ao_khoac",       "quan_tay"),
    ("di_hoc","toi_gian","nu","lanh", "ao_len",  "cardigan",       "chan_vay"),

    # tối giản - nam
    ("di_hoc","toi_gian","nam","nong", "ao_thun", "khong_co",       "quan_ong_suong"),
    ("di_hoc","toi_gian","nam","nong", "ao_thun", "ao_chong_nang",  "quan_ong_suong"),
    ("di_hoc","toi_gian","nam","nong", "polo",    "khong_co",       "kaki"),
    ("di_hoc","toi_gian","nam","nong", "so_mi",   "khong_co",       "quan_tay"),

    ("di_hoc","toi_gian","nam","mat",  "ao_thun", "hoodie",         "quan_ong_suong"),
    ("di_hoc","toi_gian","nam","mat",  "polo",    "ao_khoac",       "kaki"),
    ("di_hoc","toi_gian","nam","mat",  "so_mi",   "cardigan",       "quan_tay"),
    ("di_hoc","toi_gian","nam","mat",  "ao_len",  "ao_khoac",       "jeans"),

    ("di_hoc","toi_gian","nam","lanh", "ao_len",  "ao_khoac",       "quan_ong_suong"),
    ("di_hoc","toi_gian","nam","lanh", "ao_len",  "hoodie",         "jeans"),
    ("di_hoc","toi_gian","nam","lanh", "so_mi",   "ao_khoac",       "kaki"),
    ("di_hoc","toi_gian","nam","lanh", "ao_thun", "ao_khoac",       "jeans"),

    # sporty - nữ
    ("di_hoc","sporty","nu","nong", "ao_thun",  "khong_co",       "quan_ni"),
    ("di_hoc","sporty","nu","nong", "ao_thun",  "ao_chong_nang",  "short"),
    ("di_hoc","sporty","nu","nong", "tank_top", "ao_khoac",       "quan_ni"),
    ("di_hoc","sporty","nu","nong", "polo",     "khong_co",       "jeans"),

    ("di_hoc","sporty","nu","mat",  "ao_thun",  "hoodie",         "quan_ni"),
    ("di_hoc","sporty","nu","mat",  "ao_thun",  "ao_khoac",       "jeans"),
    ("di_hoc","sporty","nu","mat",  "polo",     "hoodie",         "kaki"),
    ("di_hoc","sporty","nu","mat",  "ao_thun",  "cardigan",       "quan_ong_suong"),

    ("di_hoc","sporty","nu","lanh", "ao_thun",  "ao_khoac",       "jeans"),
    ("di_hoc","sporty","nu","lanh", "ao_len",   "hoodie",         "quan_ni"),
    ("di_hoc","sporty","nu","lanh", "ao_thun",  "ao_khoac",       "quan_ong_suong"),
    ("di_hoc","sporty","nu","lanh", "polo",     "ao_khoac",       "kaki"),

    # sporty - nam
    ("di_hoc","sporty","nam","nong", "ao_thun",  "ao_chong_nang",  "kaki"),
    ("di_hoc","sporty","nam","nong", "ao_thun",  "khong_co",       "quan_ni"),
    ("di_hoc","sporty","nam","nong", "tank_top", "ao_khoac",       "short"),
    ("di_hoc","sporty","nam","nong", "polo",     "khong_co",       "kaki"),

    ("di_hoc","sporty","nam","mat",  "ao_thun",  "hoodie",         "kaki"),
    ("di_hoc","sporty","nam","mat",  "ao_thun",  "ao_khoac",       "quan_ong_suong"),
    ("di_hoc","sporty","nam","mat",  "polo",     "hoodie",         "jeans"),
    ("di_hoc","sporty","nam","mat",  "ao_len",   "ao_khoac",       "quan_ni"),

    ("di_hoc","sporty","nam","lanh", "ao_thun",  "ao_khoac",       "quan_ong_suong"),
    ("di_hoc","sporty","nam","lanh", "ao_len",   "hoodie",         "jeans"),
    ("di_hoc","sporty","nam","lanh", "polo",     "ao_khoac",       "kaki"),
    ("di_hoc","sporty","nam","lanh", "ao_thun",  "ao_khoac",       "quan_ni"),

    # streetwear - nữ
    ("di_hoc","streetwear","nu","nong", "crop_top", "khong_co",      "jeans"),
    ("di_hoc","streetwear","nu","nong", "crop_top", "ao_khoac",      "jeans"),
    ("di_hoc","streetwear","nu","nong", "ao_thun",  "khong_co",      "quan_ong_suong"),
    ("di_hoc","streetwear","nu","nong", "ao_thun",  "ao_chong_nang", "short"),

    ("di_hoc","streetwear","nu","mat",  "ao_thun",  "hoodie",        "jeans"),
    ("di_hoc","streetwear","nu","mat",  "crop_top", "ao_khoac",      "jeans"),
    ("di_hoc","streetwear","nu","mat",  "ao_thun",  "ao_khoac",      "quan_ong_suong"),
    ("di_hoc","streetwear","nu","mat",  "ao_len",   "hoodie",        "jeans"),

    ("di_hoc","streetwear","nu","lanh", "ao_thun",  "ao_khoac",      "jeans"),
    ("di_hoc","streetwear","nu","lanh", "ao_len",   "ao_khoac",      "quan_ong_suong"),
    ("di_hoc","streetwear","nu","lanh", "crop_top", "ao_khoac",      "jeans"),
    ("di_hoc","streetwear","nu","lanh", "ao_thun",  "hoodie",        "quan_ni"),

    # streetwear - nam
    ("di_hoc","streetwear","nam","nong", "ao_thun",  "khong_co",      "quan_ni"),
    ("di_hoc","streetwear","nam","nong", "ao_thun",  "ao_chong_nang", "quan_ong_suong"),
    ("di_hoc","streetwear","nam","nong", "tank_top", "khong_co",      "jeans"),
    ("di_hoc","streetwear","nam","nong", "ao_thun",  "khong_co",      "short"),

    ("di_hoc","streetwear","nam","mat",  "ao_thun",  "hoodie",        "jeans"),
    ("di_hoc","streetwear","nam","mat",  "ao_thun",  "ao_khoac",      "quan_ong_suong"),
    ("di_hoc","streetwear","nam","mat",  "ao_len",   "hoodie",        "jeans"),
    ("di_hoc","streetwear","nam","mat",  "polo",     "ao_khoac",      "kaki"),

    ("di_hoc","streetwear","nam","lanh", "ao_thun",  "ao_khoac",      "jeans"),
    ("di_hoc","streetwear","nam","lanh", "ao_len",   "ao_khoac",      "jeans"),
    ("di_hoc","streetwear","nam","lanh", "ao_thun",  "hoodie",        "quan_ni"),
    ("di_hoc","streetwear","nam","lanh", "ao_len",   "ao_khoac",      "quan_ong_suong"),


    # Hàn Quốc - nữ
    ("di_hoc","han_quoc","nu","nong", "ao_thun", "khong_co",  "quan_tay"),
    ("di_hoc","han_quoc","nu","nong", "so_mi",   "khong_co",  "chan_vay"),
    ("di_hoc","han_quoc","nu","nong", "polo",    "cardigan",  "quan_tay"),
    ("di_hoc","han_quoc","nu","nong", "ao_thun", "cardigan",  "chan_vay"),

    ("di_hoc","han_quoc","nu","mat",  "ao_len",  "ao_khoac",  "quan_tay"),
    ("di_hoc","han_quoc","nu","mat",  "so_mi",   "cardigan",  "chan_vay"),
    ("di_hoc","han_quoc","nu","mat",  "ao_thun", "blazer",    "quan_tay"),
    ("di_hoc","han_quoc","nu","mat",  "ao_len",  "cardigan",  "chan_vay"),

    ("di_hoc","han_quoc","nu","lanh", "ao_len",  "ao_khoac",  "quan_tay"),
    ("di_hoc","han_quoc","nu","lanh", "ao_len",  "cardigan",  "chan_vay"),
    ("di_hoc","han_quoc","nu","lanh", "so_mi",   "ao_khoac",  "quan_tay"),
    ("di_hoc","han_quoc","nu","lanh", "ao_len",  "blazer",    "chan_vay"),

    # Hàn Quốc - nam
    ("di_hoc","han_quoc","nam","nong", "ao_thun", "khong_co",  "jeans"),
    ("di_hoc","han_quoc","nam","nong", "polo",    "khong_co",  "kaki"),
    ("di_hoc","han_quoc","nam","nong", "so_mi",   "khong_co",  "quan_tay"),
    ("di_hoc","han_quoc","nam","nong", "ao_thun", "cardigan",  "kaki"),

    ("di_hoc","han_quoc","nam","mat",  "ao_len",  "ao_khoac",  "jeans"),
    ("di_hoc","han_quoc","nam","mat",  "so_mi",   "cardigan",  "quan_tay"),
    ("di_hoc","han_quoc","nam","mat",  "ao_thun", "blazer",    "kaki"),
    ("di_hoc","han_quoc","nam","mat",  "polo",    "ao_khoac",  "kaki"),

    ("di_hoc","han_quoc","nam","lanh", "ao_len",  "ao_khoac",  "jeans"),
    ("di_hoc","han_quoc","nam","lanh", "ao_len",  "cardigan",  "kaki"),
    ("di_hoc","han_quoc","nam","lanh", "so_mi",   "ao_khoac",  "quan_tay"),
    ("di_hoc","han_quoc","nam","lanh", "ao_len",  "blazer",    "kaki"),


    # vintage - nữ
    ("di_hoc","vintage","nu","nong", "so_mi",   "khong_co", "chan_vay"),
    ("di_hoc","vintage","nu","nong", "ao_thun", "cardigan", "chan_vay"),
    ("di_hoc","vintage","nu","nong", "polo",    "khong_co", "kaki"),
    ("di_hoc","vintage","nu","nong", "so_mi",   "khong_co", "quan_tay"),

    ("di_hoc","vintage","nu","mat",  "so_mi",   "cardigan", "chan_vay"),
    ("di_hoc","vintage","nu","mat",  "ao_len",  "cardigan", "quan_tay"),
    ("di_hoc","vintage","nu","mat",  "ao_thun", "blazer",   "kaki"),
    ("di_hoc","vintage","nu","mat",  "polo",    "ao_khoac", "chan_vay"),

    ("di_hoc","vintage","nu","lanh", "ao_len",  "ao_khoac", "chan_vay"),
    ("di_hoc","vintage","nu","lanh", "ao_len",  "cardigan", "quan_tay"),
    ("di_hoc","vintage","nu","lanh", "so_mi",   "ao_khoac", "kaki"),
    ("di_hoc","vintage","nu","lanh", "ao_len",  "blazer",   "chan_vay"),

    # vintage - nam
    ("di_hoc","vintage","nam","nong", "so_mi",   "khong_co", "kaki"),
    ("di_hoc","vintage","nam","nong", "polo",    "khong_co", "kaki"),
    ("di_hoc","vintage","nam","nong", "ao_thun", "cardigan", "quan_tay"),
    ("di_hoc","vintage","nam","nong", "so_mi",   "khong_co", "quan_tay"),

    ("di_hoc","vintage","nam","mat",  "so_mi",   "cardigan", "kaki"),
    ("di_hoc","vintage","nam","mat",  "ao_len",  "cardigan", "quan_tay"),
    ("di_hoc","vintage","nam","mat",  "ao_thun", "ao_khoac", "kaki"),
    ("di_hoc","vintage","nam","mat",  "polo",    "blazer",   "kaki"),

    ("di_hoc","vintage","nam","lanh", "ao_len",  "ao_khoac", "kaki"),
    ("di_hoc","vintage","nam","lanh", "ao_len",  "cardigan", "quan_tay"),
    ("di_hoc","vintage","nam","lanh", "so_mi",   "ao_khoac", "kaki"),
    ("di_hoc","vintage","nam","lanh", "ao_len",  "blazer",   "quan_tay"),

    # -------- ĐI CHƠI --------

    # tối giản - nữ
    ("di_choi","toi_gian","nu","nong", "ao_thun", "khong_co",      "short"),
    ("di_choi","toi_gian","nu","nong", "ao_thun", "ao_chong_nang", "jeans"),
    ("di_choi","toi_gian","nu","nong", "polo",    "khong_co",      "kaki"),
    ("di_choi","toi_gian","nu","nong", "so_mi",   "khong_co",      "chan_vay"),

    ("di_choi","toi_gian","nu","mat",  "ao_thun", "ao_khoac",      "short"),
    ("di_choi","toi_gian","nu","mat",  "polo",    "cardigan",      "jeans"),
    ("di_choi","toi_gian","nu","mat",  "ao_len",  "ao_khoac",      "quan_ong_suong"),
    ("di_choi","toi_gian","nu","mat",  "so_mi",   "cardigan",      "kaki"),

    ("di_choi","toi_gian","nu","lanh", "ao_len",  "ao_khoac",      "jeans"),
    ("di_choi","toi_gian","nu","lanh", "ao_len",  "hoodie",        "quan_ong_suong"),
    ("di_choi","toi_gian","nu","lanh", "so_mi",   "ao_khoac",      "kaki"),
    ("di_choi","toi_gian","nu","lanh", "polo",    "ao_khoac",      "jeans"),

    # tối giản - nam
    ("di_choi","toi_gian","nam","nong", "ao_thun", "khong_co",      "jeans"),
    ("di_choi","toi_gian","nam","nong", "polo",    "khong_co",      "kaki"),
    ("di_choi","toi_gian","nam","nong", "ao_thun", "ao_chong_nang", "short"),
    ("di_choi","toi_gian","nam","nong", "so_mi",   "khong_co",      "kaki"),

    ("di_choi","toi_gian","nam","mat",  "ao_thun", "ao_khoac",      "jeans"),
    ("di_choi","toi_gian","nam","mat",  "polo",    "cardigan",      "kaki"),
    ("di_choi","toi_gian","nam","mat",  "ao_len",  "hoodie",        "jeans"),
    ("di_choi","toi_gian","nam","mat",  "so_mi",   "ao_khoac",      "quan_tay"),

    ("di_choi","toi_gian","nam","lanh", "ao_len",  "ao_khoac",      "jeans"),
    ("di_choi","toi_gian","nam","lanh", "ao_len",  "hoodie",        "quan_ong_suong"),
    ("di_choi","toi_gian","nam","lanh", "so_mi",   "ao_khoac",      "kaki"),
    ("di_choi","toi_gian","nam","lanh", "polo",    "ao_khoac",      "jeans"),


    # sporty - nữ
    ("di_choi","sporty","nu","nong", "tank_top", "khong_co",      "short"),
    ("di_choi","sporty","nu","nong", "tank_top", "cardigan",      "quan_ni"),
    ("di_choi","sporty","nu","nong", "ao_thun",  "khong_co",      "short"),
    ("di_choi","sporty","nu","nong", "polo",     "khong_co",      "jeans"),

    ("di_choi","sporty","nu","mat",  "tank_top", "ao_khoac",      "quan_ni"),
    ("di_choi","sporty","nu","mat",  "ao_thun",  "hoodie",        "jeans"),
    ("di_choi","sporty","nu","mat",  "polo",     "ao_khoac",      "kaki"),
    ("di_choi","sporty","nu","mat",  "ao_len",   "cardigan",      "quan_ong_suong"),

    ("di_choi","sporty","nu","lanh", "ao_thun",  "ao_khoac",      "quan_ong_suong"),
    ("di_choi","sporty","nu","lanh", "ao_len",   "hoodie",        "jeans"),
    ("di_choi","sporty","nu","lanh", "tank_top", "ao_khoac",      "quan_ni"),
    ("di_choi","sporty","nu","lanh", "polo",     "ao_khoac",      "kaki"),

    # sporty - nam
    ("di_choi","sporty","nam","nong", "tank_top", "ao_chong_nang", "short"),
    ("di_choi","sporty","nam","nong", "ao_thun",  "khong_co",      "quan_ni"),
    ("di_choi","sporty","nam","nong", "polo",     "khong_co",      "kaki"),
    ("di_choi","sporty","nam","nong", "tank_top", "khong_co",      "jeans"),

    ("di_choi","sporty","nam","mat",  "ao_thun",  "ao_khoac",      "quan_ong_suong"),
    ("di_choi","sporty","nam","mat",  "ao_thun",  "hoodie",        "jeans"),
    ("di_choi","sporty","nam","mat",  "polo",     "ao_khoac",      "kaki"),
    ("di_choi","sporty","nam","mat",  "ao_len",   "hoodie",        "quan_ni"),

    ("di_choi","sporty","nam","lanh", "ao_thun",  "ao_khoac",      "quan_ong_suong"),
    ("di_choi","sporty","nam","lanh", "ao_len",   "hoodie",        "jeans"),
    ("di_choi","sporty","nam","lanh", "polo",     "ao_khoac",      "kaki"),
    ("di_choi","sporty","nam","lanh", "ao_len",   "ao_khoac",      "quan_ni"),


    # streetwear - nữ
    ("di_choi","streetwear","nu","nong", "ao_thun",  "khong_co",      "short"),
    ("di_choi","streetwear","nu","nong", "crop_top", "khong_co",      "jeans"),
    ("di_choi","streetwear","nu","nong", "tank_top", "ao_khoac",      "short"),
    ("di_choi","streetwear","nu","nong", "ao_thun",  "ao_chong_nang", "quan_ong_suong"),

    ("di_choi","streetwear","nu","mat",  "crop_top", "ao_khoac",      "jeans"),
    ("di_choi","streetwear","nu","mat",  "ao_thun",  "hoodie",        "jeans"),
    ("di_choi","streetwear","nu","mat",  "ao_len",   "ao_khoac",      "quan_ong_suong"),
    ("di_choi","streetwear","nu","mat",  "ao_thun",  "cardigan",      "short"),

    ("di_choi","streetwear","nu","lanh", "crop_top", "ao_khoac",      "jeans"),
    ("di_choi","streetwear","nu","lanh", "ao_len",   "hoodie",        "quan_ong_suong"),
    ("di_choi","streetwear","nu","lanh", "ao_thun",  "ao_khoac",      "short"),
    ("di_choi","streetwear","nu","lanh", "tank_top", "ao_khoac",      "jeans"),

    # streetwear - nam
    ("di_choi","streetwear","nam","nong", "tank_top", "khong_co",      "jeans"),
    ("di_choi","streetwear","nam","nong", "ao_thun",  "khong_co",      "short"),
    ("di_choi","streetwear","nam","nong", "ao_thun",  "ao_chong_nang", "quan_ni"),
    ("di_choi","streetwear","nam","nong", "polo",     "khong_co",      "jeans"),

    ("di_choi","streetwear","nam","mat",  "ao_thun",  "ao_khoac",      "jeans"),
    ("di_choi","streetwear","nam","mat",  "ao_len",   "hoodie",        "jeans"),
    ("di_choi","streetwear","nam","mat",  "tank_top", "ao_khoac",      "quan_ong_suong"),
    ("di_choi","streetwear","nam","mat",  "polo",     "hoodie",        "kaki"),

    ("di_choi","streetwear","nam","lanh", "ao_len",   "ao_khoac",      "jeans"),
    ("di_choi","streetwear","nam","lanh", "ao_thun",  "hoodie",        "quan_ni"),
    ("di_choi","streetwear","nam","lanh", "tank_top", "ao_khoac",      "jeans"),
    ("di_choi","streetwear","nam","lanh", "ao_len",   "hoodie",        "quan_ong_suong"),

    # Hàn Quốc - nữ
    ("di_choi","han_quoc","nu","nong", "ao_thun", "cardigan", "chan_vay"),
    ("di_choi","han_quoc","nu","nong", "so_mi",   "khong_co", "chan_vay"),
    ("di_choi","han_quoc","nu","nong", "polo",    "cardigan", "quan_tay"),
    ("di_choi","han_quoc","nu","nong", "ao_thun", "khong_co", "kaki"),

    ("di_choi","han_quoc","nu","mat",  "ao_len",  "ao_khoac", "chan_vay"),
    ("di_choi","han_quoc","nu","mat",  "so_mi",   "cardigan", "quan_tay"),
    ("di_choi","han_quoc","nu","mat",  "ao_thun", "blazer",   "chan_vay"),
    ("di_choi","han_quoc","nu","mat",  "polo",    "ao_khoac", "kaki"),

    ("di_choi","han_quoc","nu","lanh", "ao_len",  "ao_khoac", "chan_vay"),
    ("di_choi","han_quoc","nu","lanh", "ao_len",  "cardigan", "quan_tay"),
    ("di_choi","han_quoc","nu","lanh", "so_mi",   "ao_khoac", "chan_vay"),
    ("di_choi","han_quoc","nu","lanh", "ao_len",  "hoodie",   "kaki"),

    # Hàn Quốc - nam
    ("di_choi","han_quoc","nam","nong", "ao_thun", "khong_co", "kaki"),
    ("di_choi","han_quoc","nam","nong", "polo",    "khong_co", "jeans"),
    ("di_choi","han_quoc","nam","nong", "so_mi",   "cardigan", "quan_tay"),
    ("di_choi","han_quoc","nam","nong", "ao_thun", "cardigan", "kaki"),

    ("di_choi","han_quoc","nam","mat",  "ao_len",  "ao_khoac", "kaki"),
    ("di_choi","han_quoc","nam","mat",  "so_mi",   "cardigan", "quan_tay"),
    ("di_choi","han_quoc","nam","mat",  "ao_thun", "hoodie",   "jeans"),
    ("di_choi","han_quoc","nam","mat",  "polo",    "ao_khoac", "kaki"),

    ("di_choi","han_quoc","nam","lanh", "ao_len",  "ao_khoac", "kaki"),
    ("di_choi","han_quoc","nam","lanh", "ao_len",  "hoodie",   "jeans"),
    ("di_choi","han_quoc","nam","lanh", "so_mi",   "ao_khoac", "quan_tay"),
    ("di_choi","han_quoc","nam","lanh", "ao_len",  "cardigan", "kaki"),

    # vintage - nữ
    ("di_choi","vintage","nu","nong", "so_mi",   "khong_co", "chan_vay"),
    ("di_choi","vintage","nu","nong", "ao_thun", "cardigan", "chan_vay"),
    ("di_choi","vintage","nu","nong", "polo",    "khong_co", "kaki"),
    ("di_choi","vintage","nu","nong", "so_mi",   "khong_co", "quan_tay"),

    ("di_choi","vintage","nu","mat",  "so_mi",   "cardigan", "chan_vay"),
    ("di_choi","vintage","nu","mat",  "ao_len",  "cardigan", "quan_tay"),
    ("di_choi","vintage","nu","mat",  "ao_thun", "blazer",   "kaki"),
    ("di_choi","vintage","nu","mat",  "polo",    "ao_khoac", "chan_vay"),

    ("di_choi","vintage","nu","lanh", "ao_len",  "ao_khoac", "chan_vay"),
    ("di_choi","vintage","nu","lanh", "ao_len",  "cardigan", "quan_tay"),
    ("di_choi","vintage","nu","lanh", "so_mi",   "ao_khoac", "kaki"),
    ("di_choi","vintage","nu","lanh", "ao_len",  "blazer",   "chan_vay"),

    # vintage - nam
    ("di_choi","vintage","nam","nong", "so_mi",   "khong_co", "kaki"),
    ("di_choi","vintage","nam","nong", "polo",    "khong_co", "kaki"),
    ("di_choi","vintage","nam","nong", "ao_thun", "cardigan", "quan_tay"),
    ("di_choi","vintage","nam","nong", "so_mi",   "khong_co", "quan_tay"),

    ("di_choi","vintage","nam","mat",  "so_mi",   "cardigan", "kaki"),
    ("di_choi","vintage","nam","mat",  "ao_len",  "cardigan", "quan_tay"),
    ("di_choi","vintage","nam","mat",  "ao_thun", "ao_khoac", "kaki"),
    ("di_choi","vintage","nam","mat",  "polo",    "blazer",   "kaki"),

    ("di_choi","vintage","nam","lanh", "ao_len",  "ao_khoac", "kaki"),
    ("di_choi","vintage","nam","lanh", "ao_len",  "cardigan", "quan_tay"),
    ("di_choi","vintage","nam","lanh", "so_mi",   "ao_khoac", "kaki"),
    ("di_choi","vintage","nam","lanh", "ao_len",  "blazer",   "quan_tay"),
]

# ==========================
# SINH DỮ LIỆU
# ==========================
def sinh_dataset(so_mau=5000):
    rows = []
    for _ in range(so_mau):
        rule = random.choice(RULES)
        hoan_canh, phong_cach, gioi_tinh, mua, ao_trong, ao_khoac, quan = rule

        mau_da = random.choice(MAU_DA)
        rows.append({
            "mau_da":      mau_da,
            "mua":         mua,
            "gioi_tinh":   gioi_tinh,
            "hoan_canh":   hoan_canh,
            "phong_cach":  phong_cach,
            "ao_trong":    ao_trong,
            "ao_khoac":    ao_khoac,
            "quan":        quan
        })
    return rows

FIELDS = ["mau_da","mua","gioi_tinh","hoan_canh","phong_cach",
          "ao_trong","ao_khoac","quan"]

rows = sinh_dataset(5000)
with open("dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)

print(f"sinh xong {len(rows)} mau")
print("\n 5 dong dau:")
print(",".join(FIELDS))
for r in rows[:5]:
    print(",".join(str(r[k]) for k in FIELDS))

from collections import Counter
print("\nphan bo hoan canh:")
for k, v in sorted(Counter(r["hoan_canh"] for r in rows).items()):
    print(f"  {k:15s}: {v} mau")