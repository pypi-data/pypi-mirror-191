import grpc

options = [('grpc.max_send_message_length', 64 * 1024 * 1024),
           ('grpc.max_receive_message_length', 64 * 1024 * 1024)]

HOST = '20.98.160.227:5005'

CHANNEL = grpc.insecure_channel(HOST, options=options)
