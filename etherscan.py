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
        self.transaction_limit = 1080

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


    def get_last_x_transactions(self,address):
        params = {
            "module": "account",
            "action": self.action,
            "address": address,
            "apikey": self.api_key,
            "offset": self.transaction_limit
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if data["status"] == "1":
                print(len(data["result"]))
                transactions = data["result"][-self.transaction_limit:]  # Get the last X transactions
                return transactions
            else:
                error_message = data["message"]
                print(f"Error: {error_message}")
                return 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_last_x_internal_transactions(self, address):
        params = {
            "module": "account",
            "action": "txlistinternal",
            "address": address,
            "apikey": self.api_key,
            "offset": self.transaction_limit
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if data["status"] == "1":
                print(len(data["result"]))
                internal_transactions = data["result"][-self.transaction_limit:]  # Get the last X internal transactions
                return internal_transactions
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
                with open(fileNameToSave, 'w',  newline='') as f:
                    f.write(" ")

            results = self.get_last_x_transactions(contratAddress)
            fieldnames = ['blockNumber', 'blockHash', 'timeStamp', 'hash', 'nonce', 'transactionIndex', 'from', 'to', 'value',
                          'gas', 'gasPrice', 'input', 'contractAddress', 'cumulativeGasUsed', 'gasUsed', 'confirmations', 'isError']
            with open(fileNameToSave, mode='w',  newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                if results != 0:
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
    
    def createInternalTransactionFiles(self):
        print('=== Downloading internal transaction files...')
        counter = 0
        for contratAddress in self.ponzi_contract_list:
            fileNameToSave = './data/internal_transactions/' + contratAddress + '.csv'
            if not os.path.exists(fileNameToSave):
                with open(fileNameToSave, 'w',  newline='') as f:
                    f.write(" ")

            results = self.get_last_x_internal_transactions(contratAddress)
            fieldnames = ['blockNumber', 'timeStamp', 'hash', 'from', 'to', 'value',
                          'contractAddress', 'input', 'type', 'gas', 'gasUsed', 'traceId', 'isError', 'errCode']
            with open(fileNameToSave, mode='w',  newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                if results != 0:
                    for result in results:
                        # result['input'] = ''
                        # # print(result)
                        # writer.writerow(result)
                        transaction_data = {
                        'blockNumber': result['blockNumber'],
                        # 'blockHash': result['blockHash'],
                        'timeStamp': result['timeStamp'],
                        'hash': result['hash'],
                        # 'nonce': result['nonce'],
                        # 'transactionIndex': result['transactionIndex'],
                        'from': result['from'],
                        'to': result['to'],
                        'value': result['value'],
                        'contractAddress': result['contractAddress'],
                        'input': result['input'],
                        'type': result['type'],
                        'gas': result['gas'],
                        'gasUsed': result['gasUsed'],
                        'traceId': result['traceId'],
                        'isError': result['isError'],
                        'errCode': result['errCode']
                        }
                        writer.writerow(transaction_data)
                    counter += 1
            # if counter % 500 == 0 and counter > 0:
            print('{0} transactions have downloaded...'.format(counter))
        print('ponzi transactions downloading is over.')
        return True
