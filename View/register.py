import customtkinter as ctk
from PIL import Image, ImageSequence
from View import widget as wg
from View.preview import openPreview, globalizeData
from View.Controller.dx_t_img import convert_one_img
from View.Controller.help import open_controls_page
from tkinter import filedialog
from os.path import basename, join
from os import getcwd, makedirs, listdir
from shutil import copy
import time
import tkinter.messagebox as messagebox
import threading

name = []
listItem = []
nameList_File = []
edit_buttons = []

frameWidth: int
frameHeight: int
template_sidebar = None 
is_sidebar_visible = False
premade_template = False

root = 'config' 
main_register = 'config'
pre_template_image = 'config'
pretemplate_image_path = 'config'
file_label_global = 'config'

glo_regline = 'config'
glo_nameline = 'config'
glo_selectline = 'config'
glo_quarterBox = 'config'
glo_selectionBox = 'config'
glo_editline = 'config'
glo_errorLabel = 'config'
glo_getName = 'config'
glo_clearAllButton = 'config'
glo_listFrame = 'config'
registerButton = 'config'

iter = 1  # Initialize iter as an integer

colors = {
        'matte_black': '#2B2B2A',
        'pale_white': '#f5f5f5',
        'gray': '#c0c0c0',
        'darker_gray': '#4C4C4B',
        'soft_lavender': '#E6E6FA',
        'green': 'lightgreen',
        'invi': 'transparent',
        'matte_red': 'Firebrick',
}

def bind_sidebar_toggle(func):
    global is_sidebar_visible

    def wrapper(*args, **kwargs):
        close_sidebar_asClicked()
        return func(*args, **kwargs)
    return wrapper

def registerStudents(master, frame_width, frame_height):
    global root, main_register, frameWidth, frameHeight

    mainFrame = ctk.CTkFrame(
        master,
        width = frame_width,
        height = frame_height,
        fg_color = colors['pale_white']
    )

    main_register = mainFrame
    frameWidth = frame_width
    frameHeight = frame_height
    root = master

    print("Register Page - Initializing")
    print(f"Frame Width: {main_register.winfo_width()}, Frame Height: {main_register.winfo_height()}")

    sideBar(mainFrame, frame_width, frame_height, master)
    nameSection(mainFrame, frame_width, frame_height, master)
    mainFrame.pack(expand=True, fill=ctk.BOTH)

    print("Register page - rendered")

