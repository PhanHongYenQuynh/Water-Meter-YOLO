import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite (tạo mới nếu chưa tồn tại)
conn = sqlite3.connect('water_meter.db')
cursor = conn.cursor()

# Tạo bảng WT với hai cột riêng biệt: first_digits và last_two_digits
cursor.execute('''
    CREATE TABLE IF NOT EXISTS WT (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT,
        end_time TEXT,
        first_digits TEXT,  -- Cột lưu số đầu
        last_two_digits TEXT  -- Cột lưu hai số cuối
    )
''')

# Hàm lưu dữ liệu vào cơ sở dữ liệu
def save_to_database(water_meter, start_time, end_time):
    conn = sqlite3.connect('water_meter.db')
    cursor = conn.cursor()
    for meter in water_meter:
        # Tách số đầu và hai số cuối
        if len(meter) >= 2:
            first_digits = meter[:-2]  # Lấy tất cả trừ 2 số cuối
            last_two_digits = meter[-2:]  # Lấy 2 số cuối
        else:
            first_digits = meter  # Nếu chuỗi ngắn hơn 2 ký tự, giữ nguyên
            last_two_digits = ""
        
        cursor.execute('''
            INSERT INTO WT (start_time, end_time, first_digits, last_two_digits)
            VALUES (?, ?, ?, ?)
        ''', (start_time.isoformat(), end_time.isoformat(), first_digits, last_two_digits))
    
    conn.commit()
    conn.close()

# Đóng kết nối ban đầu
conn.commit()
conn.close()