import socket
import tkinter as tk
import main

print("begin")

receiver_port = 49156
# receiver_ip = socket.gethostbyname(socket.gethostname())
receiver_ip = input("server ip: ")
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_socket.bind((receiver_ip, receiver_port))
receiver_socket.listen(1)
print("Receiver IP:", receiver_ip, "    Receiver port:", receiver_port)


root = tk.Tk()

print(root.winfo_screenwidth())
print(root.winfo_screenheight())

display_width = root.winfo_screenwidth()
display_height = root.winfo_screenheight()

# window_height = int(display_height / 2)
# window_width = int(display_width / 2)

window_height = 800
window_width = 1400

left = int(display_width / 2 - window_width / 2)
top = int(display_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{top}+{left}')

app = main.RealTimePlotApp(root, receiver_socket)

root.mainloop()
