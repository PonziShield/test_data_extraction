from statistics import mean, median, stdev
import os
import csv
# import re

class ContractFeature(object):
    def __init__(self, contract_address):
        self.contract_address = contract_address
        # self.ponzi_or_nonponzi = ponzi_or_nonponzi
        self.file_name = self.contract_address + ".csv"

        # sequence of transactions features
        self.seq_size = 20
        self.tot_transactions = 100
        self.sequence_of_transactions = {
            "kr":[],
            # "bal":[],
            # "n_inv":[],
            # "n_pay":[],
            # "d_ind":[],
            "pr":[],
            # "n_max":[],
            "eth_inflow_external":[],
            "eth_inflow_internal":[],
            "eth_outflow_external":[],
            "eth_outflow_internal":[],
            "unique_incomming_addresses_internal":[],
            "unique_incomming_addresses_external":[],
            "unique_outgoing_addresses_internal":[],
            "unique_outgoing_addresses_external":[],
            "contract_total_transaction_count":[]

        }

        # -------------- chenz features from transactions ---------------------
        self.kr = 0.0  # known rate
        self.bal = 0.0  # balance
        self.n_inv = 0 # number of investment
        self.n_pay = 0  # number of payment
        self.d_ind = 0  # difference between counts of payment and investment
        self.pr = 0.0 # the proportion of investors who received at least one payment.
        self.n_max = 0.0 # the maximum of counts of payments to participants

        # local variables
        self.investors = {}  # format: {address: first_invest_timestamp}
        self.receivers = {}  # format: {address: first_payment timestamp}
        self.payment_counts = {}  # format: {address: number_of_payment_count_to_this_address}
        self.investment_count = {}  # format: {address: number_of_investment_from_this_address}

        self.get_kr_ninv_npay_pr_nmax()
        # self.get_balance()
        self.get_d_ind() 

        # -------------- LSTM features for transactions ---------------------

        self.eth_inflow_external = 0
        self.eth_inflow_internal = 0
        self.eth_outflow_external = 0
        self.eth_outflow_internal = 0
        self.get_eth_flow()

        self.unique_incomming_addresses_internal={}
        self.unique_incomming_addresses_external={}
        self.unique_outgoing_addresses_internal={}
        self.unique_outgoing_addresses_external={}
        self.get_unique_addresses()

        self.contract_total_transaction_count = 0
        self.get_contract_total_transaction_count()

        


    def get_contract_total_transaction_count(self):
        
        with open('./data/internal_transactions/' + self.file_name, 'r') as in_tx_file:
            internal_count = []
            seq_counter = 0
            locals_contract_total_transaction_count = 0
            counter = 0
            for in_tx in in_tx_file:
                if counter > 0:
                    from_address = in_tx.split(',')[3]
                    to_address = in_tx.split(',')[4]

                    if from_address == self.contract_address :
                        self.contract_total_transaction_count += 1
                        locals_contract_total_transaction_count += 1

                    # seq creation
                    if seq_counter == self.seq_size - 1:
                        seq_counter = 0
                        internal_count.append(locals_contract_total_transaction_count)
                        locals_contract_total_transaction_count = 0
                    else:
                        seq_counter += 1
                        

                counter += 1

        with open('./data/transactions/' + self.file_name, 'r') as tx_file:
            external_count = []
            seq_counter = 0
            locals_contract_total_transaction_count = 0

            counter = 0
            for tx in tx_file:
                if counter > 0:
                    from_address = tx.split(',')[6]
                    to_address = tx.split(',')[7]

                    if from_address == self.contract_address:
                        self.contract_total_transaction_count += 1

                    # seq creation
                    if seq_counter == self.seq_size - 1:
                        seq_counter = 0
                        external_count.append(locals_contract_total_transaction_count)
                        locals_contract_total_transaction_count = 0
                    else:
                        seq_counter += 1
                counter += 1

        self.sequence_of_transactions["contract_total_transaction_count"]=list(map(sum, zip( self.addPaddings(internal_count), self.addPaddings(external_count)))) 
        print('contract_total_transaction_count is {%d}' % self.contract_total_transaction_count)
        # print('feature_sequence is {%s}' % result)
    
    def get_eth_flow(self):
        with open('./data/internal_transactions/' + self.file_name, 'r') as in_tx_file:
            seq_counter = 0
            locals_eth_inflow_internal = 0
            locals_eth_outflow_internal = 0
            eth_inflow_internal=[]
            eth_outflow_internal=[]
            counter = 0
            for in_tx in in_tx_file:
                if counter > 0:
                    fields = in_tx.split(',')
                    eth_value = float(fields[5])
                    from_address = fields[3]
                    to_address = fields[4]

                    if from_address == self.contract_address:
                        self.eth_outflow_internal += eth_value
                        locals_eth_outflow_internal += eth_value

                    if to_address == self.contract_address:
                        self.eth_inflow_internal += eth_value
                        locals_eth_inflow_internal += eth_value

                    if seq_counter == self.seq_size - 1:
                        # print("^^^^^^^^^^")
                        # print(locals_eth_inflow_internal)
                        # print(locals_eth_outflow_internal)
                        seq_counter = 0
                        eth_inflow_internal.append(locals_eth_inflow_internal)
                        eth_outflow_internal.append(locals_eth_outflow_internal)
                        locals_eth_inflow_internal = 0
                        locals_eth_outflow_internal = 0
                    else:
                        seq_counter += 1

                counter += 1

        self.sequence_of_transactions["eth_inflow_internal"]=self.addPaddings(eth_inflow_internal)
        self.sequence_of_transactions["eth_outflow_internal"]=self.addPaddings(eth_outflow_internal)

        with open('./data/transactions/' + self.file_name, 'r') as tx_file:
            seq_counter = 0
            locals_eth_inflow_external = 0
            locals_eth_outflow_external = 0
            eth_inflow_external=[]
            eth_outflow_external=[]
            counter = 0
            for tx in tx_file:
                if counter > 0:
                    fields = tx.split(',')
                    eth_value = float(fields[8])
                    from_address = fields[6]
                    to_address = fields[7]

                    if from_address == self.contract_address:
                        self.eth_outflow_external += eth_value
                        locals_eth_outflow_external += eth_value
                    if to_address == self.contract_address:
                        self.eth_inflow_external += eth_value
                        locals_eth_inflow_external += eth_value
                    
                    if seq_counter == self.seq_size - 1:
                        seq_counter = 0
                        eth_inflow_external.append(locals_eth_inflow_external)
                        eth_outflow_external.append(locals_eth_outflow_external)
                        locals_eth_inflow_external = 0
                        locals_eth_outflow_external = 0
                    else:
                        seq_counter += 1

                counter += 1
            
        self.sequence_of_transactions["eth_inflow_external"]=self.addPaddings(eth_inflow_external)
        self.sequence_of_transactions["eth_outflow_external"]=self.addPaddings(eth_outflow_external)
        
        print('eth_inflow_external is {%f}' % self.eth_inflow_external)
        print('eth_inflow_internal is {%f}' % self.eth_inflow_internal)
        print('eth_outflow_external is {%f}' % self.eth_outflow_external)
        print('eth_outflow_internal is {%f}' % self.eth_outflow_internal)


    def get_unique_addresses(self):
        with open('./data/internal_transactions/' + self.file_name, 'r') as in_tx_file:
            seq_counter = 0
            local_unique_incomming_addresses_internal = {}
            local_unique_outgoing_addresses_internal = {}
            unique_incomming_addresses_internal=[]
            unique_outgoing_addresses_internal=[]
            counter = 0
            for in_tx in in_tx_file:
                if counter > 0:
                    fields = in_tx.split(',')
                    from_address = fields[3]
                    to_address = fields[4]

                    if to_address not in self.unique_outgoing_addresses_internal:
                        self.unique_outgoing_addresses_internal[to_address] = 1
                        local_unique_outgoing_addresses_internal[to_address] = 1

                    else:
                        self.unique_outgoing_addresses_internal[to_address] += 1
                        local_unique_outgoing_addresses_internal[to_address] = 1

                    if from_address not in self.unique_incomming_addresses_internal:
                        self.unique_incomming_addresses_internal[from_address] = 1
                        local_unique_incomming_addresses_internal[from_address] = 1
                    else:
                        self.unique_incomming_addresses_internal[from_address] += 1
                        local_unique_incomming_addresses_internal[from_address] = 1

                    if seq_counter == self.seq_size - 1:
                        seq_counter = 0
                        unique_incomming_addresses_internal.append(len(local_unique_incomming_addresses_internal))
                        unique_outgoing_addresses_internal.append(len(local_unique_outgoing_addresses_internal))
                        local_unique_incomming_addresses_internal = {}
                        local_unique_outgoing_addresses_internal = {}
                    else:
                        seq_counter += 1

                counter += 1
            
            self.sequence_of_transactions["unique_incomming_addresses_internal"]=self.addPaddings(unique_incomming_addresses_internal)
            self.sequence_of_transactions["unique_outgoing_addresses_internal"]=self.addPaddings(unique_outgoing_addresses_internal)

        with open('./data/transactions/' + self.file_name, 'r') as tx_file:
            counter = 0
            seq_counter = 0
            local_unique_incomming_addresses_external = {}
            local_unique_outgoing_addresses_external = {}
            unique_incomming_addresses_external=[]
            unique_outgoing_addresses_external=[]
            for tx in tx_file:
                if counter > 0:
                    fields = tx.split(',')
                    from_address = fields[6]
                    to_address = fields[7]

                    if to_address not in self.unique_outgoing_addresses_external:
                        self.unique_outgoing_addresses_external[to_address] = 1
                        local_unique_outgoing_addresses_external[to_address] = 1
                    else:
                        self.unique_outgoing_addresses_external[to_address] += 1
                        local_unique_outgoing_addresses_external[to_address] = 1

                    if from_address not in self.unique_incomming_addresses_external:
                        self.unique_incomming_addresses_external[from_address] = 1
                        local_unique_incomming_addresses_external[from_address] = 1
                    else:
                        self.unique_incomming_addresses_external[from_address] += 1
                        local_unique_incomming_addresses_external[from_address] = 1

                    if seq_counter == self.seq_size - 1:
                        seq_counter = 0
                        unique_incomming_addresses_external.append(len(local_unique_incomming_addresses_external))
                        unique_outgoing_addresses_external.append(len(local_unique_outgoing_addresses_external))
                        local_unique_incomming_addresses_external = {}
                        local_unique_outgoing_addresses_external = {}
                    else:
                        seq_counter += 1
                counter += 1
            
            self.sequence_of_transactions["unique_incomming_addresses_external"]=self.addPaddings(unique_incomming_addresses_external)
            self.sequence_of_transactions["unique_outgoing_addresses_external"]=self.addPaddings(unique_outgoing_addresses_external)

        print('unique_incomming_addresses_external is {%d}' % len(self.unique_incomming_addresses_external))
        print('unique_incomming_addresses_internal is {%d}' % len(self.unique_incomming_addresses_internal))
        print('unique_outgoing_addresses_external is {%d}' % len(self.unique_outgoing_addresses_external))
        print('unique_outgoing_addresses_internal is {%d}' % len(self.unique_outgoing_addresses_internal))



    def get_kr_ninv_npay_pr_nmax(self):
        investors_list = []  # format: {address: first_invest_timestamp}
        receivers_list = []  # format: {address: first_payment timestamp}
        with open('./data/transactions/' + self.file_name, 'r') as tx_file:
            seq_counter = 0
            local_investors={}
            counter = 0
            for tx in tx_file:
                if counter > 0:
                    fields = tx.split(',')
                    from_address = fields[6]
                    # print(from_address)
                    invest_timestamp = fields[2]
                    # print(invest_timestamp)
                    if from_address not in self.investors:
                        self.investors[from_address] = invest_timestamp
                    else:
                        if invest_timestamp < self.investors[from_address]:
                            self.investors[from_address] = invest_timestamp

                    if from_address not in self.investment_count:
                        self.investment_count[from_address] = 1
                    else:
                        self.investment_count[from_address] += 1

                    
                    
                    # seq creation
                    if from_address not in local_investors:
                        local_investors[from_address] = invest_timestamp
                    else:
                        if invest_timestamp < local_investors[from_address]:
                            local_investors[from_address] = invest_timestamp


                    if seq_counter == self.seq_size - 1:
                        seq_counter = 0
                        investors_list.append(local_investors)
                        local_investors = {}
                    else:
                        seq_counter += 1


                counter += 1

            self.n_inv = counter - 1
            # print(self.investors)
            print('n_inv is {%d}' % self.n_inv)

        with open('./data/internal_transactions/' +  self.file_name, 'r') as in_tx_file:
            seq_counter = 0
            local_receivers={}

            counter = 0
            for in_tx in in_tx_file:
                if counter > 0:
                    fields = in_tx.split(',')
                    to_address = fields[4]
                    pay_timestamp = fields[1]

                    if to_address not in self.receivers:
                        self.receivers[to_address] = pay_timestamp

                    else:
                        if pay_timestamp < self.receivers[to_address]:
                            self.receivers[to_address] = pay_timestamp

                    if to_address not in self.payment_counts:
                        self.payment_counts[to_address] = 1
                    else:
                        self.payment_counts[to_address] += 1

                    # seq creation
                    if to_address not in local_receivers:
                        local_receivers[to_address] = pay_timestamp
                    else:
                        if pay_timestamp < local_receivers[to_address]:
                            local_receivers[to_address] = pay_timestamp

                    if seq_counter == self.seq_size - 1:
                        seq_counter = 0
                        receivers_list.append(local_receivers)
                        local_receivers = {}
                    else:
                        seq_counter += 1

                counter += 1
            self.n_pay = counter - 1
            payment_count_list = [self.payment_counts[address] for address in self.receivers]
            self.n_max = max(payment_count_list) if len(payment_count_list) > 0 else 0
            print('n_max is {%d}' % self.n_max)
            # print(self.receivers)
            print('n_pay is {%d}' % self.n_pay)

            # print('--------------')
            # print("inv",len(investors_list))
            # print("rec",receivers_list)

        pay_after_investment_counter = 0
        for address in self.receivers:
            if address in self.investors and self.receivers[address] > self.investors[address]:
                pay_after_investment_counter += 1
        self.kr = pay_after_investment_counter / len(self.receivers) if len(self.receivers) > 0 else 0
        print('kr is {%f}' % self.kr)

        get_paid_investors_counter = 0
        for address in self.investors:
            if address in self.receivers:
                get_paid_investors_counter += 1
        self.pr = get_paid_investors_counter / len(self.receivers) if len(self.receivers) > 0 else 0
        print('pr is {%f}' % self.pr)

        # seq creation
        investors_list=self.addPaddingsSet(investors_list)
        receivers_list=self.addPaddingsSet(receivers_list)
        # print("inv",(investors_list))
        # print("rec",(receivers_list))
        for i in range(len(investors_list)):
            investors = investors_list[i]
            receivers = receivers_list[i]

            pay_after_investment_counter = 0
            for address in receivers:
                if address in investors and receivers[address] > investors[address]:
                    pay_after_investment_counter += 1
            kr = pay_after_investment_counter / len(receivers) if len(receivers) > 0 else 0
            self.sequence_of_transactions["kr"].append(kr)

            get_paid_investors_counter = 0
            for address in investors:
                if address in receivers:
                    get_paid_investors_counter += 1
            pr = get_paid_investors_counter / len(receivers) if len(receivers) > 0 else 0
            self.sequence_of_transactions["pr"].append(pr)
        

    # get the balance of a tx from the file flaged.csv
    def get_balance(self):
        with open('./data/transactions/' + self.file_name, 'r') as flaged_csv:
            for contract in flaged_csv:
                # print(contract.strip().split(','))
                if self.contract_address == contract.strip().split(',')[7]:
                    self.bal = float(contract.strip().split(',')[8])
                    print(self.bal)
        # print('bal is {%f}' % self.bal)

    
    def get_d_ind(self):
        all_participants = {}
        for investor in self.investment_count:
            n_i = self.payment_counts[investor] if investor in self.payment_counts else 0
            m_i = self.investment_count[investor]
            all_participants[investor] = n_i - m_i
        for payer in self.payment_counts:
            if payer not in self.investment_count:
                n_i = self.payment_counts[payer]
                m_i = 0
                all_participants[payer] = n_i - m_i

        res = all(x == 0 for x in all_participants.values())
        if res or len(all_participants) <= 2:
            self.d_ind = 0
        else:
            v_list = list(all_participants.values())
            mean_of_v_list = mean(v_list)
            median_of_v_list = median(v_list)
            std_of_v_list = stdev(v_list)
            skewness = 3 * (mean_of_v_list - median_of_v_list) / (std_of_v_list) if std_of_v_list != 0 else 0
            self.d_ind = skewness
        print('d_ind is {%f}' % self.d_ind)

    def addPaddings(self,ar1):
        if len(ar1) < self.tot_transactions//self.seq_size:
            return  ar1 + [0] * (self.tot_transactions//self.seq_size - len(ar1))
        return ar1
    
    def addPaddingsSet(self,ar1):
        if len(ar1) < self.tot_transactions//self.seq_size:
            for i in range(self.tot_transactions//self.seq_size - len(ar1)):
                ar1.append({})
            return  ar1
        return ar1

if __name__ == '__main__':

    # read ponzi_Contracts.csv and non_ponziContracts.csv file and find the balance of each contract by looking into
    contractFeature = ContractFeature('0xD79B4C6791784184e2755B2fC1659eaaB0f80456')