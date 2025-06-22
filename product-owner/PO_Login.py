from customtkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from datetime import datetime
import subprocess
import sys
import sqlite3

'''
=====================================================================================================
Function: def setup_database()
Description: 
This function sets up the SQLite database for the user and product owners.
It creates a database connection and cursor,
creates the necessary tables if they don't exist,
and inserts a default admin user if it doesn't exist.
=====================================================================================================
'''

def alter_product_owners_table():
    conn = sqlite3.connect('ProductRegistration.db')
    cursor = conn.cursor()

    try:
        # Add new columns if they don't already exist
        cursor.execute("ALTER TABLE product_owners ADD COLUMN status TEXT DEFAULT 'Pending'")
        cursor.execute("ALTER TABLE product_owners ADD COLUMN registered_at TEXT")
        conn.commit()
        print("Table altered successfully.")

    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e):
            print("Columns already exist.")
        else:
            print(f"Error altering table: {e}")
    
    finally:
        cursor.close()
        conn.close()
        
#=== Page Class: Login ===
class LoginPage(CTkFrame):
    '''
    =====================================================================================================
    Constructor: def __init__(self, parent, controller)
    Description: 
    This function initializes the LoginPage class.
    It sets up the UI elements and initializes variables for user input.
    =====================================================================================================
    '''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(width=1920, height=1080)
        self.place(x=0, y=0)
        
        # Initialize variables
        self.user_email = tk.StringVar() 
        self.user_password = tk.StringVar() 
        self.owner_email = tk.StringVar() 
        self.owner_name = tk.StringVar()
        
        # Initialize slides list and current_slide
        self.slides = []
        self.current_slide = 0
        
        self.build_ui()
        '''
    =====================================================================================================
    Function: def login(self)
    Description: 
    This function handles the Login process. 
    It retrieves the shared email and password from the entry fields,
    checks them against the database, and shows the product owner form if successful.
    =====================================================================================================
    '''
    def login(self):
        email = self.user_email.get()
        password = self.user_password.get()

        conn = sqlite3.connect('ProductRegistration.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password))
        result = cursor.fetchone()

        if result:
            self.show_productOwner()  # Switch to next page here
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

        cursor.close()
        conn.close()
    '''
    =====================================================================================================
    Function: def productOwner(self)
    Description: 
    This function handles the Product Owner registration process.
    It retrieves the personal email and name from the entry fields,
    checks if the email already exists in the database,
    and registers the new user if it doesn't.
    =====================================================================================================
    '''
    def productOwner(self):
        # Get the email and name from the entry fields
        p_email = self.owner_email.get().strip()
        name = self.owner_name.get().strip()

        # Validate input
        if not p_email or not name:
            messagebox.showerror("Input Error", "Both email and name are required.")
            return

        # Connect to the database
        conn = sqlite3.connect('ProductRegistration.db')
        cursor = conn.cursor()

        try:
            # Check if the email already exists
            cursor.execute("SELECT owner_id, name, email, status FROM product_owners WHERE email=?", (p_email,))
            result = cursor.fetchone()

            if result:
                owner_id, owner_name, owner_email, status = result

                if status == "Approved":
                    messagebox.showinfo("Login Successful", f"Welcome back, {owner_name}!")
                    subprocess.Popen([
                        sys.executable,
                        "product-owner/main_test3.py",
                        owner_name,
                        owner_email,
                        str(owner_id)
                    ])
                    self.master.destroy()

                elif status == "Pending":
                    messagebox.showwarning("Approval Pending", "Your registration is still pending admin approval.")
                elif status == "Denied":
                    messagebox.showerror("Access Denied", "Your registration has been denied by the admin.")
                else:
                    messagebox.showerror("Unknown Status", f"Your account has an unknown status: {status}")

            else:
                # Register new user
                registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status = 'Pending'

                cursor.execute('''
                    INSERT INTO product_owners (email, name, status, registered_at)
                    VALUES (?, ?, ?, ?)
                ''', (p_email, name, status, registered_at))
                conn.commit()

                messagebox.showinfo(
                    "Registration Successful",
                    "You have been registered successfully!\nPlease wait for admin approval before logging in."
                )

        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate Error", "This email is already registered.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    def show_login(self):
        # Hide the product owner form and show the login form
        self.slides[0].place(x=0, y=0)
        self.slides[1].place_forget()
        self.current_slide = 0

    def show_productOwner(self):
        # Hide the login form and show the product owner form
        self.slides[1].place(x=0, y=0)
        self.slides[0].place_forget()
        self.current_slide = 1

    def show_slide(self, index):
        self.slides[self.current_slide].place_forget()
        self.slides[index].place(x=0, y=0)
        self.current_slide = index
    '''
    =====================================================================================================
    Function: def build_ui(self)
    Description: 
    This function builds the UI for the LoginPage.
    It creates the layout, sets up the background image,
    and initializes the fonts and UI elements.
    =====================================================================================================
    '''
    def build_ui(self):
        # Define screen dimensions
        screen_height = 1080

        # Set the appearance mode and default color theme
        set_appearance_mode("light")
        set_default_color_theme("blue")

        # Frame widths
        left_frame_width = 800
        right_frame_width = 1120  # 1920 - 800 = 1120

        # Create right and left frames (image on left)
        right_frame = CTkFrame(self, width=right_frame_width, height=screen_height, fg_color="white")
        right_frame.place(x=0, y=0)

        left_frame = CTkFrame(self, width=left_frame_width, height=screen_height)
        left_frame.place(x=right_frame_width, y=0)

        # Load and set background image on the left frame
        def set_background_image(frame, image_path, width, height):
            try:
                image = Image.open(image_path)
                image = image.resize((width, height), Image.LANCZOS)
                bg_image = ImageTk.PhotoImage(image)

                label = tk.Label(frame, image=bg_image)
                label.image = bg_image  # Prevent garbage collection
                label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Error loading image: {e}")

        # Set background image
        set_background_image(left_frame, r"C:\Users\user\PycharmProjects\Semster 5\Software Engineering\Background\login_bg.jpg", left_frame_width, screen_height)

        # Fonts
        font_header = ("Arial", 56, "bold")
        font_label = ("Arial", 16)
        font_input = ("Arial", 20)
        font_button = ("Arial", 28)
        font_subheader = ("Arial", 28)

        # Create slides
        self.slides = [CTkFrame(right_frame, width=right_frame_width, height=screen_height, fg_color="white") for _ in range(2)]

        # === Slide 0: Login View ===
        login_label = CTkLabel(self.slides[0], text="Login", font=font_header, text_color="#000000", fg_color="white")
        login_label.place(x=150, y=200)

        # === Slide 0: Email and Passcode
        email_label = CTkLabel(self.slides[0], text="Email", font=font_label, text_color="#666666", fg_color="white")
        email_label.place(x=150, y=380)

        email_entry = CTkEntry(self.slides[0], width=800, height=60, font=font_input, corner_radius=20,
                            border_color="#CCCCCC", fg_color="white", text_color="#000000", textvariable=self.user_email)
        email_entry.place(x=150, y=420)

        passcode_label = CTkLabel(self.slides[0], text="Password", font=font_label, text_color="#666666", fg_color="white")
        passcode_label.place(x=150, y=500)

        passcode_entry = CTkEntry(self.slides[0], width=800, height=60, font=font_input, corner_radius=20,
                                border_color="#CCCCCC", fg_color="white", text_color="#555555", show="*", textvariable=self.user_password)
        passcode_entry.insert(0, "1234")
        passcode_entry.place(x=150, y=550)

        # LOGIN Button (inside the same slide)
        login_button = CTkButton(self.slides[0], text="LOGIN", font=font_button, text_color="#F8E5E5",
                                fg_color="#654633", hover_color="#c89ef2", corner_radius=20,
                                width=800, height=70, command=self.login)
        login_button.place(x=150, y=650)

        # Welcome labels (outside slide, top-level frame)
        signup_header = CTkLabel(self.slides[0], text="Welcome!", font=font_header, text_color="#000000", fg_color="white")
        signup_header.place(x=150, y=200)

        welcome_label = CTkLabel(
            self.slides[0],
            text="Please log in to access the system",
            font=font_subheader,
            text_color="grey",
            fg_color="white",
            wraplength=800,
            justify="left"
        )
        welcome_label.place(x=150, y=290)

        # === Slide 1: Product Owner View ===
        product_owner_label = CTkLabel(self.slides[1], text="Product Owner", font=font_header, text_color="#000000", fg_color="white")
        product_owner_label.place(x=150, y=200)

        back_button = CTkButton(self.slides[1], text="Back to Login", font=font_button,
                                text_color="white", fg_color="#888888", hover_color="#666666",
                                corner_radius=20, width=300, height=50, command=self.show_login)
        back_button.place(x=150, y=650)

        submit_button = CTkButton(self.slides[1], text="Submit", font=font_button,
                                text_color="white", fg_color="#654633", hover_color="#c89ef2",
                                corner_radius=20, width=300, height=50, command=self.productOwner)
        submit_button.place(x=500, y=650)

        # === Slide 1: Personal Email and Name ===
        p_email_label = CTkLabel(self.slides[1], text="Email", font=font_label, text_color="#666666", fg_color="white")
        p_email_label.place(x=150, y=380)
        p_email_entry = CTkEntry(self.slides[1], width=800, height=60, font=font_input, corner_radius=20,
                                border_color="#CCCCCC", fg_color="white", text_color="#000000", textvariable=self.owner_email)
        p_email_entry.place(x=150, y=420)

        name_label = CTkLabel(self.slides[1], text="Name", font=font_label, text_color="#666666", fg_color="white")
        name_label.place(x=150, y=500)
        name_entry = CTkEntry(self.slides[1], width=800, height=60, font=font_input, corner_radius=20,
                            border_color="#CCCCCC", fg_color="white", text_color="#000000", textvariable=self.owner_name)
        name_entry.place(x=150, y=550)
        
        # Show the first slide
        self.show_slide(0)

#Run the application frame in main window 
if __name__ == "__main__":
    app = CTk()  # Create the root window
    app.geometry("1200x800")  # Set desired size
    app.title("Shelf Life Management System - Login")
    app.attributes("-fullscreen", True)  # Make it full screen

    # Create and pack the frame into the window
    product_page = LoginPage(app, None)
    product_page.pack(fill="both", expand=True)

    app.mainloop()  # Start the main loop