def nameSection(master, frame_width, frame_height, root):
    global glo_clearAllButton, registerButton, glo_listFrame, glo_regline, glo_nameline, glo_selectline, glo_selectionBox, glo_quarterBox, glo_editline, glo_errorLabel, glo_getName
    
    section_width = int(frame_width * 0.65)

    nameSection = ctk.CTkFrame(
        master,
        width=section_width,
        height=frame_height,
        fg_color= colors['pale_white']
    )

    create_template_sidebar(nameSection, colors['matte_black'], colors['pale_white'])

    frame_height = main_register.winfo_height()
    listframe_height = int(frame_height * 0.5)

    listFrame = ctk.CTkScrollableFrame(
        nameSection,
        width=section_width,
        height=listframe_height
    )

    topBarFrame = ctk.CTkFrame(
        listFrame,
        width=section_width,
        height=30,
        fg_color=colors['invi']
    )
    topBarFrame.pack(side=ctk.TOP, fill=ctk.X)

    clearAllButton = ctk.CTkButton(
        topBarFrame,
        width=150,
        height=40,
        fg_color= colors['matte_black'],
        text="Clear All",
        command=lambda: delete_regName(clear_all=True),
    )

    optionFrame = ctk.CTkFrame(
        nameSection,
        width=frame_width,
        height=frame_height,
        fg_color= colors['pale_white']
    )

    dropDownFrames = ctk.CTkFrame(
        optionFrame, 
        width=400, 
        height=150, 
        fg_color= colors['pale_white']
    ) 
    
    labelFrame = ctk.CTkFrame(
        dropDownFrames, 
        width=400, 
        height=150, 
        fg_color= colors['pale_white']
    ) 

    selectionLabel = ctk.CTkLabel(
        labelFrame,
        text= "Honor :",
        font=("Helvetica", 25),
        anchor='w',
        justify="left"
    )
    
    quarterLabel = ctk.CTkLabel(
        labelFrame,
        text= "Quarter :",
        font=("Helvetica", 25),
        anchor='w',
        justify="left"
    )
    
    selectionLabel.pack(side=ctk.LEFT, padx=20, expand = True, fill=ctk.X)
    quarterLabel.pack(side=ctk.LEFT, padx=20, expand = True, fill=ctk.X)
    labelFrame.pack(side=ctk.TOP, expand=False, fill=ctk.X)

    selectionBox = ctk.CTkComboBox(
        dropDownFrames, 
        values=[
            "With Honors", 
            "With High Honors", 
            "With Highest Honors",
        ],
        width=200,
        command= lambda e: close_sidebar_asClicked()
    ) 
    selectionBox.bind("<Button-1>", lambda e: close_sidebar_asClicked())
    selectionBox.pack(side=ctk.LEFT, pady=10, padx=50, expand=True, fill=ctk.X) 
    
    quarterBox = ctk.CTkComboBox(
        dropDownFrames, 
        values=[
            "Quarter 1", 
            "Quarter 2", 
            "Quarter 3",
            "Quarter 4"
        ], 
        width=200,
        command= lambda e: close_sidebar_asClicked()
    ) 
    quarterBox.bind("<Button-1>", lambda e: close_sidebar_asClicked())
    quarterBox.pack(side=ctk.RIGHT, pady=10, padx=50, expand=True, fill=ctk.X) 

    regFrame = ctk.CTkFrame(
        optionFrame, 
        fg_color= "#f5f5f5"
    )

    textLabelFrame = ctk.CTkFrame(
        regFrame, 
        width=400, 
        height=150, 
        fg_color= colors['pale_white']
    ) 

    textInputLabel = ctk.CTkLabel(
        textLabelFrame,
        text= "Name :",
        font=("Helvetica", 25),
        anchor='w',
        justify="left"
    )
    textInputLabel.pack(side=ctk.LEFT, padx=20, pady= 20, fill=ctk.BOTH)

    tooltip_frame = ctk.CTkFrame(
        textLabelFrame,
        fg_color=colors['gray'],
        corner_radius=4
    )
    
    file_tooltip = ctk.CTkLabel(
        tooltip_frame,
        text="Register a list of name in text file",
        text_color=colors['matte_black']
    )
    file_tooltip.pack(padx=15, pady=0)
    
    def show_file_tooltip():
        tooltip_frame.place(x=file_button.winfo_x() + 170, y=file_button.winfo_y())
        
    def hide_file_tooltip():
        tooltip_frame.place_forget()

    file_button = ctk.CTkButton(
        textLabelFrame, 
        text="Add List",
        width=150,
        text_color='white',
        command = lambda: name_list_dialog()
    )

    file_button.bind('<Enter>', lambda e: show_file_tooltip())
    file_button.bind('<Leave>', lambda e: hide_file_tooltip())
    
    file_button.pack(side=ctk.LEFT,  padx=20)

    textBox = ctk.CTkFrame(
        regFrame, 
        border_width= 1, 
        corner_radius=6,
        fg_color= colors['pale_white']
    )

    getName = wg.newEntry(
        textBox, 
        border_width= 0, 
        corner_radius=0,
        fg_color= colors['pale_white']
    )

    errorLabel = ctk.CTkLabel(
        textLabelFrame,
        text= "",
        fg_color= colors['soft_lavender'],
        text_color= 'red',
    )

    textLabelFrame.pack(side=ctk.TOP, expand=True, fill=ctk.X)
    getName.pack(pady=10, padx=5, fill=ctk.X)
    textBox.pack(side=ctk.LEFT, pady=20, padx=30, expand=True, fill=ctk.X)

    regline = ctk.CTkFrame(
        listFrame,
    )
    nameline = ctk.CTkFrame(
        regline,
        fg_color = colors['soft_lavender']
    )
    selectline = ctk.CTkFrame(
        regline,
        fg_color = colors['soft_lavender']
    )
    editline = ctk.CTkFrame(
        regline
    )

    regNameButton = wg.newButton(
        regFrame, 
        height=4, 
        width=200,
        text='Register',
        fg_color= colors['matte_black'],
        command=lambda: registerName(
            getName.get().strip().title(),
            regline, 
            nameline,
            selectline,
            editline, 
            selectionBox.get(),
            quarterBox.get(),
            errorLabel,
            getName
        ),
    )
    root.bind("<Return>", lambda event: registerName(
        getName.get().strip().title(),
        regline, 
        nameline,
        selectline,
        editline, 
        selectionBox.get(),
        quarterBox.get(),
        errorLabel,
        getName
    ))
    regNameButton.pack(side=ctk.LEFT, pady=20, padx=30, fill=ctk.BOTH)

    regFrame.pack(side=ctk.BOTTOM, pady=30, padx=30, fill=ctk.X, expand=True)
    dropDownFrames.pack(side=ctk.BOTTOM, padx=30, pady=5, expand=False, fill=ctk.BOTH) 
    listFrame.pack(side=ctk.TOP, padx=50, pady=30, expand=True, fill=ctk.BOTH)
    optionFrame.pack(side=ctk.TOP, expand=False, fill=ctk.BOTH)
    nameSection.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH)
 


    glo_regline = regline
    glo_nameline = nameline
    glo_selectline = selectline
    glo_selectionBox = selectionBox
    glo_quarterBox = quarterBox
    glo_editline = editline
    glo_errorLabel = errorLabel
    glo_getName = getName
    glo_clearAllButton = clearAllButton
    registerButton = regNameButton
    glo_listFrame = listFrame

    root.bind("<Down>", lambda e: scroll_to_bottom())
    root.bind("<Up>", lambda e: scroll_to_top())

