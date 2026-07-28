import os
from flask import Flask, render_template, request, redirect
from supabase import create_client, Client

app = Flask(__name__)

# 1. Kết nối với Supabase qua API Key (Được cấu hình ở Biến môi trường)
# Nếu chạy dưới máy, bạn có thể điền thẳng URL và ANON_KEY vào dạng chuỗi "..."
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://vogdtyleygtryydyxjym.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_suAZLYQ0eQEV3iDWtO8Zog_7EAMGpwK")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# ĐIỀU HƯỚNG TRANG WEB

@app.route('/')
def index():
    # Lấy các khoản chi tiêu từ bảng ChiTieu trên Supabase
    response = supabase.table("ChiTieu").select("*").execute()
    
    # Dữ liệu trả về từ Supabase là danh sách các dictionary:
    # [{'ID': 1, 'TEN_KHOAN_CHI': 'Lương', 'LOAI_GD': 'Thu Nhập', 'SO_TIEN': 1000}, ...]
    cac_giao_dich_raw = response.data

    # Chuyển dữ liệu về dạng tuple (ID, TEN_KHOAN_CHI, LOAI_GD, SO_TIEN)
    # để khớp với template index.html cũ của bạn
    cac_giao_dich = [
        (gd['ID'], gd['TEN_KHOAN_CHI'], gd['LOAI_GD'], gd['SO_TIEN']) 
        for gd in cac_giao_dich_raw
    ]

    # Tính toán các chỉ só
    tong_chi = sum(gd[3] for gd in cac_giao_dich if gd[2]=="Chi Tiêu")
    tong_thu = sum(gd[3] for gd in cac_giao_dich if gd[2]=="Thu Nhập")
    so_du = tong_thu - tong_chi


    # Bơm dữ liệu vào html
    return render_template('index.html',ds_giao_dich = cac_giao_dich,
                                        tong_thu = tong_thu,
                                        tong_chi = tong_chi,
                                        so_du = so_du)

# Thêm Khoản chi

@app.route('/add_financial', methods=['POST'])
def add_financial():

    #1. Lấy dữ liệu từ ô input
    ten = request.form.get('TEN_KHOAN_CHI')
    loai = request.form.get('LOAI_GD')
    so_tien = float(request.form.get('SO_TIEN'))

    #2. Kết nối vào DB và chèn dữ liệu
    data = {
        "TEN_KHOAN_CHI": ten,
        "LOAI_GD": loai,
        "SO_TIEN": so_tien
    }    
    supabase.table("ChiTieu").insert("data").execute()

    #3. Sau khi lưu xong, reload để cập nhật dữ liệu
    return redirect('/')

# CHẠY ỨNG DỤNG

if __name__ == '__main__':
    app.run(debug=True)  # Khởi động web server của Flask
