import socket
import numpy as np
from prediction import predict
import pickle
import statistics

PORT = 5077
IP = '192.168.1.44'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
while True:
    s.listen(1)
    print("Ears open")

    conn, addr = s.accept()
    print('Client connected: ', addr)
    full_msg = b''
    while conn:
        try:
            data = conn.recv(1024)
            full_msg += data
            if len(full_msg) == 5274:
                decoded_data = pickle.loads(full_msg)
                full_msg = b''
                batch = np.array(decoded_data, dtype="float32")
                pred_list = []
                for img in range(batch.shape[0]):
                    image = batch[img, :, :].reshape(1, 1, 32, 32)
                    pred_list.append(predict(image))
                final_prediction = str(statistics.mode(pred_list)).encode()
                print(final_prediction)
                conn.sendall(final_prediction)
                print("prediction sent")
                break

        except KeyboardInterrupt:
            if s:
                s.close()
                print("Sever closed")
            break

