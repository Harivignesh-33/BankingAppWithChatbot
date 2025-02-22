import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import customerdetails, transaction, customertree, transtree, homepage
from transaction import Transac

class AdminPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1024x768")
        self.configure(bg="#F8F9FA")

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.after(10, self.full_screen)

        main_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        ctk.CTkLabel(main_frame, text="Admin Dashboard",
                     font=("Arial", 25, "bold"), text_color="#333").pack(pady=10)

        self.load_images()
        self.create_buttons(main_frame)

    def full_screen(self):
        """Ensures proper full-screen behavior without flickering."""
        self.state("zoomed")

    def load_images(self):
        """Load and resize images for buttons."""
        self.icons = {}
        image_files = {
            "Customer Registration": "./Images/cus_reg.png",
            "View Customer": "./Images/view_cus.png",
            "Transaction": "./Images/transaction.png",
            "View Transaction": "./Images/view_transaction.png",
            "Logout": "./Images/exit.png"
        }

        for key, path in image_files.items():
            try:
                img = Image.open(path)
                img = img.resize((180, 180), Image.LANCZOS)  # Adjusted for button size
                self.icons[key] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading {key}: {e}")
                self.icons[key] = None

    def create_buttons(self, parent):
        """Create buttons with a size of 192x163 pixels."""
        buttons = [
            ("Customer Registration", self.link1, "#1ABC9C"),  # Turquoise
            ("View Customer", self.link2, "#3498DB"),  # Blue
            ("Transaction", self.link3, "#F39C12"),  # Orange
            ("View Transaction", self.link4, "#9B59B6"),  # Purple
            ("Logout", self.logout, "#E74C3C")  # Red
        ]

        button_frame = ctk.CTkFrame(parent, fg_color="white")
        button_frame.pack(pady=10, expand=True, fill='both')

        for i, (text, command, color) in enumerate(buttons):
            btn = ctk.CTkButton(button_frame, text=text, font=("Arial", 18, "bold"),
                                width=230, height=230,  # Updated button size
                                fg_color=color, hover_color=self.darken_color(color),
                                image=self.icons.get(text), compound="top",
                                command=command, corner_radius=20)
            btn.grid(row=i // 3, column=i % 3, padx=100, pady=40)

    def darken_color(self, color, factor=0.8):
        """Helper function to darken a given hex color."""
        color = color.lstrip("#")
        rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(int(c * factor) for c in rgb)
        return f"#{darker_rgb[0]:02X}{darker_rgb[1]:02X}{darker_rgb[2]:02X}"

    # Button Functions
    def link1(self):
        self.open_window("Customer Registration", customerdetails.UserLoginPage)

    def link2(self):
        self.open_window("View Customers", customertree.CustomerTree)

    def link3(self):
        """Open the Transaction window without opening multiple instances"""
        if hasattr(self, "transaction_window") and self.transaction_window.winfo_exists():
            self.transaction_window.lift()
            self.transaction_window.focus_force()
        else:
            self.transaction_window = Transac(self)

    def link4(self):
        self.open_window("View Transactions", transtree.TransactionTree)

    def open_window(self, title, function):
        """Opens a new window without closing or hiding the AdminPage, ensuring it appears on top."""
        new_window = ctk.CTkToplevel(self)
        new_window.geometry("1024x768")  # Adjust size as needed
        new_window.title(title)

        # Bring the new window to the front
        new_window.lift()
        new_window.attributes('-topmost', True)
        new_window.focus_force()

        function(new_window)  # Call the respective function to initialize the window

    def logout(self):
        """Logs out and returns to the homepage."""
        self.destroy()
        homepage.Homepage().run()


if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()
