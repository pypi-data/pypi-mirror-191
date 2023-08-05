import json
import grpc
from .channel import CHANNEL
from .gRPC_proto.user import user_pb2, user_pb2_grpc, auth_pb2_grpc, auth_pb2


class User:
    def __init__(self, username, password):
        self.stub = user_pb2_grpc.UserControllerStub(CHANNEL)
        self.auth_stub = auth_pb2_grpc.AuthenticationStub(CHANNEL)
        self.username = username
        self.password = password

    def change_password(self, new_password):
        try:
            response = self.stub.ChangePassword(
                user_pb2.PasswordRequest(username=self.username, password=self.password,
                                         new_password=new_password))
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def change_key(self):
        try:
            response = self.stub.ChangeKey(
                user_pb2.KeyRequest(username=self.username, password=self.password))
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def get_key(self):
        try:
            response = self.stub.GetKey(
                user_pb2.KeyRequest(username=self.username, password=self.password))
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def login(self):
        try:
            response = self.auth_stub.Login(auth_pb2.LoginRequest(username=self.username, password=self.password))
            meta = [('jwt-access-token', json.loads(response.token)['token'])]
            return meta
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
