import customtkinter as ctk
from tkinter import messagebox
import os
import re
from View.register import registerStudents
from PIL import Image

def validate_credentials(username, password):
    # Check if username starts with letter and contains no special characters
    if not username[0].isalpha() or not re.match("^[a-zA-Z0-9]*$", username):
        return False, "Username must start with a letter and contain no special characters"
    
    if not re.match("^[a-zA-Z0-9]*$", password):
        return False, "Password must not contain special characters"
    
    return True, "Valid credentials"

def check_existing_username(username):
    if not os.path.exists("account/username.txt"):
        return False
    
    with open("account/username.txt", "r") as file:
        usernames = file.read().splitlines()
        return username in usernames

def verify_login(username, password):
    if not os.path.exists("account/username.txt") or not os.path.exists("account/password.txt"):
        return False
    
    with open("account/username.txt", "r") as ufile, open("account/password.txt", "r") as pfile:
        usernames = ufile.read().splitlines()
        passwords = pfile.read().splitlines()
        
        try:
            index = usernames.index(username)
            return passwords[index] == password
        except ValueError:
            return False

def save_credentials(username, password):
    os.makedirs("account", exist_ok=True)
    
    with open("account/username.txt", "a") as ufile, open("account/password.txt", "a") as pfile:
        ufile.write(f"{username}\n")
        pfile.write(f"{password}\n")

def handle_register(master):
    # Hide the main window when the register window is opened
    master.withdraw()

    register_window = ctk.CTkToplevel()
    register_window.title("Register")
    register_window.geometry("300x400")

    regFrame = ctk.CTkFrame(
        register_window,
        fg_color=("#1F1F1F", "#454545"),
        bg_color=("#1F1F1F", "#454545")  
    )
    regFrame.pack(expand=True, fill="both")

    
    def on_close():
        register_window.destroy()
        # show the main window when the register window is closed
        master.deiconify() 

    register_window.protocol("WM_DELETE_WINDOW", on_close)

    def verify_app_code():
        app_code = app_code_entry.get()
        try:
            with open("account/admin.txt", "r") as file:
                admin_codes = file.read().splitlines()
                if app_code in admin_codes:
                    app_code_frame.pack_forget()
                    register_frame.pack(pady=100, padx=40)
                    # Resize the register window to match the main window
                    master.update_idletasks()

                    vp_width = master.winfo_screenwidth()
                    vp_height = master.winfo_screenheight()

                    screen_x = (vp_width - 600) // 2
                    screen_y = (vp_height - 800) // 2
                    register_window.geometry(f'600x650+{screen_x}+{screen_y}')
                else:
                    messagebox.showerror("Error", "Incorrect Code")
        except FileNotFoundError:
            messagebox.showerror("Error", "Admin codes file not found")
    def register():
        username = username_entry.get()
        password = password_entry.get()
        
        valid, message = validate_credentials(username, password)
        if not valid:
            messagebox.showerror("Error", message)
            return
        
        if check_existing_username(username):
            messagebox.showerror("Error", "Username already exists")
            return
        
        save_credentials(username, password)
        messagebox.showinfo("Success", "Registration successful!")
        register_window.destroy()
        master.deiconify()  # Remap the main window when registration is successful
    
    app_code_frame = ctk.CTkFrame(
        regFrame,
        fg_color="#353535",
        bg_color="#353535", 
        border_width=4,
        corner_radius=15
    )
    app_code_frame.pack(pady=60)
    
    ctk.CTkLabel(
        app_code_frame, 
        text="Enter Admin Code",
        font=('Century Gothic', 15),
        text_color="white",
    ).pack(pady=(20, 10))

    app_code_entry = ctk.CTkEntry(
        app_code_frame, 
        show="*",
        placeholder_text="Admin Code",
    )
    app_code_entry.pack(pady=10, padx=40)

    verify_button = ctk.CTkButton(
        app_code_frame, 
        text="Verify", 
        command=verify_app_code
    )
    verify_button.pack(pady=(10, 40))
    

    # REGISTER WINDOW
    register_frame = ctk.CTkFrame(
        regFrame,
        fg_color="#353535",
        bg_color="#353535", 
        border_width=4,
        corner_radius=15
    )

    ctk.CTkLabel(
        register_frame, 
        text="Register an Account", 
        font=('Century Gothic', 15),
        text_color="white"
    ).pack(pady=(45, 10))
    
    username_entry = ctk.CTkEntry(
        register_frame,
        placeholder_text="Usename",
        width=230
    )
    username_entry.pack(pady=10, padx=50)

    password_entry = ctk.CTkEntry(
        register_frame, 
        show="*",
        placeholder_text="Password",
        width=230
    )
    password_entry.pack(pady=10, padx=50)
    
    register_button = ctk.CTkButton(
        register_frame, 
        text="Register",
        command=register,
        width=220,
    )
    register_button.pack(pady=(20, 40))

    # Center the register window on the screen
    register_window.update_idletasks()
    
    screen_x = (register_window.winfo_screenwidth() - 400) // 2
    screen_y = (register_window.winfo_screenheight() - 500) // 2
    register_window.geometry(f'400x300+{screen_x}+{screen_y}')

    # Bind Enter key to verify and register functions
    register_window.bind('<Return>', lambda event: verify_button.invoke() if app_code_frame.winfo_ismapped() else register_button.invoke())

