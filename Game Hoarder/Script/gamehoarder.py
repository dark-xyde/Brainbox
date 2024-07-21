"""
Author: darkXyde
Date: 06-24
Description: [Brief description of what the script does]

This script is a Python application for managing and transferring game files between SSD, HDD, and other storage locations.
It includes features for configuration management, folder scanning, file transfer, and a user interface using Tkinter.

Feel free to modify and adapt this script as needed. A shout-out or mention would be greatly appreciated!

"""


import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import subprocess
import configparser
from threading import Thread
import sys

# Path to save the config file
config_file_path = os.path.expanduser('~/.game_manager/config.ini')

def display_ascii_art():
    ascii_art = r"""
    
                                                                                                                     
 @@@@@@@@   @@@@@@   @@@@@@@@@@   @@@@@@@@     @@@  @@@   @@@@@@    @@@@@@   @@@@@@@   @@@@@@@   @@@@@@@@  @@@@@@@   
@@@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@@@@@@     @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  
!@@        @@!  @@@  @@! @@! @@!  @@!          @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@@  @@!       @@!  @@@  
!@!        !@!  @!@  !@! !@! !@!  !@!          !@!  @!@  !@!  @!@  !@!  @!@  !@!  @!@  !@!  @!@  !@!       !@!  @!@  
!@! @!@!@  @!@!@!@!  @!! !!@ @!@  @!!!:!       @!@!@!@!  @!@  !@!  @!@!@!@!  @!@!!@!   @!@  !@!  @!!!:!    @!@!!@!   
!!! !!@!!  !!!@!!!!  !@!   ! !@!  !!!!!:       !!!@!!!!  !@!  !!!  !!!@!!!!  !!@!@!    !@!  !!!  !!!!!:    !!@!@!    
:!!   !!:  !!:  !!!  !!:     !!:  !!:          !!:  !!!  !!:  !!!  !!:  !!!  !!: :!!   !!:  !!!  !!:       !!: :!!   
:!:   !::  :!:  !:!  :!:     :!:  :!:          :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  :!:       :!:  !:!  
 ::: ::::  ::   :::  :::     ::    :: ::::     ::   :::  ::::: ::  ::   :::  ::   :::   :::: ::   :: ::::  ::   :::  
 :: :: :    :   : :   :      :    : :: ::       :   : :   : :  :    :   : :   :   : :  :: :  :   : :: ::    :   : :                                                                                                                        
     __         __    _  __        __   
 ___/ /__ _____/ /__ | |/_/_ _____/ /__ 
/ _  / _ `/ __/  '_/_>  </ // / _  / -_)
\_,_/\_,_/_/ /_/\_\/_/|_|\_, /\_,_/\__/ 
                        /___/           

                                                        
                                               remain calm
                                
     
                                the slower your drives. 
                                                      the longer it takes.
    
    """       
    print(ascii_art)
    
if __name__ == "__main__":
    display_ascii_art()
    
