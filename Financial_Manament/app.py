# Truy cập thư viện sqlite3
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Kết nối database

def financial_history_db():
    # Kết nối financial_history đến thư viện sqlite3, Nếu chưa có thì sẽ tạo file
    conn = sqlite3.connect("financial_history.db")

    # Tạo con trỏ cho file
    cursor = conn.cursor()

    # Tạo bảng
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ChiTieu (
                   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                   TEN_KHOAN_CHI TEXT NOT NULL,
                   LOAI_GD TEXT NOT NULL,
                   SO_TIEN FLOAT NOT NULL
                   )
                   ''')
    conn.commit()
    conn.close()

# ĐIỀU HƯỚNG TRANG WEB

@app.route('/')
def index():
    conn = sqlite3.connect("financial_history.db")
    cursor = conn.cursor()

    # Lấy các khoản chi tiêu
    cursor.execute("SELECT * FROM ChiTieu")
    cac_giao_dich = cursor.fetchall()
    conn.close()

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
    conn = sqlite3.connect('financial_history.db')
    cursor = conn.cursor()
    cursor.execute("" 
    "INSERT INTO ChiTieu (TEN_KHOAN_CHI, LOAI_GD, SO_TIEN) VALUES(?, ?, ?)",
    (ten, loai, so_tien)
    )
    conn.commit()
    conn.close()

    #3. Sau khi lưu xong, reload để cập nhật dữ liệu
    return redirect('/')

# CHẠY ỨNG DỤNG

if __name__ == '__main__':
    financial_history_db() # Chay ham tao DB
    app.run(debug=True)  # Khởi động web server của Flask