def open_login_page(master):

    loginWindow = ctk.CTkFrame(
        master, 
        width=600, 
        height=700,
        fg_color=("#1F1F1F", "white"),  
    )
    loginWindow.pack(fill="both", expand=True)

    login_frame = ctk.CTkFrame(
        loginWindow, 
        width=600, 
        height=700,
        fg_color="#353535",
        bg_color="#353535", 
        border_width=4,
        corner_radius=15
    )
    login_frame.place(relx=0.5, rely=0.45, anchor="center")
    
    ctk.CTkLabel(
        login_frame, 
        text="Log into your Account", 
        font=('Century Gothic', 20),
        text_color="#E0E0E0"
    ).pack(pady=(45, 20))
    
    username_entry = ctk.CTkEntry(
        login_frame, 
        placeholder_text="Username",
        width=230
    )
    username_entry.pack(pady=10, padx=40)
    
    password_entry = ctk.CTkEntry(
        login_frame, 
        placeholder_text="Password", 
        show="*",
        width=230
    )
    password_entry.pack(pady=10, padx=40)
    
    
    def set_fullscreen(event=None):
        master.state('zoomed')
        master.bind('<Escape>', exit_fullscreen) 

    def exit_fullscreen(event=None): 
        master.attributes('-fullscreen', False)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        
        if verify_login(username, password):
            vp_width = master.winfo_screenwidth()
            vp_height = master.winfo_screenheight()

            min_width = 1120 
            min_height = 830

            if vp_width < min_width:
                frame_width = vp_width
                frame_x = 50
                min_width = vp_width
            else:
                frame_width = max(int(vp_width * 0.65), min_width)
                frame_x = (vp_width - frame_width) // 2

            if vp_height < min_height:
                frame_height = vp_height
                frame_y = 50
                min_height = vp_height
            else:
                frame_height = max(int(vp_height * 0.8), min_height)
                frame_y = (vp_height - frame_height) // 2

            master.geometry(f'{frame_width}x{frame_height}+{frame_x}+{frame_y}')

            master.resizable(True, True)
            master.minsize(min_width, min_height)
            master.frame_width = frame_width
            master.frame_height = frame_height
            master.frame_x = frame_x
            master.frame_y = frame_y
            master.min_height = min_height

            loginWindow.destroy()
            registerStudents(master, frame_width, frame_height)
            master.after(100, set_fullscreen)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    login_button = ctk.CTkButton(
        login_frame, 
        text="Login", 
        command=login,
        width=220,
        corner_radius=6,
        fg_color="#2E8B57",
        text_color="#E0E0E0"
    )
    login_button.pack(pady=10)

    register_button = ctk.CTkButton(
        login_frame, 
        text="Register", 
        command=lambda: handle_register(master),
        width=220,
        corner_radius=6,
        fg_color="#2E8B57",
        text_color="#E0E0E0"
    )
    register_button.pack(pady=(0, 40))

    master.bind('<Return>', lambda event: login()) 
    
    return login_frame

