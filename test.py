from feature_extraction import *



fe = ContractFeature("0x5fe5b7546d1628f7348b023a0393de1fc825a4fd")

print("$$$$$$$$$$$$$$$$$$$$$$$")
print(fe.sequence_of_transactions)

# print(len(fe.unique_incomming_addresses_external))
# print("--------------------------")
# print(len(fe.unique_incomming_addresses_internal))
# print("--------------------------")
# print(len(fe.unique_outgoing_addresses_external))
# print("--------------------------")
# print(len(fe.unique_outgoing_addresses_internal))

# print("=====================================")
# print(fe.eth_inflow_external)
# print("--------------------------")
# print(fe.eth_inflow_internal)
# print("--------------------------")
# print(fe.eth_outflow_external)
# print("--------------------------")
# print(fe.eth_outflow_internal)



# from etherscan import *

# eth_api = ETH_API("74EXH3ZYYXPYAA9M1AAUCHSXXQ62MVXANW",["0x5fe5b7546d1628f7348b023a0393de1fc825a4fd"])
# eth_api.createInternalTransactionFiles()
# # print(transactions)
# # i_tx=eth_api.get_last_x_internal_transactions("0x5fe5b7546d1628f7348b023a0393de1fc825a4fd", 10)
# # print(i_tx)