import logging
import os
import grpc

import user_data_pb2
import user_data_pb2_grpc


class UserClient:
    def __init__(self, user_id):
        self.user_id = int(user_id)
        # Open a communication channel with UsersService
        self.channel = grpc.insecure_channel(os.getenv('USER_SERVICE_HOST'))
        # Creating stub to get data
        self.stub = user_data_pb2_grpc.GetUserDataStub(self.channel)

    def __enter__(self):
        # Call common method between both microservices passing the request type
        return self.stub.GetUser(
            user_data_pb2.UserDataRequest(id=self.user_id)
        )

    def __exit__(self, type, value, traceback):
        # Logging the process
        logging.info('Received info using gRPC', [type, value, traceback])
