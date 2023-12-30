import csv
import pandas as pd

from feature_extraction import *
from feature_extraction_realtime import *
from etherscan import *
import numpy as np


class RealtimeDataExtractor:
    def __init__(self,contract_address):
        self.contract_address = contract_address
        self.api_key="74EXH3ZYYXPYAA9M1AAUCHSXXQ62MVXANW"
            
    def createTransactionDataset(self):
        eth_api = ETH_API(self.api_key,[])
        internal_transactions= eth_api.get_last_x_internal_transactions(self.contract_address)
        external_transactions= eth_api.get_last_x_transactions(self.contract_address)

        fe=ContractFeatureRealtime(internal_transactions,external_transactions,self.contract_address)
        data=fe.sequence_of_transactions

        # Convert the dictionary values to NumPy arrays
        arrays = [np.array(data[key]) for key in data]
        # Stack the arrays horizontally to create a single 2D array
        result = np.column_stack(arrays)

        return result
