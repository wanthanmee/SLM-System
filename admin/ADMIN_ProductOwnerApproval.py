import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import customtkinter as ctk
from datetime import datetime

class ProductOwnerApproval(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.DB_NAME = "ProductRegistration.db"
        self.selected_owners = set()

        self.build_ui()
        self.display_owners()
        self.display_audit_log()

    def build_ui(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(header_frame, text="PRODUCT OWNER APPROVAL DASHBOARD", font=("Arial", 24, "bold"), text_color="#2E4053").pack(side="left")

        self.delete_btn = ctk.CTkButton(header_frame, text="Delete Selected", fg_color="#E74C3C", width=120, state="disabled", command=self.delete_selected)
        self.delete_btn.pack(side="right", padx=5)

        # Filter
        filter_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        filter_frame.pack(fill="x", pady=(0, 10))

        self.date_label = ctk.CTkLabel(filter_frame, text=f"Current Date: {datetime.now().strftime('%Y-%m-%d')}", font=("Arial", 12))
        self.date_label.pack(side="left", padx=10)

        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Search by name...", textvariable=self.search_var, width=300)
        search_entry.pack(side="left", padx=10)

        self.filter_var = tk.StringVar(value="All")
        status_filter = ctk.CTkComboBox(filter_frame, variable=self.filter_var, values=["All", "Pending", "Approved", "Denied"], width=150)
        status_filter.pack(side="left", padx=10)

        self.from_date_var = tk.StringVar()
        self.to_date_var = tk.StringVar()

        from_entry = DateEntry(filter_frame, date_pattern='y-mm-dd', textvariable=self.from_date_var)
        from_entry.pack(side="left", padx=5)

        to_entry = DateEntry(filter_frame, date_pattern='y-mm-dd', textvariable=self.to_date_var)
        to_entry.pack(side="left", padx=5)

        ctk.CTkButton(filter_frame, text="Clear Dates", command=lambda: [self.from_date_var.set(""), self.to_date_var.set(""), self.display_owners()]).pack(side="left", padx=10)
        ctk.CTkButton(filter_frame, text="Refresh", command=self.display_owners).pack(side="left", padx=10)

        self.search_var.trace_add("write", lambda *args: self.display_owners())
        self.filter_var.trace_add("write", lambda *args: self.display_owners())
        self.from_date_var.trace_add("write", lambda *args: self.display_owners())
        self.to_date_var.trace_add("write", lambda *args: self.display_owners())

        # Content
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(expand=True, fill="both")

        self.owners_scrollable_frame = self._create_scrollable_panel(content_frame, side="left", label="PRODUCT OWNERS")
        self.audit_scrollable_frame = self._create_scrollable_panel(content_frame, side="right", label="DELETION AUDIT LOG", width=400)

    def _create_scrollable_panel(self, parent, side, label, width=None):
        kwargs = {}
        if width is not None:
            kwargs["width"] = width

        panel = ctk.CTkFrame(parent, **kwargs)
        
        panel.pack(side=side, fill="both", expand=True, padx=10)

        ctk.CTkLabel(panel, text=label, font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))

        canvas = tk.Canvas(panel, bg="#FAE6E6", highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def toggle_selection(self, owner_id):
        if owner_id in self.selected_owners:
            self.selected_owners.remove(owner_id)
        else:
            self.selected_owners.add(owner_id)
        self.delete_btn.configure(state="normal" if self.selected_owners else "disabled")

    def fetch_product_owners(self):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()

            query = """SELECT owner_id, name, email, status, strftime('%Y-%m-%d', registered_at) FROM product_owners WHERE 1=1"""
            params = []

            if self.search_var.get():
                query += " AND name LIKE ?"
                params.append(f"%{self.search_var.get()}%")

            if self.filter_var.get() != "All":
                query += " AND status = ?"
                params.append(self.filter_var.get())

            if self.from_date_var.get():
                query += " AND date(registered_at) >= ?"
                params.append(self.from_date_var.get())
            if self.to_date_var.get():
                query += " AND date(registered_at) <= ?"
                params.append(self.to_date_var.get())

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data:\n{e}")
            return []

    def display_owners(self):
        for widget in self.owners_scrollable_frame.winfo_children():
            widget.destroy()

        owners = self.fetch_product_owners()
        self.date_label.configure(text=f"Current Date: {datetime.now().strftime('%Y-%m-%d')}")

        for owner in owners:
            owner_id, name, email, status, registered_at = owner

            card_frame = ctk.CTkFrame(self.owners_scrollable_frame, border_width=1, border_color="#D3D3D3", corner_radius=8)
            card_frame.pack(fill="x", padx=5, pady=5)

            chk_var = tk.IntVar(value=1 if owner_id in self.selected_owners else 0)
            ctk.CTkCheckBox(card_frame, text="", variable=chk_var, command=lambda oid=owner_id: self.toggle_selection(oid)).pack(side="left", padx=10)

            info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=5)

            ctk.CTkLabel(info_frame, text=name, font=("Arial", 14, "bold")).pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"{email}\nRegistered: {registered_at}", font=("Arial", 12), text_color="#666666").pack(anchor="w")

            status_color = {"Pending": "#F39C12", "Approved": "#27AE60", "Denied": "#E74C3C"}.get(status, "#3498DB")

            status_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            status_frame.pack(side="right", padx=10)

            ctk.CTkLabel(status_frame, text=status, fg_color=status_color, text_color="white", font=("Arial", 12, "bold"), corner_radius=4, width=80).pack(pady=5)

            btn_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
            btn_frame.pack()

            ctk.CTkButton(btn_frame, text="Approve", fg_color="#27AE60", width=80, command=lambda oid=owner_id: self.update_status(oid, "Approved")).pack(pady=2)
            ctk.CTkButton(btn_frame, text="Deny", fg_color="#E74C3C", width=80, command=lambda oid=owner_id: self.update_status(oid, "Denied")).pack(pady=2)

    def update_status(self, owner_id, new_status):
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE product_owners SET status = ? WHERE owner_id = ?", (new_status, owner_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Status updated to {new_status}")
            self.display_owners()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")

    def delete_selected(self):
        if not self.selected_owners:
            messagebox.showwarning("Warning", "No owners selected")
            return

        if messagebox.askyesno("Confirm", f"Delete {len(self.selected_owners)} selected owners permanently?"):
            try:
                conn = sqlite3.connect(self.DB_NAME)
                cursor = conn.cursor()
                cursor.executemany("INSERT INTO PO_delete_audit_log (owner_id, deleted_by, deleted_at) VALUES (?, ?, datetime('now'))", [(oid, "admin") for oid in self.selected_owners])
                cursor.executemany("DELETE FROM product_owners WHERE owner_id = ?", [(oid,) for oid in self.selected_owners])
                conn.commit()
                conn.close()

                messagebox.showinfo("Success", f"Deleted {len(self.selected_owners)} owners")
                self.selected_owners.clear()
                self.delete_btn.configure(state="disabled")
                self.display_owners()
                self.display_audit_log()
            except Exception as e:
                messagebox.showerror("Error", f"Deletion failed: {e}")

    def display_audit_log(self):
        for widget in self.audit_scrollable_frame.winfo_children():
            widget.destroy()

        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PO_delete_audit_log ORDER BY deleted_at DESC LIMIT 50")
            logs = cursor.fetchall()
            conn.close()

            for log in logs:
                log_id, owner_id, deleted_by, deleted_at = log

                log_frame = ctk.CTkFrame(self.audit_scrollable_frame, border_width=1, border_color="#D3D3D3", corner_radius=8)
                log_frame.pack(fill="x", padx=5, pady=3)

                log_text = f"ID: {owner_id} | {deleted_at.split()[0]}\nDeleted by: {deleted_by}"
                ctk.CTkLabel(log_frame, text=log_text, font=("Arial", 11), anchor="w", justify="left").pack(fill="x", padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load audit log: {e}")

if __name__ == "__main__":
    ProductOwnerApproval()