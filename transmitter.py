import socket
import pickle
import time
import pandas as pd
import numpy as np

df = pd.read_csv("df_test.csv")
data = np.array(df['consumption'][50:])

data1 = {
    "vector001": [1, 2, 3, 4, 5],
    "vector002": [6, 7, 8, 9, 10]
}


receiver_port = 49156
# receiver_ip = '192.168.1.9'
receiver_ip = '127.0.1.1'


for d in data:
    data_bytes = pickle.dumps(d)
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sender_socket.connect((receiver_ip, receiver_port))
        sender_socket.sendall(data_bytes)
        print(time.strftime("[%Y-%m-%d %H:%M:%S]"), "  Data sent to", receiver_ip)
    except Exception as e:
        print("Error:", e)
    sender_socket.close()
    time.sleep(1)
