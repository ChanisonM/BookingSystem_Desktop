import customtkinter as ctk 
import sqlite3
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BookingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Booking App")
        self.geometry("800x600")

       # --- ส่วนของฟอร์ม (UI Elements) ---
        self.label_title = ctk.CTkLabel(self, text="Booking Sevice", font=("Arial", 20 , "bold"))
        self.label_title.pack(pady=20)

        self.entry_name = ctk.CTkEntry(self, placeholder_text="Firstname" , width=300)
        self.entry_name.bind('<FocusOut>', self.validate_name)  
        self.entry_name.pack(pady=10)

        self.gender_var = ctk.StringVar(value="Male")
        self.gender_menu = ctk.CTkOptionMenu(self, values=["Male", "Female" , "Other"] , variable=self.gender_var,width=300)
        self.gender_menu.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email" , width=300)
        self.entry_email.bind('<FocusOut>', self.validate_email)
        self.entry_email.pack(pady=10)


        self.entry_phone = ctk.CTkEntry(
            self, 
            placeholder_text="Phone Number" , 
            width=300,
           )  
        self.entry_phone.pack(pady=10)

        self.entry_phone.bind('<FocusOut>', self.validate_phone)

        self.time_label = ctk.CTkLabel(self, text="Select Time:")
        self.time_label.pack(pady=(19 , 0))

        self.time_option = ["10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
        self.time_var = ctk.StringVar(value=self.time_option[0])
        self.time_menu = ctk.CTkOptionMenu(self, values=self.time_option, variable=self.time_var , width=300)
        self.time_menu.pack(pady=10)

        self.button_submit = ctk.CTkButton(self, text="Save", command=self.submit_booking)
        self.button_submit.pack(pady=20)

        self.button_show = ctk.CTkButton(
            self,
            text="Show Data", 
            command=self.show_data,
            fg_color="transparent",
            border_width=2,
            border_color="#565B5E",
            )
        self.button_show.pack(pady=10)  


    def validate_name(self, event):
        P = self.entry_name.get()
        if P == "" :
            self.entry_name.configure(border_color="red")
            self.label_title.configure(text="Error: Name is invalid" , text_color="red")
        else:
            self.label_title.configure(text="" , text_color="red")
            self.entry_name.configure(border_color=["#979DA2", "#565B5E"])

    def validate_phone(self, event):
        P = self.entry_phone.get()
        if P != "" and (not P.isdigit() or len(P) > 10):
            self.entry_phone.configure(border_color="red") # เปลี่ยนสีกรอบเป็นสีแดงเตือน
            self.label_title.configure(text="Error: Phone number is invalid" , text_color="red")
        else:
            self.label_title.configure(text="" , text_color="red")
            self.entry_phone.configure(border_color=["#979DA2", "#565B5E"]) # กลับเป็นสีปกติ
    
    def validate_email(self, event):   
        email = self.entry_email.get()
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if email != "" and not re.match(email_pattern, email):
            self.entry_email.configure(border_color="red") # เปลี่ยนสีกรอบเป็นสีแดงเตือน
            self.label_title.configure(text="Error: Email format is invalid" , text_color="red")
        else:
            self.label_title.configure(text="" , text_color="red")
            self.entry_email.configure(border_color=["#979DA2", "#565B5E"]) # กลับเป็นสีปกติ 
   
    def submit_booking(self):
        name = self.entry_name.get()
        gender = self.gender_var.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        booking_time = self.time_var.get()
    
         

        try :
            conn = sqlite3.connect("booking_data.db")
            cursor = conn.cursor()
            
            sql = '''INSERT INTO bookings (customer_name , gender , email , phone, status ,booking_time) 
                    VALUES (? , ? , ? , ? , ? , ?)'''
            cursor.execute(sql , (name , gender , email , phone, "Pending", booking_time))
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


    def show_data(self):
        # 1. สร้างหน้าต่างใหม่ (Toplevel Window) สำหรับโชว์ข้อมูล
        data_window = ctk.CTkToplevel(self)
        data_window.title("Booking Data")
        data_window.geometry("600x400")

        # 2. สร้าง Frame แบบเลื่อนได้ (Scrollable)
        scollable_frame = ctk.CTkScrollableFrame(data_window)
        scollable_frame.pack(fill="both", expand=True)

        # 3. ดึงข้อมูลจาก Database
        try:
            conn = sqlite3.connect("booking_data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT customer_name, phone , booking_time FROM bookings")
            rows = cursor.fetchall()

            # 4. วนลูปสร้าง Label โชว์ข้อมูลทีละแถว
            for index , row in enumerate(rows):
                info_text = f"{index + 1}. Name: {row[0]} | Phone: {row[1]} | Time: {row[2]}"
                lable = ctk.CTkLabel(scollable_frame, text=info_text , font=("Arial", 14))
                lable.pack(pady=5)

                # ปุ่มลบ (Delete)
                # เราจะส่งชื่อ (row[0]) ไปที่ฟังก์ชันลบ (หรือส่ง ID ถ้าคุณดึง ID มาด้วย)
                delete_button = ctk.CTkButton(
                    scollable_frame, 
                    text="Delete", 
                    fg_color="red", 
                    hover_color="#990000",
                    command=lambda name=row[0]: self.delete_booking(name , data_window)
                )
                delete_button.pack(pady=5)
            conn.close()
        except Exception as e:
            print("Error fetching data:", e)

    def delete_booking(self, name , data_window):
        try:
            conn = sqlite3.connect("booking_data.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE customer_name = ?", (name,))
            conn.commit()
            conn.close()
            print(f"Booking for {name} deleted successfully!")
            data_window.destroy()  # ปิดหน้าต่างข้อมูลหลังจากลบ
            self.show_data()  # รีเฟรชหน้าต่างข้อมูลหลังจากลบ
        except Exception as e:
            print("Error deleting booking:", e)

if __name__ == "__main__":
    app = BookingApp()
    app.mainloop()