import socket
import threading

SERVER = '127.0.0.1'
PORT = 1234


def listen_server(client):
    while True:
        msg = client.recv(2048).decode('utf-8')
        if msg != '':
            username = msg.split("%")[0]
            payload = msg.split("%")[1]

            print(f'{username}: {payload}')
        else:
            print(f'The message received is empty')


def send_msg(client):
    while True:
        msg = input("You: ") 
        if msg != '':
            client.sendall(msg.encode())
        else:
            print("Empty message")
            continue

def connect(client):

    username = input("Enter your username: ")

    if username != '':
        # sending username to server
        client.sendall(username.encode())
    else:
        print('Please enter your username.')
        exit(0)

    threading.Thread(target=listen_server, args=(client, )).start()
    send_msg(client)

def main():

    # socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # server connection
    try:
        client.connect((SERVER, PORT))
        print('Client successfully connected')
    except:
        print(f"Could not connect to server {SERVER} {PORT}")

    connect(client)

if __name__ == '__main__':
    main()