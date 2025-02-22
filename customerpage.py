import customtkinter as ctk
from PIL import Image, ImageTk
import transactioncus, cus_transtree


class CustomerPage(ctk.CTkToplevel):
    def __init__(self, homepage, acc_no, customer_name="Customer"):
        super().__init__()
        self.homepage = homepage
        self.acc_no = str(acc_no).strip()  # Ensure it's a string
        self.customer_name = customer_name

        # ✅ Debug Print
        print(f"📌 DEBUG: Received acc_no = '{self.acc_no}' (Type: {type(self.acc_no)})")

        # ✅ Validate Account Number
        if not self.acc_no.isdigit():  # Ensure it's a number
            print(f"❌ ERROR: Invalid acc_no '{self.acc_no}'. Expected a numeric account number.")
            self.acc_no = "000000"  # Default to a placeholder or handle appropriately

        self.title("Customer Dashboard")
        self.geometry("1024x768")
        self.configure(bg="#F8F9FA")

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.after(10, self.full_screen)

        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        main_frame.pack(padx=30, pady=30, fill='both', expand=True)

        # ✅ Welcome Header Section
        self.create_welcome_header(main_frame)

        self.load_images()
        self.create_buttons(main_frame)

    def full_screen(self):
        """Ensures full-screen behavior."""
        self.state("zoomed")

    def create_welcome_header(self, parent):
        """Creates a professional welcome header with customer name."""
        header_frame = ctk.CTkFrame(parent, fg_color="white")
        header_frame.pack(fill="x", pady=20)

        ctk.CTkLabel(header_frame, text="Customer Dashboard",
                     font=("Arial", 28, "bold"), text_color="#333").pack(pady=(10, 5))

        name_label = ctk.CTkLabel(header_frame,
                                  text=f"👋 Welcome, {self.customer_name}!",
                                  font=("Arial", 34, "bold"),
                                  text_color="#1ABC9C")
        name_label.pack(pady=10)

    def load_images(self):
        """Loads and resizes images for buttons."""
        self.icons = {}
        image_files = {
            "Transaction": "./Images/transaction.png",
            "View Transactions": "./Images/view_transaction.png",
            "Logout": "./Images/exit.png"
        }

        for key, path in image_files.items():
            try:
                img = Image.open(path)
                img = img.resize((180, 180), Image.LANCZOS)
                self.icons[key] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading {key}: {e}")
                self.icons[key] = None

    def create_buttons(self, parent):
        """Creates navigation buttons in a single row with balanced spacing."""
        button_frame = ctk.CTkFrame(parent, fg_color="white")
        button_frame.pack(pady=20, expand=True, fill='both')

        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        buttons = [
            ("Transaction", self.open_transaction, "#1ABC9C"),
            ("View Transactions", self.view_transactions, "#3498DB"),
            ("Logout", self.logout, "#E74C3C")
        ]

        for col, (text, command, color) in enumerate(buttons):
            btn = ctk.CTkButton(button_frame, text=text, font=("Arial", 20, "bold"),
                                width=230, height=230, fg_color=color,
                                hover_color=self.darken_color(color),
                                image=self.icons.get(text), compound="top",
                                command=command, corner_radius=25)
            btn.grid(row=0, column=col, padx=50, pady=70)

    def darken_color(self, color, factor=0.85):
        """Darkens a given hex color for hover effect."""
        color = color.lstrip("#")
        rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{darker_rgb[0]:02X}{darker_rgb[1]:02X}{darker_rgb[2]:02X}"

    def open_transaction(self):
        """Opens the transaction page."""
        if hasattr(self, "trans_window") and self.trans_window.winfo_exists():
            self.trans_window.lift()
            self.trans_window.focus_force()
        else:
            self.trans_window = ctk.CTkToplevel(self)
            self.trans_window.geometry("600x500")
            self.trans_window.title("Transactions")
            transactioncus.transac(self.trans_window)

            self.trans_window.protocol("WM_DELETE_WINDOW", self.on_child_window_close)

    def view_transactions(self):
        """Opens the transaction history page in full screen and stays on top."""
        print(f"📌 DEBUG: Account No before opening history: '{self.acc_no}'")

        if hasattr(self, "history_window") and self.history_window.winfo_exists():
            self.history_window.lift()
            self.history_window.focus_force()
        else:
            self.history_window = ctk.CTkToplevel(self)
            self.history_window.title("Transaction History")
            self.history_window.state("zoomed")
            self.history_window.attributes('-topmost', True)

            # ✅ Pass VALIDATED account number
            print(f"📌 DEBUG: Passing acc_no = {self.acc_no} to CustomerTransactionTree")
            cus_transtree.CustomerTransactionTree(self.history_window, self.acc_no)

            self.history_window.protocol("WM_DELETE_WINDOW", self.on_history_window_close)

    def on_history_window_close(self):
        """Closes transaction history window without affecting the main UI."""
        self.history_window.destroy()

    def on_child_window_close(self):
        """Closes the transaction window properly."""
        self.trans_window.destroy()

    def logout(self):
        """Logs out and returns to homepage."""
        self.destroy()
        self.homepage.deiconify()
