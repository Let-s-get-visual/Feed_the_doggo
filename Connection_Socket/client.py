import socket
import numpy as np
import pickle



HOST = '88.1.56.23'    
PORT = 5077

def send_data(crop_array):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    print('Client connected.')

    data = pickle.dumps(crop_array)
    # print(len(data))

    # data = crop_array.tobytes()

    # print(len(data))
    s.sendall(data)
    
    while True: 
        # if user_input == "exit":  
        #     break
        answer = s.recv(1024)
        if answer:
            print(answer)
            s.close()
            print('connection closed')
            return answer.decode()