def scroll_to_bottom():
    global glo_listFrame
    glo_listFrame._parent_canvas.yview_moveto(1.0)

def scroll_to_top():
    global glo_listFrame
    glo_listFrame._parent_canvas.yview_moveto(0.0)

@bind_sidebar_toggle
def register_filter(input_text, selection, quarter, errorLabel, edit_mode=False, old_name=None, new_name=None):
    if len(input_text) == 0: 
        errorLabel.configure(text='Please enter a Name')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return
    
    if len(input_text) < 5:
        errorLabel.configure(text='Name too short')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return

    if not all(word.replace('.','').isalpha() for word in input_text.split()): 
        errorLabel.configure(text='Special Characters are not allowed')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return
    
    for n in name:
        if input_text in n[0] and not edit_mode:
            errorLabel.configure(text=f'{n[0]} is already registered')
            errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
            return
    
    if edit_mode:
        for n in name:
            if old_name == n[0]:
                continue
            if new_name in n[0]:
                errorLabel.configure(text=f'{n[0]} is already registered')
                errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
                return

    if not selection: 
        errorLabel.configure(text='Please add a Selection Option')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return

    if not quarter: 
        errorLabel.configure(text='Please add a Quarter Option')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return

    errorLabel.pack_forget()
    return True

def registerName(input_text, regline, nameline, selectline, editline, selection, quarter, errorLabel, getName):
    global iter, name, listItem, edit_buttons, glo_clearAllButton

    frame_width = main_register.winfo_width()
    frame_height = main_register.winfo_height()
    print(f"Frame dimensions - Width: {frame_width}, Height: {frame_height}")

    if not register_filter(input_text, selection, quarter, errorLabel): return
    
    glo_clearAllButton.pack(side=ctk.TOP, pady=10)

    getName.delete(0, ctk.END)
    
    fontSize = 20
    textFont = "Helvetica"
    listColor = colors['soft_lavender']

    nameSpace = ctk.CTkFrame(
        nameline,
        corner_radius=0,
        fg_color= listColor
    )

    newLabel = ctk.CTkLabel(
        nameSpace,
        text=input_text,
        font=(textFont, 25),
        anchor='w',
        corner_radius=0,
        fg_color= listColor
    )
    newLabel.pack(side=ctk.LEFT, pady=20)
    nameSpace.pack(side=ctk.TOP, pady=0, padx= 30, expand = True, fill=ctk.BOTH)

    attributeSpace = ctk.CTkFrame(
        selectline,
        fg_color= listColor
    )

    honorSel = ctk.CTkLabel(
        attributeSpace,
        text= selection,
        font=(textFont, fontSize),
        anchor='e',
        fg_color= listColor
    )
    honorSel.pack(side=ctk.TOP)

    quarterSel = ctk.CTkLabel(
        attributeSpace,
        text= quarter,
        font=(textFont, fontSize),
        anchor='e',
        fg_color= listColor
    )
    quarterSel.pack(side=ctk.TOP)
    attributeSpace.pack(side=ctk.TOP, pady=6)

    edit_icon = ctk.CTkImage(
        light_image = Image.open('./resources/edit_line.png'), 
        dark_image = Image.open('./resources/edit_line.png'), 
        size=(30, 30)
    )

    editButton = ctk.CTkButton(
        editline, 
        height=50, 
        width=50,
        image=edit_icon,
        fg_color='transparent',
        text=''
    )
    editButton.pack(side=ctk.TOP, expand=True)
    edit_buttons.append(editButton)

    other_buttons = [btn for btn in editline.winfo_children() if btn != editButton]

    editButton.configure(
        command=lambda: reWrite_name(
            nameSpace, 
            selectline, 
            editline, 
            newLabel, 
            honorSel, 
            quarterSel, 
            editButton, 
            other_buttons,
            errorLabel,
            regline
    ))

    nameline.pack(side=ctk.LEFT, expand=True, fill=ctk.X, pady=5, padx=5)
    selectline.pack(side=ctk.LEFT, expand=True, fill=ctk.X, pady=5, padx=5)
    editline.pack(side=ctk.RIGHT, expand=True, fill=ctk.BOTH, pady=5)
    regline.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

    name.append([input_text, selection, quarter])
    listItem.append([newLabel, honorSel, quarterSel, editButton])
    iter += 1

