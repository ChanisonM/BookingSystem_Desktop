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

        self.button_submit = ctk.CTkButton(self, text="Save", command=self.submit_booking)
        self.button_submit.pack(pady=20)


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
    
        if name == "" or email == "" or phone == "":
            self.label_title.configure(text="Error: Please fill in all fields" , text_color="red")
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