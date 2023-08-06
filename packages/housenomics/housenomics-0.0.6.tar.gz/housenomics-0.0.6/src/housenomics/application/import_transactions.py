class ServiceImportTransactions:
    def execute(self, source_transactions, transactions):
        for transaction in source_transactions:
            transactions.append(transaction)