@bind_sidebar_toggle
def reWrite_name(nameline, selectline, editLine, nameLabel, honorLabel, quarterLabel, editButton, other_buttons, errorlabel, regline):
    global name, edit_buttons
    editButton.configure(
        text="Save", 
        image=None, 
        width=80, 
        height=40, 
        state="normal",
        fg_color= colors['matte_black'], 
        command=lambda: save_name(
            entry, 
            nameLabel, 
            selection_dropdown,
            honorLabel, 
            quarter_dropdown, 
            quarterLabel, 
            editButton, 
            nameline, 
            selectline, 
            editLine, 
            other_buttons,
            errorlabel,
            regline,
            deleteButton
    ))

    nameLabel.pack_forget()
    honorLabel.pack_forget()
    quarterLabel.pack_forget()
    selectline.pack_forget()

    entryFont = ctk.CTkFont(family="Helvetica", size=15)
    entry = ctk.CTkEntry(
        nameline, 
        width=200, 
        height=40,
        font = entryFont
    )
    entry.insert(0, nameLabel.cget("text"))
    entry.pack(side=ctk.LEFT, pady=20)

    for button in edit_buttons:
        button.configure(state="disabled")

    editButton.configure(state="normal")

    selection_options = [
        "With Honors", 
        "With High Honors", 
        "With Highest Honors"
    ]
    
    selection_var = ctk.StringVar(value=honorLabel.cget("text"))
    selection_dropdown = ctk.CTkOptionMenu(
        nameline, 
        variable=selection_var, 
        values=selection_options
    )
    selection_dropdown.pack(side=ctk.LEFT, pady=20, padx=15)

    quarter_options = [
        "Quarter 1", 
        "Quarter 2", 
        "Quarter 3", 
        "Quarter 4"
    ]
    quarter_var = ctk.StringVar(value=quarterLabel.cget("text"))
    quarter_dropdown = ctk.CTkOptionMenu(
        nameline, 
        variable=quarter_var, 
        values=quarter_options
    )
    quarter_dropdown.pack(side=ctk.LEFT, pady=20, padx=15)

    trash_icon = ctk.CTkImage(
        light_image = Image.open('./resources/icons/trash.png'),
        dark_image = Image.open('./resources/icons/trash.png'),
        size=(25, 25)
    )
    
    deleteButton = ctk.CTkButton(
        nameline, 
        height=20, 
        width=20,
        fg_color='transparent',
        text='',
        image=trash_icon,
        command=lambda:
            delete_regName(
                nameLabel,
                honorLabel,
                editButton,
                selectline
            )
    )
    deleteButton.pack(side=ctk.RIGHT, pady=20)

