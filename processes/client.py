import logging
import argparse
import cmd
import grpc

from generated import spec_pb2, spec_pb2_grpc

class CRAQShell(cmd.Cmd):
    
    def __init__(self, args):
        super(CRAQShell, self).__init__()
        self.intro = '/******************** CRAQ Python ********************/\n Type help or ? to list commands.\n '
        self.prompt = '(CRAQ) '
        
        read_channel = grpc.insecure_channel(f'localhost:{args.read}')
        self.read_stub = spec_pb2_grpc.NodeStub(read_channel)
        
        write_channel = grpc.insecure_channel(f'localhost:{args.coordinator}')
        self.write_stub = spec_pb2_grpc.CoordinatorStub(write_channel)

    def do_read(self, k):
        """read [KEY]
        Read the value for specified [KEY] from read node."""
        reply = self.read_stub.Read(spec_pb2.ReadRequest(key=k))
        print(f'{reply.key}: {reply.value}')
    
    def do_write(self, inp):
        """write [KEY] [VALUE]
        Write the [VALUE] for specified [KEY] to CRAQ store."""
        k, v = inp.split()
        reply = self.write_stub.Write(spec_pb2.WriteRequest(key=k, value=v))
        print(f'Update was {"successful" if reply.success else "unsuccessful"}')

if __name__ == "__main__":
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--coordinator", help="Port of the coordinator process.", default=5200)
    parser.add_argument("-r", "--read", help="Port of the node process to read from.", default=5201)
    args = parser.parse_args()
    CRAQShell(args).cmdloop()