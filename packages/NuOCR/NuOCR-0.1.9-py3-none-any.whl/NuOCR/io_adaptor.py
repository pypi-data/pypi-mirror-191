from .channel import CHANNEL
from .gRPC_proto.io_adaptors import io_adaptors_pb2, io_adaptors_pb2_grpc


class FTP:
    def __init__(self, metadata, host, port, username, password, isSecure=False):
        self.stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(CHANNEL)
        self.metadata = metadata
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.isSecure = isSecure

    def inbound(self, remoteFolder, remoteFilename='', base64=''):
        response = self.stub.FTPInBound(
            io_adaptors_pb2.FTPRequest(host=self.host, port=self.port, username=self.username, password=self.password,
                                       isSecure=self.isSecure, remoteFolder=remoteFolder,
                                       remoteFilename=remoteFilename, base64=base64), metadata=self.metadata)
        return response

    def outbound(self, base64, remoteFolder, remoteFilename):
        response = self.stub.FTPOutBound(
            io_adaptors_pb2.FTPRequest(host=self.host, port=self.port, username=self.username, password=self.password,
                                       isSecure=self.isSecure, remoteFolder=remoteFolder,
                                       remoteFilename=remoteFilename, base64=base64), metadata=self.metadata)
        return response.status


class S3:
    def __init__(self, metadata, regionName, accessKey, secretKey, bucketName):
        self.stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(CHANNEL)
        self.metadata = metadata
        self.regionName = regionName
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.bucketName = bucketName

    def inbound(self, folderName, filename='', base64=''):
        response = self.stub.S3InBound(
            io_adaptors_pb2.S3Request(regionName=self.regionName, accessKey=self.accessKey, secretKey=self.secretKey,
                                      bucketName=self.bucketName, folderName=folderName, filename=filename,
                                      base64=base64), metadata=self.metadata
        )
        return response

    def outbound(self, base64, filename, folderName):
        response = self.stub.S3OutBound(
            io_adaptors_pb2.S3Request(regionName=self.regionName, accessKey=self.accessKey, secretKey=self.secretKey,
                                      bucketName=self.bucketName, folderName=folderName, filename=filename,
                                      base64=base64), metadata=self.metadata
        )
        return response.status


class Blob:
    def __init__(self, metadata, accountName, accountKey, containerName):
        self.stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(CHANNEL)
        self.metadata = metadata
        self.accountName = accountName
        self.accountKey = accountKey
        self.containerName = containerName

    def inbound(self, filename, base64='', mimeType='', filepath=''):
        response = self.stub.BlobInBound(
            io_adaptors_pb2.BlobRequest(base64=base64, storageAccountName=self.accountName,
                                        storageAccountKey=self.accountKey, blobContainerName=self.containerName,
                                        blobFilepath=filepath, blobFilename=filename, mimeType=mimeType
                                        ), metadata=self.metadata)
        return response

    def outbound(self, filename, base64, mimeType, filepath=''):
        response = self.stub.BlobOutBound(
            io_adaptors_pb2.BlobRequest(base64=base64, storageAccountName=self.accountName,
                                        storageAccountKey=self.accountKey, blobContainerName=self.containerName,
                                        blobFilepath=filepath, blobFilename=filename, mimeType=mimeType
                                        ), metadata=self.metadata)
        return [response.blobName, response.blobUrl]
