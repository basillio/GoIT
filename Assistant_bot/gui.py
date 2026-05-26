"""
GUI module for Personal Assistant Bot
Provides a modern Tkinter-based graphical interface
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
from contacts import ContactBook
from notes import NoteBook
from color_manager import ColorManager
from settings_manager import SettingsManager
from notification_manager import NotificationManager


class AssistantGUI:
    """Main GUI application class"""

    def __init__(self, root):
        self.root = root
        self.root.title("Personal Assistant Bot - GUI")
        self.root.geometry("1000x650")
        self.root.minsize(800, 500)

        # Initialize data managers
        self.contact_book = ContactBook()
        self.note_book = NoteBook()
        self.color_manager = ColorManager()
        self.settings_manager = SettingsManager()
        self.notification_manager = NotificationManager(self.contact_book, self.settings_manager)

        # Create menu bar
        self.create_menu_bar()

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.contacts_tab = ttk.Frame(self.notebook)
        self.notes_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.contacts_tab, text="📋 Contacts")
        self.notebook.add(self.notes_tab, text="📝 Notes")
        self.notebook.add(self.settings_tab, text="⚙️ Settings")

        # Setup tabs
        self.setup_contacts_tab()
        self.setup_notes_tab()
        self.setup_settings_tab()

        # Refresh data
        self.refresh_contacts()
        self.refresh_notes()

        # Show birthday notifications on startup
        self.show_birthday_notifications_on_startup()

        # Start periodic birthday checks
        self.notification_manager.start_periodic_check(callback=self.on_birthday_notification)

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Personal Assistant Bot v1.0\n\n"
            "A modern GUI application for managing\n"
            "contacts and notes.\n\n"
            "Features:\n"
            "• Contact management with validation\n"
            "• Notes with tags\n"
            "• Full-text search\n"
            "• Birthday reminders"
        )

    def show_birthday_notifications_on_startup(self):
        """Show birthday notifications on startup if enabled"""
        if not self.settings_manager.get("notifications.show_on_startup", True):
            return

        notification = self.notification_manager.check_birthdays()
        if notification:
            messagebox.showinfo(notification["title"], notification["message"])

    def on_birthday_notification(self, notification):
        """Callback for periodic birthday notifications"""
        messagebox.showinfo(notification["title"], notification["message"])

    def get_color_indicator(self, hex_color):
        """Convert hex color to colored square indicator"""
        # Return a single space that will show the background color
        return " "

    # ==================== CONTACTS TAB ====================

    def setup_contacts_tab(self):
        """Setup contacts management tab"""
        # Search frame
        search_frame = ttk.LabelFrame(self.contacts_tab, text="Search & Actions", padding=10)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.contacts_search_var = tk.StringVar()
        self.contacts_search_var.trace("w", lambda *args: self.filter_contacts())
        search_entry = ttk.Entry(search_frame, textvariable=self.contacts_search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Buttons frame
        button_frame = ttk.Frame(search_frame)
        button_frame.pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="➕ Add", command=self.add_contact_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="✏️ Edit", command=self.edit_contact_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_contact_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🎂 Birthdays", command=self.show_birthdays_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="📌 Notes & Tags", command=self.manage_contact_notes_tags_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🎨 Color", command=self.set_contact_color_dialog).pack(side=tk.LEFT, padx=2)

        # Treeview frame
        tree_frame = ttk.Frame(self.contacts_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        # Treeview
        self.contacts_tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Phone", "Phone2", "Email", "Email2", "Address", "Birthday"),
            height=15,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        vsb.config(command=self.contacts_tree.yview)
        hsb.config(command=self.contacts_tree.xview)

        # Define columns (Color column removed)
        self.contacts_tree.column("#0", width=0, stretch=tk.NO)
        self.contacts_tree.column("Name", anchor=tk.W, width=120)
        self.contacts_tree.column("Phone", anchor=tk.W, width=100)
        self.contacts_tree.column("Phone2", anchor=tk.W, width=100)
        self.contacts_tree.column("Email", anchor=tk.W, width=120)
        self.contacts_tree.column("Email2", anchor=tk.W, width=120)
        self.contacts_tree.column("Address", anchor=tk.W, width=100)
        self.contacts_tree.column("Birthday", anchor=tk.W, width=80)

        # Define headings with sorting
        self.contacts_tree.heading("#0", text="", anchor=tk.W)
        self.contacts_tree.heading("Name", text="Name", anchor=tk.W, command=lambda: self.sort_contacts("Name"))
        self.contacts_tree.heading("Phone", text="Phone", anchor=tk.W, command=lambda: self.sort_contacts("Phone"))
        self.contacts_tree.heading("Phone2", text="Phone 2", anchor=tk.W, command=lambda: self.sort_contacts("Phone2"))
        self.contacts_tree.heading("Email", text="Email", anchor=tk.W, command=lambda: self.sort_contacts("Email"))
        self.contacts_tree.heading("Email2", text="Email 2", anchor=tk.W, command=lambda: self.sort_contacts("Email2"))
        self.contacts_tree.heading("Address", text="Address", anchor=tk.W, command=lambda: self.sort_contacts("Address"))
        self.contacts_tree.heading("Birthday", text="Birthday", anchor=tk.W, command=lambda: self.sort_contacts("Birthday"))

        # Configure color tags
        self.contacts_tree.tag_configure("color_FF6B6B", background="#FF6B6B")
        self.contacts_tree.tag_configure("color_4ECDC4", background="#4ECDC4")
        self.contacts_tree.tag_configure("color_45B7D1", background="#45B7D1")
        self.contacts_tree.tag_configure("color_FFA07A", background="#FFA07A")
        self.contacts_tree.tag_configure("color_98D8C8", background="#98D8C8")
        self.contacts_tree.tag_configure("color_F7DC6F", background="#F7DC6F")
        self.contacts_tree.tag_configure("color_BB8FCE", background="#BB8FCE")
        self.contacts_tree.tag_configure("color_85C1E2", background="#85C1E2")
        self.contacts_tree.tag_configure("color_F8B88B", background="#F8B88B")
        self.contacts_tree.tag_configure("color_A8E6CF", background="#A8E6CF")

        self.contacts_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Track sort state
        self.contacts_sort_column = None
        self.contacts_sort_reverse = False

    def refresh_contacts(self):
        """Refresh contacts treeview"""
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)

        for contact in self.contact_book.list_all_contacts():
            item_id = self.contacts_tree.insert(
                "",
                tk.END,
                values=(
                    contact.name,
                    contact.phone or "",
                    contact.phone2 or "",
                    contact.email or "",
                    contact.email2 or "",
                    contact.address or "",
                    contact.birthday or ""
                )
            )

            # Apply color tag if color is set
            if contact.color:
                color_hex = contact.color.upper().replace("#", "")
                color_tag = f"color_{color_hex}"
                self.contacts_tree.item(item_id, tags=(color_tag,))

    def filter_contacts(self):
        """Filter contacts based on search query"""
        query = self.contacts_search_var.get()

        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)

        if query:
            results = self.contact_book.search_contact(query)
        else:
            results = self.contact_book.list_all_contacts()

        for contact in results:
            item_id = self.contacts_tree.insert(
                "",
                tk.END,
                values=(
                    contact.name,
                    contact.phone or "",
                    contact.phone2 or "",
                    contact.email or "",
                    contact.email2 or "",
                    contact.address or "",
                    contact.birthday or ""
                )
            )

            # Apply color tag if color is set
            if contact.color:
                color_hex = contact.color.upper().replace("#", "")
                color_tag = f"color_{color_hex}"
                self.contacts_tree.item(item_id, tags=(color_tag,))

    def sort_contacts(self, column):
        """Sort contacts by column"""
        # Toggle sort direction if same column clicked
        if self.contacts_sort_column == column:
            self.contacts_sort_reverse = not self.contacts_sort_reverse
        else:
            self.contacts_sort_column = column
            self.contacts_sort_reverse = False

        # Get all contacts
        contacts = self.contact_book.list_all_contacts()

        # Sort by column
        if column == "Name":
            contacts.sort(key=lambda c: c.name, reverse=self.contacts_sort_reverse)
        elif column == "Phone":
            contacts.sort(key=lambda c: c.phone or "", reverse=self.contacts_sort_reverse)
        elif column == "Phone2":
            contacts.sort(key=lambda c: c.phone2 or "", reverse=self.contacts_sort_reverse)
        elif column == "Email":
            contacts.sort(key=lambda c: c.email or "", reverse=self.contacts_sort_reverse)
        elif column == "Email2":
            contacts.sort(key=lambda c: c.email2 or "", reverse=self.contacts_sort_reverse)
        elif column == "Address":
            contacts.sort(key=lambda c: c.address or "", reverse=self.contacts_sort_reverse)
        elif column == "Birthday":
            contacts.sort(key=lambda c: c.birthday or "", reverse=self.contacts_sort_reverse)

        # Refresh treeview with sorted data
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)

        for contact in contacts:
            item_id = self.contacts_tree.insert(
                "",
                tk.END,
                values=(
                    contact.name,
                    contact.phone or "",
                    contact.phone2 or "",
                    contact.email or "",
                    contact.email2 or "",
                    contact.address or "",
                    contact.birthday or ""
                )
            )

            # Apply color tag if color is set
            if contact.color:
                color_hex = contact.color.upper().replace("#", "")
                color_tag = f"color_{color_hex}"
                self.contacts_tree.item(item_id, tags=(color_tag,))

    def add_contact_dialog(self):
        """Show dialog to add new contact"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Contact")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Form fields
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Phone:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        phone_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=phone_var, width=30).grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Phone 2:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        phone2_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=phone2_var, width=30).grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Email:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        email_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=email_var, width=30).grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Email 2:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        email2_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=email2_var, width=30).grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Address:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        address_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=address_var, width=30).grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Birthday (DD.MM.YYYY):").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        birthday_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=birthday_var, width=30).grid(row=6, column=1, padx=10, pady=5)

        # Color picker
        ttk.Label(dialog, text="Color:").grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)
        color_var = tk.StringVar(value="")
        color_label = ttk.Label(dialog, text="No color", width=20)
        color_label.grid(row=7, column=1, padx=10, pady=5)

        def pick_color():
            color = colorchooser.askcolor(color=color_var.get() or "#FF6B6B")[1]
            if color:
                color_var.set(color)
                color_label.config(text=color)

        ttk.Button(dialog, text="Pick Color", command=pick_color).grid(row=8, column=0, columnspan=2, pady=10)

        def save_contact():
            try:
                result = self.contact_book.add_contact(
                    name_var.get(),
                    phone_var.get() or None,
                    phone2_var.get() or None,
                    email_var.get() or None,
                    email2_var.get() or None,
                    address_var.get() or None,
                    birthday_var.get() or None,
                    color=color_var.get() or None
                )
                messagebox.showinfo("Success", result)
                self.refresh_contacts()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_contact).grid(row=9, column=0, columnspan=2, pady=20)

    def edit_contact_dialog(self):
        """Show dialog to edit selected contact"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to edit")
            return

        item = selection[0]
        values = self.contacts_tree.item(item)["values"]
        name = values[0]  # Name is at index 0 (no Color column)

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Contact - {name}")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()

        # Form fields
        ttk.Label(dialog, text="Phone:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        phone_var = tk.StringVar(value=values[1])
        ttk.Entry(dialog, textvariable=phone_var, width=30).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Phone 2:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        phone2_var = tk.StringVar(value=values[2])
        ttk.Entry(dialog, textvariable=phone2_var, width=30).grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Email:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        email_var = tk.StringVar(value=values[3])
        ttk.Entry(dialog, textvariable=email_var, width=30).grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Email 2:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        email2_var = tk.StringVar(value=values[4])
        ttk.Entry(dialog, textvariable=email2_var, width=30).grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Address:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        address_var = tk.StringVar(value=values[5])
        ttk.Entry(dialog, textvariable=address_var, width=30).grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Birthday (DD.MM.YYYY):").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        birthday_var = tk.StringVar(value=values[6])
        ttk.Entry(dialog, textvariable=birthday_var, width=30).grid(row=5, column=1, padx=10, pady=5)

        # Color picker
        ttk.Label(dialog, text="Color:").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        color_var = tk.StringVar(value=self.contact_book.contacts[name].color or "")
        color_label = ttk.Label(dialog, text=color_var.get() or "No color", width=20)
        color_label.grid(row=6, column=1, padx=10, pady=5)

        def pick_color():
            color = colorchooser.askcolor(color=color_var.get() or "#FF6B6B")[1]
            if color:
                color_var.set(color)
                color_label.config(text=color)

        ttk.Button(dialog, text="Pick Color", command=pick_color).grid(row=7, column=0, columnspan=2, pady=10)

        def save_changes():
            try:
                # Handle color: empty string means no color, otherwise use the color value
                color_value = color_var.get() if color_var.get() else None

                result = self.contact_book.edit_contact(
                    name,
                    phone=phone_var.get() or None,
                    phone2=phone2_var.get() or None,
                    email=email_var.get() or None,
                    email2=email2_var.get() or None,
                    address=address_var.get() or None,
                    birthday=birthday_var.get() or None,
                    color=color_value
                )
                messagebox.showinfo("Success", result)
                self.refresh_contacts()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_changes).grid(row=8, column=0, columnspan=2, pady=20)

    def delete_contact_dialog(self):
        """Delete selected contact"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to delete")
            return

        item = selection[0]
        name = self.contacts_tree.item(item)["values"][0]  # Name is at index 0 (no Color column)

        if messagebox.askyesno("Confirm", f"Delete contact '{name}'?"):
            try:
                result = self.contact_book.delete_contact(name)
                messagebox.showinfo("Success", result)
                self.refresh_contacts()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def show_birthdays_dialog(self):
        """Show contacts with birthdays in N days"""
        days = simpledialog.askinteger("Birthdays", "Show birthdays in how many days?", minvalue=0, maxvalue=365)
        if days is None:
            return

        try:
            results = self.contact_book.get_birthdays_in_days(days)
            if results:
                message = f"Contacts with birthdays in {days} days:\n\n"
                for contact in results:
                    message += f"• {contact.name} - {contact.birthday}\n"
                messagebox.showinfo("Birthdays", message)
            else:
                messagebox.showinfo("Birthdays", f"No contacts with birthdays in {days} days")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_color_palette_dialog(self, title="Choose Color"):
        """Show custom color palette dialog"""
        palette = {
            "Red": "#FF6B6B",
            "Cyan": "#4ECDC4",
            "Blue": "#45B7D1",
            "Orange": "#FFA07A",
            "Green": "#98D8C8",
            "Yellow": "#F7DC6F",
            "Purple": "#BB8FCE",
            "Sky": "#85C1E2",
            "Peach": "#F8B88B",
            "Mint": "#A8E6CF",
        }

        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x280")
        dialog.transient(self.root)
        dialog.grab_set()

        selected_color = tk.StringVar()

        ttk.Label(dialog, text="Select a color:", font=("Arial", 10, "bold")).pack(pady=10)

        # Create color buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Add "No Color" button
        no_color_btn = tk.Button(
            button_frame,
            text="No Color",
            bg="lightgray",
            fg="black",
            width=12,
            command=lambda: (selected_color.set(""), dialog.destroy())
        )
        no_color_btn.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        for i, (color_name, hex_color) in enumerate(palette.items()):
            row = (i // 2) + 1
            col = i % 2
            btn = tk.Button(
                button_frame,
                text=f"● {color_name}",
                bg=hex_color,
                fg="white" if color_name not in ["Yellow", "Peach", "Mint"] else "black",
                width=12,
                command=lambda c=hex_color: (selected_color.set(c), dialog.destroy())
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Cancel button
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=10)

        dialog.wait_window()
        return selected_color.get() if selected_color.get() else None

    def set_contact_color_dialog(self):
        """Set color for selected contact"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to set color")
            return

        item = selection[0]
        name = self.contacts_tree.item(item)["values"][0]  # Name is at index 0 (no Color column)

        color = self.show_color_palette_dialog(f"Choose color for {name}")
        if color:
            try:
                self.contact_book.edit_contact(name, color=color)
                messagebox.showinfo("Success", f"Color set for {name}")
                self.refresh_contacts()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def manage_contact_notes_tags_dialog(self):
        """Show dialog to manage contact notes and tags"""
        selection = self.contacts_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact")
            return

        item = selection[0]
        name = self.contacts_tree.item(item)["values"][0]  # Name is at index 0 (no Color column)

        if name not in self.contact_book.contacts:
            messagebox.showerror("Error", f"Contact '{name}' not found")
            return

        contact = self.contact_book.contacts[name]

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Manage Notes & Tags - {name}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Notes section
        ttk.Label(dialog, text="Notes (one per line):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        notes_text = tk.Text(dialog, height=8, width=50)
        notes_text.grid(row=1, column=0, padx=10, pady=5)
        notes_text.insert(tk.END, "\n".join(contact.notes) if contact.notes else "")

        # Tags section
        ttk.Label(dialog, text="Tags (comma-separated):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        tags_var = tk.StringVar(value=", ".join(contact.tags) if contact.tags else "")
        ttk.Entry(dialog, textvariable=tags_var, width=50).grid(row=3, column=0, padx=10, pady=5)

        def save_changes():
            try:
                notes = [note.strip() for note in notes_text.get("1.0", tk.END).strip().split("\n") if note.strip()]
                tags = [tag.strip() for tag in tags_var.get().split(",") if tag.strip()]

                self.contact_book.edit_contact(name, notes=notes, tags=tags)
                messagebox.showinfo("Success", "Notes and tags updated")
                self.refresh_contacts()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_changes).grid(row=4, column=0, pady=20)

    # ==================== NOTES TAB ====================

    def setup_notes_tab(self):
        """Setup notes management tab"""
        # Search frame
        search_frame = ttk.LabelFrame(self.notes_tab, text="Search & Filter", padding=10)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.notes_search_var = tk.StringVar()
        self.notes_search_var.trace("w", lambda *args: self.filter_notes())
        search_entry = ttk.Entry(search_frame, textvariable=self.notes_search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(search_frame, text="Tags:").pack(side=tk.LEFT, padx=5)
        self.notes_tags_var = tk.StringVar()
        self.notes_tags_var.trace("w", lambda *args: self.filter_notes())
        tags_entry = ttk.Entry(search_frame, textvariable=self.notes_tags_var, width=30)
        tags_entry.pack(side=tk.LEFT, padx=5)

        # Buttons frame
        button_frame = ttk.Frame(search_frame)
        button_frame.pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="➕ Add", command=self.add_note_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="✏️ Edit", command=self.edit_note_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_note_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🎨 Color", command=self.set_note_color_dialog).pack(side=tk.LEFT, padx=2)

        # Treeview frame
        tree_frame = ttk.Frame(self.notes_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        # Treeview
        self.notes_tree = ttk.Treeview(
            tree_frame,
            columns=("Text", "Tags", "Created"),
            height=15,
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        vsb.config(command=self.notes_tree.yview)
        hsb.config(command=self.notes_tree.xview)

        # Define columns (removed Color column)
        self.notes_tree.column("#0", width=0, stretch=tk.NO)
        self.notes_tree.column("Text", anchor=tk.W, width=300)
        self.notes_tree.column("Tags", anchor=tk.W, width=150)
        self.notes_tree.column("Created", anchor=tk.W, width=120)

        # Define headings with sorting
        self.notes_tree.heading("#0", text="", anchor=tk.W)
        self.notes_tree.heading("Text", text="Text", anchor=tk.W, command=lambda: self.sort_notes("Text"))
        self.notes_tree.heading("Tags", text="Tags", anchor=tk.W, command=lambda: self.sort_notes("Tags"))
        self.notes_tree.heading("Created", text="Created", anchor=tk.W, command=lambda: self.sort_notes("Created"))

        # Track sort state
        self.notes_sort_column = None
        self.notes_sort_reverse = False

        self.notes_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def refresh_notes(self):
        """Refresh notes treeview"""
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)

        for note in self.note_book.list_all_notes():
            text_preview = note.text[:50] + "..." if len(note.text) > 50 else note.text
            tags_str = ", ".join(note.tags) if note.tags else ""
            created = note.created_at[:10] if note.created_at else ""

            self.notes_tree.insert(
                "",
                tk.END,
                iid=note.id,
                values=(text_preview, tags_str, created)
            )

    def filter_notes(self):
        """Filter notes based on search query and tags"""
        search_query = self.notes_search_var.get()
        tags_query = self.notes_tags_var.get()

        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)

        results = self.note_book.list_all_notes()

        # Filter by search query
        if search_query:
            results = [n for n in results if search_query.lower() in n.text.lower()]

        # Filter by tags
        if tags_query:
            tags = [t.strip() for t in tags_query.split(",")]
            results = [n for n in results if any(tag.lower() in [t.lower() for t in n.tags] for tag in tags)]

        for note in results:
            text_preview = note.text[:50] + "..." if len(note.text) > 50 else note.text
            tags_str = ", ".join(note.tags) if note.tags else ""
            created = note.created_at[:10] if note.created_at else ""

            self.notes_tree.insert(
                "",
                tk.END,
                iid=note.id,
                values=(text_preview, tags_str, created)
            )

    def sort_notes(self, column):
        """Sort notes by column"""
        # Toggle sort direction if same column clicked
        if self.notes_sort_column == column:
            self.notes_sort_reverse = not self.notes_sort_reverse
        else:
            self.notes_sort_column = column
            self.notes_sort_reverse = False

        # Get all notes
        notes = self.note_book.list_all_notes()

        # Sort by column
        if column == "Text":
            notes.sort(key=lambda n: n.text, reverse=self.notes_sort_reverse)
        elif column == "Tags":
            notes.sort(key=lambda n: ", ".join(n.tags) if n.tags else "", reverse=self.notes_sort_reverse)
        elif column == "Created":
            notes.sort(key=lambda n: n.created_at or "", reverse=self.notes_sort_reverse)

        # Refresh treeview with sorted data
        for item in self.notes_tree.get_children():
            self.notes_tree.delete(item)

        for note in notes:
            text_preview = note.text[:50] + "..." if len(note.text) > 50 else note.text
            tags_str = ", ".join(note.tags) if note.tags else ""
            created = note.created_at[:10] if note.created_at else ""

            self.notes_tree.insert(
                "",
                tk.END,
                iid=note.id,
                values=(text_preview, tags_str, created)
            )

    def add_note_dialog(self):
        """Show dialog to add new note"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Note")
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Note Text:").grid(row=0, column=0, sticky=tk.NW, padx=10, pady=5)
        text_frame = ttk.Frame(dialog)
        text_frame.grid(row=0, column=1, padx=10, pady=5, sticky=tk.NSEW)

        text_widget = tk.Text(text_frame, height=10, width=40, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(dialog, text="Tags (comma-separated):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        tags_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=tags_var, width=40).grid(row=1, column=1, padx=10, pady=5)

        def save_note():
            text = text_widget.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "Note text cannot be empty")
                return

            tags = [t.strip() for t in tags_var.get().split(",")] if tags_var.get() else []

            try:
                result = self.note_book.add_note(text, tags)
                messagebox.showinfo("Success", result)
                self.refresh_notes()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_note).grid(row=2, column=0, columnspan=2, pady=20)

        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_columnconfigure(1, weight=1)

    def edit_note_dialog(self):
        """Show dialog to edit selected note"""
        selection = self.notes_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a note to edit")
            return

        note_id = selection[0]
        note = self.note_book.notes[note_id]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Note")
        dialog.geometry("500x350")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Note Text:").grid(row=0, column=0, sticky=tk.NW, padx=10, pady=5)
        text_frame = ttk.Frame(dialog)
        text_frame.grid(row=0, column=1, padx=10, pady=5, sticky=tk.NSEW)

        text_widget = tk.Text(text_frame, height=10, width=40, wrap=tk.WORD)
        text_widget.insert("1.0", note.text)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(dialog, text="Tags (comma-separated):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        tags_var = tk.StringVar(value=", ".join(note.tags))
        ttk.Entry(dialog, textvariable=tags_var, width=40).grid(row=1, column=1, padx=10, pady=5)

        def save_changes():
            text = text_widget.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "Note text cannot be empty")
                return

            tags = [t.strip() for t in tags_var.get().split(",")] if tags_var.get() else []

            try:
                result = self.note_book.edit_note(note_id, text=text, tags=tags)
                messagebox.showinfo("Success", result)
                self.refresh_notes()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dialog, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2, pady=20)

        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_columnconfigure(1, weight=1)

    def delete_note_dialog(self):
        """Delete selected note"""
        selection = self.notes_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a note to delete")
            return

        note_id = selection[0]
        note = self.note_book.notes[note_id]
        text_preview = note.text[:50] + "..." if len(note.text) > 50 else note.text

        if messagebox.askyesno("Confirm", f"Delete note: '{text_preview}'?"):
            try:
                result = self.note_book.delete_note(note_id)
                messagebox.showinfo("Success", result)
                self.refresh_notes()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def set_note_color_dialog(self):
        """Set color for selected note"""
        selection = self.notes_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a note to set color")
            return

        note_id = selection[0]
        note = self.note_book.notes[note_id]
        text_preview = note.text[:30] + "..." if len(note.text) > 30 else note.text

        color = self.show_color_palette_dialog(f"Choose color for note: {text_preview}")
        if color:
            try:
                self.note_book.edit_note(note_id, color=color)
                messagebox.showinfo("Success", "Color set for note")
                self.refresh_notes()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    # ==================== SETTINGS TAB ====================

    def setup_settings_tab(self):
        """Setup settings management tab"""
        # Create main frame with scrollbar
        main_frame = ttk.Frame(self.settings_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Notifications section
        notif_frame = ttk.LabelFrame(main_frame, text="📬 Notifications", padding=10)
        notif_frame.pack(fill=tk.X, pady=10)

        self.notif_enabled_var = tk.BooleanVar(value=self.settings_manager.get("notifications.enabled", True))
        ttk.Checkbutton(notif_frame, text="Enable notifications", variable=self.notif_enabled_var,
                       command=self.on_notification_enabled_changed).pack(anchor=tk.W, pady=5)

        ttk.Label(notif_frame, text="Days in advance:").pack(anchor=tk.W, pady=5)
        self.notif_days_var = tk.StringVar(value=str(self.settings_manager.get("notifications.days_in_advance", 7)))
        days_combo = ttk.Combobox(notif_frame, textvariable=self.notif_days_var, values=["1", "3", "7", "14", "30"], width=10)
        days_combo.pack(anchor=tk.W, pady=5)
        days_combo.bind("<<ComboboxSelected>>", lambda e: self.on_notification_days_changed())

        ttk.Label(notif_frame, text="Check interval:").pack(anchor=tk.W, pady=5)
        self.notif_interval_var = tk.StringVar(value=self.settings_manager.get("notifications.check_interval", "1h"))
        interval_combo = ttk.Combobox(notif_frame, textvariable=self.notif_interval_var, values=["1h", "6h", "daily"], width=10)
        interval_combo.pack(anchor=tk.W, pady=5)
        interval_combo.bind("<<ComboboxSelected>>", lambda e: self.on_notification_interval_changed())

        self.notif_startup_var = tk.BooleanVar(value=self.settings_manager.get("notifications.show_on_startup", True))
        ttk.Checkbutton(notif_frame, text="Show on startup", variable=self.notif_startup_var,
                       command=self.on_notification_startup_changed).pack(anchor=tk.W, pady=5)

        # UI section
        ui_frame = ttk.LabelFrame(main_frame, text="🎨 User Interface", padding=10)
        ui_frame.pack(fill=tk.X, pady=10)

        ttk.Label(ui_frame, text="Theme:").pack(anchor=tk.W, pady=5)
        self.theme_var = tk.StringVar(value=self.settings_manager.get("ui.theme", "light"))
        theme_combo = ttk.Combobox(ui_frame, textvariable=self.theme_var, values=["light", "dark"], width=10)
        theme_combo.pack(anchor=tk.W, pady=5)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.on_theme_changed())

        ttk.Label(ui_frame, text="Auto-save interval (seconds):").pack(anchor=tk.W, pady=5)
        self.autosave_var = tk.StringVar(value=str(self.settings_manager.get("ui.auto_save_interval", 30)))
        autosave_spin = ttk.Spinbox(ui_frame, from_=5, to=300, textvariable=self.autosave_var, width=10)
        autosave_spin.pack(anchor=tk.W, pady=5)
        autosave_spin.bind("<FocusOut>", lambda e: self.on_autosave_changed())

        # Buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_settings_to_defaults).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Settings", command=self.save_all_settings).pack(side=tk.LEFT, padx=5)

    def on_notification_enabled_changed(self):
        """Handle notification enabled change"""
        self.settings_manager.set_notifications_enabled(self.notif_enabled_var.get())

    def on_notification_days_changed(self):
        """Handle notification days change"""
        try:
            days = int(self.notif_days_var.get())
            self.settings_manager.set_notification_days(days)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def on_notification_interval_changed(self):
        """Handle notification interval change"""
        self.settings_manager.set_check_interval(self.notif_interval_var.get())

    def on_notification_startup_changed(self):
        """Handle notification startup change"""
        self.settings_manager.set("notifications.show_on_startup", self.notif_startup_var.get())

    def on_theme_changed(self):
        """Handle theme change"""
        self.settings_manager.set_theme(self.theme_var.get())
        messagebox.showinfo("Info", "Theme will be applied on next restart")

    def on_autosave_changed(self):
        """Handle auto-save interval change"""
        try:
            interval = int(self.autosave_var.get())
            if interval < 5 or interval > 300:
                raise ValueError("Interval must be between 5 and 300 seconds")
            self.settings_manager.set_auto_save_interval(interval)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def save_all_settings(self):
        """Save all settings"""
        messagebox.showinfo("Success", "All settings have been saved")

    def reset_settings_to_defaults(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            self.settings_manager.reset_to_defaults()
            # Reload UI values
            self.notif_enabled_var.set(self.settings_manager.get("notifications.enabled", True))
            self.notif_days_var.set(str(self.settings_manager.get("notifications.days_in_advance", 7)))
            self.notif_interval_var.set(self.settings_manager.get("notifications.check_interval", "1h"))
            self.notif_startup_var.set(self.settings_manager.get("notifications.show_on_startup", True))
            self.theme_var.set(self.settings_manager.get("ui.theme", "light"))
            self.autosave_var.set(str(self.settings_manager.get("ui.auto_save_interval", 30)))
            messagebox.showinfo("Success", "Settings reset to defaults")


def main():
    """Launch the GUI application"""
    root = tk.Tk()
    app = AssistantGUI(root)

    def on_closing():
        """Handle window closing event"""
        app.notification_manager.stop_periodic_check()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
