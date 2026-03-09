import customtkinter as ctk 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BookingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Booking App")
        self.geometry("600x400")

        # Create a label
        self.label = ctk.CTkLabel(self, text="Welcome to the Booking App!", font=("Arial", 24))
        self.label.pack(pady=40) 

        # Create a button
        self.button = ctk.CTkButton(self, text="Start Project", command=self.button_callback)
        self.button.pack(pady=20)

    def button_callback(self):
        self.label.configure(text="Button Clicked!")

        
if __name__ == "__main__":
    app = BookingApp()
    app.mainloop()