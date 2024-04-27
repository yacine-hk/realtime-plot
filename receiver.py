import socket
import pickle
import time

import matplotlib.pyplot as plt
import numpy as np
import keras

receiver_port = 49156
receiver_ip = socket.gethostbyname(socket.gethostname())
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_socket.bind((receiver_ip, receiver_port))
# receiver_socket.bind(("192.168.1.9", receiver_port))
receiver_socket.listen(1)
print("Receiver IP:", receiver_ip, "    Receiver port:", receiver_port)


for i in range(10000):
    print("Waiting for a connection...")
    connection, sender_address = receiver_socket.accept()
    print("Connected to:", sender_address)
    data_bytes = b""
    while True:
        chunk = connection.recv(4096)
        if not chunk:
            break
        data_bytes += chunk
    data = pickle.loads(data_bytes)

    x_data.append(len(x_data) + 1)
    y_data.append(data)
    model = keras.models.load_model('temp_popul.keras')
    pred_val = np.array(y_scaler.inverse_transform(model.predict(X_test_seq[i][None,...])))
    y_pred_data.append(pred_val.item())
    # print("==============>", pred_val)
    # print("==============>", X_test_seq[0])
    plt.clf()
    plt.plot(x_data, y_data, label='true value')
    plt.plot(x_data, y_pred_data, label='predicted')
    plt.xlabel('Time')
    plt.ylabel('Data')
    plt.legend(loc='upper left')
    plt.title('Real-time Data Plot')
    plt.pause(0.11)  # Pause to allow plot to update
    print('shapes: ', len(x_data), len(y_data), len(y_pred_data))
    print(time.strftime("[%Y-%m-%d %H:%M:%S]"), "- Sender's IP:", sender_address[0], "- Received data:", data)
    connection.close()


plt.show()
