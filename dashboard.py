import tkinter as tk
from tkinter import messagebox
import time
import applogic
from loaddata import load_patient_data
from record import RecordBloodSugarForm

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None

        # Bind the Enter and Leave events to the widget
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        # Create a tooltip window when the mouse enters the widget
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, bg="white", relief="solid", borderwidth=1, font=("Helvetica", 10))
        label.pack()

    def hide_tooltip(self, event):
        # Destroy the tooltip window when the mouse leaves the widget
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class dashForm:
    def __init__(self, dashboard, login_form, username):
        self.dashboard = dashboard
        self.login_form = login_form
        self.username = username
        self.record_form_active = False
        #Prevention of application not exiting propertly
        dashboard.protocol("WM_DELETE_WINDOW", self.exitApp)

        # Set dashboard title
        self.dashboard.title(f"Dashboard - {username}")

        # Center the window
        window_width = 1000
        window_height = 700
        screen_width = self.dashboard.winfo_screenwidth()
        screen_height = self.dashboard.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.dashboard.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Create a frame at the top of the window for user info and logout
        top_frame = tk.Frame(self.dashboard, bg='lightgrey')
        top_frame.pack(fill=tk.X)

        # Display user's name and ID at the top left
        user_info = f"{username}, ID: {self.get_user_id()}"
        user_label = tk.Label(top_frame, text=user_info, font=("Helvetica", 12), bg='lightgrey')
        user_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Create a label for the clock
        self.clock_label = tk.Label(top_frame, font=("Helvetica", 10), bg='lightgrey')
        self.clock_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.update_clock()  # Start updating the clock

        # Create a logout button and place it at the top right
        logout_button = tk.Button(top_frame, text="Logout", command=self.logout, bg='lightgrey')
        logout_button.pack(side=tk.RIGHT, padx=10, pady=5)

        middle_frame = tk.Frame(self.dashboard)
        middle_frame.pack(fill=tk.BOTH, expand=True)

        # Load patient data and display it
        low,high,date = self.load_patient_data(username, middle_frame)

        # Create a frame at the bottom of the window for help and blood sugar record button
        bottom_frame = tk.Frame(self.dashboard, bg='lightgrey')
        bottom_frame.pack(fill=tk.X)

        # Create a placeholder help button at the bottom left
        help_button = tk.Button(bottom_frame, text="Help", font=("Helvetica", 12), command=self.show_help)
        help_button.pack(side=tk.LEFT, anchor=tk.SW, padx=20, pady=20)

        # Create a button to record blood sugar level
        blood_lvl_button = tk.Button(bottom_frame, text="Record Blood Sugar Level", font=("Helvetica", 12), command=lambda: self.open_record_panel(username, low, high))
        blood_lvl_button.pack(side=tk.RIGHT, anchor=tk.SE, padx=20, pady=20)

        # tooltips
        logout_dialog = "Click to logout and return to the login screen"
        Tooltip(logout_button, logout_dialog)

        help_dialog = "Click for guidance on how the app works"
        Tooltip(help_button, help_dialog)

        blood_dialog = "Click to record your blood sugar level"
        Tooltip(blood_lvl_button, blood_dialog)

        # Check if the user has recorded their blood sugar reading for today
        auto_switch = self.check_blood_sugar(date)
        if auto_switch == True:
            self.open_record_panel(username, low, high)


    def open_record_panel(self, username, low, high):
        # Function to open a new panel for recording blood sugar level
        self.record_form_active = True
        while self.record_form_active:
            record_form = RecordBloodSugarForm(self.dashboard, username, low, high, self)
            self.dashboard.wait_window(record_form.record_window)


    def get_user_id(self):
        # This method returns the user ID based on the username.
        if self.username == "Sara Norman":
            return "5344-9709"
        elif self.username == "Gregg Norman":
            return "1275-4307"
        return ""

    def logout(self):
        # Hide the dashboard and show the login form
        self.dashboard.withdraw()
        self.login_form.root.deiconify()

    def update_clock(self):
        # Update the clock every second
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.clock_label.config(text=current_time)
        self.dashboard.after(1000, self.update_clock)  # Call update_clock every second
    
    def load_patient_data(self, username, middle_frame):
        # Load patient data using the function from loaddata.py
        patient_info, daily_readings = load_patient_data(username)

        # Check if patient data was loaded successfully
        if not patient_info:
            tk.Label(middle_frame, text="Data file not found.", font=("Helvetica", 12)).pack(pady=10)
            return

        # Display patient information
        patient_frame = tk.Frame(middle_frame)
        patient_frame.pack(padx=10, pady=50)

        doctor_info = f"Doctor: {patient_info['doctor_name']} | Phone: {patient_info['doctor_phone']}"
        tk.Label(patient_frame, text=doctor_info, font=("Helvetica", 12)).pack()

        glucose_info = f"Glucose Levels: Low: <{patient_info['low_glucose']} mg/dL, Normal: {patient_info['low_glucose']}-{patient_info['high_glucose']} mg/dL, High: >{patient_info['high_glucose']} mg/dL"
        tk.Label(patient_frame, text=glucose_info, font=("Helvetica", 12)).pack()

        # Create a frame for daily readings
        readings_frame = tk.Frame(middle_frame)
        readings_frame.pack(padx=10, pady=10)

        # Display daily readings
        tk.Label(readings_frame, text="Daily Readings:", font=("Helvetica", 12)).pack()
        for reading_date, glucose_level, reason_level in daily_readings:
            reading_info = f"{reading_date}: {glucose_level} mg/dL - Reading: {reason_level}"
            tk.Label(readings_frame, text=reading_info, font=("Helvetica", 12)).pack()
            latest_date = reading_date

        print(latest_date)
        return patient_info['low_glucose'], patient_info['high_glucose'], latest_date
    
    def check_blood_sugar(self, latest_date):
        # Function to check if the user has recorded their blood sugar reading for today
        # In a real application, you would implement logic to check if the reading for today exists in the data
        # For demonstration purposes, let's assume today's date is '2024-04-11'
        today_date = time.strftime('%Y-%m-%d')  # You can get the current date dynamically
        print("DEBUG CBS: ", today_date)
        print("DEBUG CBS: ", latest_date)
        # Check if today's reading is available in the data
        # Replace this with your actual logic to check if the reading for today exists in the data
        reading_available = self.date_matching(today_date, latest_date)
        returner = False
        if not reading_available:
            # If the reading is not available, prompt the user to record it
            returner = self.prompt_record_reading()
        if returner == True:
            return True
        else:
            return False

    def date_matching(self, today_date, latest_date):
        # Function to check if the user has already input their blood sugar for todays date
        if today_date == latest_date:
            return True
        return False

    def prompt_record_reading(self):
        # Function to prompt the user to record their blood sugar reading
        # Display a popup message box
        response = messagebox.askyesno("Record Blood Sugar Reading", "You haven't recorded your blood sugar reading for today. Would you like to record it now?")

        if response == True:
            # If the user wants to record the reading, implement your logic here
            # For demonstration purposes, let's print a message
            return True

            
        elif response == False:
            messagebox.showinfo("Record Immediately!", "Please immediately record your blood sugar level and report back to the app!")

    def show_help(self):
        # Function to display guidance on how the app works
        help_text = """
        Welcome to the Blood Sugar Monitoring App!\n
        This app helps you track your blood sugar levels and provides useful information about your health.\n
        To record your blood sugar level, click on the 'Record Blood Sugar Level' button and enter your reading.\n
        You can also view your past readings in the dashboard.\n
        Once you have logged your blood sugar level, you may want to logout and log back in to refesh your data.\n
        If you need further assistance, please consult your doctor.\n
        """
        messagebox.showinfo("Help", help_text)
    
    def exitApp(self):
        applogic.stop_program()