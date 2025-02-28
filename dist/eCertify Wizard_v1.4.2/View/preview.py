import customtkinter as ctk
from View import widget as wg
from View.Controller.gn_crt import generate_certificate
from View.Controller.dx_t_img import convert_one_img
from PIL import Image
from os.path import join, basename, exists
from os import getcwd, makedirs
from tkinter import filedialog
import tkinter.messagebox as messagebox
from shutil import copytree, rmtree
import threading

frame_width: int
frame_height: int
colors: dict
back_page = False
output_directory = False

root = 'config'
main_preview_page = 'config'
img_name = 'config'
register_page = 'config'
kvscroll_Frame = 'config'
kvcustom_scroll = 'config'
input_file = 'config'
glo_errorLabel = 'config'

saved_disabledText = ['[name]', '[honor]', '[quarter]']
key_value_pairs = ['[name]', '[honor]', '[quarter]']
disable_list = [True, True, True]
output_types = []

disabled_labels = []
key_pre_determine = []
reg_names = []
var_editMode = []
kvPair_widget = []
kvpairLabels = []
kv_delete_btn = []
pre_determine_var = []
predeter_keyLabels = []
default_keys = ['[name]', '[honor]', '[quarter]']

img_progress = None
pdf_progress = None
docx_progress = None

def globalizeData(app, main_register, frameWidth, frameHeight, color_pallete, image_name, registered_names, inputFile, input_file_name):
    global root, frame_height, frame_width, kvPair_widget, kvpairLabels, colors, img_name, reg_names, input_file, inputFile_name, register_page
    try:
        frame_width = frameWidth
        frame_height = frameHeight
        colors = color_pallete
        img_name = image_name
        reg_names = registered_names
        inputFile_name = input_file_name
        register_page = main_register
        root = app
        input_file = inputFile

        return 'Sucess'
        
    except Exception as e:
        return e

def openPreview(master):
    global main_preview_page

    mainFrame = ctk.CTkFrame(
        master,
        width=frame_width,
        height=frame_height,
        fg_color= colors['green']
    )
    main_preview_page = mainFrame

    # SECTION FRAMES
    sidebarSection()
    editingSection()
    
    mainFrame.pack(expand=True, fill=ctk.BOTH)



# ______________________________________________ SIDEBAR SECTION FUNCTION ______________________________________________

def sidebarSection():
    primary_color = colors['matte_black']

    # Side Bar Menu
    sideBarSection = ctk.CTkFrame(
        main_preview_page,
        width= int(frame_width * 0.05),
        height= frame_height,
        fg_color= primary_color,
        corner_radius=0   
    )

    # Previous page button
    top_div = ctk.CTkFrame(
        sideBarSection,
        fg_color= primary_color,
    )

    prevBtn_image = ctk.CTkImage(
        light_image = Image.open('./resources/left-arrows.png'), 
        dark_image = Image.open('./resources/left-arrows.png'), 
        size=(40,40)
    )

    prev_button = wg.newButton(
        top_div,
        width= 40,
        height= 40,
        image= prevBtn_image,
        compound='left',
        text='',
        fg_color= primary_color,
        hover_color= colors['darker_gray'],
        command = goBack_regPage
    )

    prev_button.pack(side=ctk.TOP, padx=10, pady=20)
    top_div.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)

    sideBarSection.pack(side= ctk.LEFT, fill=ctk.Y)



# ______________________________________________ EDITING SECTION FUNCTION ______________________________________________
edit_section_frame = 'config'
def editingSection():
    global edit_section_frame
    editSection = ctk.CTkFrame(
        main_preview_page,
        width=frame_width,
        height=int(frame_height * 0.6),
        fg_color=colors['gray'],
        corner_radius=0   
    )
    edit_section_frame = editSection

    prvs = prev_section()
    wg.n_br_(prvs, 'horizontal', pad_x = 5)

    settingBarFrame = ctk.CTkFrame(
        editSection,
        width=frame_width,
        height=int(frame_height * 0.4),
        corner_radius=0   
    ) 

    format_setting_section(settingBarFrame)
    wg.n_br_(settingBarFrame)
    keyword_setting_section(settingBarFrame)
    
    settingBarFrame.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)
    editSection.pack(side=ctk.RIGHT, expand=True, fill=ctk.BOTH)


# __________________ Key-Word Section __________________

