import tkinter as tk

def on_continue_click(window):
    # Close the popup window
    window.destroy()

def popup():
    # Create the main window
    root = tk.Tk()
    root.title("Hand Tracking Reminder")

    # Create the label with the message
    message = "Please keep your hand 25 to 30 cm from the screen for better tracking."
    label = tk.Label(root, text=message)
    label.pack(padx=20, pady=20)

    # Create the continue button
    continue_button = tk.Button(root, text="Continue", command=lambda: on_continue_click(root))
    continue_button.pack(padx=20, pady=10)

    # Run the window
    root.mainloop()

