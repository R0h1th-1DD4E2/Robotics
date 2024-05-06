import keyboard
from bot_control import BotControl
import time

class KeyboardController:
    def __init__(self, bot_address):
        self.robot_controller = BotControl(bot_address)
        self.pwm = 100

    def increase_pwm(self):
        self.pwm += 10
        if self.pwm > 255:
            self.pwm = 255

    def decrease_pwm(self):
        self.pwm -= 10
        if self.pwm < 50:
            self.pwm = 50

    def run(self):
        while True:
            if keyboard.is_pressed('q'):
                break
            elif keyboard.is_pressed('w') and keyboard.is_pressed('d'):
                self.robot_controller.bot_command('DFRT', self.pwm)  # Forward Right
            elif keyboard.is_pressed('w') and keyboard.is_pressed('a'):
                self.robot_controller.bot_command('DFLT', self.pwm)  # Forward Left
            elif keyboard.is_pressed('s') and keyboard.is_pressed('d'):
                self.robot_controller.bot_command('DWRT', self.pwm)  # Backward Right
            elif keyboard.is_pressed('s') and keyboard.is_pressed('a'):
                self.robot_controller.bot_command('DWLT', self.pwm)  # Backward Left
            elif keyboard.is_pressed('w'):
                self.robot_controller.bot_command('FWD', self.pwm)  # Forward
            elif keyboard.is_pressed('s'):
                self.robot_controller.bot_command('BWD', self.pwm)  # Backward
            elif keyboard.is_pressed('a'):
                self.robot_controller.bot_command('LT', self.pwm)   # Left
            elif keyboard.is_pressed('d'):
                self.robot_controller.bot_command('RT', self.pwm)   # Right
            elif keyboard.is_pressed(' '):
                self.robot_controller.bot_command('STP', 0)   # Stop
            elif keyboard.is_pressed('up'):
                self.increase_pwm()  # Increase PWM
            elif keyboard.is_pressed('down'):
                self.decrease_pwm()  # Decrease PWM

            time.sleep(0.05)