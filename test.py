import tkinter as tk
from tkinter import messagebox
import threading
from hand_control import HandTrackingController
from keyboard_control import KeyboardController

class ControlGUI:
    def __init__(self, bot_address):
        self.root = tk.Tk()
        self.root.title("Bot Control")
        self.bot_address = bot_address

        self.hand_tracking_controller = HandTrackingController(bot_address)
        self.keyboard_controller = KeyboardController(bot_address)

        self.mode = "Keyboard"

        self.create_widgets()

    def create_widgets(self):
        self.mode_label = tk.Label(self.root, text="Current Mode: Keyboard", font=("Arial", 12))
        self.mode_label.pack(pady=10)

        self.switch_button = tk.Button(self.root, text="Switch to Hand Gesture Control", command=self.switch_control_mode)
        self.switch_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_program)
        self.quit_button.pack(pady=5)

    def switch_control_mode(self):
        if self.mode == "Keyboard":
            self.mode = "Hand Gesture"
            self.mode_label.config(text="Current Mode: Hand Gesture")
            self.switch_button.config(text="Switch to Keyboard Control")
            threading.Thread(target=self.hand_tracking_controller.gesture_tracking).start()
        else:
            self.mode = "Keyboard"
            self.mode_label.config(text="Current Mode: Keyboard")
            self.switch_button.config(text="Switch to Hand Gesture Control")
            self.hand_tracking_controller.stop_gesture_tracking()
            threading.Thread(target=self.keyboard_controller.run).start()

    def quit_program(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.mode == "Hand Gesture":
                self.hand_tracking_controller.stop_gesture_tracking()
            self.root.destroy()

if __name__ == "__main__":
    bot_address = "your_bot_address_here"
    app = ControlGUI(bot_address)
    app.root.mainloop()