def keyword_setting_section(master):
    global var_editMode, glo_errorLabel, kvedit_mode, kvscroll_Frame, kvcustom_scroll, predeter_keyLabels, output_directory, root

    keyword_section_width = frame_width // 2

    keyword_setting_section = ctk.CTkFrame(
        master,
        width=keyword_section_width,
        height=int(frame_height * 0.4),
        fg_color='white'
    )

    keyword_settings_label = ctk.CTkLabel(
        keyword_setting_section, 
        text="Keyword Settings Section"
    )
    if not root.frame_height <= 830:
        keyword_settings_label.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=10, pady=10)

    keyword_frame = ctk.CTkFrame(
        keyword_setting_section,
        fg_color="transparent",
    )


    # Button frame
    button_frame = ctk.CTkFrame(
        keyword_setting_section,
        fg_color="transparent"
    )

    btnColor = colors['matte_black']
    buttonWidth = 100
    buttonHeight = 40
    btnPadx = 10
    btnPady = 5
    btnHov = 'blue'
    kwScrollWidth = int(keyword_section_width * 0.9)

    # Add button
    add_button = ctk.CTkButton(
        button_frame,
        text="+",
        width= buttonWidth,
        height= buttonHeight,
        fg_color= btnColor,
        hover_color= btnHov,
        command= kv_addEntry
    )


    # Delete button
    edit_button = ctk.CTkButton(
        button_frame,
        text="Save",
        width= buttonWidth,
        height= buttonHeight,
        fg_color= btnColor,
        hover_color= btnHov,
        command= kvpair_edit_mode
    )

    # Clear button
    clear_button = ctk.CTkButton(
        button_frame,
        text="Clear",
        width= buttonWidth,
        height= buttonHeight,
        fg_color= btnColor,
        hover_color= btnHov,
        command= clear_all_kvPairs
    )

    if not root.frame_height < 829:
        add_button.pack(side=ctk.LEFT, padx=btnPadx, pady=btnPady)
        edit_button.pack(side=ctk.LEFT, padx=btnPadx, pady=btnPady)
        clear_button.pack(side=ctk.LEFT, padx=btnPadx, pady=btnPady)
    else:
        add_button.pack(side=ctk.TOP, padx=btnPady, pady=btnPadx)
        edit_button.pack(side=ctk.TOP, padx=btnPady, pady=btnPadx)
        clear_button.pack(side=ctk.TOP, padx=btnPady, pady=btnPadx)

    keywordlist_scroll = ctk.CTkScrollableFrame(
        keyword_frame,
        width=kwScrollWidth,
        border_width=5,
        border_color=colors['matte_black'],
        corner_radius=10,
        fg_color=colors['pale_white'],
    )

    if not root.frame_height < 829:
        errorLabel = ctk.CTkLabel(
            button_frame,
            text= "",
            fg_color= colors['soft_lavender'],
            text_color= 'red',
        )
        errorLabel.pack(side=ctk.LEFT, expand = True, fill=ctk.BOTH)
    else:
        errorLabel = ctk.CTkLabel(
            keyword_setting_section,
            text= "",
            fg_color= colors['soft_lavender'],
            text_color= 'red',
        )
        errorLabel.pack(side=ctk.BOTTOM, pady=10, padx=20 , expand = True, fill=ctk.BOTH)

    
    glo_errorLabel = errorLabel


    # Custom scrollbar with invisible appearance
    custom_scrollbar = ctk.CTkScrollbar(
        keywordlist_scroll,
        orientation='vertical',
        width=0,
        fg_color=colors['pale_white'],  
        button_color=colors['pale_white'], 
        button_hover_color=colors['pale_white'],
        corner_radius=0
    )
    custom_scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

    kvscroll_Frame = keywordlist_scroll
    kvcustom_scroll = custom_scrollbar

    # KV Frames
    key_frame = ctk.CTkFrame(
        keywordlist_scroll,
        width=int(kwScrollWidth * 0.5),
        fg_color=colors['invi'],
        border_width=3,
        border_color='black'
    )

    value_frame = ctk.CTkFrame(
        keywordlist_scroll,
        width=int(kwScrollWidth * 0.5),
        fg_color=colors['invi'],
        border_width=3,
        border_color='black'
    )

    kv_deleteframe = ctk.CTkFrame(
        keywordlist_scroll,
        width=int(kwScrollWidth * 0.2),
        fg_color=colors['invi'],
        border_width=3,
        border_color='black'
    )

        
    key_frame.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=5)
    value_frame.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=5)
    kv_deleteframe.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=5)
    keywordlist_scroll.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH, padx=5, pady=5)

    if not root.frame_height < 829:
        keyword_frame.pack(side=ctk.TOP, expand=True, fill=ctk.X, padx=20, pady=5)
        button_frame.pack(side=ctk.TOP, anchor='nw',expand=True, fill=ctk.BOTH, padx=30, pady=5)
    else:
        keyword_frame.pack(side=ctk.LEFT, expand=True, fill=ctk.X, padx=5, pady=0)
        button_frame.pack(side=ctk.LEFT, anchor='nw',expand=True, fill=ctk.BOTH, padx=5, pady=30)

    keyword_setting_section.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH)

    """ K E Y B I N D S """

    # Edit / Save
    root.bind("<Control-e>", lambda e: kvpair_edit_mode())
    root.bind("<Control-E>", lambda e: kvpair_edit_mode())
    root.bind("<Control-s>", lambda e: kvpair_edit_mode())
    root.bind("<Control-S>", lambda e: kvpair_edit_mode())
    root.bind("<Return>", lambda e: kvpair_edit_mode())

    # Clear
    root.bind("<Control-c>", lambda e: clear_all_kvPairs())
    root.bind("<Control-C>", lambda e: clear_all_kvPairs())

    # Add
    root.bind("<Control-a>", lambda e: kv_addEntry())
    root.bind("<Control-A>", lambda e: kv_addEntry())
    root.bind("<Control-+>", lambda e: kv_addEntry())
    root.bind("<Control-=>", lambda e: kv_addEntry())

    # Scroll
    root.bind("<Down>", lambda e: scroll_to_bottom())
    root.bind("<Up>", lambda e: scroll_to_top())

    # Globalize         0           1             2             3             4
    var_editMode = [key_frame, value_frame, kwScrollWidth, edit_button, kv_deleteframe]

    default_values = ['N A M E', 'H O N O R', 'Q U A R T E R']

    for i in range(3):

        # VALUE
        value_Label = ctk.CTkLabel(
            value_frame,
            text=default_values[i], 
            width=int(var_editMode[2] * 0.5) - 10
        )
        value_Label.pack(side=ctk.TOP, pady=5, padx=5)

        if not back_page:
            # KEY
            key_entry = ctk.CTkEntry(
                key_frame,
                border_color= 'lightblue',
                width=int(var_editMode[2] * 0.5)
            )
            key_entry.pack(side=ctk.TOP, pady=5, padx=10, fill=ctk.X)
            key_entry.insert(0, f'{default_keys[i]}')

            disable_btn = ctk.CTkButton(
                kv_deleteframe, 
                text='ON', 
                width=30,
                fg_color='lightgreen',
                text_color='black',
                command = lambda i=i: disable_keyWord(i)
            )
            disable_btn.pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)
            
            pre_determine_var.append([key_entry, disable_btn])

    kvpair_edit_mode()
    if back_page: 
        output_directory = False
        kvpair_edit_mode()



