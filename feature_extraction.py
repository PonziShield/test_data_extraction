from statistics import mean, median, stdev
import os
import csv
# import re

class ContractFeature(object):
    def __init__(self, contract_address, ponzi_or_nonponzi):
        self.contract_address = contract_address
        self.ponzi_or_nonponzi = ponzi_or_nonponzi
        self.file_name = self.contract_address + ".csv"

        # features from transactions
        self.kr = 0.0  # known rate
        self.bal = 0.0  # balance
        self.n_inv = 0 # number of investment
        self.n_pay = 0  # number of payment
        self.d_ind = 0  # difference between counts of payment and investment
        self.pr = 0.0 # the proportion of investors who received at least one payment.
        self.n_max = 0.0 # the maximum of counts of payments to participants

        # features from opcode
        self.action_freq = {}
        self.action_ratio = {}

        # local variables
        self.investors = {}  # format: {address: first_invest_timestamp}
        self.receivers = {}  # format: {address: first_payment timestamp}
        self.payment_counts = {}  # format: {address: number_of_payment_count_to_this_address}
        self.investment_count = {}  # format: {address: number_of_investment_from_this_address}

        self.get_kr_ninv_npay_pr_nmax()
        # self.get_balance()

        # self.get_d_ind()  # TODO
        # self.get_action_frequency()  # get the frequency of each action in the opcode of a smart contract

    def get_kr_ninv_npay_pr_nmax(self):
        with open('./data/transactions/' + self.file_name, 'r') as tx_file:
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

                counter += 1
            self.n_inv = counter - 1
            print(self.investors)
            print('n_inv is {%d}' % self.n_inv)

        with open('./data/internal_transactions/' +  self.file_name, 'r') as in_tx_file:
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

                counter += 1
            self.n_pay = counter - 1
            payment_count_list = [self.payment_counts[address] for address in self.receivers]
            self.n_max = max(payment_count_list) if len(payment_count_list) > 0 else 0
            print('n_max is {%d}' % self.n_max)
            print(self.receivers)
            print('n_pay is {%d}' % self.n_pay)

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


if __name__ == '__main__':

    # read ponzi_Contracts.csv and non_ponziContracts.csv file and find the balance of each contract by looking into
    contractFeature = ContractFeature('0xD79B4C6791784184e2755B2fC1659eaaB0f80456', 'nonponzi')