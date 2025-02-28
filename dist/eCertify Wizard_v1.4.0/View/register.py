import customtkinter as ctk
from PIL import Image, ImageSequence
from View import widget as wg
from View.preview import openPreview, globalizeData
from View.Controller.dx_t_img import convert_one_img
from tkinter import filedialog
from os.path import basename, join
from os import getcwd, makedirs
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


""" ~~~~~~~~~ DECORATORS ~~~~~~~~~ """

def bind_sidebar_toggle(func):
    global is_sidebar_visible

    def wrapper(*args, **kwargs):
        close_sidebar_asClicked()
        return func(*args, **kwargs)
    return wrapper


""" ~~~~~~~~~ MAIN WIDGETS ~~~~~~~~~ """

def registerStudents(master, frame_width, frame_height):
    global root, main_register, frameWidth, frameHeight
    
    mainFrame = ctk.CTkFrame(
        master,
        width = frame_width,
        height = frame_height,
        fg_color = colors['pale_white']
    )

    # Globalize Root Config
    main_register = mainFrame
    frameWidth = frame_width
    frameHeight = frame_height
    root = master

    sideBar(mainFrame, frame_width, frame_height)
    nameSection(mainFrame, frame_width, frame_height, master)
    mainFrame.pack(expand=True, fill=ctk.BOTH)

