def set_forms(root, login, dashboard):
    global root_global, login_global, dashboard_global
    root_global = root
    login_global = login
    dashboard_global = dashboard

def stop_program():
    if root_global:
        root_global.destroy()
    if login_global:
        login_global.destroy()
    if dashboard_global:
        dashboard_global.destroy()
