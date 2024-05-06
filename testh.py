from hand_control import HandTrackingController
import time

bot_address = ('192.168.1.100', 8080)  # Replace with your bot address

def main():
    # Create an instance of HandTrackingController
    controller = HandTrackingController(bot_address)

    # Start hand tracking
    controller.start_tracking()

    # Start gesture tracking
    controller.gesture_tracking()

    # Let the hand tracking and gesture recognition run for some time
    time.sleep(30)  # Adjust the time as needed

    # Clean up resources
    controller.stop()

if __name__ == "__main__":
    main()
