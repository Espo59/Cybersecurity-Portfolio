# Decentralized Real Estate Blockchain Simulation

This project implements a peer-to-peer (P2P) decentralized blockchain network designed to manage real estate transactions. It features a distributed ledger, Proof of Work (PoW) mining, and a consensus algorithm to ensure data consistency across multiple nodes.

---

## 📂 Project Components

* **`blockchain_8000.py`, `blockchain_8001.py`, `blockchain_8003.py`**: These scripts represent individual nodes in the network. Each node runs its own Flask web server, maintains a local copy of the ledger, and communicates with other peers.
* **`main_blockchain.py`**: The orchestrator script. It automates the simulation by launching node processes, submitting transactions, and triggering the consensus protocol to show how the network synchronizes.

## ⚙️ Core Features

* **Proof of Work (PoW)**: Each block requires a computational "puzzle" to be solved before it can be added to the chain, securing the network against tampering.
* **Consensus Algorithm**: Implements the "Longest Chain Rule." If nodes have conflicting versions of the ledger, they automatically adopt the longest valid chain available in the network.
* **Immutable Ledger**: Each block contains the SHA-256 hash of the previous block, creating an unbreakable chain of data.
* **REST API**: Each node exposes endpoints to interact with the blockchain:
    * `GET /mine`: Solve the PoW and create a new block.
    * `POST /transactions/new`: Add property data (ID, Channel, Data, Timestamp) to the next block.
    * `GET /chain`: Retrieve the full state of the blockchain.
    * `POST /nodes/register`: Add a new neighbor node to the network.
    * `GET /nodes/resolve`: Trigger the consensus algorithm to sync with neighbors.

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Flask
- Requests

`pip install Flask requests`

### Running the Simulation
The easiest way to test the system is to run the main orchestrator:

`python3 main_blockchain.py`

This script will automatically:

* Start Node 8000 and Node 8001.

* Submit a transaction to Node 8000.

* Mine the block on Node 8000.

* Register the nodes with each other.

* Demonstrate how Node 8001 updates its chain to match Node 8000 via the Consensus Algorithm.

---

# 🛠 Manual Usage
You can also run nodes manually in separate terminals:

# Terminal 1

`python3 blockchain_8000.py`

# Terminal 2

`python3 blockchain_8001.py`

Then use Postman or cURL to send transactions to http://localhost:8000/transactions/new.

--- 

# 📝 Transaction Example
Th
e nodes are configured to handle real estate data. Example payload:


```JSON
{
    "id": "REF-101",
    "canale": "Sales",
    "dati": "Luxury Penthouse in Rome",
    "timestamp": "1713360000"
}
```

---

# 🔐 Future Enhancements
To make this network production-ready, it should be combined with an mTLS (Mutual TLS) layer (using secure_socket_server.py) 
to ensure that only authorized nodes with valid certificates can participate in the peer-to-peer communication.

---

# 📜 License
Distributed under the MIT License. See LICENSE for more information.
