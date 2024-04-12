import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from loaddata import save_patient_data
import time


class RecordBloodSugarForm:
    def __init__(self, parent, username, low, high, dashboard_instance):
        # Create a new top-level window for recording blood sugar
        self.record_window = tk.Toplevel(parent)
        self.record_window.title(f"Record Blood Sugar Level - {username}")
        self.dashboard_instance = dashboard_instance

        #Prevention of application not exiting propertly
        self.record_window.protocol("WM_DELETE_WINDOW", self.close_record)

        # Center the window
        window_width = 400
        window_height = 300
        screen_width = self.record_window.winfo_screenwidth()
        screen_height = self.record_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.record_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Create a frame for the form
        frame = ttk.Frame(self.record_window, padding=(10, 10, 10, 10))
        frame.pack(expand=True, fill=tk.BOTH)

        # Create and pack widgets for the blood sugar level input
        self.blood_sugar_label = ttk.Label(frame, text="Blood Sugar Level:")
        self.blood_sugar_label.pack(pady=(0, 10))

        self.blood_sugar_entry = ttk.Entry(frame)
        self.blood_sugar_entry.pack(pady=(0, 20))
        
        submit_button = ttk.Button(frame, text="Submit", command=lambda: self.submit_reading(username, low, high))
        submit_button.pack()
        # Create a button to submit the blood sugar level

    def submit_reading(self, username, low, high):
        # This function will handle the submission of the blood sugar reading
        # You can retrieve the blood sugar level from self.blood_sugar_entry.get()
        blood_sugar_level = 0
        blood_sugar_level = int(self.blood_sugar_entry.get())
        if blood_sugar_level <= 0 or blood_sugar_level >= 999 or blood_sugar_level == None:
            messagebox.showerror("Submission Failed", "Invalid number, please enter numbers ranging from 0 to 999")
        else:
            date = time.strftime('%Y-%m-%d')
            if blood_sugar_level >= int(low) and blood_sugar_level <= int(high):
                reason_level = "Normal"
                save_patient_data(username, date, str(blood_sugar_level), reason_level)
            elif blood_sugar_level < int(low):
                reason_level = askstring('Low blood sugar', 'Your blood sugar level seems very low, what\'s the reason?')
                print(reason_level)
                while len(reason_level) <= 4:
                   reason_level = askstring('Low blood sugar', 'Your Answer is invalid, please try again') 
                save_patient_data(username, date, str(blood_sugar_level), reason_level)
            elif blood_sugar_level > int(high):
                reason_level = askstring('High blood sugar', 'Your blood sugar level seems too high, what\'s the reason?')
                print(reason_level)
                while len(reason_level) <= 4:
                   reason_level = askstring('High blood sugar', 'Your Answer is invalid, please try again') 
                save_patient_data(username, date, str(blood_sugar_level), reason_level)
        self.close_record()
    
    def close_record(self):
        # Set record_form_active flag to False
        self.dashboard_instance.record_form_active = False
        self.record_window.withdraw()

            

