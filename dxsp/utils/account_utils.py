"""
 DEX SWAP
🔒 USER RELATED
"""


from loguru import logger

from dxsp.config import settings


class AccountUtils:

    """
    Class AccountUtils to interact with private related methods
    such as account balance, signing transactions, etc.

    Args:
        None

    Methods:
        get_info()
        get_help()
        get_account_balance()
        get_trading_asset_balance()
        get_account_position
        get_account_margin
        get_account_open_positions
        get_account_transactions()
        get_account_pnl
        get_approve
        get_sign
        get_gas
        get_gas_price

    """

    def __init__(
        self,
        w3,
        contract_utils,
        wallet_address,
        private_key,
        trading_asset_address,
        block_explorer_url,
        block_explorer_api,
    ):
        self.w3 = w3
        self.wallet_address = self.w3.to_checksum_address(wallet_address)
        self.account_number = (
            f"{str(self.w3.net.version)} - " f"{str(self.wallet_address)[-8:]}"
        )
        self.private_key = private_key
        self.trading_asset_address = self.w3.to_checksum_address(trading_asset_address)
        self.contract_utils = contract_utils
        self.block_explorer_url = block_explorer_url
        self.block_explorer_api = block_explorer_api

    async def get_account_balance(self):
        """
        Retrieves the account balance of the user.

        Returns:
            str: A formatted string containing
            the account balance in Bitcoin (₿) and
            the trading asset balance like USDT (💵).
        """
        try:
            account_balance = self.w3.eth.get_balance(
                self.wallet_address
            )
            account_balance = self.w3.from_wei(account_balance, "ether") or 0
            trading_asset_balance = await self.get_trading_asset_balance()
            balance = f"{self.account_number} \n"
            balance += f"₿ {round(account_balance,5)}\n$ {trading_asset_balance}"
            return balance
        except Exception as error:
            logger.error(error)

    async def get_trading_asset_balance(self):
        """
        Retrieves the balance of the trading asset
        for the current wallet address.

        Returns:
            The balance of the trading asset as a float.
            If the balance is not available,
            it returns 0.
        """
        trading_asset = await self.contract_utils.get_data(
            contract_address=self.trading_asset_address
        )
        trading_asset_balance = await trading_asset.get_token_balance(
            self.wallet_address
        )
        return trading_asset_balance if trading_asset_balance else 0

    async def get_account_position(self):
        """
        Retrieves the account position.

        Returns:
            str: A string representing the account position.
        """
        position = f"📊 Position {self.account_number} \n"
        position += f"Opened: {str(await self.get_account_open_positions())}\n"
        position += f"Margin: {str(await self.get_account_margin())}"
        return position

    async def get_account_margin(self):
        """
        Get the account margin. Not yet implemented

        Returns:
            int: The account margin.
        """
        return 0

    async def get_account_open_positions(self):
        """
        Get the open positions for the account.
        Not yet implemented

        :return: The number of open positions
        for the account.
        """
        return 0

    async def get_account_pnl(self):
        """
        Get the open positions for the account.
        Not yet implemented

        :return: The number of open positions
        for the account.
        """
        return f"{self.account_number}: 0"

    async def get_approve(self, token_address):
        """
        Given a token address, approve a token

        Args:
            token_address (str): The token address

        Returns:
            approval_tx_hash

        """
        try:
            token = await self.contract_utils.get_data(contract_address=token_address)
            if token.contract is None:
                return
            approved_amount = self.w3.to_wei(2**64 - 1, "ether")
            owner_address = self.w3.to_checksum_address(self.wallet_address)
            dex_router_address = self.w3.to_checksum_address(
                settings.dex_router_contract_addr
            )
            allowance = token.contract.functions.allowance(
                owner_address, dex_router_address
            ).call()
            if allowance == 0:
                approval_tx = token.contract.functions.approve(
                    dex_router_address, approved_amount
                )
                approval_tx_hash = await self.get_sign(approval_tx.transact())
                return self.w3.eth.wait_for_transaction_receipt(approval_tx_hash)
        except Exception as error:
            logger.error("Approval failed {}", error)

    async def get_sign(self, transaction):
        """
        Given a transaction, sign a transaction

        Args:
            transaction (Transaction): The transaction

        Returns:
            signed_tx_hash

        """
        try:
            signed_tx = self.w3.eth.account.sign_transaction(
                transaction, self.private_key
            )
            return self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        except Exception as error:
            logger.error("Sign failed {}", error)

    async def get_gas(self, transaction):
        """
        Given a transaction, get gas estimate

        Args:
            transaction (Transaction): The transaction

        Returns:
            int: The gas estimate

        """
        gas_limit = self.w3.eth.estimate_gas(transaction) * 1.25
        return int(self.w3.to_wei(gas_limit, "wei"))

    async def get_gas_price(self):
        """
        search get gas price

        Returns:
            int: The gas price

        """
        return round(self.w3.from_wei(self.w3.eth.generate_gas_price(), "gwei"), 2)
