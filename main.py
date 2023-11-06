from collect_dapp_data import *


eth_api = ETH_API()

token_add="0x96184d9C811Ea0624fC30C80233B1d749B9E485B"

# tx_df = eth_api.get_transfers(token_add)
try:
    name, symbol = eth_api.get_token_name(token_add)
    tdata= eth_api.get_transfers(token_add)
    # Convert the abnormal address to checksum address
    # checksum_address = Web3.toChecksumAddress(token_add)

    # print(f"{checksum_address} transfers collected")
    print(f"{symbol} transfers collected")

    print(tdata)

    print(f"--------------------------------")

    # t=eth_api.get_transfers(token_add)
    # print(t)
    # reviews = reddit_api.collect_reddit(symbol, name)
except Exception as err:
    # some token have name and symbol as bytes32. By changing the ABI those tokens also can be collected
    print(f"Exception occured  : {err}")
    print(f"abnormal address: {token_add}")
    # im_grad_all = np.zeros((1429, 4839))
    # im_grad_val = np.zeros((1349, 5056))
    # im_sent_val = np.zeros((1349, 5056))
    # im_sent_grad = np.zeros((1349, 5056))
    # return "Invalid input/Token name is abnormal", im_grad_all, im_grad_val, im_sent_val, im_sent_grad