@bind_sidebar_toggle
def delete_regName(name_label=None, honor_label=None, edit_button=None, selectline=None, clear_all=False):
    global name, glo_regline, iter, glo_clearAllButton

    if clear_all and messagebox.askokcancel("Confirm", "Are you sure you want to clear all names?"):
        children = glo_regline.winfo_children()
        for child in children:
            subchildren = child.winfo_children()
            for subchild in subchildren:
                subchild.pack_forget()
        
        iter = 1
        name = []
        glo_regline.pack_forget()
        glo_clearAllButton.pack_forget()
        return
    if clear_all: return

    selected_line = list(filter(lambda x: x[0] == name_label.cget("text"), name))[0]
    selected_line_index = name.index(selected_line)
    name.pop(selected_line_index)

    name_label.pack_forget()
    name_label.master.pack_forget()
    honor_label.master.pack_forget()
    edit_button.pack_forget()

    for button in edit_buttons:
        button.configure(state="normal")

    selectline.pack(side=ctk.LEFT, expand=True, fill=ctk.X, pady=5, padx=5)

    if len(name) == 0:
        glo_regline.pack_forget()

def save_name(entry, nameLabel, selection_dropdown, honorLabel, quarter_dropdown, quarterLabel, editButton, nameline, selectline, editLine, other_buttons, errorLabel, regline, deleteButton):
    global name

    old_name = nameLabel.cget("text").title()
    new_name = entry.get().title()
    new_selection = selection_dropdown.get()
    new_quarter = quarter_dropdown.get()

    if not register_filter(
        new_name, 
        new_selection, 
        new_quarter, 
        errorLabel, 
        edit_mode = True, 
        old_name = old_name, 
        new_name = new_name
    ): return

    nameLabel.configure(text=new_name)
    entry.pack_forget()

    honorLabel.configure(text=new_selection)
    selection_dropdown.pack_forget()

    quarterLabel.configure(text=new_quarter)
    quarter_dropdown.pack_forget()
    deleteButton.pack_forget()

    nameLabel.pack(side=ctk.LEFT, pady=20)
    honorLabel.pack(side=ctk.TOP)
    quarterLabel.pack(side=ctk.TOP)
    selectline.pack(side=ctk.LEFT, expand=True, fill=ctk.X, pady=5, padx=5)

    edit_icon = ctk.CTkImage(
        light_image = Image.open('./resources/edit_line.png'), 
        dark_image = Image.open('./resources/edit_line.png'), 
        size=(30, 30)
    )
    editButton.configure(
        text='', 
        image=edit_icon, 
        width=50, 
        height=50,
        fg_color='transparent',
        command=lambda: reWrite_name(
            nameline, 
            selectline, 
            editLine, 
            nameLabel, 
            honorLabel, 
            quarterLabel, 
            editButton, 
            other_buttons,
            errorLabel,
            regline
    ))

    for button in edit_buttons:
        button.configure(state="normal")

    editButton.pack(side=ctk.TOP, expand=True)

    for i, item in enumerate(name):
        if item[0] == old_name:
            name[i] = [new_name, new_selection, new_quarter]
            break

def edit_Registered_Line(nameline, attributeLine, editLine, nameLabel, honorLabel, quarterLabel, editButton):
    reWrite_name(nameline, attributeLine, editLine, nameLabel, honorLabel, quarterLabel, editButton)

loading_label = None
loading_animation = None
loading_frame = None
gif_frames = 'config'
preview_btn = 'config'

