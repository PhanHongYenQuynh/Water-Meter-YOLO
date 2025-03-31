import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite (tạo mới nếu chưa tồn tại)
conn = sqlite3.connect('water_meter.db')
cursor = conn.cursor()

# Tạo bảng WT với hai cột riêng biệt: white_digits và red_digits
cursor.execute('''
    CREATE TABLE IF NOT EXISTS WT (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT,
        end_time TEXT,
        white_digits TEXT,  -- Cột lưu số trắng
        red_digits TEXT     -- Cột lưu số đỏ
    )
''')

# Hàm lưu dữ liệu vào cơ sở dữ liệu
def save_to_database(water_meter, start_time, end_time):
    conn = sqlite3.connect('water_meter.db')
    cursor = conn.cursor()
    for meter in water_meter:
        # Tổng số chữ số luôn là 6
        if len(meter) == 6:
            # Nếu số đỏ là 3 chữ số (giả định dựa trên giá trị lớn, ví dụ: >= 100)
            if int(meter[-3:]) >= 100:
                white_digits = meter[:3]  # 3 số trắng
                red_digits = meter[3:]    # 3 số đỏ
            else:
                white_digits = meter[:4]  # 4 số trắng
                red_digits = meter[4:]    # 2 số đỏ
        else:
            # Nếu không đủ 6 chữ số (trường hợp lỗi), giữ nguyên toàn bộ làm số trắng
            white_digits = meter
            red_digits = ""
        
        cursor.execute('''
            INSERT INTO WT (start_time, end_time, white_digits, red_digits)
            VALUES (?, ?, ?, ?)
        ''', (start_time.isoformat(), end_time.isoformat(), white_digits, red_digits))
    
    conn.commit()
    conn.close()

# Đóng kết nối ban đầu
conn.commit()
conn.close()