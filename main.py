import customtkinter as ctk 
import sqlite3
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BookingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Booking App")
        self.geometry("600x400")

       # --- ส่วนของฟอร์ม (UI Elements) ---
        self.label_title = ctk.CTkLabel(self, text="จองคิวรับบริการ", font=("Arial", 20 , "bold"))
        self.label_title.pack(pady=20)

        self.entry_name = ctk.CTkEntry(self, placeholder_text="ชื่อจริง" , width=300)
        self.entry_name.pack(pady=10)

        self.gender_var = ctk.StringVar(value="ชาย")
        self.gender_menu = ctk.CTkOptionMenu(self, values=["ชาย", "หญิง" , "อื่นๆ"] , variable=self.gender_var,width=300)
        self.gender_menu.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="อีเมล" , width=300)
        self.entry_email.pack(pady=10)


        self.entry_phone = ctk.CTkEntry(
            self, 
            placeholder_text="หมายเลขโทรศัพท์" , 
            width=300,
           )  
        self.entry_phone.pack(pady=10)

        self.entry_phone.bind('<FocusOut>', self.validate_phone)

        self.button_submit = ctk.CTkButton(self, text="บันทึก", command=self.submit_booking)
        self.button_submit.pack(pady=20)

    def validate_phone(self, event):
        # P คือค่าปัจจุบันในช่องกรอกหลังจากที่เรากดปุ่มบนคีย์บอร์ด
        # เงื่อนไข: ถ้าเป็นค่าว่าง (ลบจนหมด) หรือ เป็นตัวเลขล้วน และยาวไม่เกิน 10 หลัก
        
        P = self.entry_phone.get()
        # ถ้าไม่เป็นตัวเลข หรือ ยาวเกิน 10 หลัก
        if P != "" and (not P.isdigit() or len(P) > 10):
            self.entry_phone.configure(border_color="red") # เปลี่ยนสีกรอบเป็นสีแดงเตือน
            self.label_title.configure(text="Error: หมายเลขโทรศัพท์ไม่ถูกต้อง" , text_color="red")
        else:
            self.label_title.configure(text="" , text_color="red")
            self.entry_phone.configure(border_color=["#979DA2", "#565B5E"]) # กลับเป็นสีปกติ
    
    def submit_booking(self):
        name = self.entry_name.get()
        gender = self.gender_var.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
      
    #   From Validate 
        if not name:
            self.label_title.configure(text="Error: ชื่อไม่สามารถเว้นว่างได้" , text_color="red")
            return
        
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            self.label_title.configure(text="Error: รูปแบบอีเมลไม่ถูกต้อง" , text_color="red")
            return

        try :
            conn = sqlite3.connect("booking_data.db")
            cursor = conn.cursor()
            
            sql = '''INSERT INTO bookings (customer_name , gender , email , phone) 
                    VALUES (? , ? , ? , ?)'''
            cursor.execute(sql , (name , gender , email , phone))
            conn.commit()
            conn.close()
            print("Booking submitted successfully!")
            self.label_title.configure(text="Booking submitted successfully!" , text_color="green")
            self.clear_form()
        except Exception as e:
            print("Error submitting booking:", e)

    def clear_form(self):
        self.entry_name.delete(0, ctk.END)
        self.gender_var.set("Male")
        self.entry_email.delete(0, ctk.END)
        self.entry_phone.delete(0, ctk.END)
        self.entry_name.focus()  # ตั้งโฟกัสกลับไปที่ช่องกรอกชื่อ

if __name__ == "__main__":
    app = BookingApp()
    app.mainloop()