class _MsgProtoBase_UnitedMessage_pb2:
    def ByteSize(*args, **kwargs):
        pass

    def Clear(*args, **kwargs):
        pass

    def ClearExtension(*args, **kwargs):
        pass

    def ClearField(*args, **kwargs):
        pass

    def CopyFrom(*args, **kwargs):
        pass

    def DiscardUnknownFields(*args, **kwargs):
        pass

    def FindInitializationErrors(*args, **kwargs):
        pass

    def FromString(*args, **kwargs):
        pass

    def HasExtension(*args, **kwargs):
        pass

    def HasField(*args, **kwargs):
        pass

    def IsInitialized(*args, **kwargs):
        pass

    def ListFields(*args, **kwargs):
        pass

    def MergeFrom(*args, **kwargs):
        pass

    def MergeFromString(*args, **kwargs):
        pass

    def ParseFromString(*args, **kwargs):
        pass

    def RegisterExtension(*args, **kwargs):
        pass

    def SerializePartialToString(*args, **kwargs):
        pass

    def SerializeToString(*args, **kwargs):
        pass

    def SetInParent(*args, **kwargs):
        pass

    def UnknownFields(*args, **kwargs):
        pass

    def WhichOneof(*args, **kwargs):
        pass


class DataUnited(_MsgProtoBase_UnitedMessage_pb2):
    def __init__(self, int_value=None, str_value=None):
        self.int_value = int_value
        self.str_value = str_value


class UnitedMessage(_MsgProtoBase_UnitedMessage_pb2):
    def __init__(self, msg_body=None, msg_id=None, msg_type=None, opaque_data=None, routing_key=None, session=None, session_id=None):
        self.msg_body = msg_body
        self.msg_id = msg_id
        self.msg_type = msg_type
        self.opaque_data = opaque_data
        self.routing_key = routing_key
        self.session = session
        self.session_id = session_id


