import sqlite3

def create_database():
    # Code to create a database
    # เชื่อมต่อฐานข้อมูล (ถ้าไม่มีไฟล์ มันจะสร้างให้ใหม่ชื่อ booking_data.db)
    conn = sqlite3.connect('booking_data.db')
    cursor = conn.cursor()

    # คำสั่ง SQL สำหรับสร้างตาราง
    cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                booking_date TEXT NOT NULL,
                booking_time TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
        )
    ''')

    conn.commit()  # บันทึกการเปลี่ยนแปลง
    conn.close()  # ปิดการเชื่อมต่อฐานข้อมูล

if __name__ == "__main__":
    create_database()
