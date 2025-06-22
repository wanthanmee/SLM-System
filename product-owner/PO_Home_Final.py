import customtkinter as ctk
import sqlite3

class PO_Home(ctk.CTkFrame):
    '''
    =====================================================================================================
    Function: def __init__(self, parent, controller=None)
    Description: 
    This function initializes the PO_Home frame, which is a subclass of CTkFrame
    It sets up the frame to fill the parent window and configures its appearance.
    It creates a title label and three statistic boxes to display quick stats.
    =====================================================================================================
    '''
    def __init__(self, parent, controller=None,  owner_id=None):
        super().__init__(parent)
        self.controller = controller
        self.owner_id = owner_id

        self.configure(fg_color="white")

        # Title
        title = ctk.CTkLabel(self, text="QUICK STATS", font=("Arial", 24, "bold"), text_color="#4A2C14")
        title.pack(pady=(20, 10))

        # Stats grid
        stats_frame = ctk.CTkFrame(self, fg_color="white")
        stats_frame.pack(pady=20)

        self.registered_box = self.create_stat_box(stats_frame, "Products Registered", "0", "#FCE5E5")
        self.pending_box = self.create_stat_box(stats_frame, "Products Pending Approval", "0", "#F1F0FB")
        self.approved_box = self.create_stat_box(stats_frame, "Products Approved", "0", "#FCE5E5")

        self.registered_box.grid(row=0, column=0, padx=10, pady=10)
        self.pending_box.grid(row=0, column=1, padx=10, pady=10)
        self.approved_box.grid(row=0, column=2, padx=10, pady=10)

        refresh_button = ctk.CTkButton(self, text="Refresh Stats", command=self.update_stats)
        refresh_button.pack(pady=10)

        self.update_stats()
    '''
    =====================================================================================================
    Function: def create_stat_box(self, parent, title, value, color):
    Description: 
    This function creates a statistic box with a title, value, and background color.
    It returns the created box.
    =====================================================================================================
    '''
    def create_stat_box(self, parent, title, value, color):
        box = ctk.CTkFrame(parent, width=200, height=120, fg_color=color, corner_radius=15)
        box.grid_propagate(False)

        label_title = ctk.CTkLabel(box, text=title, font=("Arial", 14, "bold"), text_color="#4A2C14")
        label_title.pack(pady=(15, 5))

        label_value = ctk.CTkLabel(box, text=value, font=("Arial", 24, "bold"), text_color="#4A2C14")
        label_value.pack()

        box.value_label = label_value
        return box
    
    def fetch_stats_from_db(self):
        print(self.owner_id)

        if not self.owner_id:
            return 0, 0, 0

        try:
            conn = sqlite3.connect("ProductRegistration.db")
            cursor = conn.cursor()

            # Filter by owner_id
            cursor.execute("SELECT COUNT(*) FROM products WHERE owner_id = ?", (self.owner_id,))
            registered = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM products WHERE owner_id = ? AND status = 'Pending'", (self.owner_id,))
            pending = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM products WHERE owner_id = ? AND status = 'Approved'", (self.owner_id,))
            approved = cursor.fetchone()[0]

            conn.close()
            return registered, pending, approved

        except sqlite3.Error as e:
            print("Database error:", e)
            return 0, 0, 0

    def update_stats(self):
        registered, pending, approved = self.fetch_stats_from_db()
        self.registered_box.value_label.configure(text=str(registered))
        self.pending_box.value_label.configure(text=str(pending))
        self.approved_box.value_label.configure(text=str(approved))


# Standalone mode
if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Optional
    root = ctk.CTk()
    root.title("Home")
    root.geometry("1200x800")

    frame = PO_Home(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()