""" __________________ Key-Value Pair Section __________________ """

# Name/Honor/Quarter takes 1,2,3 ID
kvedit_mode = True
add_on = False

def kvpair_edit_mode():
    global var_editMode, kvPair_widget, kvedit_mode, kvpairLabels, root, add_on

    # Checks if there are empty fields
    for pair in kvPair_widget:
        key = pair[0].get()
        value = pair[1].get()

        if not key or not value:
            glo_errorLabel.configure(text="Can't save empty fields")
            return 

    # BUTTON TOGGLE
    if kvedit_mode or add_on: 
        # STATE: 'save'
        kvedit_mode = False
        add_on = False
        glo_errorLabel.configure(text=". . . SAVING . . .")
        kvpair_save_edit()

    else: 
        # STATE: 'edit'
        kvedit_mode = True
        var_editMode[4].pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=5)
        var_editMode[4].after(100, kv_load_Entries)

var_add_forDelete = False
def kv_addEntry():
    global back_page, var_editMode, var_add_forDelete, kvPair_widget, kvedit_mode, kvpairLabels, root, add_on, kv_delete_btn

    if not kvedit_mode:
        kv_load_Entries()

    var_add_forDelete = True
    var_editMode[3].configure(
        text="Save"
    )
    kvedit_mode = True

    var_editMode[4].pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=5)

    key_entry = ctk.CTkEntry(
        var_editMode[0],
        border_color= colors['matte_red'],
        width=int(var_editMode[2] * 0.5)
    )
    key_entry.pack(side=ctk.TOP, pady=5, padx=10, fill=ctk.X)
    key_entry.focus_set()

    value_entry = ctk.CTkEntry(
        var_editMode[1], 
        border_color= colors['matte_red'],
        width=int(var_editMode[2] * 0.5)
    )
    value_entry.pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)

    delete_btn = ctk.CTkButton(
            var_editMode[4], 
            text='X', 
            width=30,
            fg_color='red',
            command = lambda: print('Something')
    )
    delete_btn.pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)

    kv_delete_btn.append(delete_btn)

    kvPair_widget.append([key_entry, value_entry])

    kvscroll_Frame.after(100, scroll_to_bottom)

    # Allows cursor switching
    key_entry.bind("<Tab>", lambda e: focus_next_entry(e, value_entry))
    value_entry.bind("<Tab>", lambda e: focus_next_entry(e, key_entry))

    add_on = True

    for i, btn in enumerate(kv_delete_btn):
        btn.configure(command = lambda i=i: kv_load_Entries([True, i]))



