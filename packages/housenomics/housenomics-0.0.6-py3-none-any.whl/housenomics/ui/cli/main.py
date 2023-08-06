import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from sqlalchemy import delete
from sqlalchemy.orm import Session

from housenomics.application.import_transactions import ServiceImportTransactions
from housenomics.application.list_transactions import ServiceListTransactions
from housenomics.application.report_by_seller import ServiceReportBySeller
from housenomics.infrastructure.cgd_csv_file import GatewayCGD
from housenomics.infrastructure.database import Database
from housenomics.infrastructure.transactions import Transactions
from housenomics.transaction import Transaction

logging_format: dict = {
    "level": logging.CRITICAL,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

logging.basicConfig(**logging_format)
logger = logging.getLogger(__name__)

application_help = """
Housenomics helps you manage your personal finances.
"""

app = typer.Typer(add_completion=False, help=application_help)

# SelectOfScalar.inherit_cache = True  # type: ignore
# Select.inherit_cache = True  # type: ignore


@app.command(name="import", help="Imports the transactions to feed the application")
def import_(file_path: Path):
    with Session(Database().engine) as session:
        gateway_cgd = GatewayCGD(file_path)
        transactions = Transactions(session)
        ServiceImportTransactions().execute(gateway_cgd, transactions)
        session.commit()


@app.command(name="list", help="Lists all transactions")
def list_(
    _: str = typer.Argument(
        default="transactions",
        help="The item to be listed",
    ),
):
    with Session(Database().engine) as session:
        results = ServiceListTransactions().execute(session)
        for m in results:
            print(f"Description: '{m.description:>22}', Value: {m.value:>10}")


@app.command(name="report", help="Reports the transactions filtered by seller")
def report(
    seller: str,
    since: Optional[datetime] = typer.Option(
        default=None, help="Show report since specified date"
    ),
    on: Optional[datetime] = typer.Option(
        default=None, help="Show report on specified date"
    ),
):
    with Session(Database().engine) as session:
        t = ServiceReportBySeller().execute(seller, session, since, on)

    print(f"Lookup: '{seller}', Value: {round(t, 2)}")


@app.command(name="version", help="Shows current version")
def version():
    typer.echo("0.0.6")


@app.command(
    name="reset",
    help="Deletes all financial information from the application",
)
def reset():
    delete_information = typer.confirm(
        "Are you sure you want to delete all financial information ?"
    )
    if not delete_information:
        raise typer.Abort()

    with Session(Database().engine) as session:
        statement = delete(Transaction)
        session.execute(statement)
        session.commit()


if __name__ == "__main__":
    app()