# _______________________________________________ NAME SECTION FUNCTIONS _______________________________________________ 

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

    # Display Name within the scrollable frame
    listFrame = ctk.CTkScrollableFrame(
        nameSection,
        width=section_width,
        height=int(frame_height * 0.5)
    )

    # frame bar, top of the listFrame
    topBarFrame = ctk.CTkFrame(
        listFrame,
        width=section_width,
        height=30,
        fg_color=colors['invi']
    )
    topBarFrame.pack(side=ctk.TOP, fill=ctk.X)

    # "Clear All" button
    clearAllButton = ctk.CTkButton(
        topBarFrame,
        width=150,
        height=40,
        fg_color= colors['matte_black'],
        text="Clear All",
        command=lambda: delete_regName(clear_all=True),
    )

    # Register Option
    optionFrame = ctk.CTkFrame(
        nameSection,
        width=frame_width,
        height=frame_height,
        fg_color= colors['pale_white']
    )


    # ComboBox container
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

    # label
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
    
    selectionLabel.pack(side=ctk.LEFT, padx=20, expand = True, fill=ctk.BOTH)
    quarterLabel.pack(side=ctk.LEFT, padx=20, expand = True, fill=ctk.BOTH)

    if not root.frame_height <= 830:
        labelFrame.pack(side=ctk.TOP, expand=True, fill=ctk.X)

    # Dropdown
    selectionBox = ctk.CTkComboBox(
        dropDownFrames, 
        values=[
            "With Honors", 
            "With High", 
            "With Highest",
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

    # Text/Button Register Name
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

    # label
    textInputLabel = ctk.CTkLabel(
        textLabelFrame,
        text= "Name :",
        font=("Helvetica", 25),
        anchor='w',
        justify="left"
    )
    textInputLabel.pack(side=ctk.LEFT, padx=20, pady= 20, fill=ctk.BOTH)

    file_button = ctk.CTkButton(
        textLabelFrame, 
        text="Add List",
        width=150,
        text_color='white',
        command = lambda: name_list_dialog()
    ) 
    
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


     # Line Containers
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
    # Main Frame
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
    # Enter Key Binding
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

    # Insert Parent-Component
    regFrame.pack(side=ctk.BOTTOM, pady=30, padx=30, fill=ctk.X)
    dropDownFrames.pack(side=ctk.BOTTOM, padx=30, pady=5, expand=True, fill=ctk.BOTH) 
    listFrame.pack(padx=50, pady=30, side=ctk.TOP, expand=True, fill=ctk.BOTH)
    optionFrame.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)
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

 # ____________________________ F I L T E R S ____________________________

@bind_sidebar_toggle
def register_filter(input_text, selection, quarter, errorLabel, edit_mode=False, old_name=None, new_name=None):
    
    # Empty Input
    if len(input_text) == 0: 
        errorLabel.configure(text='Please enter a Name')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return
    
    # Input Length
    if len(input_text) < 5:
        errorLabel.configure(text='Name too short')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return

    # Special Characters
    if not all(word.replace('.','').isalpha() for word in input_text.split()): 
        errorLabel.configure(text='Special Characters are not allowed')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return
    
    # Repeated Entries
    for n in name:
        if input_text in n[0] and not edit_mode:
            errorLabel.configure(text=f'{n[0]} is already registered')
            errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
            return
    
    # Repeated Entries Edit Mode
    if edit_mode:
        for n in name:
            if old_name == n[0]:
                continue
            if new_name in n[0]:
                errorLabel.configure(text=f'{n[0]} is already registered')
                errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
                return

    # Empty Selection
    if not selection: 
        errorLabel.configure(text='Please add a Selection Option')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return

    # Empty Quarter
    if not quarter: 
        errorLabel.configure(text='Please add a Quarter Option')
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
        return

    errorLabel.pack_forget()
    return True


# Add Name to list
iter = 1
def registerName(input_text, regline, nameline, selectline, editline, selection, quarter, errorLabel, getName):
    global iter, name, listItem, edit_buttons, glo_clearAllButton

    # Filter
    if not register_filter(input_text, selection, quarter, errorLabel): return
    
    # Clear All Button
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

    # Generated label
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

    # Attribute Space
    attributeSpace = ctk.CTkFrame(
        selectline,
        fg_color= listColor
    )

    # Attribute Label
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

    # Button
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

    # Collect other buttons to disable during editing
    other_buttons = [btn for btn in editline.winfo_children() if btn != editButton]

    # Set the command after the button is created
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
    # Change the button to save mode
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

    # Hide all the current line being edited
    nameLabel.pack_forget()
    honorLabel.pack_forget()
    quarterLabel.pack_forget()
    selectline.pack_forget()

    # switch the label to an entry
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

    # Dropdown for selection
    selection_options = [
        "With Honors", 
        "With High", 
        "With Highest"
    ]
    
    selection_var = ctk.StringVar(value=honorLabel.cget("text"))
    selection_dropdown = ctk.CTkOptionMenu(
        nameline, 
        variable=selection_var, 
        values=selection_options
    )
    selection_dropdown.pack(side=ctk.LEFT, pady=20, padx=15)

    # Dropdown for quarter
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

    deleteButton = ctk.CTkButton(
        nameline, 
        height=20, 
        width=20,
        fg_color='red',
        text='X',
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

    # Update Name list
    selected_line = list(filter(lambda x: x[0] == name_label.cget("text"), name))[0]
    selected_line_index = name.index(selected_line)
    name.pop(selected_line_index)

    # Remove the line from the display
    name_label.pack_forget()
    name_label.master.pack_forget()
    honor_label.master.pack_forget()
    edit_button.pack_forget()

    # Re-enable the other buttons
    for button in edit_buttons:
        button.configure(state="normal")

    selectline.pack(side=ctk.LEFT, expand=True, fill=ctk.X, pady=5, padx=5)

    if len(name) == 0:
        glo_regline.pack_forget()



def save_name(entry, nameLabel, selection_dropdown, honorLabel, quarter_dropdown, quarterLabel, editButton, nameline, selectline, editLine, other_buttons, errorLabel, regline, deleteButton):
    global name

    # Function to save the changes and switch back to the label
    old_name = nameLabel.cget("text").title()
    new_name = entry.get().title()
    new_selection = selection_dropdown.get()
    new_quarter = quarter_dropdown.get()

    # Check if the new values pass the register filter
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

    # Make all labels reappear
    nameLabel.pack(side=ctk.LEFT, pady=20)
    honorLabel.pack(side=ctk.TOP)
    quarterLabel.pack(side=ctk.TOP)
    selectline.pack(side=ctk.LEFT, expand=True, fill=ctk.X, pady=5, padx=5)

    # Change the button back to edit mode
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

    # Re-enable the other buttons
    for button in edit_buttons:
        button.configure(state="normal")

    # Show the edit button again
    editButton.pack(side=ctk.TOP, expand=True)

    # Update the global name list
    for i, item in enumerate(name):
        if item[0] == old_name:
            name[i] = [new_name, new_selection, new_quarter]
            break

def edit_Registered_Line(nameline, attributeLine, editLine, nameLabel, honorLabel, quarterLabel, editButton):
    # Edit Option
    reWrite_name(nameline, attributeLine, editLine, nameLabel, honorLabel, quarterLabel, editButton)
    



# ____________________________ T E M P L A T E   S I D E B A R ____________________________

# ___ SIDEBAR SECTION FUNCTION ___

loading_label = None
loading_animation = None
loading_frame = None
gif_frames = 'config'
preview_btn = 'config'

def sideBar(master, frame_width, frame_height):
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

    # Premade-Section
    premade_temp_sect = ctk.CTkFrame(
        sidebarFrame,
        fg_color= primary_color,
    )
    btnSz = [300, 200]

    template1 = ctk.CTkImage(
        light_image = Image.open('./resources/template_img/template1.png'), 
        dark_image = Image.open('./resources/template_img/template1.png'), 
        size=(
            btnSz[0],
            btnSz[1]
        )
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

    preTemplateLabel = ctk.CTkLabel(
        premade_temp_sect,
        font= text_font,
        text = 'Template',
        anchor='w',
        justify="left",
        text_color= secondary_color
    )
    preTemplateLabel.pack(side=ctk.TOP, expand = True, fill=ctk.BOTH)
    templateImage.pack(side=ctk.TOP)


    # Custom-Section
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
    
    open_file_button = ctk.CTkButton(
        getFileFrame, 
        text="Open File", 
        command= lambda: open_file_dialog(),
        anchor='w'
    )

    open_file_button.pack(side=ctk.TOP, pady=20, padx=25, expand=True, fill=ctk.X) 
    file_label.pack(side=ctk.TOP, pady=10, padx=25, expand=True, fill=ctk.X) 
    getFileFrame.pack(side=ctk.LEFT, pady=10, expand=True, fill=ctk.X) 


    # Preview Section
    preview_btn_sect = ctk.CTkFrame(
        sidebarFrame,
        fg_color= primary_color
    )

    # LOADING ANIMATION
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

    # Create a label for the loading text
    loading_label = ctk.CTkLabel(
        loading_frame,
        text_color= 'white',
        text = "Uploading Template",
        font = ("Helvetica", 12)
    )
    loading_label.pack(side=ctk.LEFT, padx=5)

    # Create a label for the loading animation
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
    
    # Globalize
    preview_btn = previewButton

# Function to update the GIF frames
def update_gif(frame_index):
        global gif_frames, loading_frame

        frame = gif_frames[frame_index]
        loading_animation.configure(image=frame)
        frame_index = (frame_index + 1) % len(gif_frames)
        loading_animation.after(100, update_gif, frame_index)


def toggle_loading_animation():
    """Toggles the loading animation visibility"""
    global loading_label, loading_animation,loading_frame

    if loading_label.winfo_ismapped():
        loading_frame.pack_forget()
    else:
        loading_frame.pack(side=ctk.BOTTOM, expand = True)
        loading_frame.update_idletasks()


# Upload template processor
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

    # Globalize
    input_file = filepath
    input_file_name = filename


# Get File Name List
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
    
    return name_list


# Save template
def save_file(file_path, file_name):

    templateFolder = join(getcwd(), 'custom_template')
    makedirs(templateFolder, exist_ok=True)

    # Current-File Path
    saveto_path = join(templateFolder, file_name)

    try:
        copy(file_path, saveto_path)
        return True
    except Exception as e:
        return None


def create_template_sidebar(master, primary_color, secondary_color):
    """Creates the template selection sidebar"""
    global template_sidebar, pre_template_image

    # Main frame slider
    mainFrame = ctk.CTkFrame(
        master,
        width=300,
        height=frameHeight,
        fg_color=primary_color
    )

    # Title
    title = ctk.CTkLabel(
        mainFrame,
        text="Templates",
        font=("Helvetica", 20, "bold"),
        text_color=secondary_color
    )
    title.pack(pady=10, padx=5)

    # Scrollable container
    scroll_frame = ctk.CTkScrollableFrame(
        mainFrame,
        width= 280,
        height=frameHeight-100,
        fg_color="transparent"
    )
    scroll_frame.pack(pady=5, padx=5, fill="both", expand=True)

    # Template button size
    btn_width = 300
    btn_height = 200

    template_paths = [
        "./resources/template_img/template1.png",
        "./resources/template_img/template2.png",
    ]

    template1 = ctk.CTkImage(
        light_image = Image.open(template_paths[0]), 
        dark_image = Image.open(template_paths[0]), 
        size=(btn_width, btn_height)
    )

    # Add new template button
    btn1 = ctk.CTkButton(
        scroll_frame,
        width=btn_width,
        height=btn_height,
        text="",
        font=("Helvetica", 40),
        fg_color=primary_color,
        hover_color=colors['darker_gray'],
        image= template1,
        command= lambda: templateSelected(1, template1, template_paths)
    )
    btn1.pack(pady=5)

    template2 = ctk.CTkImage(
        light_image = Image.open(template_paths[1]), 
        dark_image = Image.open(template_paths[1]), 
        size=(btn_width, btn_height)
    )

    # Add new template button
    btn2 = ctk.CTkButton(
        scroll_frame,
        width=btn_width,
        height=btn_height,
        text="",
        font=("Helvetica", 40),
        fg_color=primary_color,
        hover_color=colors['darker_gray'],
        image= template2,
        command= lambda: templateSelected(2, template2, template_paths)
    )
    btn2.pack(pady=5)
    
    template_sidebar = mainFrame

    # Initially place it outside view
    mainFrame.place(x=-350, y=0)
    return mainFrame

def templateSelected(template_id: int, image_template: ctk.CTkImage, image_path: list):
    """Handles the template selection"""
    global pre_template_image, pretemplate_image_path

    custom_template_folder = join(getcwd(), 'custom_template')
    makedirs(custom_template_folder, exist_ok=True)
    
    match template_id:
        case 1:
            pre_template_image.configure(image=image_template)
            pretemplate_image_path = image_path[0]
            copy(join(getcwd(), 'template', 'RECOGNITION.docx'), custom_template_folder)
            open_file_dialog(premade_temp=True, pre_made_temp_path = './template/RECOGNITION.docx')

        case 2:
            pre_template_image.configure(image=image_template)
            pretemplate_image_path = image_path[1]
            copy(join(getcwd(), 'template', 'CertificateAppreciation.docx'), custom_template_folder)
            open_file_dialog(premade_temp=True, pre_made_temp_path = './template/CertificateAppreciation.docx')

        case _:
            pre_template_image.configure(image=image_template)

def toggle_template_sidebar():
    """Toggles the template sidebar visibility with animation"""
    global is_sidebar_visible

    def run_animation():
        global template_sidebar, is_sidebar_visible
        if not is_sidebar_visible:
            # Slide in
            template_sidebar.lift()
            for x in range(-308, 20, 20):
                template_sidebar.place(x=x, y=0)
                template_sidebar.update()
                time.sleep(0.005)
            is_sidebar_visible = True
        else:
            # Slide out
            for x in range(20, -330, -20):
                template_sidebar.place(x=x, y=0)
                template_sidebar.update()
                time.sleep(0.005)
            is_sidebar_visible = False

    # Run the animation in a separate thread
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

# Opens next page
def preview_page_setup():
    global premade_template, one_click_preview, glo_errorLabel

    one_click_preview = False

    # Add file to app dir
    if save_file(input_file, input_file_name):
        ...
    else:
        one_click_preview = True
        toggle_loading_animation()
        return glo_errorLabel.configure(text = 'Failed to save template file.')

    # Convert file to image for prev
    img_path = convert_one_img(name, input_file_name)
    if img_path:
        ...
    else:
        one_click_preview = True
        toggle_loading_animation()
        return glo_errorLabel.configure(text = 'Failed to generate Image.')

    # Turn off loading animation
    toggle_loading_animation()

    # Provide all data to next modal/page
    if globalizeData(root, main_register, frameWidth, frameHeight, colors, img_path, name, input_file, input_file_name):
        ...
    else:
        one_click_preview = True
        return glo_errorLabel.configure(text = 'Internal Server Error, Cannot globalize Data.')

    # hide current modal
    main_register.pack_forget()

    one_click_preview = True

    # open next modal
    openPreview(root)