import socket
import pynput

mouse_controller = pynput.mouse.Controller()

# Define the server's IP address and port
server_ip = '192.168.1.98'  # Replace with your MacBook's IP address
server_port = 8081  # Choose a port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {server_ip}:{server_port}")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")


prev_data = client_socket.recv(9)


def move_mouse(x, y):
    global mouse_controller
    mouse_controller.position = (x, y)


while True:
    # Receive data from the client
    data = client_socket.recv(9)  # Adjust the buffer size as needed

    if not data:
        break  # Connection closed by the client

    # Process the received data (e.g., control the mouse)
    # Implement your logic here

    if data != prev_data:
        prev_data = data
        x = int(str(data[0:4])[2:-1])
        y = int(str(data[4:8])[2:-1])
        z = int(str(data[8:9])[2:-1])
        print("Moving mouse to:", x, y)
        print("Clicking mouse:", z)

        if z == 2:
            mouse_controller.press(pynput.mouse.Button.left)
        elif z == 1:
            mouse_controller.release(pynput.mouse.Button.left)
        elif z == 4:
            mouse_controller.press(pynput.mouse.Button.right)
        elif z == 3:
            mouse_controller.release(pynput.mouse.Button.right)

        move_mouse(x, y)


# Close the sockets
client_socket.close()
server_socket.close()
