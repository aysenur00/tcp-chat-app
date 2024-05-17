import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
clients = []

# send messages to all the people in the chat room
def send_chat_room(msg):
    for client in clients:
        send_private_msg(msg, client[1])

# send private message
def send_private_msg(msg, client):
    client.sendall(msg.encode())

# listen for messages to come
def listen_port(client, username):

    while True:
        msg = client.recv(2048).decode('utf-8')
        if msg != '':
            final_msg = username + '%' + msg
            send_chat_room(final_msg)
        else:
            print(f'The message sent from client {username} is empty')


# function for handling clients
def client_handler(client):
    #
    while True:
        # 2048 = size of the message
        username = client.recv(2048).decode('utf-8')
        if username != '':
            clients.append((username, client))
            send_chat_room(f"INFO%{username} entered chat room")
            break
        else:
            print("No user connected.")

    threading.Thread(target=listen_port, args=(client, username, )).start()
    
# main function
def main():
    # creating socket class object 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Server has started running on {HOST} {PORT}")
    except:
        print("Unable binding.")

    # limit server with 5 concurrent clients
    server.listen(5)

    while True:
        # client = socket obj of client
        client, addr = server.accept()
        print(f"Client connected with {addr[0]}: {addr[1]}")

        threading.Thread(target= client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()