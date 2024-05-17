import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
clients = []
messages = []
groups = {}

# print group
def print_groups():
    print("Groups:")
    for group_name, members in groups.items():
        print(f"- {group_name}: {', '.join(members)}")

# create a group
def create_group(group_name, username):
    if group_name not in groups:
        groups[group_name] = {username}
        print_groups()
        return True
    else:
        print(f"Group '{group_name}' already exists.")
        return False

# add person to group 
def add_to_group(group_name, username):
    if group_name in groups:
        groups[group_name].add(username)
        print_groups()
        return True
    else:
        return False

# send group message to a specific group
def send_message_group(group_name, msg, username):
    if group_name in groups:
        sent = False
        for client in clients:
            if client[0] in groups[group_name]:
                final_msg = username + '%' + msg
                send_private_msg(final_msg, client[1])
                sent = True
        return sent
    else:
        return False
            
# send messages to all the people in the chat room
def send_message_all(msg):
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
                send_message_all(final_msg)
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

    if command.startswith('/creategroup'):
        group_name = command.split(' ', 1)[1]
        create_group(group_name, username)
        client.sendall(f"INFO%Group '{group_name}' created successfully.".encode())
    
    if command.startswith('/joingroup'):
        group_name = command.split(' ', 1)[1]
        if add_to_group(group_name, username):
            client.sendall(f"INFO%You joined group '{group_name}' successfully.".encode())
        else:
            client.sendall(f"INFO%Group '{group_name}' does not exist.".encode())
        

    if command.startswith('/sendgroup'):
        group_name = command.split(' ', 2)[1]
        msg = command.split(' ', 2)[2]
        send_status = send_message_group(group_name, msg, username)
        if send_status:
            print(f"Message sent to group '{group_name}'")
        else:
            print(f"Group '{group_name}' does not exist.")

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
            send_message_all(f"\nINFO%{username} entered chat room")
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