def focus_next_entry(event, next_widget):
    next_widget.focus_set()
    return "break"

def scroll_to_bottom():
    global kvscroll_Frame
    kvscroll_Frame._parent_canvas.yview_moveto(1.0)

def scroll_to_top():
    global kvscroll_Frame
    kvscroll_Frame._parent_canvas.yview_moveto(0.0)

def is_visible(widget):
    return widget.winfo_ismapped()


def delete_entry(delete_pair):
    global kvPair_widget, kv_delete_btn, var_editMode, kvpairLabels, delete_btn, add_on, var_add_forDelete

    delete_click_index = delete_pair[1]

    kvPair_widget[delete_click_index][0].pack_forget()
    kvPair_widget[delete_click_index][1].pack_forget()
    kvPair_widget.pop(delete_click_index)

    for btn in kv_delete_btn:
        btn.pack_forget()

    delete_btn = []
    kv_delete_btn = []

    # convert Label into Widget
    for i, pair in enumerate(kvPair_widget):
        
        pair[0].pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)
        pair[1].pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)

        # DELETE BUTTON
        delete_btn = ctk.CTkButton(
            var_editMode[4], 
            text='X', 
            width=30,
            fg_color='red',
            command = lambda i=i: kv_load_Entries([True, i])
        )
        delete_btn.pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)
        
        # PARSE
        kv_delete_btn.append(delete_btn)
        kvpairLabels = []



