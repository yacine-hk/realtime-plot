import socket
import pickle
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import threading
import time
from tensorflow import keras

from sequence import X_test_seq, y_scaler


model = keras.models.load_model('temp_popul.keras')

list_data = list(range(100))
y_pred_data = []
for i in list_data:
    pred_val = np.array(y_scaler.inverse_transform(model.predict(X_test_seq[i][None, ...])))
    y_pred_data.append(pred_val.item())

df = pd.read_csv("df_test.csv")
data = np.array(df['consumption'][50:])
data_time = np.array(df['date'][50:])
data_time = data_time[:100]

y_true_data = []
y_true_data.append(data[0])

# y_error = []
# yjfa_error = []


class RealTimePlotApp:
    def __init__(self, root, receiver_socket):
        self.receiver_socket = receiver_socket

        self.root = root
        self.root.title("Real-Time Plot App")

        self.y_error = []
        self.y_true_data = []

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(20, 5), gridspec_kw={'height_ratios': [2, 1]})
        # self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        # self.fig, self.ax1 = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.start_button = ttk.Button(root, text="Start", command=self.start_plot)
        self.start_button.pack(side=tk.LEFT)

        self.pause_button = ttk.Button(root, text="Pause", command=self.pause_plot)
        self.pause_button.pack(side=tk.LEFT)

        self.continue_button = ttk.Button(root, text="Continue", command=self.continue_plot)
        self.continue_button.pack(side=tk.LEFT)

        self.is_running = False
        self.plot_thread = None
        self.continue_from_pause = False  # Flag to indicate if the plot should continue from pause
        self.pause_time = 0

        self.index = 0

    def start_plot(self):
        print("start")
        if not self.is_running:
            self.is_running = True
            # self.update_plot()

            # self.plot_thread = threading.Thread(target=self.update_plot)
            self.plot_thread = threading.Thread(target=self.fetch_data)
            self.plot_thread.start()

    def pause_plot(self):
        self.is_running = False
        self.continue_from_pause = True

    def continue_plot(self):
        if not self.is_running and self.continue_from_pause:
            self.is_running = True
            self.plot_thread = threading.Thread(target=self.update_plot)
            self.plot_thread.start()

    def fetch_data(self):
        for i in range(10000):
            print("Waiting for a connection...")
            connection, sender_address = self.receiver_socket.accept()
            print("Connected to:", sender_address)
            data_bytes = b""
            while True:
                chunk = connection.recv(4096)
                if not chunk:
                    break
                data_bytes += chunk
            data = pickle.loads(data_bytes)
            self.y_true_data.append(data)
            self.update_plot()
            print(time.strftime("[%Y-%m-%d %H:%M:%S]"), "- Sender's IP:", sender_address[0], "- Received data:", data)
            connection.close()

    def update_plot(self):
        print("update")
        if not self.continue_from_pause:
            global i, x_data, limit
            limit = 10
            i = 0
            x_data = list(range(100))
        # print(i, len(y_pred_data))
        # while self.is_running and i < len(self.y_true_data):
        print("i = ", self.index)
        self.ax1.clear()
        if self.index <= limit:
            self.ax1.set_xlim(left=0, right=limit)
            self.ax2.set_xlim(left=0, right=limit)
        else:
            self.ax1.set_xlim(left=self.index-10, right=self.index+limit)
            self.ax2.set_xlim(left=self.index-10, right=self.index+limit)

        out_true_data = self.y_true_data[:i+1]
        x_data_plot = data_time[:self.index+1]
        error = self.y_true_data[self.index] - y_pred_data[self.index]
        self.y_error.append(error)
        y_error_plot = self.y_error[:self.index+1]

        self.ax1.plot(data_time, y_pred_data, 'r-', marker='o', label='pred data')
        self.ax1.plot(self.y_true_data, 'g-', marker='o', label='true data')

        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.set_title('Real-Time Plot')
        self.ax1.tick_params(axis='x', labelrotation=90)
        self.ax1.legend(loc='upper right')

        self.ax2.plot(data_time, np.zeros(100), 'k', linewidth=0)
        bar_color = ['red' if err < 0 else 'green' for err in y_error_plot]
        print("bar: ", len(x_data_plot), len(y_error_plot[:self.index+1]))
        self.ax2.bar(x_data_plot, np.abs(y_error_plot), color=bar_color, width=0.1)
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Amplitude')
        self.ax2.set_title('Real-Time Plot')
        self.ax2.tick_params(axis='x', labelrotation=90)
        self.ax2.set_title('Error Plot (Red: Underestimate, Green: Overestimate)')

        self.fig.tight_layout()

        self.canvas.draw()

        # y_true_data.append(data[i+1])
        self.index += 1
        time.sleep(0.01)


print("begin")

receiver_port = 49156
receiver_ip = socket.gethostbyname(socket.gethostname())
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

app = RealTimePlotApp(root, receiver_socket)

"""
while 1:
    #tk.update_idletasks()
    root.update()
    time.sleep(0.01)
"""
root.mainloop()
