from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from .ttypes import *



class TimestampHandler:
    def getCurrentTimestamp(self):
        # Implement logic to retrieve current timestamp
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


handler = TimestampHandler()
processor = TimestampService.Processor(handler)
transport = TSocket.TServerSocket(port=10000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
print("Starting Thrift server...")
server.serve()
