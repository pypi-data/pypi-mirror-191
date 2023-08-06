import csv
import pathlib

import pendulum

from housenomics.transaction import Transaction


def transaction_from_source(transaction):
    transaction_parts = transaction[0].split(";")

    # Date
    date = transaction_parts[0].split("-")
    date.reverse()
    date = pendulum.parse("-".join(date))

    unit = transaction_parts[3].replace(".", "")
    decimals = transaction[1].split(";")[0]
    is_credit = False
    if not unit:
        is_credit = True
        unit = transaction_parts[4].replace(".", "")

    value: float = 0
    if is_credit:
        value = float(f"{unit}.{decimals}")

    if not is_credit:
        value = -1 * float(f"{unit}.{decimals}")

    m = Transaction(
        description=transaction_parts[2],
        date_of_movement=date,
        value=value,
    )
    return m


class GatewayCGD:
    def __init__(self, csv_file_path: pathlib.Path):
        self.csv_file_path = csv_file_path
        self.read_obj = None

    def __iter__(self):
        self.read_obj = open(self.csv_file_path, "r", encoding="ISO-8859-1")
        self.csv_reader = csv.reader(self.read_obj)

        return _Converter(self.csv_reader)

    def __del__(self):
        if self.read_obj is not None:
            self.read_obj.close()


class _Converter:
    def __init__(self, csv_reader):
        self._reader = csv_reader
        # Ignore headers
        for i in range(7):
            next(self._reader)

    def __next__(self):
        value = next(self._reader)
        if value[0].split(";")[0] == "('":  # Ignore last lines
            raise StopIteration

        # Ignore last lines...
        if "Saldo conta" in value[0]:
            raise StopIteration

        t = transaction_from_source(value)

        return t
