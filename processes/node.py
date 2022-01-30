import logging
import argparse
from concurrent import futures
import grpc
import dbm

from generated import spec_pb2, spec_pb2_grpc

class Node(spec_pb2_grpc.Node):

  def __init__(self, args):
    super(Node, self).__init__()
    # establish connection with coordinator and get chain info.
    # we will assume we are the tail
    channel = grpc.insecure_channel(f'localhost:{args.coordinator}')
    self.coordinator = spec_pb2_grpc.CoordinatorStub(channel)
    self.args = args
    self.parentInfo: spec_pb2.RegisterReply = self.coordinator.Register(spec_pb2.RegisterRequest(port=args.port))

  def Read(self, request: spec_pb2.ReadRequest, context) -> spec_pb2.ReadReply:
    with dbm.open(f'.{self.args.port}-dbm', 'r') as store:
      val = store.get(request.key, bytearray()).decode('utf8')
    return spec_pb2.ReadReply(key=request.key, value=val)

  def Write(self, request: spec_pb2.WriteRequest, context) -> spec_pb2.WriteReply:
    try:
      with dbm.open(f'.{self.args.port}-dbm', 'c') as store:
        store[request.key] = request.value
      return spec_pb2.WriteReply(success=True)
    except Exception:
      return spec_pb2.WriteReply(success=False)
  
def serve(args):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
  spec_pb2_grpc.add_NodeServicer_to_server(Node(args), server)
  server.add_insecure_port(f'[::]:{args.port}')
  server.start()
  server.wait_for_termination()

if __name__ == '__main__':
  logging.basicConfig()
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--port", help="Port to run the node process on.", default=5201)
  parser.add_argument("-c", "--coordinator", help="Port of the coordinator process.", default=5200)
  args = parser.parse_args()
  serve(args)