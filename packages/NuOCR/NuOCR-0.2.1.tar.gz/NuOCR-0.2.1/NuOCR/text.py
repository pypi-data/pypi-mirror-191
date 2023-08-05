from .gRPC_proto.text_processor import text_processor_pb2_grpc, text_processor_pb2
from .channel import CHANNEL


class TextProcessors:
    def __init__(self, metadata, text=''):
        self.metadata = metadata
        self.text = text

    def Summarizer(self):
        try:
            stub = text_processor_pb2_grpc.TextProcessorControllerStub(CHANNEL)
            request = text_processor_pb2.Request(
                text=self.text,
            )
            response = stub.Summarize(request, metadata=self.metadata)
            return response.summary
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def SentimentAnalysis(self):
        try:
            stub = text_processor_pb2_grpc.TextProcessorControllerStub(CHANNEL)
            request = text_processor_pb2.Request(
                text=self.text,
            )
            response = stub.SentimentAnalysis(request, metadata=self.metadata)
            return response.summary
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
