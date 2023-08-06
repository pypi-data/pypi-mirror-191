from sqlalchemy import select

from housenomics.transaction import Transaction


class ServiceListTransactions:
    def execute(self, session):
        statement = select(Transaction)
        return session.scalars(statement).all()