def sideBar(master, frame_width, frame_height, main_window):
    global pre_template_image, preview_btn, file_label_global, loading_label, loading_animation, gif_frames, loading_frame

    primary_color = colors['matte_black']
    secondary_color = colors['pale_white']
    text_font = ("Helvetica", 30)

    sidebarFrame = ctk.CTkFrame(
        master,
        width=int(frame_width * 0.35),
        height=frame_height,
        fg_color= colors['matte_black']
    )

    premade_temp_sect = ctk.CTkFrame(
        sidebarFrame,
        fg_color= primary_color,
    )
    btnSz = [300, 200]

    template1 = ctk.CTkImage(
        light_image = Image.open('./resources/template_img/template1.png'), 
        dark_image = Image.open('./resources/template_img/template1.png'), 
        size=(btnSz[0], btnSz[1])
    )

    templateImage = wg.newButton(
        premade_temp_sect,
        width= btnSz[0],
        height= btnSz[1],
        image= template1,
        compound='left',
        text='',
        fg_color= primary_color,
        command= toggle_template_sidebar
    )
    pre_template_image = templateImage

    label_frame = ctk.CTkFrame(
        premade_temp_sect,
        fg_color= primary_color
    )

    preTemplateLabel = ctk.CTkLabel(
        label_frame,
        font= text_font,
        text = 'Template',
        anchor='w',
        justify="left",
        text_color= secondary_color
    )
    
    add_icon = ctk.CTkImage(
        light_image = Image.open('./resources/icons/help.png'),
        dark_image = Image.open('./resources/icons/help.png'),
        size=(30, 30)
    )
    tooltip = ctk.CTkLabel(
        label_frame,
        text="Help",
        fg_color='gray',
        text_color='black',
        corner_radius=4
    )
    
    def show_tooltip(event):
        tooltip.place(x=helpButton.winfo_x() + 7, y=helpButton.winfo_y() + 45)
        
    def hide_tooltip(event):
        tooltip.place_forget()

    helpButton = ctk.CTkButton(
        label_frame,
        width=40,
        height=40,
        image=add_icon,
        text='',
        fg_color='transparent',
        hover_color=colors['darker_gray'],
        command=lambda: open_controls_page(main_window)
    )
    
    helpButton.bind('<Enter>', show_tooltip)
    helpButton.bind('<Leave>', hide_tooltip)

    preTemplateLabel.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH)
    helpButton.pack(side=ctk.RIGHT)
    label_frame.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)
    templateImage.pack(side=ctk.TOP)

    custom_temp_sect = ctk.CTkFrame(
        sidebarFrame,
        fg_color= primary_color
    )
    cusTempLabel = ctk.CTkLabel(
        custom_temp_sect,
        font= text_font,
        text = 'Custom',
        anchor='w',
        justify="left",
        text_color= secondary_color
    )
    cusTempLabel.pack(side=ctk.TOP, expand = True, fill=ctk.BOTH)

    getFileFrame = ctk.CTkFrame(
        custom_temp_sect,
        fg_color= primary_color
    )

    file_label = ctk.CTkLabel(
        getFileFrame, 
        text="No file selected",
        fg_color= colors['gray'],
    ) 
    file_label_global = file_label
    
    file_tooltip = ctk.CTkLabel(
        getFileFrame,
        text="Use my own template",
        fg_color='white',
        text_color=colors['matte_black'],
        corner_radius=4
    )

    def show_file_tooltip(event):
        file_tooltip.place(x=open_file_button.winfo_x() + 125, y=open_file_button.winfo_y() + 40)
        
    def hide_file_tooltip(event):
        file_tooltip.place_forget()

    open_file_button = ctk.CTkButton(
        getFileFrame, 
        text="Open File", 
        command= lambda: open_file_dialog(),
        anchor='w'
    )

    open_file_button.bind('<Enter>', show_file_tooltip)
    open_file_button.bind('<Leave>', hide_file_tooltip)

    open_file_button.pack(side=ctk.TOP, pady=20, padx=25, expand=True, fill=ctk.X) 
    file_label.pack(side=ctk.TOP, pady=10, padx=25, expand=True, fill=ctk.X) 
    getFileFrame.pack(side=ctk.LEFT, pady=10, expand=True, fill=ctk.X) 

    preview_btn_sect = ctk.CTkFrame(
        sidebarFrame,
        fg_color= primary_color
    )

    gif_path = './resources/icons/loader.gif'
    gif_image = Image.open(gif_path)
    gif_frames = [
        ctk.CTkImage(
            light_image=frame.copy().convert('RGBA').resize((100, 100)),
            dark_image=frame.copy().convert('RGBA').resize((100, 100))
        ) for frame in ImageSequence.Iterator(gif_image)
    ]
    gif_image.close()

    loading_frame = ctk.CTkFrame(
        preview_btn_sect, 
        fg_color= colors['invi'],
        width = 200, 
        height = 200
    )

    loading_label = ctk.CTkLabel(
        loading_frame,
        text_color= 'white',
        text = "Uploading Template",
        font = ("Helvetica", 12)
    )
    loading_label.pack(side=ctk.LEFT, padx=5)

    loading_animation = ctk.CTkLabel(
        loading_frame,
        text='',
        image = gif_frames[0]
    )
    loading_animation.pack(side=ctk.LEFT, padx=5)

    update_gif(0)

    previewButton = ctk.CTkButton(
        preview_btn_sect, 
        text="Preview",
        fg_color= secondary_color,
        corner_radius=15,
        width=180,
        height=80,
        text_color= 'black',
        font=text_font,
        command = lambda: filter_pageProcedure(file_label=file_label)
        
    )

    previewButton.pack(side=ctk.BOTTOM, pady=20, padx=15, expand=True, fill=ctk.X) 
    premade_temp_sect.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH, padx=40, pady=20,)
    custom_temp_sect.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH, padx=40, pady=20,)
    preview_btn_sect.pack(side=ctk.TOP, expand=True, fill=ctk.X, padx=40)
    sidebarFrame.pack(side=ctk.LEFT, fill=ctk.Y)
    
    preview_btn = previewButton

