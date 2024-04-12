import tkinter as tk
from login import loginForm
import applogic

root_global = None
login_global = None
dashboard_global = None

def create_root():
    global root_global
    root_global = tk.Tk()
    root_global.title("Diabetes Monitoring System")

def create_login():
    global login_global
    login_global = loginForm(root_global)

def run_application():
    create_root()
    create_login()
    applogic.set_forms(root_global, login_global, dashboard_global)
    root_global.mainloop()

if __name__ =="__main__":
    run_application()