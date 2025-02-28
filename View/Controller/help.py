import customtkinter as ctk
from PIL import Image

def open_controls_page(main_window):
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
        main_window.deiconify()

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

    # Keep the window on top
    controls_window.attributes("-topmost", True)