def update_gif(frame_index):
        global gif_frames, loading_frame

        frame = gif_frames[frame_index]
        loading_animation.configure(image=frame)
        frame_index = (frame_index + 1) % len(gif_frames)
        loading_animation.after(100, update_gif, frame_index)

def toggle_loading_animation():
    global loading_label, loading_animation,loading_frame

    if loading_label.winfo_ismapped():
        loading_frame.pack_forget()
    else:
        loading_frame.pack(side=ctk.BOTTOM, expand = True)
        loading_frame.update_idletasks()

input_file = 'config'
input_file_name = 'config'

@bind_sidebar_toggle
def open_file_dialog(premade_temp = False, pre_made_temp_path = None): 
    global input_file, input_file_name, file_label_global, premade_template
    premade_template = False

    if premade_temp:
        filepath = pre_made_temp_path
    else:
        filepath = filedialog.askopenfilename( 
            defaultextension=".docx",
            filetypes=[ 
                ("Document files", "*.docx"), 
                ("PowerPoint files", "*.pptx *.ppt"), 
                ("All files", "*.*") 
            ]
        ) 

    filename = basename(filepath) 

    if not filepath: return
    
    if len(filename) <= 18: 
        file_label_global.configure(text=f"Selected file:      {filename}")
    else:
        file_label_global.configure(text=f"Selected file:      {filename[:18]} . . .")

    input_file = filepath
    input_file_name = filename

def name_list_dialog() -> list:
    global  glo_getName, nameList_File, glo_selectline, glo_nameline, glo_regline, glo_quarterBox, glo_selectionBox, glo_editline, glo_errorLabel

    filepath = filedialog.askopenfilename(
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ]
    )

    if not filepath:
        return

    name_list = []
    with open(filepath, 'r') as file:
        for line in file:
            name_list.append(line.strip())
    
    for name in name_list:
        registerName(
                name.strip().title(),
                glo_regline, 
                glo_nameline,
                glo_selectline, 
                glo_editline,
                glo_selectionBox.get(),
                glo_quarterBox.get(),
                glo_errorLabel,
                glo_getName
        )
    
    print(name_list)

    return name_list

def save_file(file_path, file_name):

    templateFolder = join(getcwd(), 'custom_template')
    makedirs(templateFolder, exist_ok=True)

    saveto_path = join(templateFolder, file_name)

    try:
        copy(file_path, saveto_path)
        return True
    except Exception as e:
        return None

