#This subscript was created by G. Jedrzejowski
#It creates a path for a CSV file downloaded from wartosci punktowe google sheet - Regulamin tab

import tkinter as tk
from tkinter import filedialog
import os

def get_csv_path():
    """
    Handles logic for selecting a CSV path. 
    Returns the file path as a string.
    """
    try:
        user_choice = input("Use hardcoded path? (1/0): ")
        # Handle cases where user types nothing or letters
        flag_hardcoded = int(user_choice) if user_choice.isdigit() else 1
    except ValueError:
        print("Invalid input, defaulting to hardcoded path.")
        flag_hardcoded = 1

    if flag_hardcoded == 1:
        csv_file = "csv/wartosci punktowe - Regulamin.csv"
        print(f"Using hardcoded path: {csv_file}")
        return csv_file

    # If flag is 0, open the Window
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    csv_file = filedialog.askopenfilename(
        title="Select your CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if not csv_file:
        print("No file selected. Exiting.")
        return None
    
    print(f"Selected file: {csv_file}")
    return csv_file