from sqlalchemy import select

from housenomics.transaction import Transaction


class ServiceReportBySeller:
    def execute(self, lookup, session, since=None, on=None):
        statement = select(Transaction)
        if since:
            statement = statement.where(Transaction.date_of_movement >= since)
        if on:
            statement = statement.where(Transaction.date_of_movement == on)
        clean_movements = []
        for m in session.scalars(statement):
            clean_movements.append(
                {
                    "description": m.description,
                    "value": m.value,
                }
            )
        total: float = 0
        for movement in clean_movements:
            if lookup.lower() in str(movement["description"]).lower():
                total += float(movement["value"])  # type: ignore
        return total
