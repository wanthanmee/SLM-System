import customtkinter as ctk
import subprocess
import sys
import sqlite3
from tkinter import messagebox
from login_db import hash_password, create_database

class AdminLoginPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        self.configure(fg_color="white")

        # Get screen width for layout
        screen_width = self.winfo_screenwidth()
        white_width = int(screen_width * 0.50)

        # Left white frame (50%)
        left_frame = ctk.CTkFrame(self, width=white_width, fg_color="#FCF9F9")
        left_frame.pack(side="left", fill="both")

        # Right gray frame (50%)
        right_frame = ctk.CTkFrame(self, fg_color="#EAEAF4")
        right_frame.pack(side="right", fill="both", expand=True)

        # Centered login box inside left_frame
        center_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome text
        ctk.CTkLabel(center_frame, text="Welcome!", font=("Arial", 28, "bold"), text_color="black").pack(pady=(0, 10))
        ctk.CTkLabel(center_frame, text="Please log in to access the system", font=("Arial", 16), text_color="gray").pack(pady=(0, 30))

        # Username entry
        self.username_entry = ctk.CTkEntry(center_frame, placeholder_text="Username", width=400, height=40, corner_radius=10)
        self.username_entry.pack(pady=10)

        # Password entry
        self.password_entry = ctk.CTkEntry(center_frame, placeholder_text="Password", show="*", width=400, height=40, corner_radius=10)
        self.password_entry.pack(pady=10)

        # Login button
        ctk.CTkButton(
            center_frame,
            text="LOGIN",
            width=400,
            height=40,
            corner_radius=10,
            fg_color="#654633",
            hover_color="#503524",
            text_color="white",
            command=self.login
        ).pack(pady=30)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('ProductRegistration.db')
        cursor = conn.cursor()

        hashed_pw = hash_password(password)
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, hashed_pw))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo(title="Login Successful", message="Welcome Admin.")
            admin_name, admin_email = result[1], result[2]

            subprocess.Popen([
                sys.executable,
                "admin/main_admin3.py",
                admin_name,
                admin_email
            ])

            self.parent.destroy()
        else:
            messagebox.showerror(title="Login Unsuccessful", message="Username or Password incorrect.")

# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    create_database()

    app = ctk.CTk()
    app.title("Shelf Life Management System - Admin Login")
    app.geometry("1200x800")
    app.attributes("-fullscreen", True)

    login_page = AdminLoginPage(app)
    login_page.pack(fill="both", expand=True)

    app.mainloop()