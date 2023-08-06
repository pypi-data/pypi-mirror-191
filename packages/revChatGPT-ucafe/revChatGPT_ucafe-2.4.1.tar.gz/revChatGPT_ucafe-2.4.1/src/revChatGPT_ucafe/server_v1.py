"""
Official API for ChatGPT
"""
import asyncio
import json
import os
import sys
from os import environ
from os import getenv
from os.path import exists

import socket
import threading
import traceback
from revChatGPT.V1 import Chatbot

def configure():
    """
    Looks for a config file in the following locations:
    """
    config_files = ["config.json"]
    xdg_config_home = getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        config_files.append(f"{xdg_config_home}/revChatGPT/config.json")
    user_home = getenv("HOME")
    if user_home:
        config_files.append(f"{user_home}/.config/revChatGPT/config.json")

    config_file = next((f for f in config_files if exists(f)), None)
    if config_file:
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)
    else:
        print("No config file found.")
        raise Exception("No config file found.")
    return config

class TCPServer:
    def __init__(self,port,config):
        self.port = port
        self.config = config
        self.connection_password = config.get("connection_password")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Waiting for connection")
    

    def reliable_send(self, client_socket, data):
        json_data = json.dumps(data)
        client_socket.send(json_data.encode('utf-8'))
    
    def reliable_recv(self,client_socket):
        received_data = ""
        while True:
            try:
                received_data = received_data + client_socket.recv(1024).decode('utf-8')
                return json.loads(received_data)
            except ValueError:
                continue
    

    async def client_handler(self,client_socket):
        try:
            if self.connection_password != None:
                print("Validating connection")
                passwd = self.reliable_recv(client_socket)
                if self.connection_password == passwd:
                    print("Validated")
                    self.reliable_send(client_socket, "OK")
                else:
                    print("Invalid")
                    self.reliable_send(client_socket, "Failed")
                    client_socket.shutdown(socket.SHUT_RDWR)
                    return

            print("Logging in...")
            chatbot = Chatbot(self.config)
            print("Logged in\n")

            while True:
                print("You:")
                prompt = self.reliable_recv(client_socket)
                print(prompt)
                print()
                print("ChatGPT:")
                prev_text = ""
                for data in chatbot.ask(
                    prompt,
                    conversation_id=self.config.get("conversation"),
                    parent_id=self.config.get("parent_id"),
                ):
                    result = data["message"][len(prev_text) :]
                    print(result, end="", flush=True)
                    prev_text = data["message"]
                print("\n")
                self.reliable_send(client_socket, prev_text)
        except Exception:
            print(traceback.format_exc())
            client_socket.shutdown(socket.SHUT_RDWR)
        
    def handle(self,client_socket):
        asyncio.run(self.client_handler(client_socket))

    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("Connected from %s:%d" % (client_address[0], client_address[1]))
            t = threading.Thread(target=self.handle, args=(client_socket,))
            t.start()

if __name__ == "__main__":
    tcp_server = TCPServer(5000, configure())
    tcp_server.run()
