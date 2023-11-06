import requests
import os
import csv


class ETH_API:
    def __init__(self,api_key,ponzi_contract_list):
        self.base_url = "https://api.etherscan.io/api"
        self.endpoint = "account"
        self.action = "txlist"
        self.api_key = api_key
        self.ponzi_contract_list=ponzi_contract_list

    def get_transactions_count(self,address):

        
        params = {
            "module": "account",
            "action": self.action,
            "address": address,
            "apikey": self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if data["status"] == "1":
                return len(data["result"])
            else:
                error_message = data["message"]
                print(f"Error: {error_message}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def get_last_x_transactions(self,address, num_transactions):
        params = {
            "module": "account",
            "action": self.action,
            "address": address,
            "apikey": self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if data["status"] == "1":
                print(len(data["result"]))
                transactions = data["result"][-num_transactions:]  # Get the last X transactions
                return transactions
            else:
                error_message = data["message"]
                print(f"Error: {error_message}")
                return 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def createTransactionFiles(self):
        print('=== Downloading transaction files...')
        counter = 0
        for contratAddress in self.ponzi_contract_list:
            fileNameToSave = './data/transactions/' + contratAddress + '.csv'
            if not os.path.exists(fileNameToSave):
                with open(fileNameToSave, 'w') as f:
                    f.write(" ")

            results = self.get_last_x_transactions(contratAddress,10)
            fieldnames = ['blockNumber', 'blockHash', 'timeStamp', 'hash', 'nonce', 'transactionIndex', 'from', 'to', 'value',
                          'gas', 'gasPrice', 'input', 'contractAddress', 'cumulativeGasUsed', 'gasUsed', 'confirmations', 'isError']
            with open(fileNameToSave, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for result in results:
                    # result['input'] = ''
                    # # print(result)
                    # writer.writerow(result)
                    transaction_data = {
                    'blockNumber': result['blockNumber'],
                    'blockHash': result['blockHash'],
                    'timeStamp': result['timeStamp'],
                    'hash': result['hash'],
                    'nonce': result['nonce'],
                    'transactionIndex': result['transactionIndex'],
                    'from': result['from'],
                    'to': result['to'],
                    'value': result['value'],
                    'gas': result['gas'],
                    'gasPrice': result['gasPrice'],
                    'input': result['input'],
                    'contractAddress': result['contractAddress'],
                    'cumulativeGasUsed': result['cumulativeGasUsed'],
                    'gasUsed': result['gasUsed'],
                    'confirmations': result['confirmations'],
                    'isError': result['isError']
                    }
                    writer.writerow(transaction_data)
            counter += 1
            # if counter % 500 == 0 and counter > 0:
            print('{0} transactions have downloaded...'.format(counter))
        print('ponzi transactions downloading is over.')
        return True


# # Replace 'YOUR_API_KEY' with your actual Etherscan API key
# api_key = "74EXH3ZYYXPYAA9M1AAUCHSXXQ62MVXANW"

# # Replace 'YOUR_ADDRESS' with the Ethereum address for which you want to retrieve transactions
# address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

# # Specify the number of transactions you want to retrieve
# num_transactions = 10  # Change this to the desired number of transactions

# # Create an instance of the ETH_API class
# eth_api = ETH_API(api_key)

# transactions = eth_api.get_last_x_transactions(address, num_transactions)
# transactions_count = eth_api.get_transactions_count(address)
# print(f"Total number of transactions: {transactions_count}")

# if transactions:
   
#     print(f"Last {num_transactions} transactions for address {address}:")
#     for tx in transactions:
#         print(tx)
#         # print(f"Tx Hash: {tx['hash']}")
#         # print(f"Block Number: {tx['blockNumber']}")
#         # print(f"Timestamp: {tx['timeStamp']}")
#         # print(f"From: {tx['from']}")
#         # print(f"To: {tx['to']}")
#         # print(f"Value: {tx['value']} wei")
#         print("------")
# else:
#     print("Failed to retrieve transactions.")
