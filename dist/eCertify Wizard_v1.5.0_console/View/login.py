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
    password_entry.pack(pady=(10, 0), padx=50)
    
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

def open_controls_page(master):
    controls_window = ctk.CTkToplevel()
    controls_window.title("Controls")
    controls_window.geometry("900x800")  # Increased window size

    controls_frame = ctk.CTkFrame(
        controls_window,
        fg_color=("#1F1F1F", "#454545"),
        bg_color=("#1F1F1F", "#454545")
    )
    controls_frame.pack(expand=True, fill="both")

    def on_close():
        controls_window.destroy()
        master.deiconify()

    controls_window.protocol("WM_DELETE_WINDOW", on_close)

    # Add a scrollable frame with increased width
    scrollable_frame = ctk.CTkScrollableFrame(
        controls_frame,
        width=880,
        height=780,
        fg_color=("#1F1F1F", "#454545"),
        bg_color=("#1F1F1F", "#454545")
    )
    scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Load all guide images
    guide_images = []
    for i in range(11):  # 0 to 11
        try:
            img = Image.open(f"./resources/guide/{i}.png")
            # Increased image size
            guide_images.append(ctk.CTkImage(light_image=img, dark_image=img, size=(700, 400)))
        except Exception as e:
            print(f"Error loading image {i}: {e}")

    questions = [
        ("How to register?", "To register, simply click the register button, and the system will ask you the admin code, the admin code are only shared to some people who been grant an access to the application, insuring that only some of people can use the application, after typing the admin code, you need to type your own username and password, after typing your username and password, you'll be automatically transfer to the first page where you can log in your account that you already registered."),
        ("Adding a template", "To add a template, go to the templates section on the left side. Choose from a list of available templates and click on the one you'd like to use. Once selected, you can customize it."),
        ("Want to use your own template?", "Adding a custom template is as easy as clicking the Open File button under the custom label, with this we can add our own template allowing for more control over our certificate design."),
        ("Adding a List of name", "To add multiple names or list, click the 'Add List' button next to the 'Name' label. You can either manually add student names by typing them in or attach a file from Excel or Notepad with the student names. Follow the prompts to complete this step."),
        ("Selecting honors and quarters", "To select honors and quarters, you can manually type your own or go to the honors label, use the drop-down selection menu, select the appropriate honors (e.g., With High Honors) and specify the relevant quarter (e.g., Q3). This will personalize your certificates."),
        ("How to delete or edit registered name", "To delete or edit a name that already registered, you can see a logo on the right side of name's, tap it and u will see a button for editing, and deleting."),
        ("Preview page", "This page is made up of three parts, the preview image, the key-value pairs, and the format settings. This page is responsible for editing the final outcome of the generated certificates."),
        ("Keyword settings section?", "This section has two main components the keys and values, the words on the left side(keys) represents the text you want the system to search while the right side (values) are the words you want to replace those words with. If multiple intance of the same key word is found, all of it are replaced with the value. The three existing keywords represents the names/honor/quarter, the key you add on the NAME value will replace that key with the current name of the list."),
        ("Key-Value Pair Controls", "You can add a new pair, delete, save, and clear with all the surrounding button. With this example i added the key DATE, the system will search for all the words DATE on the template and replace it with the TIME value."),
        ("Result: ", ""),
        ("Publishing", "Once you've finished editing, choose the format you desired in your certificate, you can choose pdf, docx, image, or all format at the same time. When everything is ready, you can then download all the files by clicking the publish button, depending on the amount, it may take some time for the system to finish generating the certificates.")
    ]

    for idx, (question, answer) in enumerate(questions):
        # Question Label
        question_label = ctk.CTkLabel(
            scrollable_frame,
            text=question,
            font=('Century Gothic', 15, 'bold'),
            text_color="white",
            anchor='w'
        )
        question_label.pack(pady=(30, 2), padx=20, anchor='w')  # Reduced from (10, 5)

        # Answer Label with increased wraplength
        answer_label = ctk.CTkLabel(
            scrollable_frame,
            text=answer,
            font=('Century Gothic', 12),
            text_color="white",
            anchor='w',
            wraplength=850,
            justify='left'
        )
        answer_label.pack(pady=(0, 20), padx=20, anchor='w')  # Reduced from (0, 10)

        # Add image after each Q&A if available
        if idx < len(guide_images):
            image_label = ctk.CTkLabel(
                scrollable_frame,
                text="",
                image=guide_images[idx]
            )
            image_label.pack(pady=(30, 10))  # Reduced from (0, 20)

    # Center the window on screen
    controls_window.update_idletasks()
    screen_width = controls_window.winfo_screenwidth()
    screen_height = controls_window.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 800) // 2
    controls_window.geometry(f"900x800+{x}+{y}")

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
    password_entry.pack(pady=(10, 0), padx=40)
    
    
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

            print("Login Successful")
            loginWindow.forget()
            registerStudents(master, frame_width, frame_height)
            master.after(500, set_fullscreen) 
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

    def on_register_hover(event):
        register_label.configure(text_color="#007BFF")

    def on_register_leave(event):
        register_label.configure(text_color="lightgray")

    register_label = ctk.CTkLabel(
        login_frame, 
        text="Register Account", 
        font=('Century Gothic', 12, "underline"),
        text_color="lightgray",
        cursor="hand2"
    )
    register_label.pack(pady=(0, 5), anchor="e", padx=48)
    register_label.bind("<Button-1>", lambda e: handle_register(master))
    register_label.bind("<Enter>", on_register_hover)
    register_label.bind("<Leave>", on_register_leave)
    login_button.pack(pady=(5,10))

    controls_button = ctk.CTkButton(
        login_frame, 
        text="Open Controls", 
        command=lambda: open_controls_page(master),
        width=220,
        corner_radius=6,
        fg_color="#2E8B57",
        text_color="#E0E0E0"
    )
    controls_button.pack(pady=(0, 40))

    master.bind('<Return>', lambda event: login()) 
    
    return login_frame