def kv_load_Entries(delete_pair = [False]):
    global var_editMode, kvPair_widget, kvedit_mode, kvpairLabels, kv_delete_btn, root, key_value_pairs

    var_editMode[3].configure(
        text="Save"
    )

    # DELETE
    if delete_pair[0]:  
        delete_entry(delete_pair)
        return

    pre_determine_kvpairs()
    
    delete_btn = []
    kv_delete_btn = []
    kvPair_widget = []

    # convert Label into Widget
    for i, pair in enumerate(kvpairLabels):

        # SETUP
        pair[0].pack_forget()
        pair[1].pack_forget()

        key = pair[0].cget("text")
        value = pair[1].cget("text")

        # KEY
        key_entry = ctk.CTkEntry(
            var_editMode[0], 
            width=int(var_editMode[2] * 0.5) - 10
        )
        key_entry.pack(side=ctk.TOP, pady=5, padx=10, fill=ctk.X)

        key_entry.insert(0, key) # Text
        
        # VALUE
        value_entry = ctk.CTkEntry(
            var_editMode[1], 
            width=int(var_editMode[2] * 0.5) - 10
        )
        value_entry.pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)
        value_entry.insert(0, value) # Text

        # DELETE BUTTON
        delete_btn = ctk.CTkButton(
            var_editMode[4], 
            text='X', 
            width=30,
            fg_color='red',
            command = lambda i=i: kv_load_Entries([True, i])
        )
        delete_btn.pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)
        
        # PARSE
        kv_delete_btn.append(delete_btn)
        kvPair_widget.append([key_entry, value_entry])
        kvpairLabels = []

    if len(kvPair_widget):
        kvPair_widget[0][0].focus_set()

    

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

         0           1             2             3             4
    [key_frame, value_frame, kwScrollWidth, edit_button, kv_deleteframe]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def kvpair_save_edit():
    global var_editMode, disabled_labels, key_pre_determine, predeter_keyLabels, disable_list, default_keys, pre_determine_var, key_value_pairs, kvedit_mode, kvPair_widget, kvpairLabels, kv_delete_btn, root

    # START
    var_editMode[3].configure(
        text="Edit"
    )

    for key in predeter_keyLabels:
        key.pack_forget()
        predeter_keyLabels = []

    key_pre_determine = []
    predeter_keyLabels = []
    for i, pair in enumerate(pre_determine_var):
        pair[0].pack_forget()
        
        if not disable_list[i]:
            # DISABLED KEY
            key_Label = ctk.CTkLabel(
                var_editMode[0], 
                text= pair[0].get(),
                bg_color='#d3d3d3',
                width=int(var_editMode[2] * 0.5) - 10
            )
        else:
            # KEY
            key_Label = ctk.CTkLabel(
                var_editMode[0], 
                text= pair[0].get(),
                bg_color='lightblue',
                width=int(var_editMode[2] * 0.5) - 10
            )

        key_pre_determine.append(key_Label.cget('text'))
        default_keys.append(pair[0].get())
        predeter_keyLabels.append(key_Label)

        key_Label.pack(side=ctk.TOP, pady=5, padx=5)
    
    key_value_pairs = []
    for i, bool in enumerate(disable_list):
        if not bool:
            key_pre_determine[i] = ''

    key_value_pairs.append(key_pre_determine)
    
    # Convert Entry to Label
    for i, pair in enumerate(kvPair_widget):

        # SETUP
        pair[0].pack_forget()
        pair[1].pack_forget()
        key = pair[0].get()
        value = pair[1].get()

        # KEY
        key_Label = ctk.CTkLabel(
            var_editMode[0], 
            text= key,
            width=int(var_editMode[2] * 0.5) - 10
        )
        key_Label.pack(side=ctk.TOP, pady=5, padx=5)

        # VALUE
        value_Label = ctk.CTkLabel(
            var_editMode[1],
            text=value, 
            width=int(var_editMode[2] * 0.5) - 10
        )
        value_Label.pack(side=ctk.TOP, pady=5, padx=5)

        # PARSE
        kvpairLabels.append([key_Label, value_Label])

        key_value_pairs.append([key, value])

    for btn in kv_delete_btn:
        btn.pack_forget()   

    change_preview_image_thread()
    kv_delete_btn = []
    var_editMode[4].pack_forget()


def pre_determine_kvpairs():
    global var_editMode, saved_disabledText, pre_determine_var, default_keys, predeter_keyLabels, disabled_labels, disable_list, key_value_pairs, key_pre_determine

    for label in disabled_labels:
        label.pack_forget()
        
    disabled_labels = []

    for btn in pre_determine_var:
        btn[1].pack_forget()
        pre_determine_var = []

    for key in predeter_keyLabels:
        key.destroy()

    predeter_keyLabels = []

    for i in range(3):

        # KEY
        if not disable_list[i]:
            key_entry = ctk.CTkEntry(
                var_editMode[0],
                border_color= 'lightblue',
                width=int(var_editMode[2] * 0.5),
                justify='center',
                fg_color='#d3d3d3',
                state = 'normal'
            )
            key_entry.delete(0, ctk.END)
            key_entry.insert(0, saved_disabledText[i])
            key_entry.configure(state = 'disabled')

        else:
            key_entry = ctk.CTkEntry(
                var_editMode[0],
                border_color= 'lightblue',
                width=int(var_editMode[2] * 0.5)
            )
            key_entry.delete(0, ctk.END)
            key_entry.insert(0, key_value_pairs[0][i])

        key_entry.pack(side=ctk.TOP, pady=5, padx=10, fill=ctk.X)

        # DISABLE BUTTON
        if not disable_list[i]:
            disable_btn = ctk.CTkButton(
                var_editMode[4], 
                text='OFF', 
                width=30,
                fg_color='red',
                text_color='black',
                command = lambda i=i: disable_keyWord(i)
            )
            
        else:
            disable_btn = ctk.CTkButton(
                    var_editMode[4], 
                    text='ON', 
                    width=30,
                    fg_color='lightgreen',
                    text_color='black',
                    command = lambda i=i: disable_keyWord(i)
            )
        disable_btn.pack(side=ctk.TOP , pady=5, padx=10, fill=ctk.X)

        pre_determine_var.append([key_entry, disable_btn])

