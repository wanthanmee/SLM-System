import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys 

# Import your existing modules
from PO_Home_Final import PO_Home
from PO_ProductRegister_Final import ProductRegistration
from PO_ProductList_Final import ProductListPage

try:
    PO_NAME = sys.argv[1]
    PO_EMAIL = sys.argv[2]
    PO_ID = sys.argv[3]
except IndexError:
    PO_NAME = "Unknown"
    PO_EMAIL = "Unknown"
    PO_ID = "Unknown"

class App(ctk.CTk):
    '''
    =====================================================================================================
    Constructor: def __init__(self)
    Description: 
    This function initializes the main application window for the Shelf Life Management System.
    It sets the title, geometry, and main layout with a sidebar and content area.
    =====================================================================================================
    '''    
    def __init__(self, owner_name = None, owner_email= None, owner_id = None):
        super().__init__()
        
        self.owner_name = owner_name
        self.owner_email = owner_email
        self.owner_id = owner_id

        self.title("Shelf Life Management System - Product Owner")
        #self.geometry("1920x1080")
        self.attributes("-fullscreen", True)  # ← ✅ Make it full screen
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))  # Optional: ESC to exit fullscreen

        self.configure(fg_color="white")

        # Store current profile image path
        self.current_profile_image = None

        # Create main layout using pack for both sidebar and content area.
        # Sidebar (left) and Container (content area, right)
        self.sidebar = ctk.CTkFrame(self, width=270, fg_color="#FBC3A5", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        # Prevent the sidebar from resizing its contents automatically
        self.sidebar.pack_propagate(False)

        self.container = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.container.pack(side="left", fill="both", expand=True)

        self.create_sidebar()
        self.create_frames()

        # Show home page by default
        self.show_frame("PO_Home")

        print(type(self))


    def create_default_profile_image(self):
        """Create a default profile image with a basic avatar design"""
        size = self.profile_size  # Ensure this is set before this function is called
        img = Image.new("RGBA", (size, size), (200, 200, 200, 255))  # Background

        draw = ImageDraw.Draw(img)
        
        # Draw circular head
        head_radius = size // 4
        head_center = (size // 2, size // 3)
        draw.ellipse([
            (head_center[0] - head_radius, head_center[1] - head_radius),
            (head_center[0] + head_radius, head_center[1] + head_radius)
        ], fill=(255, 255, 255, 255))  # white

        # Draw simple body
        body_top = head_center[1] + head_radius
        draw.rectangle([
            (size // 4, body_top),
            (3 * size // 4, size)
        ], fill=(255, 255, 255, 255))

        # Convert to ImageTk.PhotoImage
        self.default_profile_tk = ImageTk.PhotoImage(img)
    '''
    =====================================================================================================
    Function: def create_sidebar(self)
    Description: 
    This function creates the sidebar for the application, including a profile section,
    navigation buttons, and a profile picture change option.
    =====================================================================================================
    '''   
    def create_sidebar(self):
        # Profile section container within the sidebar
        profile_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_container.pack(pady=(30, 20), padx=20, fill="x")

        # Profile picture setup
        self.profile_size = 100
        self.create_default_profile_image()
        
        # Create profile label *after* image exists
        self.profile_label = ctk.CTkLabel(profile_container, text="", image=self.default_profile_tk)
        self.profile_label.pack(pady=10)

        if self.current_profile_image and os.path.exists(self.current_profile_image):
            self.display_profile_image(self.current_profile_image)
        else:
            default_img_path = "C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/profile_icon.png"
            self.display_profile_image(default_img_path)

        # Dynamic Welcome text with Product Owner's name
        welcome_text = f"Welcome, {self.owner_name}" if self.owner_name else "Welcome, Name"
        self.welcome_label = ctk.CTkLabel(profile_container, 
                                        text=f"Welcome, {PO_NAME}", 
                                        font=("Arial", 18), 
                                        text_color="black")
        self.welcome_label.pack()

        # Load icons from specified paths
        self.load_icons()

        # Navigation menu container
        nav_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_container.pack(pady=(20, 0), padx=15, fill="x")

        # Define navigation button data
        self.nav_buttons_data = [
            ("Home", self.home_icon, self.show_home),
            ("Product Registration", self.register_icon, self.show_register),
            ("Product List", self.list_icon, self.show_list),
        ]

        self.nav_buttons = []
        # Create and pack each navigation button
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

        # Profile picture change button at the bottom of the sidebar
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
        # Pack it at the bottom with padding
        change_pic_btn.pack(side="bottom", pady=(0, 30), padx=20)
    '''
    =====================================================================================================
    Function: def load_icons(self)
    Description: 
    This function loads navigation icons from specified paths and handles errors if files are not found.
    It sets the icons to None if loading fails, preventing application crashes.
    =====================================================================================================
    '''
    def load_icons(self):
        """Load navigation icons from your specified paths"""
        try:
            base_path = "C:/Users/user/PycharmProjects/Semster 5/Software Engineering/Dashboard Icons/"
            self.home_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE home 1.jpeg"), size=(40, 40))
            self.register_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE register.jpeg"), size=(40, 40))
            self.list_icon = ctk.CTkImage(light_image=Image.open(f"{base_path}SE list.jpeg"), size=(40, 40))

        except Exception as e:
            print(f"Error loading icons: {e}")
            # Fallback to None if files are not found
            self.home_icon = None
            self.register_icon = None
            self.list_icon = None

    '''
    =====================================================================================================
    Function: def create_circular_image(self, image_path, size)
    Description: 
    This function creates a circular image from a given image path and size.
    It uses PIL to open the image, resize it, and apply a circular mask.
    =====================================================================================================
    '''
    def create_circular_image(self, image_path, size):
        """Create circular image for profile display"""
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
    '''
    =====================================================================================================
    Function: def change_profile_picture(self)
    Description: 
    This function allows the user to change their profile picture.
    It opens a file dialog to select an image, creates a circular version of the image,
    and updates the profile label with the new image.
    =====================================================================================================
    '''
    def change_profile_picture(self):
        """Allow user to change profile picture"""
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                circular_img = self.create_circular_image(file_path, self.profile_size)
                if circular_img:
                    # Store reference to prevent garbage collection
                    self.profile_image_tk = ImageTk.PhotoImage(circular_img)
                    self.profile_label.configure(image=self.profile_image_tk)
                    self.profile_label.image = self.profile_image_tk  # Optional but still helpful
                    self.current_profile_image = file_path  # optional: store current path
                messagebox.showinfo("Success", "Profile picture updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    '''
    =====================================================================================================
    Function: def display_profile_image(self, image_path)
    Description: 
    This function displays the profile image in a circular format.
    If the image does not exist, it creates a default profile image.
    =====================================================================================================
    '''
    def display_profile_image(self, image_path):
        """Display profile image in circular format"""
        if os.path.exists(image_path):
            circular_img = self.create_circular_image(image_path, self.profile_size)
            if circular_img:
                self.profile_image_tk = ImageTk.PhotoImage(circular_img)
                self.profile_label.configure(image=self.profile_image_tk)
                self.profile_label.image = self.profile_image_tk
        else:
            self.create_default_profile_image()
            if hasattr(self, 'default_profile_tk'):
                self.profile_label.configure(image=self.default_profile_tk)
                self.profile_label.image = self.default_profile_tk

    '''
    =====================================================================================================
    Function: def display_profile_image(self, image_path)
    Description:
    This function displays the profile image in a circular format.
    If the image does not exist, it uses a default profile image created by create_default_profile_image.
    =====================================================================================================
    '''  
    def display_profile_image(self, image_path):
        """Display profile image in circular format"""
        if os.path.exists(image_path):
            circular_img = self.create_circular_image(image_path, self.profile_size)
            if circular_img:
                self.profile_image_tk = ImageTk.PhotoImage(circular_img)
                self.profile_label.configure(image=self.profile_image_tk)
                self.profile_label.image = self.profile_image_tk
        else:
            # Use default image if the path doesn't exist
            self.profile_label.configure(image=self.default_profile_tk)
            self.profile_label.image = self.default_profile_tk

    '''
    =====================================================================================================
    Function: def create_circular_image_from_pil(self, img, size)
    Description: 
    This function creates a circular image from a PIL image.
    It uses a mask to draw an ellipse and paste the image onto a new circular canvas.
    =====================================================================================================
    '''
    def create_circular_image_from_pil(self, img, size):
        """Create circular image from a PIL image"""
        try:
            mask = Image.new("L", (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            circular_img = Image.new("RGBA", (size, size))
            circular_img.paste(img, (0, 0), mask=mask)
            return circular_img
        except Exception as e:
            print(f"Error creating circular image from PIL: {e}")
            return None
    '''
    =====================================================================================================
    Function: def open_profile_page(self)
    Description: 
    This function opens a profile settings popup when the profile image is clicked.
    It allows the user to view and change their profile name and picture.
    =====================================================================================================
    '''
    def open_profile_page(self):
        """Open profile page popup when profile image is clicked"""
        profile_window = ctk.CTkToplevel(self)
        profile_window.title("Profile Settings")
        profile_window.geometry("400x300")
        profile_window.configure(fg_color="white")
        
        profile_window.transient(self)
        profile_window.grab_set()
        
        title_label = ctk.CTkLabel(profile_window, text="Profile Settings", font=("Arial", 20), text_color="#8B4513")
        title_label.pack(pady=20)
        
        if hasattr(self, 'profile_label') and hasattr(self.profile_label, 'image'):
            current_img = getattr(self.profile_label, 'image', None)
            if current_img:
                profile_display = tk.Label(profile_window, image=current_img, bg="white")
                profile_display.pack(pady=10)
        
        name_frame = ctk.CTkFrame(profile_window, fg_color="transparent")
        name_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(name_frame, text="Name:", font=("Arial", 14)).pack(anchor="w")
        name_entry = ctk.CTkEntry(name_frame, placeholder_text="Enter your name", width=300)
        name_entry.pack(pady=5)
        name_entry.insert(0, "Name")
        
        button_frame = ctk.CTkFrame(profile_window, fg_color="transparent")
        button_frame.pack(pady=20)
        '''
        =====================================================================================================
        Function: def save_profile(self)
        Description: 
        This function saves the profile changes made by the user.
        It updates the welcome label with the new name and shows a success message.
        If the name is empty, it shows a warning message.
        =====================================================================================================
        '''
        def save_profile():
            new_name = name_entry.get().strip()
            if new_name:
                self.welcome_label.configure(text=f"Welcome, {new_name}")
                messagebox.showinfo("Success", "Profile updated successfully!")
                profile_window.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter a valid name!")
        
        save_btn = ctk.CTkButton(button_frame, text="Save Changes", command=save_profile,
                                 fg_color="#8B4513", hover_color="#A0522D")
        save_btn.pack(side="left", padx=10)
        
        change_pic_btn = ctk.CTkButton(
            button_frame,
            text="Change Picture",
            command=lambda: [self.change_profile_picture(), profile_window.focus()],
            fg_color="#CD853F",
            hover_color="#D2B48C"
        )
        change_pic_btn.pack(side="right", padx=10)
    '''
    =====================================================================================================
    Function: def create_frames(self)
    Description: 
    This function creates the frames for different pages in the application.
    It initializes each frame, packs it into the container, and hides all frames initially.
    =====================================================================================================
    '''
    def create_frames(self):

        self.frames = {}
        
        for F in (PO_Home, ProductRegistration, ProductListPage):
            page_name = F.__name__

            # Pass owner_id to all frames
            frame = F(parent=self.container, controller=self, owner_id=self.owner_id)

            frame.pack(fill="both", expand=True)
            frame.pack_forget()
            self.frames[page_name] = frame

    '''
    =====================================================================================================
    Function: def show_frame(self, page_name)
    Description: 
    This function shows the selected frame based on the page name.
    It hides all other frames and updates the navigation button states to reflect the active page.
    =====================================================================================================
    '''
    def show_frame(self, page_name):
        """Show the selected frame and update navigation button states."""
        # Hide all frames first
        for frame in self.frames.values():
            frame.pack_forget()
        # Then pack the chosen frame to display it
        self.frames[page_name].pack(fill="both", expand=True)
        
        # Update button colors for active state
        for i, (text, icon, command) in enumerate(self.nav_buttons_data):
            if (page_name == "PO_Home" and text == "Home") or \
               (page_name == "ProductRegistration" and text == "Product Registration") or \
               (page_name == "ProductListPage" and text == "Product List"):
                self.nav_buttons[i].configure(fg_color="white", text_color="black")
            else:
                self.nav_buttons[i].configure(fg_color="#FBC3A5", text_color="black")

    def show_home(self):
        self.show_frame("PO_Home")

    def show_register(self):
        self.show_frame("ProductRegistration")

    def show_list(self):
        self.show_frame("ProductListPage")




if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = App(PO_NAME, PO_EMAIL, PO_ID)
    app.attributes("-fullscreen", True)  # Make it full screen

    app.mainloop()