def create_template_sidebar(master, primary_color, secondary_color):
    global template_sidebar, pre_template_image

    mainFrame = ctk.CTkFrame(
        master,
        width=300,
        height=frameHeight,
        fg_color=primary_color
    )

    title = ctk.CTkLabel(
        mainFrame,
        text="Templates",
        font=("Helvetica", 20, "bold"),
        text_color=secondary_color
    )
    title.pack(pady=10, padx=5)

    scroll_frame = ctk.CTkScrollableFrame(
        mainFrame,
        width= 280,
        height=frameHeight-100,
        fg_color="transparent"
    )
    scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)

    btn_width = 300
    btn_height = 200

    template_files = [f for f in listdir('./template') if f.endswith('.docx')]
    template_images = [f for f in listdir('./resources/template_img') if f.lower().endswith('.png')]

    for i, image_file in enumerate(template_images, 1):
        image_path = f'./resources/template_img/{image_file}'
        template_img = ctk.CTkImage(
            light_image = Image.open(image_path),
            dark_image = Image.open(image_path),
            size=(btn_width, btn_height)
        )

        btn = ctk.CTkButton(
            scroll_frame,
            width=btn_width,
            height=btn_height,
            text="",
            font=("Helvetica", 40),
            fg_color=primary_color,
            hover_color=colors['darker_gray'],
            image=template_img,
            command=lambda t=i, img=template_img: templateSelected(t, img)
        )
        btn.pack(pady=5)
    
    template_sidebar = mainFrame

    mainFrame.place(x=-350, y=0)
    return mainFrame

def templateSelected(template_id: int, image_template: ctk.CTkImage):
    global pre_template_image, pretemplate_image_path

    custom_template_folder = join(getcwd(), 'custom_template')
    makedirs(custom_template_folder, exist_ok=True)
    
    pre_template_image.configure(image=image_template)
    pretemplate_image_path = f'./resources/template_img/{template_id}.png'
    copy(join(getcwd(), 'template', f'template{template_id}.docx'), custom_template_folder)
    open_file_dialog(premade_temp=True, pre_made_temp_path = f'./template/template{template_id}.docx')

def toggle_template_sidebar():
    global is_sidebar_visible

    def run_animation():
        global template_sidebar, is_sidebar_visible
        if not is_sidebar_visible:
            template_sidebar.lift()
            for x in range(-308, 20, 20):
                template_sidebar.place(x=x, y=0)
                template_sidebar.update()
                time.sleep(0.005)
            is_sidebar_visible = True
        else:
            for x in range(20, -330, -20):
                template_sidebar.place(x=x, y=0)
                template_sidebar.update()
                time.sleep(0.005)
            is_sidebar_visible = False

    threading.Thread(target=run_animation).start()

def close_sidebar_asClicked():
    global is_sidebar_visible
    if is_sidebar_visible:
        toggle_template_sidebar()

one_click_preview = True
@bind_sidebar_toggle
def filter_pageProcedure(file_label):
    global preview_btn, one_click_preview, is_sidebar_visible

    if len(name) == 0:
        glo_errorLabel.configure(text='Please register a name')
        glo_errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return
    
    if file_label.cget("text") == "No file selected":
        glo_errorLabel.configure(text='Please add a template')
        glo_errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return

    if one_click_preview:
        toggle_loading_animation()
        threading.Thread(target=preview_page_setup).start()
    else:
        return

def preview_page_setup():
    global premade_template, one_click_preview, glo_errorLabel

    one_click_preview = False

    if save_file(input_file, input_file_name):
        ...
    else:
        one_click_preview = True
        toggle_loading_animation()
        return glo_errorLabel.configure(text = 'Failed to save template file.')

    img_path = convert_one_img(name, input_file_name)
    if img_path:
        ...
    else:
        one_click_preview = True
        toggle_loading_animation()
        return glo_errorLabel.configure(text = 'Failed to generate Image. Ensure Microsoft Word or WPS is installed.')

    toggle_loading_animation()

    if globalizeData(root, main_register, frameWidth, frameHeight, colors, img_path, name, input_file, input_file_name):
        ...
    else:
        one_click_preview = True
        return glo_errorLabel.configure(text = 'Internal Server Error, Cannot globalize Data.')

    main_register.pack_forget()

    one_click_preview = True

    openPreview(root)