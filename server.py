import socket
import pickle
import time
import pandas as pd
import numpy as np

df = pd.read_csv("df_test.csv")
data = np.array(df['consumption'][50:])


receiver_port = 49156
# receiver_ip = '127.0.1.1'
receiver_ip = input("client ip: ")

i = 0
while i < len(data):
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sender_socket.connect((receiver_ip, receiver_port))
        data_bytes = pickle.dumps(data[i])
        sender_socket.sendall(data_bytes)
        print(time.strftime("[%Y-%m-%d %H:%M:%S]"), "  Data sent to", receiver_ip)
        i += 1
    except Exception as e:
        print("Error:", e)
    sender_socket.close()
    time.sleep(1)
