import csv
import pandas as pd

from feature_extraction import *
from etherscan import *


class CreateDataset:
    def __init__(self,no_of_files):
        self.no_of_files = no_of_files
        self.dataset = "./data/PonziDataset.csv"
        self.api_key="74EXH3ZYYXPYAA9M1AAUCHSXXQ62MVXANW"

        df = pd.read_csv(self.dataset)
        self.filtered_df = df[['address', 'label']]
    
    def createFeatureDataset(self):
        filtered_df = self.filtered_df
        for i in range(len(filtered_df)):
            
            if i>self.no_of_files:
                break
            
            print(filtered_df.loc[i, "address"], filtered_df.loc[i, "label"])
            fileNameToSave = './data/data_set/' + filtered_df.loc[i, "address"] + '.csv'
            fe=ContractFeature(filtered_df.loc[i, "address"])

            data=fe.sequence_of_transactions
            data['label'] = [filtered_df.loc[i, "label"]]*len(data['kr'])

            self.write_to_csv(fileNameToSave, data)
            print("-----------------------------------------------------------------------")
            
    def createTransactionDataset(self):
        filtered_df = self.filtered_df
        contract_adresses=filtered_df.loc[:self.no_of_files, "address"].tolist()
        eth_api = ETH_API(self.api_key,contract_adresses)
        eth_api.createTransactionFiles()
        eth_api.createInternalTransactionFiles()



    def write_to_csv(self, filename, data):

        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write header
            header = list(data.keys())
            csvwriter.writerow(header)
            # Write rows
            for row_values in zip(*data.values()):
                csvwriter.writerow(row_values)

        print(f'Data has been written to {filename}.')


                    

