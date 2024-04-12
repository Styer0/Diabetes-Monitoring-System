import tkinter as tk
from tkinter import messagebox
from dashboard import dashForm

# Function to handle login action
class loginForm:
    def __init__ (self, root):
        self.root = root
        root.title("Login")
        # Center the window
        window_width = 500
        window_height = 500

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))

        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        
        def login_dash(user_id):
            if user_id == "5344-9709":
                self.dashboard = tk.Toplevel(self.root)
                self.root.withdraw()
                dashForm(self.dashboard, self, "Sara Norman")
            elif user_id == "1275-4307":
                self.dashboard = tk.Toplevel(self.root)
                self.root.withdraw()
                dashForm(self.dashboard, self, "Gregg Norman")
            else:
                messagebox.showerror("Login Failed", "Invalid user ID")
        
        # Function to handle Sara's login
        def sara_login():
            login_dash("5344-9709")

        # Function to handle Gregg's login
        def gregg_login():
            login_dash("1275-4307")
        
        # Create labels with custom font size
        label_title = tk.Label(self.root, text="Select Your Name to Login:", font=("Helvetica", 20))
        label_title.pack(pady=30)

        # Create buttons for Sara and Gregg
        sara_button = tk.Button(self.root, text="Sara Norman", command=sara_login, font=("Helvetica", 14))
        sara_button.pack(pady=20)

        gregg_button = tk.Button(self.root, text="Gregg Norman", command=gregg_login, font=("Helvetica", 14))
        gregg_button.pack(pady=5)