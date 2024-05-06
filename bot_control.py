import socket

class BotControl:
    def __init__(self, botaddress_port):
        self.botaddress_port = botaddress_port

    def bot_command(self, move: str, pwm: int) -> None:
        msg4robot = ','.join([move,f'{pwm},{pwm},{pwm},{pwm}'])
        print(msg4robot)
        bytesToSend = str.encode(msg4robot)
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(bytesToSend, self.botaddress_port)

    @staticmethod
    def pwm_map(pinch_distance: int) -> int:
        if pinch_distance < 50:
            return 50
        elif pinch_distance > 255:
            return 255
        else:
            return pinch_distance
