import tkinter as tk
from tkinter import ttk, filedialog
import threading
from videoDenoiser import denoise

def process_file(file_path):
    """
    This function is executed in a separate thread to avoid blocking the GUI
    It calls the denoise function from videoDenoiser.py
    :param file_path: the path of the file to denoise
    Stores the resulting file in the same directory of the input file
    """
    try:
        denoise(file_path)
        # Display a message box when the process is completed
        tk.messagebox.showinfo(title="Success", message="Completed")
        # Reset the progress bar after completion
        progress_var.set(0)
        progress_bar.stop()
    except Exception as e:
        # Display the error message in a message box
        tk.messagebox.showerror(title="Error", message=str(e))


def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        selected_file.set(file_path)
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)

def execute_process():
    file_path = selected_file.get()
    if file_path:
        # Configure the progress bar
        progress_var.set(0)
        progress_bar.start()

        # Create a separate thread to run the process_file function
        threading.Thread(target=process_file, args=(file_path,), daemon=True).start()

# Create the main window
root = tk.Tk()
# Set the title of the window to "Audio Denoiser" + the emoji for a music note
root.title("Audio Denoiser \U0001F3B5")
root.geometry("500x150")  # Set the initial dimensions of the window
root.resizable(False, False)  # Make the window non-resizable
# Style configuration for the ttk theme
style = ttk.Style()
style.configure('TButton', padding=5)

# Create an entry widget to display the selected file path
selected_file = tk.StringVar()
path_entry = ttk.Entry(root, textvariable=selected_file, state='readonly', width=30)
path_entry.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Create a button with the label "Select" to open the file dialog
open_button = ttk.Button(root, text="Select", command=open_file_dialog)
open_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Create a progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, mode='indeterminate')
progress_bar.grid(row=1, column=0, columnspan=2, pady=10)

# Create a button to execute the process_file function (optional)
execute_button = ttk.Button(root, text="Denoise", command=execute_process)
execute_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the GUI application
root.mainloop()