def save_config(ssd_path, ssd_name, hdd_path, hdd_name, setups_path, setups_name):
    try:
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
        config = configparser.ConfigParser()
        config['Paths'] = {
            'SSDPath': ssd_path,
            'HDDPath': hdd_path,
            'SetupsPath': setups_path
        }
        config['Names'] = {
            'SSDName': ssd_name,
            'HDDName': hdd_name,
            'SetupsName': setups_name
        }
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
    except PermissionError as e:
        messagebox.showerror("Permission Error", f"Unable to save configuration file: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(config_file_path):
        return "F:/Games", "SSD", "D:/Games", "HDD", "E:/Setups/Games", "Setups"
    
    config.read(config_file_path)
    ssd_path = config.get('Paths', 'SSDPath', fallback="F:/Games")
    hdd_path = config.get('Paths', 'HDDPath', fallback="D:/Games")
    setups_path = config.get('Paths', 'SetupsPath', fallback="E:/Setups/Games")
    ssd_name = config.get('Names', 'SSDName', fallback="SSD")
    hdd_name = config.get('Names', 'HDDName', fallback="HDD")
    setups_name = config.get('Names', 'SetupsName', fallback="Setups")
    return ssd_path, ssd_name, hdd_path, hdd_name, setups_path, setups_name

def setup_config():
    def on_finish():
        ssd_path = path_ssd.get()
        hdd_path = path_hdd.get()
        setups_path = path_setups.get()
        ssd_name = name_ssd.get() or "SSD"
        hdd_name = name_hdd.get() or "HDD"
        setups_name = name_setups.get() or "Setups"
        save_config(ssd_path, ssd_name, hdd_path, hdd_name, setups_path, setups_name)
        setup_window.destroy()
        relaunch_app()  # Relaunch the application

    def browse_path(entry):
        folder_selected = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)

    setup_window = tk.Tk()
    setup_window.title("Setup")

    tk.Label(setup_window, text="SSD Game Folder:").pack(pady=5)
    path_ssd = tk.Entry(setup_window, width=50)
    path_ssd.pack(pady=5)
    tk.Button(setup_window, text="Browse", command=lambda: browse_path(path_ssd)).pack(pady=5)

    tk.Label(setup_window, text="Name for SSD (leave blank for default):").pack(pady=5)
    name_ssd = tk.Entry(setup_window, width=50)
    name_ssd.pack(pady=5)

    tk.Label(setup_window, text="HDD Game Folder:").pack(pady=5)
    path_hdd = tk.Entry(setup_window, width=50)
    path_hdd.pack(pady=5)
    tk.Button(setup_window, text="Browse", command=lambda: browse_path(path_hdd)).pack(pady=5)

    tk.Label(setup_window, text="Name for HDD (leave blank for default):").pack(pady=5)
    name_hdd = tk.Entry(setup_window, width=50)
    name_hdd.pack(pady=5)

    tk.Label(setup_window, text="Setups Location:").pack(pady=5)
    path_setups = tk.Entry(setup_window, width=50)
    path_setups.pack(pady=5)
    tk.Button(setup_window, text="Browse", command=lambda: browse_path(path_setups)).pack(pady=5)

    tk.Label(setup_window, text="Name for Setups (leave blank for default):").pack(pady=5)
    name_setups = tk.Entry(setup_window, width=50)
    name_setups.pack(pady=5)

    tk.Button(setup_window, text="Finish", command=on_finish).pack(pady=20)
    setup_window.mainloop()

def relaunch_app():
    """Relaunch the application with updated configuration."""
    python = sys.executable
    os.execv(python, ['python'] + sys.argv)

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024**3)  # Size in GB

def get_free_space(path):
    try:
        return shutil.disk_usage(path).free / (1024**3)  # Free space in GB
    except Exception as e:
        messagebox.showerror("Error", f"Could not access disk space for {path}: {e}")
        return 0

def scan_directory(location):
    folders = []
    try:
        for folder in os.listdir(location):
            folder_path = os.path.join(location, folder)
            if os.path.isdir(folder_path):
                try:
                    folder_size = get_folder_size(folder_path)
                    folders.append((folder, folder_size))
                except Exception as e:
                    messagebox.showerror("Error", f"Could not calculate size for {folder_path}: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not access directory {location}: {e}")
    return folders

def populate_columns():
    for col, location, name in zip([colA, colB, colC], [locA, locB, locC], [nameA, nameB, nameC]):
        # Clear the existing items in the column
        for item in col.get_children():
            col.delete(item)
        
        # Populate folders and sizes
        for folder, size in scan_directory(location):
            col.insert('', 'end', text=folder, values=(f"{size:.2f} GB",))
        
        # Update total size and free space labels
        col_label = col_frame_labels[columns.index(col)]
        total_size = get_folder_size(location)
        free_space = get_free_space(location)
        col_label.config(text=f"{name} ({location}) - Total Size: {total_size:.2f} GB - Free Space: {free_space:.2f} GB")
    
    # Update button texts after columns are populated
    btn_transfer_A_to_B.config(text=f"Transfer to {nameB}")
    btn_transfer_B_to_A.config(text=f"Transfer to {nameA}")

