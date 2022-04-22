from credmark.cmf.engine.mocks import ModelMock, ModelMockConfig
from credmark.cmf.model import Model
from credmark.cmf.types.ledger import (BlockTable, ContractTable,
                                       LedgerModelOutput, LogTable,
                                       ReceiptTable, TokenTable,
                                       TokenTransferTable, TraceTable,
                                       TransactionTable)
from credmark.dto import EmptyInput
from models.examples.example_dtos import ExampleModelOutput
from models.tmp_abi_lookup import CMK_ADDRESS


class ExampleLedgerOutput(ExampleModelOutput):
    ledger_output: LedgerModelOutput


@Model.describe(
    slug='example.ledger-blocks',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerBlock(Model):
    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_blocks(columns=[BlockTable.Columns.DIFFICULTY],
                                          limit="10",
                                          order_by=BlockTable.Columns.NUMBER + " desc")

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of Ledger's blocks")
        output.log("To fetch some information about the past 10 blocks:")
        output.log_io(input="""ledger.get_blocks(columns=[BlockTable.Columns.DIFFICULTY],limit="10",order_by=BlockTable.Columns.NUMBER + " desc")""",
                      output=ledger_output)

        return output


# This mock config can be used as mock data for the 'example.ledger-transactions'
# model below.
# Run with: credmark-dev run example.ledger-transactions -m models.examples.ledger_examples.ledger_transactions_mocks
ledger_transactions_mocks = ModelMockConfig(
    models={
        'ledger.transaction_data':
        ModelMock({"data":
                   [{"hash": "0x8862c4b7bc8b7d48f1671b413dd3b5e0b785d2001443ff3e13ba9602eddb7ef2"},
                    {"hash": "0x9a1bbc5508e4fed1e7f08d791740dfb03aa8560965c78c92b6ee8fcc350021db"},
                    {"hash": "0x00643f90efc4b949e4c8ed8abfa61d36b035297a996a066c967f64df3d2c7040"}]})
    })


@Model.describe(
    slug='example.ledger-transactions',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerTransactions(Model):
    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_transactions(columns=[TransactionTable.Columns.HASH],
                                                where=f'{TransactionTable.Columns.BLOCK_TIMESTAMP}={self.context.block_number.timestamp}',
                                                limit="10",
                                                order_by=TransactionTable.Columns.GAS)

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of Ledger's transactions")
        output.log("To fetch 10 transactions hashes mined in the requested block:")
        output.log_io(input="ledger.get_transactions(columns=[TransactionTable.Columns.HASH], "
                      "where=f'{TransactionTable.Columns.BLOCK_TIMESTAMP}={self.context.block_number.timestamp}', "
                      "limit=\"10\", "
                      "order_by=TransactionTable.Columns.GAS)",
                      output=ledger_output)

        return output


@Model.describe(
    slug='example.ledger-transactions-gas-stats',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerTransactionsMaxGas(Model):
    """
    This model uses aggregate functions to return min, max, and average gas used
    in transactions up to the requested block.
    """

    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_transactions(aggregates=[
            ledger.Aggregate(f'MIN({TransactionTable.Columns.GAS})', 'min_gas'),
            ledger.Aggregate(f'MAX({TransactionTable.Columns.GAS})', 'max_gas'),
            ledger.Aggregate(f'AVG({TransactionTable.Columns.GAS})', 'avg_gas')
        ])

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of aggregates in Ledger")
        output.log("To fetch min, max, and average gas used in transactions up to the requested block:")

        output.log_io(input="""
ledger.get_transactions(aggregates=[
    ledger.Aggregate(f'MIN({TransactionTable.Columns.GAS})', 'min_gas'),
    ledger.Aggregate(f'MAX({TransactionTable.Columns.GAS})', 'max_gas'),
    ledger.Aggregate(f'AVG({TransactionTable.Columns.GAS})', 'avg_gas')
        ])""",
                      output=ledger_output)

        return output


@Model.describe(
    slug='example.ledger-receipts',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerReceipts(Model):

    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_receipts(columns=[ReceiptTable.Columns.CONTRACT_ADDRESS,
                                                     ReceiptTable.Columns.CUMULATIVE_GAS_USED,
                                                     ReceiptTable.Columns.GAS_USED],
                                            where=f'{ReceiptTable.Columns.BLOCK_NUMBER}={self.context.block_number}',
                                            limit="10",
                                            order_by=f'{ReceiptTable.Columns.CONTRACT_ADDRESS} desc')

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of Ledger's receipts")
        output.log("To fetch 10 receipts in the requested block:")

        output.log_io(input="""
ledger.get_receipts(columns=[ReceiptTable.Columns.CONTRACT_ADDRESS,
                             ReceiptTable.Columns.CUMULATIVE_GAS_USED,
                             ReceiptTable.Columns.GAS_USED],
                    where=f'{ReceiptTable.Columns.BLOCK_NUMBER}={self.context.block_number}',
                    limit="10",
                    order_by=f'{ReceiptTable.Columns.CONTRACT_ADDRESS} desc')""",
                      output=ledger_output)

        return output


@Model.describe(
    slug='example.ledger-token-transfers',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerTokenTransfers(Model):

    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_erc20_transfers(columns=list(TokenTransferTable.columns()),
                                                   where=f'{TokenTransferTable.Columns.FROM_ADDRESS}=\'{CMK_ADDRESS.lower()}\' or \
                                                       {TokenTransferTable.Columns.TO_ADDRESS}=\'{CMK_ADDRESS.lower()}\'',
                                                   order_by=f'{TokenTransferTable.Columns.BLOCK_NUMBER} desc',
                                                   limit="10")

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of Ledger's ERC20 token transfers")
        output.log("To fetch 10 most recent ERC20 Token Transfers into or out of an address, with respect to blocknumber:")

        output.log_io(input="""
ledger.get_erc20_transfers(columns=list(TokenTransferTable.columns()),
                            where=f'{TokenTransferTable.Columns.FROM_ADDRESS}=\'{CMK_ADDRESS.lower()}\' or {TokenTransferTable.Columns.TO_ADDRESS}=\'{CMK_ADDRESS.lower()}\'',
                            order_by=f'{TokenTransferTable.Columns.BLOCK_NUMBER} desc',
                            limit="10")""",
                      output=ledger_output)

        return output


@Model.describe(
    slug='example.ledger-tokens',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerTokens(Model):

    """
    TODO: NOT IMPLEMENTED YET
    """

    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_erc20_tokens(columns=list(TokenTable.columns()),
                                                limit="100",
                                                order_by=TokenTable.Columns.BLOCK_NUMBER)

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of Ledger's ERC20 tokens")
        output.log("To fetch 100 ERC20 Tokens:")

        output.log_io(input="""
ledger.get_erc20_tokens(columns=list(TokenTable.columns()),
                        limit="100",
                        order_by=TokenTable.Columns.BLOCK_NUMBER)""",
                      output=ledger_output)

        return output


@Model.describe(
    slug='example.ledger-logs',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerLogs(Model):
    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_logs(columns=[LogTable.Columns.ADDRESS,
                                                 LogTable.Columns.DATA],
                                        where=f'{LogTable.Columns.BLOCK_NUMBER}={self.context.block_number}',
                                        limit="10",
                                        order_by=f'{LogTable.Columns.ADDRESS} desc')

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of Ledger's logs")
        output.log("To fetch 10 logs for the current block:")

        output.log_io(input="""
ledger.get_logs(columns=[LogTable.Columns.ADDRESS,
                            LogTable.Columns.DATA],
                where=f'{LogTable.Columns.BLOCK_NUMBER}={self.context.block_number}'),
                limit="10",
                order_by=f'{LogTable.Columns.ADDRESS} desc'""",
                      output=ledger_output)

        return output


@Model.describe(
    slug='example.ledger-contracts',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerContracts(Model):

    """
    TODO: NOT IMPLEMENTED YET
    """

    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_contracts(columns=list(ContractTable.columns()),
                                             limit="100", order_by=ContractTable.Columns.BLOCK_NUMBER)

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of Ledger's Contracts")
        output.log("To fetch 100 Contracts:")

        output.log_io(input="""
ledger.get_contracts(columns=list(ContractTable.columns()),
                    limit="100", order_by=ContractTable.Columns.BLOCK_NUMBER)""",
                      output=ledger_output)

        return output


@Model.describe(
    slug='example.ledger-traces',
    version="1.0",
    developer="Credmark",
    input=EmptyInput,
    output=ExampleLedgerOutput)
class ExampleLedgerTraces(Model):

    """
    This model returns all traces mined in the current block
    """

    def run(self, _):
        ledger = self.context.ledger
        ledger_output = ledger.get_traces(columns=[TraceTable.Columns.BLOCK_NUMBER,
                                                   TraceTable.Columns.ERROR,
                                                   TraceTable.Columns.CALL_TYPE],
                                          where=f'{TraceTable.Columns.BLOCK_NUMBER}={self.context.block_number}',
                                          limit="100",
                                          order_by=TraceTable.Columns.FROM_ADDRESS)

        output = ExampleLedgerOutput(github_url="https://github.com/credmark/credmark-models-py/blob/main/models/examples/ledger_examples.py",
                                     documentation_url="https://developer-docs.credmark.com/en/latest/components.html#ledger",
                                     ledger_output=ledger_output)

        output.log("This model demonstrates the functionality of Ledger's Traces")
        output.log("To fetch 100 traces for the current block:")

        output.log_io(input="""
ledger.get_traces(columns=[TraceTable.Columns.BLOCK_NUMBER,
                        TraceTable.Columns.ERROR,
                        TraceTable.Columns.CALL_TYPE],
                    where=f'{TraceTable.Columns.BLOCK_NUMBER}={self.context.block_number}',
                    limit="100",
                    order_by=TraceTable.Columns.FROM_ADDRESS""",
                      output=ledger_output)

        return output
