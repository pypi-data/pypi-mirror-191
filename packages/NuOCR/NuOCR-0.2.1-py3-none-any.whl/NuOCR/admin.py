from .gRPC_proto.user import user_pb2, user_pb2_grpc
from .channel import CHANNEL
import grpc

class Admin:
    def __init__(self, metadata):
        self.stub = user_pb2_grpc.UserControllerStub(CHANNEL)
        self.metadata = metadata

    def create_user(self, params):
        try:
            response = self.stub.Create(
                user_pb2.User(username=params['username'], password=params['password'], email=params['email'],
                              first_name=params['first_name'], last_name=params['last_name']), metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def list_user(self):
        for post in self.stub.List(user_pb2.UserListRequest(), metadata=self.metadata):
            print(post, end='')

    def retrieve_user(self, id):
        try:
            response = self.stub.Retrieve(user_pb2.UserRetrieveRequest(id=id), metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def update_user(self, params):
        try:
            response = self.stub.Update(
                user_pb2.User(username=params['username'], password=params['password'], email=params['email'],
                              first_name=params['first_name'], last_name=params['last_name']), metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def delete_user(self, params):
        try:
            response = self.stub.Destroy(
                user_pb2.User(username=params['username'], password=params['password'], email=params['email'],
                              first_name=params['first_name'], last_name=params['last_name']), metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def add_access(self, params):
        try:
            response = self.stub.AddAccess(
                user_pb2.UserRequest(username=params['username'], access=params['access']), metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def remove_access(self, params):
        try:
            response = self.stub.RemoveAccess(
                user_pb2.UserRequest(username=params['username'], access=params['access']), metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