def on_transfer(source_col, source_loc, target_loc):
    selected_folders = [source_col.item(i, 'text') for i in source_col.selection()]
    total_size = sum([get_folder_size(os.path.join(source_loc, folder)) for folder in selected_folders])
    free_space = get_free_space(target_loc)

    confirmation = messagebox.askyesno("Confirm Transfer", 
        f"Total size: {total_size:.2f} GB\n"
        f"Free space: {free_space:.2f} GB\n"
        f"Projected free space after transfer: {(free_space - total_size):.2f} GB\n\n"
        "Do you want to proceed?")
    
    if confirmation:
        transfer_folders(source_col, selected_folders, source_loc, target_loc, total_size)

def transfer_folders(source_col, selected_folders, source_loc, target_loc, total_size):
    progress_win = tk.Toplevel(app)
    progress_win.title("Transferring...")
    progress_label = tk.Label(progress_win, text="Transferring files...")
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_win, length=300, mode='determinate')
    progress_bar.pack(pady=10)

    def move_files():
        num_folders = len(selected_folders)
        for i, folder in enumerate(selected_folders):
            src = os.path.join(source_loc, folder)
            dst = os.path.join(target_loc, folder)
            try:
                shutil.move(src, dst)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move {folder}: {e}")
                continue
            progress_bar['value'] = ((i + 1) / num_folders) * 100
            progress_win.update_idletasks()
        progress_win.destroy()
        populate_columns()

    Thread(target=move_files).start()

def open_folder(event):
    item = colC.selection()[0]
    folder = colC.item(item, 'text')
    folder_path = os.path.join(locC, folder)
    
    folder_path = os.path.normpath(folder_path)
    
    print(f"Opening folder: {folder_path}")  
    
    try:
        subprocess.Popen(f'explorer "{folder_path}"', shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open folder: {e}")

def open_preferences():
    setup_config()

# Initial setup check
if not os.path.exists(config_file_path):
    setup_config()

# Load configuration
locA, nameA, locB, nameB, locC, nameC = load_config()

# Set up the main window
app = tk.Tk()
app.title("Game Library Manager")

# Create a frame for the menu and label
header_frame = tk.Frame(app)
header_frame.pack(fill='x')

# Add the Preferences button
preferences_button = tk.Button(header_frame, text="Preferences", command=open_preferences)
preferences_button.pack(side=tk.LEFT, padx=5, pady=5)

# Add the label with the text
label_text = tk.Label(header_frame, text="May the winds be ever in your favour!")
label_text.pack(side=tk.RIGHT, padx=5, pady=5)

# Create the main frame and other UI elements as before
frame = tk.Frame(app)
frame.pack(fill='both', expand=True)

columns = []
col_frame_labels = []

for i, (location, name) in enumerate([(locA, nameA), (locB, nameB), (locC, nameC)]):
    col_frame = tk.Frame(frame)
    col_frame.grid(row=0, column=i, padx=5, pady=5)
    
    col_label = tk.Label(col_frame, text=f"{name} ({location}) - Total Size: {get_folder_size(location):.2f} GB - Free Space: {get_free_space(location):.2f} GB")
    col_label.pack()
    col_frame_labels.append(col_label)
    
    tree = ttk.Treeview(col_frame, columns=('Size',), show='tree headings', selectmode='extended')
    tree.heading('#0', text='Folder Name')
    tree.heading('Size', text='Size')
    tree.column('Size', width=100)
    tree.pack(expand=True, fill='both')
    
    columns.append(tree)

colA, colB, colC = columns
colC.bind('<Double-1>', open_folder)

# Buttons for transferring files
btn_transfer_A_to_B = tk.Button(frame, text=f"Transfer to {nameB}", command=lambda: on_transfer(colA, locA, locB), bg='lightgrey')
btn_transfer_A_to_B.grid(row=1, column=0)

btn_transfer_B_to_A = tk.Button(frame, text=f"Transfer to {nameA}", command=lambda: on_transfer(colB, locB, locA), bg='lightgrey')
btn_transfer_B_to_A.grid(row=1, column=1)

populate_columns()

# Add a frame at the bottom for the italic text
footer_frame = tk.Frame(app)
footer_frame.pack(side=tk.BOTTOM, fill='x', pady=5)

footer_label = tk.Label(footer_frame, text="Do not panik if it blanks out its just updating.", font=("Arial", 10, "italic"))
footer_label.pack()

app.mainloop()
