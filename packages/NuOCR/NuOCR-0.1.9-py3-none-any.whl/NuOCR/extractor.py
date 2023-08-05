import grpc
import json
from .channel import CHANNEL
from .gRPC_proto.extractor import extractor_pb2, extractor_pb2_grpc


class Extractor:
    def __init__(self, metadata):
        self.stub = extractor_pb2_grpc.ExtractorControllerStub(CHANNEL)
        self.metadata = metadata

    def form_recognizer(
            self,
            fileName,
            extractionType,
            inputType="base64",
            url='',
            base64='',
            pages=None,
            mimeType='application/pdf',
            rawJson=False,
            language=''
    ):
        try:
            request = extractor_pb2.FormRequest(language=language,
                                                inputType=inputType,
                                                fileName=fileName,
                                                url=url,
                                                base64=base64,
                                                pages=pages,
                                                mimeType=mimeType,
                                                extractionType=extractionType,
                                                rawJson=rawJson)
            response = self.stub.FormRecognition(request, metadata=self.metadata)
            return json.loads(response.body)
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def doc_recognizer(
            self,
            fileName,
            extractionType,
            inputType="base64",
            url='',
            base64='',
            mimeType='application/pdf',
            extractionHints=False,
            rawJson=False,
    ):
        try:
            request = extractor_pb2.DocRequest(
                fileName=fileName,
                inputType=inputType,
                url=url,
                base64=base64,
                mimeType=mimeType,
                extractionType=extractionType,
                extractionHints=extractionHints,
                rawJson=rawJson
            )
            response = self.stub.DocAI(request, metadata=self.metadata)
            return json.loads(response.body)
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def vin_extractor(
            self,
            fileName,
            inputType="base64",
            extractionType='vin',
            url='',
            base64='',
            preProcessors=[],
            mimeType='application/pdf',
            rawJson=False,
            language='',
    ):
        try:
            request = extractor_pb2.VinRequest(language=language,
                                               inputType=inputType,
                                               fileName=fileName,
                                               url=url,
                                               base64=base64,
                                               preProcessors=preProcessors,
                                               mimeType=mimeType,
                                               extractionType=extractionType,
                                               rawJson=rawJson)
            response = self.stub.VinNumber(request, metadata=self.metadata)
            return json.loads(response.body)
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))

    def extract(
            self,
            fileName,
            language='',
            inputType='base64',
            url='',
            base64='',
            pages=0,
            mimeType='application/pdf',
            extractionType='',
            rawJson=False,
            preProcessors=[],
            extractionHints=[],
    ):

        try:
            request = extractor_pb2.Request(language=language,
                                            inputType=inputType,
                                            fileName=fileName,
                                            url=url,
                                            base64=base64,
                                            pages=pages,
                                            mimeType=mimeType,
                                            extractionType=extractionType,
                                            rawJson=rawJson,
                                            preProcessors=preProcessors,
                                            extractionHints=extractionHints,
                                            )
            response = self.stub.Extractor(request, metadata=self.metadata)
            return json.loads(response.body)
        except grpc.RpcError as e:
            raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