def disable_keyWord(i):
    global key_value_pairs, pre_determine_var, disable_list, disabled_labels, saved_disabledText

    disable_btn = pre_determine_var[i][1]
    entry = pre_determine_var[i][0]

    disable_btn.configure(
        text='ON' if disable_btn.cget('text') == 'OFF' else 'OFF',
        fg_color='lightgreen' if disable_btn.cget('text') == 'OFF' else 'red'
    )

    disable_list[i] = False if disable_btn.cget('text') == 'OFF' else True

    if disable_btn.cget('text') == 'OFF':
        saved_disabledText[i] = entry.get()
        entry.configure(
            justify='center',
            fg_color='#d3d3d3',
            state = 'disabled'
        )
    else:
        entry.configure(
            justify='left',
            fg_color = 'white',
            state = 'normal'
        )
        entry.delete(0, ctk.END)
        entry.insert(0, saved_disabledText[i])
    


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

         0           1             2              3
    [key_frame, value_frame, kwScrollWidth, edit_button]


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
def clear_all_kvPairs(goBack = False):
    global var_editMode, disabled_labels, toggle_disable, disable_dict, predeter_keyLabels, default_keys, key_value_pairs, kvedit_mode, kvPair_widget, kvpairLabels, kv_delete_btn, root, input_file, inputFile_name
    if goBack or messagebox.askokcancel("Confirm", "Are you sure you want to clear all pairs?"):

        if var_editMode:
            kvpair_save_edit()

        for pair in kvPair_widget:
            pair[0].destroy()
            pair[1].destroy()

        for pair in kvpairLabels:
            pair[0].destroy()
            pair[1].destroy()

        for btn in kv_delete_btn:
            btn.destroy()

        for label in disabled_labels:
            label.pack_forget()
        
        disabled_labels = []
        kvPair_widget = []
        kvpairLabels = []
        kv_delete_btn = []
        # toggle_disable = [[True, 0], [True, 1], [True, 2]]
        # disable_dict = {'[name]': False, '[honor]': False, '[quarter]': False}
        redefault = ['[name]', '[honor]', '[quarter]']

        for i, pair in enumerate(pre_determine_var):
            pair[0].delete(0, ctk.END)
            pair[0].insert(0, redefault[i])

        kvpair_save_edit()

# ___________________ Format Section ___________________

fileLabel_format = 'config'
image_checkbox_var = 'config'
pdf_checkbox_var = 'config'
docx_checkbox_var = 'config'
def format_setting_section(master):
    global fileLabel_format, output_types, image_checkbox_var, pdf_checkbox_var, docx_checkbox_var, img_progress, pdf_progress, docx_progress, root
    
    format_output_section = ctk.CTkFrame(
        master,
        fg_color=("#ffffff", "#2986cc"),  # White to blue gradient
        width=frame_width // 2, 
        height=int(frame_height * 0.4),
        corner_radius=0,
        border_width=0.5,
        border_color="#999999"  # Gray border
    )

    # Top section for checkboxes and progress bars
    top_section = ctk.CTkFrame(
        format_output_section,
        fg_color="transparent"
    )
    top_section.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    # Format settings label (only show if window height allows)
    if root.frame_height >= 830:
        Format_settings_label = ctk.CTkLabel(
            top_section, 
            text="Format Settings Section"
        )
        Format_settings_label.pack(side=ctk.TOP, pady=5)

    # Frames for each format type
    docxFrame = ctk.CTkFrame(
        top_section,
        fg_color="transparent"
    )
    docxFrame.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=2)

    pdfFrame = ctk.CTkFrame(
        top_section,
        fg_color="transparent"
    )
    pdfFrame.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=2)

    imgFrame = ctk.CTkFrame(
        top_section,
        fg_color="transparent"
    )
    imgFrame.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=2)

    # CHECKBOXES
    image_checkbox_var = ctk.StringVar()
    image_checkbox = ctk.CTkCheckBox(
        imgFrame, 
        text="Image",
        variable=image_checkbox_var,
        onvalue="IMG",
        offvalue="",
        command=update_output_types
    )
    image_checkbox.pack(side=ctk.TOP, anchor='w', padx=5, pady=4)

    pdf_checkbox_var = ctk.StringVar()
    pdf_checkbox = ctk.CTkCheckBox(
        pdfFrame,
        text="PDF",
        variable=pdf_checkbox_var,
        onvalue="PDF",
        offvalue="",
        command=update_output_types
    )
    pdf_checkbox.pack(side=ctk.TOP, anchor='w', padx=5, pady=4)

    docx_checkbox_var = ctk.StringVar(value="DOCX")
    docx_checkbox = ctk.CTkCheckBox(
        docxFrame,
        text="DOCX",
        variable=docx_checkbox_var,
        onvalue="DOCX",
        offvalue="",
        command=update_output_types
    )
    docx_checkbox.pack(side=ctk.TOP, anchor='w', padx=5, pady=4)

    # Progress bars
    img_progress = ctk.CTkProgressBar(imgFrame, fg_color='lightblue')
    img_progress.set(0)
    img_progress.pack(side=ctk.TOP, fill=ctk.X, padx=5, pady=4)
    
    pdf_progress = ctk.CTkProgressBar(pdfFrame, fg_color='lightblue')
    pdf_progress.set(0)
    pdf_progress.pack(side=ctk.TOP, fill=ctk.X, padx=5, pady=4)

    docx_progress = ctk.CTkProgressBar(docxFrame, fg_color='lightblue')
    docx_progress.set(0)
    docx_progress.pack(side=ctk.TOP, fill=ctk.X, padx=5, pady=4)

    update_output_types()

    # Bottom section for publish button
    bottom_section = ctk.CTkFrame(
        format_output_section, 
        fg_color="transparent",
        height=60  # Fixed height for button section
    )
    bottom_section.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=5)
    bottom_section.pack_propagate(False)  # Prevent shrinking

    publish_btn = wg.newButton(
        bottom_section,
        text = 'Publish',
        fg_color = colors['matte_black'],
        text_color = "white",
        width = 200,
        height = 40,
        command = publish_certificates_thread
    )
    publish_btn.pack(side=ctk.TOP, expand=True,pady=5)

    format_output_section.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH)

