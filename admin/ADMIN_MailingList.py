import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ProductDetailsWindow:
    def __init__(self, parent, product_data):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Product Details")
        self.window.geometry("600x400")
        self.product_data = product_data

        frame = ctk.CTkFrame(self.window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Product Information", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        for label_text, value in [
            ("Product Name:", product_data['product_name']),
            ("Product Code / ID:", product_data['batch_id']),
            ("Description:", product_data['description']),
            ("Testing Date:", product_data['testing_date'])
        ]:
            row = ctk.CTkFrame(frame)
            row.pack(anchor="w", fill="x", pady=5)
            ctk.CTkLabel(row, text=label_text, width=180, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=str(value), anchor="w").pack(side="left")

        ctk.CTkButton(frame, text="Send Reminder Email", command=self.send_reminder_email).pack(pady=20)

    def get_owner_email(self, product_id):
        try:
            conn = sqlite3.connect('ProductRegistration.db')
            cursor = conn.cursor()

            cursor.execute("SELECT owner_id FROM products WHERE id = ?", (product_id,))
            result = cursor.fetchone()

            if result:
                owner_id = result[0]

                cursor.execute("SELECT email FROM product_owners WHERE owner_id = ?", (owner_id,))
                email_result = cursor.fetchone()

                conn.close()
                return (email_result[0], None) if email_result and email_result[0] else (None, None)

            conn.close()
            return None, None

        except Exception as e:
            print(f"Error fetching owner email: {e}")
            return None, None

    def send_reminder_email(self):
        owner_email, _ = self.get_owner_email(self.product_data['id'])

        if not owner_email:
            messagebox.showerror("Error", "Could not find email address for this product.")
            return

        sender_email = "kelvankiew7@gmail.com"
        sender_password = "sztz tbsq rchn gagb"  # App password
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = owner_email
        msg['Subject'] = f"⏰ Reminder: Please Test Your Product Barcode Before {self.product_data['testing_date']}"

        # FULL EMAIL BODY (as requested)
        body = f"""
Dear Product Owner,

This is a friendly reminder that the testing date for your product {self.product_data['product_name']} is scheduled for {self.product_data['testing_date']}.

To avoid any delays or complications during the testing process, please ensure that the barcode for your product is tested and verified before the scheduled date.

Product Name: {self.product_data['product_name']}
Product Code / ID: {self.product_data['batch_id']}
Scheduled Test Date: {self.product_data['testing_date']}

If you have already completed the barcode testing, please disregard this message.

For any assistance or questions, feel free to contact the Quality Assurance team at joelvincent@gmail.com

Thank you for your cooperation.

Best regards,
Shelf With Me Co
SHELF ME
+60122345678
        """

        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            messagebox.showinfo("Success", f"Reminder email sent to {owner_email}")
        except Exception as e:
            messagebox.showerror("Email Error", str(e))


class ProductRegistrationUI(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Product Testing Reminder", font=("Arial", 18, "bold"))
        label.pack(pady=10)

        # Use standard Treeview (no visual conflict with CTkFrame)
        self.tree = ttk.Treeview(self, columns=("ID", "Batch ID", "Product Name", "Description", "Testing Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.show_product_details)

        self.load_data()

    def show_product_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        values = self.tree.item(selected_item[0])['values']
        product_data = {
            'id': values[0],
            'batch_id': values[1],
            'product_name': values[2],
            'description': values[3],
            'testing_date': values[4]
        }
        ProductDetailsWindow(self, product_data)

    def load_data(self):
        try:
            conn = sqlite3.connect('ProductRegistration.db')
            cursor = conn.cursor()

            target_date = (datetime.now() + relativedelta(months=2)).strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT id, batch_id, product_name, description, testing_date 
                FROM products
                WHERE DATE(testing_date) = DATE(?)
                ORDER BY testing_date ASC
            """, (target_date,))

            self.tree.delete(*self.tree.get_children())
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

            conn.close()
        except Exception as e:
            print(f"Database load error: {e}")
