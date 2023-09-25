import socket
import pynput
import time
import tkinter as tk
import threading

print("Starting client...")
time.sleep(5)

# Define the server's IP address and port (same as in the server script)
server_ip = '192.168.1.98'  # Replace with your MacBook's IP address
server_port = 8081  # Use the same port number as in the server script

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))
print("Connected to server!")


tick_rate = 1 / 128  # Number of packets sent per second

mouse_controller = pynput.mouse.Controller()

z = 1


def on_click(x, y, button, pressed):
    global z

    if button == pynput.mouse.Button.left:
        if pressed:
            z = 2
            print("Left click pressed")
        else:
            z = 1
            print("Left click released")
    elif button == pynput.mouse.Button.right:
        if pressed:
            z = 4
            print("Right click pressed")
        else:
            z = 3
            print("Right click released")


mouse_listener = pynput.mouse.Listener(on_click=on_click)
mouse_listener.start()

prev_x, prev_y = mouse_controller.position
prev_z = 0


def adjust_mouse_position(x, y):
    # Adjust the mouse position to the server screen's dimensions

    x_input_min = 0
    x_input_max = 1919
    y_input_min = 0
    y_input_max = 1079

    x_output_min = 0
    x_output_max = 1679
    y_output_min = 0
    y_output_max = 1049

    x = ((x - x_input_min) * (x_output_max - x_output_min) / (x_input_max - x_input_min)) + x_output_min
    y = ((y - y_input_min) * (y_output_max - y_output_min) / (y_input_max - y_input_min)) + y_output_min

    return int(x), int(y)


def block_mouse_input(event):
    return "break"  # Prevents any mouse events from being processed


def unblock_mouse_input():
    root.unbind("<Button-1>")
    root.unbind("<Button-2>")
    root.unbind("<Button-3>")


root = tk.Tk()
root.attributes("-alpha", 0.01)  # Set window transparency to 0 (completely invisible)
root.attributes("-topmost", True)  # Keep the window on top of other windows
root.attributes("-fullscreen", True)  # Make the window fullscreen

# Bind mouse events to block_mouse_input function
root.bind("<Button-1>", block_mouse_input)  # Left mouse button click
root.bind("<Button-2>", block_mouse_input)  # Middle mouse button click
root.bind("<Button-3>", block_mouse_input)  # Right mouse button click

# To unblock mouse input, call unblock_mouse_input() function when needed

screen_width = root.winfo_screenwidth() + 200
screen_height = root.winfo_screenheight() + 200

# Resize the window to cover the entire screen, including the taskbar
root.geometry(f"{screen_width}x{screen_height}+0+-30")
root.config(cursor="none")  # Hide the mouse cursor


def send_mouse_data():
    global x, y, z, prev_x, prev_y, prev_z
    while True:
        # Capture mouse input (you can use a library like PyAutoGUI for this)
        # Send the mouse input data to the server
        x, y = mouse_controller.position
        if x != prev_x or y != prev_y or z != prev_z:
            prev_x = x
            prev_y = y
            prev_z = z
            x, y = adjust_mouse_position(x, y)
            mouse_data = str(x).zfill(4) + str(y).zfill(4) + str(z)
            client_socket.send(mouse_data.encode())
            print("Sent: " + mouse_data)
            print("z: " + str(z))

            if z == 1 or z == 3:
                z = 0

        # Wait for one tick
        time.sleep(tick_rate)

    # Close the socket when done
    client_socket.close()
    gui_thread.cancel()
    thread.cancel()


thread = threading.Thread(target=send_mouse_data)
thread.start()
root.mainloop()
thread.join()