def publish_certificates_thread():
    global output_directory, glo_errorLabel

    # CHECK IF THERES NOTHING CHECKED WHEN TRYING TO PUBLISH
    if len(output_types) == 0:
        return  glo_errorLabel.configure(text="No output format selected")

    open_file_dialog()

    if not output_directory:
        glo_errorLabel.configure(text="No folder selected")
        return
    
    
    glo_errorLabel.configure(text=". . . Generating Certificates . . .")
    img_progress.set(0.1)
    pdf_progress.set(0.1)
    docx_progress.set(0.1)
    threading.Thread(target=add_to_output_directory).start()
    

# SET THE OUTPUT TYPES
def update_output_types():
    global output_types, image_checkbox_var, pdf_checkbox_var, docx_checkbox_var, img_progress, pdf_progress, docx_progress

    # Clear the list
    output_types.clear()

    # Check the state of each checkbox and update the list
    if image_checkbox_var.get():
        output_types.append("IMG")
        img_progress.configure(progress_color='blue')
    else:
        img_progress.configure(progress_color='gray')

    if pdf_checkbox_var.get():
        output_types.append("PDF")
        pdf_progress.configure(progress_color='blue')
    else:
        pdf_progress.configure(progress_color='gray')
        
    if docx_checkbox_var.get():
        output_types.append("DOCX")
        docx_progress.configure(progress_color='blue')
    else:
        docx_progress.configure(progress_color='gray')


# SAVE DIRECTORY
def open_file_dialog():
    global output_directory, fileLabel_format

    output_directory = filedialog.askdirectory()


# COPY THE FILES
def add_to_output_directory():
    global output_directory, reg_names, inputFile_name, img_progress, pdf_progress, docx_progress
    
    # Reset progress bars
    if "IMG" in output_types:
        img_progress.set(0)
        img_progress.pack(side=ctk.TOP, fill=ctk.X, padx=5, pady=5)
    if "PDF" in output_types:
        pdf_progress.set(0)
        pdf_progress.pack(side=ctk.TOP, fill=ctk.X, padx=5, pady=5)
    if "DOCX" in output_types:
        docx_progress.set(0)
        docx_progress.pack(side=ctk.TOP, fill=ctk.X, padx=5, pady=5)

    generate_certificate(reg_names, inputFile_name, output_types, key_value_pairs)

    source_directory = join(getcwd(), 'public')
    base_destination_path = join(output_directory, 'E_Certificate')
    destination_path = base_destination_path

    counter = 1
    while exists(destination_path):
        destination_path = f"{base_destination_path}_{counter}"
        counter += 1
    try:
        # Copy directory
        copytree(source_directory, destination_path)
        glo_errorLabel.configure(text="Certificates published successfully")

        # Delete public folder
        rmtree(source_directory)
    except Exception as e:
        glo_errorLabel.configure(text="Error publishing certificates")


