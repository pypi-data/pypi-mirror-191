"""
Official API for ChatGPT
"""
import asyncio
import json
import os
import sys

import socket
import threading
import traceback
from revChatGPT.V2 import Chatbot

class TCPServer:
    def __init__(self,port,args):
        self.port = port
        self.args = args
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
            if self.args.connection_password != None:
                print("Validating connection")
                passwd = self.reliable_recv(client_socket)
                if self.args.connection_password == passwd:
                    print("Validated")
                    self.reliable_send(client_socket, "OK")
                else:
                    print("Invalid")
                    self.reliable_send(client_socket, "Failed")
                    client_socket.shutdown(socket.SHUT_RDWR)
                    return

            print("Logging in...")
            chatbot = Chatbot(
                email=self.args.email,
                password=self.args.password,
                paid=self.args.paid,
                proxy=self.args.proxy,
                insecure=self.args.insecure_auth,
                session_token=self.args.session_token,
            )
            print("Logged in\n")

            while True:
                print("You:")
                prompt = self.reliable_recv(client_socket)
                print(prompt)
                print()
                print("ChatGPT:")
                result_str = ""
                async for line in chatbot.ask(prompt=prompt):
                    result = line["choices"][0]["text"].replace("<|im_end|>", "")
                    print(result, end="")
                    sys.stdout.flush()
                    result_str = result_str + result
                print()
                self.reliable_send(client_socket, result_str)
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
    """
    Testing main function
    """
    import argparse

    print(
        """
        ChatGPT - A command-line interface to OpenAI's ChatGPT (https://chat.openai.com/chat)
        Repo: github.com/acheong08/ChatGPT
        """,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--email",
        help="Your OpenAI email address",
        required=False,
    )
    parser.add_argument(
        "-p",
        "--password",
        help="Your OpenAI password",
        required=False,
    )
    parser.add_argument(
        "--paid",
        help="Use the paid API",
        action="store_true",
    )
    parser.add_argument(
        "--proxy",
        help="Use a proxy",
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        "--insecure-auth",
        help="Use an insecure authentication method to bypass OpenAI's geo-blocking",
        action="store_true",
    )
    parser.add_argument(
        "--session_token",
        help="Alternative to email and password authentication. Use this if you have Google/Microsoft account.",
        required=False,
    )
    parser.add_argument(
        "--connection_password",
        help="TCP connection password",
        required=False,
    )
    args = parser.parse_args()

    tcp_server = TCPServer(5000, args)
    tcp_server.run()
