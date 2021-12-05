# craq-python

Package `craq-python` implements CRAQ (Chain Replication with Apportioned Queries)
as described in [the CRAQ paper](https://pdos.csail.mit.edu/6.824/papers/craq.pdf). MIT Licensed.

CRAQ is a replication protocol that allows reads from any replica while still
maintaining strong consistency. CRAQ _should_ provide better read throughput
than Raft and Paxos. Read performance grows linearly with the number of nodes
added to the system. Network chatter is significantly lower compared to Raft and
Paxos.

### Learn more about CRAQ
[CRAQ Paper](https://pdos.csail.mit.edu/6.824/papers/craq.pdf)

[Chain Replication: How to Build an Effective KV Storage](https://medium.com/coinmonks/chain-replication-how-to-build-an-effective-kv-storage-part-1-2-b0ce10d5afc3)

[MIT 6.824 Distributed Systems Lecture on CRAQ (80mins)](http://nil.csail.mit.edu/6.824/2020/video/9.html)

```
            +------------------+
            |                  |
      +-----+   Coordinator    |
      |     |                  |
Write |     +------------------+
      |
      v
  +---+----+     +--------+     +--------+
  |        +---->+        +---->+        |
  |  Node  |     |  Node  |     |  Node  |
  |        +<----+        +<----+        |
  +---+-+--+     +---+-+--+     +---+-+--+
      ^ |            ^ |            ^ |
 Read | |       Read | |       Read | |
      | |            | |            | |
      + v            + v            + v
```

## Processes
There are 3 packages that should be started to run the system. The `node` and `coordinator`
implementation in [processes](processes) uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) for communication and [dbm](https://docs.python.org/3/library/dbm.html) for storage. The `client` for interacting with the CRAQ system is implemented in [cmd](cmd).

### Coordinator
Facilitates new writes to the chain; allows nodes to announce themselves to the
chain; manages the order of the nodes of the chain. One Coordinator should be
run for each chain. For better resiliency, you _could_ run a cluster of
Coordinators and use something like Raft or Paxos for leader election, but
that's outside the scope of this project. Run using `python coordinator.py`.

#### Run Flags
```sh
-- port # Port to run the coordinator process on. Default: 5200
```

### Node
Represents a single node in the chain. Responsible for storing writes, serving
reads, and forwarding messages along the chain. In practice, you would probably
have a single Node process running on a machine. Each Node should have it's own
storage unit. Run using `python node.py`.

#### Run Flags
```sh
--port # Port to run the node process on. Default: 5201
--coordinator # Port of the coordinator process. Default: :1235
```

### Client
Basic CLI tool for interacting with the chain. Allows writes and reads. The one
included in this project uses the [cmd](https://docs.python.org/3/library/cmd.html) package. Run using `python client.py`.

#### Run Flags
```sh
--coordinator # Port of the coordinator process. Default: :1234
--read # Port of the node process to read from. Default: :1235
```