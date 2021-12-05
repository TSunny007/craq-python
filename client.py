import requests
import argparse
import cmd

class CRAQShell(cmd.Cmd):
    intro = '/******************** CRAQ Python ********************/\n Type help or ? to list commands.\n '
    prompt = '(CRAQ) '

    def do_read(self, k):
        """read [KEY]
        Read the value for specified [KEY] from read node."""
        print(requests.get(f'http://127.0.0.1:{args.read}/read', params={'key': k}).json())
    
    def do_write(self, inp):
        """write [KEY] [VALUE]
        Write the [VALUE] for specified [KEY] to CRAQ store."""
        k, v = inp.split()
        print(requests.post(f'http://127.0.0.1:{args.coordinator}/write', data={k: v}).json())
    

def parse(arg):
    return arg.split()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="port to run the client", default=5000)
    parser.add_argument("-c", "--coordinator", help="port of the coordinator process", default=5200)
    parser.add_argument("-r", "--read", help="port of the node process to read from", default=5201)
    args = parser.parse_args()

    CRAQShell().cmdloop()