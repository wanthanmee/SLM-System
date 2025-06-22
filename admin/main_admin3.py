import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# Import admin pages
from ADMIN_Home_Final import ADMIN_Home
from ADMIN_ProductApproval import ProductListPage
from ADMIN_ProductOwnerApproval import ProductOwnerApproval
from ADMIN_MailingList import ProductRegistrationUI

try:
    ADMIN_NAME = sys.argv[1]
    ADMIN_EMAIL = sys.argv[2]
except IndexError:
    ADMIN_NAME = "Unknown"
    ADMIN_EMAIL = "Unknown"

class AdminApp(ctk.CTk):
    def __init__(self, admin_name=None, admin_email=None):
        super().__init__()

        self.admin_name = admin_name
        self.admin_email = admin_email

        self.title("Shelf Life Management System - Admin")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))

        self.configure(fg_color="white")

        self.current_profile_image = None

        self.sidebar = ctk.CTkFrame(self, width=270, fg_color="#FBC3A5", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.container = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.container.pack(side="left", fill="both", expand=True)

        self.create_sidebar()
        self.create_frames()

        self.show_frame("ADMIN_Home")

    def create_default_profile_image(self):
        size = self.profile_size
        img = Image.new("RGBA", (size, size), (200, 200, 200, 255))
        draw = ImageDraw.Draw(img)
        head_radius = size // 4
        head_center = (size // 2, size // 3)
        draw.ellipse([
            (head_center[0] - head_radius, head_center[1] - head_radius),
            (head_center[0] + head_radius, head_center[1] + head_radius)
        ], fill=(255, 255, 255, 255))
        body_top = head_center[1] + head_radius
        draw.rectangle([
            (size // 4, body_top),
            (3 * size // 4, size)
        ], fill=(255, 255, 255, 255))
        self.default_profile_tk = ImageTk.PhotoImage(img)

    def create_sidebar(self):
        profile_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_container.pack(pady=(30, 20), padx=20, fill="x")

        self.profile_size = 100
        self.create_default_profile_image()

        self.profile_label = ctk.CTkLabel(profile_container, text="", image=self.default_profile_tk)
        self.profile_label.pack(pady=10)

        if self.current_profile_image and os.path.exists(self.current_profile_image):
            self.display_profile_image(self.current_profile_image)
        else:
            default_img_path = "C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/profile_icon.png"
            self.display_profile_image(default_img_path)

        welcome_text = f"Welcome, {self.admin_name}" if self.admin_name else "Welcome, Admin"
        self.welcome_label = ctk.CTkLabel(profile_container,
                                          text=welcome_text,
                                          font=("Arial", 18),
                                          text_color="black")
        self.welcome_label.pack()

        self.load_icons()

        nav_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_container.pack(pady=(20, 0), padx=15, fill="x")

        self.nav_buttons_data = [
            ("Home", self.home_icon, self.show_home),
            ("Product Approval", self.register_icon, self.show_product_approval),
            ("Product Owner Approval", self.list_icon, self.show_owner_approval),
            ("Mailbox", self.mailbox_icon, self.show_mailbox),
        ]

        self.nav_buttons = []
        for text, icon, command in self.nav_buttons_data:
            btn = ctk.CTkButton(
                nav_container,
                text=f"  {text}",
                command=command,
                anchor="w",
                width=220,
                height=50,
                corner_radius=25,
                fg_color="white" if text == "Home" else "#FBC3A5",
                text_color="black",
                hover_color="#f8b78f",
                font=("Arial", 14),
                image=icon,
                compound="left"
            )
            btn.pack(pady=5, padx=10)
            self.nav_buttons.append(btn)

        change_pic_btn = ctk.CTkButton(
            self.sidebar,
            text="📷 Change Profile Picture",
            command=self.change_profile_picture,
            fg_color="#CD853F",
            hover_color="#D2B48C",
            text_color="white",
            font=("Arial", 12),
            height=35,
            width=200
        )
        change_pic_btn.pack(side="bottom", pady=(0, 30), padx=20)

    def load_icons(self):
        try:
            base_path = "C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/"
            self.home_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE home 1.jpeg"), size=(40, 40))
            self.register_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE register.jpeg"), size=(40, 40))
            self.list_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE list.jpeg"), size=(40, 40))
            self.mailbox_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE mail.jpeg"), size=(40, 40))
        except Exception as e:
            print(f"Error loading icons: {e}")
            self.home_icon = None
            self.register_icon = None
            self.list_icon = None
            self.mailbox_icon = None

    def create_circular_image(self, image_path, size):
        try:
            img = Image.open(image_path).resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
            mask = Image.new("L", (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            circular_img = Image.new("RGBA", (size, size))
            circular_img.paste(img, (0, 0), mask=mask)
            return circular_img
        except Exception as e:
            print(f"Error creating circular image: {e}")
            return None

    def change_profile_picture(self):
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if file_path:
            try:
                circular_img = self.create_circular_image(file_path, self.profile_size)
                if circular_img:
                    self.profile_image_tk = ImageTk.PhotoImage(circular_img)
                    self.profile_label.configure(image=self.profile_image_tk)
                    self.profile_label.image = self.profile_image_tk
                    self.current_profile_image = file_path
                messagebox.showinfo("Success", "Profile picture updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def display_profile_image(self, image_path):
        if os.path.exists(image_path):
            circular_img = self.create_circular_image(image_path, self.profile_size)
            if circular_img:
                self.profile_image_tk = ImageTk.PhotoImage(circular_img)
                self.profile_label.configure(image=self.profile_image_tk)
                self.profile_label.image = self.profile_image_tk
        else:
            self.profile_label.configure(image=self.default_profile_tk)
            self.profile_label.image = self.default_profile_tk

    def create_frames(self):
        self.frames = {}

        pages = {
            "ADMIN_Home": ADMIN_Home,
            "ProductApprovalPage": ProductListPage,
            "ProductOwnerApprovalPage": ProductOwnerApproval,
            "AdminMailboxPage": ProductRegistrationUI
        }

        for page_name, PageClass in pages.items():
            frame = PageClass(self.container, controller=self)
            self.frames[page_name] = frame
            frame.pack_forget()

    def show_frame(self, page_name):
        for name, frame in self.frames.items():
            if name == page_name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

        highlight_map = {
            "ADMIN_Home": "Home",
            "ProductApprovalPage": "Product Approval",
            "ProductOwnerApprovalPage": "Product Owner Approval",
            "AdminMailboxPage": "Mailbox"
        }

        selected_label = highlight_map.get(page_name)

        for i, (text, icon, command) in enumerate(self.nav_buttons_data):
            if text == selected_label:
                self.nav_buttons[i].configure(fg_color="white", text_color="black")
            else:
                self.nav_buttons[i].configure(fg_color="#FBC3A5", text_color="black")

    def show_home(self):
        self.show_frame("ADMIN_Home")

    def show_product_approval(self):
        self.show_frame("ProductApprovalPage")

    def show_owner_approval(self):
        self.show_frame("ProductOwnerApprovalPage")

    def show_mailbox(self):
        self.show_frame("AdminMailboxPage")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = AdminApp(ADMIN_NAME, ADMIN_EMAIL)
    app.mainloop()
