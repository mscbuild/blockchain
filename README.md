 # 🧱 Basic Blockchain

  ![](https://komarev.com/ghpvc/?username=mscbuild) 
 ![](https://img.shields.io/github/license/mscbuild/e-learning) 
 ![](https://img.shields.io/github/repo-size/mscbuild/blockchain)
![](https://img.shields.io/badge/PRs-Welcome-green)
![](https://img.shields.io/badge/code%20style-python-green)
![](https://img.shields.io/github/stars/mscbuild)
![](https://img.shields.io/badge/Topic-Github-lighred)
![](https://img.shields.io/website?url=https%3A%2F%2Fgithub.com%2Fmscbuild)

 ✅ Features We'll Build.
 
<li>Define a Block class

<li>Build a Blockchain class to manage the chain

<li>Add Proof-of-Work (PoW)

<li>Verify the blockchain's integrity

### 🧱 Step 1: Define the Block Structure

### ⛓️ Step 2: Create the Blockchain Class

### 🧪 Step 3: Test the Blockchain

### 💸 Step 4: Add Transactions and Wallets

### 🧾 Features to Add:

<li>Transactions with digital signatures

<li>Wallets using public/private key pairs

<li>Verifiable signatures

Mining reward for creating new blocks

### 🔐 Step 1: Install Cryptography Library

We'll use ecdsa for key generation and signing.
```ruby
pip install ecdsa
```

### 🔑 Step 2: Wallet (Key Generation)

 You can now create wallets:

 ```ruby
private, public = generate_wallet()
```
### 📤 Step 3: Define a Transaction Class

### 🔗 Step 4: Integrate Transactions in the Blockchain

Modify your `Blockchain` class to support transactions and mining rewards:

### ✅ Test: Send and Mine a Transaction

### 🌐 Part 3: Flask API for Blockchain Node

### 🧰 Requirements

Install Flask and Requests:

```ruby
pip install flask requests
```

### 🧠 Overview of Features

Your node will support:

<li>Mining blocks (`/mine`)

<li>Viewing the blockchain (`/chain`)

<li>Creating transactions (`/transactions/new`)

<li>Registering nodes (`/nodes/registe`r)

<li>Resolving conflicts (`consensus`) (`/nodes/resolve`)

### 🖥️ Step 1: Set Up the Flask App

### ⛏️ Step 2: Mining Endpoint

### 📜 Step 3: Get Full Blockchain

### 💸 Step 4: Create New Transaction

### 🧩 Step 5: Node Registration & Consensus

You’ll need to track other nodes and sync with the longest chain.

First, add this to your `Blockchain` class:

Now add these Flask endpoints:

### ▶️ Run the Node

Save everything in a file like node.py, then run it with:

```ruby
python node.py
```
Your node will now be accessible on:
```bash
http://127.0.0.1:5000/
```
### ✅ Python Code to Create Blockchain Checklist PDF (`checklist_pdf.py`)

Use tools like Postman or curl to test creating transactions, mining, and syncing with other nodes on different ports.
