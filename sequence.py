import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow import keras

path = "BDD_E_temp_population.csv"
df = pd.read_csv(path, index_col=[0], parse_dates=[0])

train_size = int(len(df) * 0.8)
train, test = (df[:train_size], df[train_size:])
y_np = df.loc[:, ['consumption']]

X_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()

X_scaler = X_scaler.fit(np.asarray(df[df.columns[1:]]))
df[df.columns[1:]] = X_scaler.transform(np.asarray(df[df.columns[1:]]))

y_scaler = y_scaler.fit(y_np)
df[df.columns[0]] = y_scaler.transform(y_np)

df_test = df[train_size:]


def to_sequence(data, time_steps=1):
    x_seq = []
    y_seq = []
    for i in range(len(data) - time_steps):
        window = data.iloc[i:i + time_steps, :]
        x_seq.append(window)
        y_seq.append(data.iloc[i+time_steps, 0])

    return np.array(x_seq), np.array(y_seq)


time_steps = 50
# X_test_seq, y_test_seq = to_sequence(df_test, time_steps)
X_test_seq, _ = to_sequence(df_test, time_steps)
