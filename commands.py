import os

def handle_command(client,message, clients, usernames):
    if message == 'count':
        user_count(client, clients)
    elif message == 'help':
        help_message(client)
    elif message == 'users':
        show_users(client, usernames)
    elif message == 'clear':
        clear_chat(client)
    else:
        client.send(f"Invalid command.".encode('utf-8'))

def user_count(client, clients):
    client.send(f"Number of users online: {len(clients)}".encode('utf-8'))

def show_users(client, usernames):
    usr = ", ".join(usernames)
    client.send(f"Online users:\n{usr}".encode('utf-8'))

def clear_chat(client):
    client.send(b'\033c')

def help_message(client):
    help_msg = b"Commands: \n/Count - for number of users in the chat\n/Users - for online users\n/Clear - for clearing chat\n"
    client.send(help_msg)