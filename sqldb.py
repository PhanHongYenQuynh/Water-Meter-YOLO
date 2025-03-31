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
        # Giả định: 4 số trắng, số còn lại là số đỏ (có thể 2 hoặc 3 chữ số)
        if len(meter) >= 4:
            white_digits = meter[:-3] if len(meter) > 4 else meter[:-2]  # 4 số trắng nếu tổng >= 5 chữ số, còn lại là số đỏ
            red_digits = meter[-3:] if len(meter) > 4 else meter[-2:]    # 3 số đỏ hoặc 2 số đỏ
        else:
            white_digits = meter  # Nếu ngắn hơn 4, coi như chỉ có số trắng
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