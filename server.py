import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
clients = []
messages = []
# send messages to all the people in the chat room
def send_chat_room(msg):
    for client in clients:
        send_private_msg(msg, client[1])

# send private message
def send_private_msg(msg, client):
    client.sendall(msg.encode())

# listen for messages to come
def listen_port(client, username):
    global messages
    while True:
        msg = client.recv(2048).decode('utf-8')
        if msg != '':
            if msg.startswith('/'):
                handle_command(client, username, msg)
            else:
                final_msg = username + '%' + msg
                messages.append((username, msg))
                send_chat_room(final_msg)
        else:
            print(f'The message sent from client {username} is empty')

# handle client commands
def handle_command(client, username, command):
    if command.startswith('/search '):
        # split only once with maxsplit param 1
        keyword = command.split(' ', 1)[1]
        results = search_messages(keyword)
        send_private_msg(f"INFO%Search results for '{keyword}':\n{results}", client)
    
    if command.startswith('/history'):
        send_private_msg(f"INFO%Message history:\n{history()}", client)

# get all messages
def history():
    return '\n'.join([f"{username}: {msg}" for username, msg in messages])

# search keyword
def search_messages(keyword):
    results = [f"{username}: {msg}" for username, msg in messages if keyword in msg]
    return '\n'.join(results) if results else "No messages found."


# function for handling clients
def client_handler(client):
    
    while True:
        # 2048 = size of the message
        username = client.recv(2048).decode('utf-8')
        if username != '':
            clients.append((username, client))
            send_chat_room(f"\nINFO%{username} entered chat room")
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