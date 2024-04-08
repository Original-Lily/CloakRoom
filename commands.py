import os

def handle_command(client, message, clients, usernames):
    command_handlers = {
        'count': user_count,
        'help': help_message,
        'users': lambda: show_users(client, usernames),
        'clear': lambda: clear_chat(client),
    }
    handler = command_handlers.get(message, lambda: client.send("Invalid command.".encode('utf-8')))
    handler()

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