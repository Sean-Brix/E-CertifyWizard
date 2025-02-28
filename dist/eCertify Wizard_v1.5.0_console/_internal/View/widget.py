import customtkinter as ctk

colors = {
        'matte_black': '#2B2B2A',
        'pale_white': '#f5f5f5',
        'gray': '#c0c0c0',
        'darker_gray': '#a9a9a9',
        'soft_lavender': '#E6E6FA',
        'green': 'lightgreen'
}

font = {
    'first':("Helvetica", 25)
}

# Button
def newButton(master: ctk.CTkFrame, **kwargs):
    kwargs.setdefault('text', 'Default Text')
    kwargs.setdefault('width', 20)
    kwargs.setdefault('height', 3)
    kwargs.setdefault('corner_radius', 5)
    kwargs.setdefault('hover_color', colors['gray'])
    kwargs.setdefault('command', lambda: print("Button Clicked"))

    newButton = ctk.CTkButton(master, **kwargs)
    return newButton

# Text
def newText(master: ctk.CTkFrame, **kwargs):
    kwargs.setdefault('width', 50)
    kwargs.setdefault('height', 3)
    kwargs.setdefault('font', font['first'])

    newText = ctk.CTkTextbox(master, **kwargs)
    return newText

# Entries
def newEntry(master: ctk.CTkFrame, **kwargs):
    kwargs.setdefault('width', 10)
    kwargs.setdefault('font',  font['first'])

    newEntry = ctk.CTkEntry(master, **kwargs)
    return newEntry

# Line
def n_br_(master, orientation = 'vertical', pad_y = 0, pad_x = 0, **kwargs):
    kwargs.setdefault('fg_color', colors['matte_black'])
    kwargs.setdefault('border_color', colors['matte_black'])
    kwargs.setdefault('corner_radius', 5)
    kwargs.setdefault('width', 2)
    kwargs.setdefault('height', 2)


    line = ctk.CTkFrame(master, **kwargs)

    match orientation.lower():
        case 'vertical':
            line.pack(side = ctk.LEFT, pady = pad_y, padx = pad_x, fill=ctk.Y)
        case 'horizontal':
            line.pack(side = ctk.TOP, pady = pad_y, padx = pad_x, fill=ctk.X)
        case _:
            return print('Invalid Orientation [Cant add line]')
    
    return line

    