preview_image_frame = 'config'
prvFram_height = 'config'

# ____________________ Preview File ____________________

def prev_section():
    global preview_image_frame, frame_width, prvFram_height, edit_section_frame

    prvFram_height = int(frame_height * 0.6)

    previewFrame = ctk.CTkFrame(
        edit_section_frame,
        width = frame_width,
        height = prvFram_height,
        fg_color= colors['pale_white'],
        corner_radius=0   
    )

    setPreview_image()

    previewFrame.pack(side=ctk.TOP, expand=True, fill=ctk.BOTH)
    return previewFrame

# Reload the template Image
stop_event = threading.Event()
lock = threading.Lock()

def change_preview_image():
    global reg_names, glo_errorLabel

    new_img = convert_one_img(reg_names, inputFile_name, keyValue_pairs= key_value_pairs)

    if new_img is None:
        glo_errorLabel.configure(text = "Error: Image conversion failed.")
        return
    
    new_path = join(getcwd(), 'temporary', new_img) 
    setPreview_image(new_path)

def change_preview_image_thread():
    global stop_event, lock

    # ONLY RUNS THE MOST RECENT THREAD
    stop_event.set()
    stop_event = threading.Event()

    def thread_target():
        lock_acquired = False
        try:
            if not lock.acquire(blocking=False):
                return
            lock_acquired = True

            while not stop_event.is_set():
                change_preview_image()
                glo_errorLabel.configure(text="SAVED SUCCESSFULLY")
                break
        finally:
            if lock_acquired:
                lock.release()
    
    # STARTS A NEW THREAD
    threading.Thread(target=thread_target).start()


# Add prev-image
preview_image_show = 'config'
def setPreview_image(new_path = False):
    global preview_image_frame, preview_image_show, img_name, prvFram_height, edit_section_frame, frame_width
    
    # CHANGING THE IMAGE
    if new_path:
        img_path = new_path

        try:
            light_img = Image.open(img_path)

            original_width, original_height = light_img.size 

            image_aspect_ratio = original_width / original_height 
            frame_aspect_ratio = frame_width / prvFram_height 
            
            if image_aspect_ratio > frame_aspect_ratio: 
                new_width = frame_width 
                new_height = int(frame_width / image_aspect_ratio) 
            else:
                new_height = prvFram_height 
                new_width = int(prvFram_height * image_aspect_ratio) 
            
            # RESIZED IMAGE
            resized_image = light_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # ORIGINAL IMAGE
            template_image = ctk.CTkImage( 
                light_image= resized_image, 
                size= resized_image.size
            )

            preview_image_show.configure(image=template_image)

        except FileNotFoundError:
            print(f'setPreview_image() - New path File not found: {img_path}')
        except Exception as e:
            print(f"setPreview_image() - New path Error loading image: {e}")

        return


    # ADD STARTING IMAGE
    img_path = join(getcwd(), 'temporary', img_name) 

    try:
        light_img = Image.open(img_path)

        original_width, original_height = light_img.size 

        image_aspect_ratio = original_width / original_height 
        frame_aspect_ratio = frame_width / prvFram_height 
        
        if image_aspect_ratio > frame_aspect_ratio: 
            new_width = frame_width 
            new_height = int(frame_width / image_aspect_ratio) 
        else:
            new_height = prvFram_height 
            new_width = int(prvFram_height * image_aspect_ratio) 
        
        # RESIZED IMAGE
        resized_image = light_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # ORIGINAL IMAGE
        template_image = ctk.CTkImage( 
            light_image= resized_image, 
            size= resized_image.size
        )

        showImage = ctk.CTkLabel(
            edit_section_frame,
            image= template_image,
            text=''
        )
        showImage.pack(expand=True, fill=ctk.BOTH)
        preview_image_show = showImage

    except FileNotFoundError:
        print(f'setPreview_image() - File not found: {img_path}')
    except Exception as e:
        print(f'setPreview_image() - Error {e}')

    return

def goBack_regPage():
    global kvPair_widget, kvpairLabels, kvedit_mode, back_page, add_on, key_value_pairs, disable_list

    if not kvedit_mode:
        kvpair_edit_mode()

    back_page = True

    register_page.pack(expand=True, fill=ctk.BOTH)
    main_preview_page.pack_forget()

    # Reset key-value pairs to only have pre-determined labels
    disable_list = [True, True, True]
    clear_all_kvPairs(True)

