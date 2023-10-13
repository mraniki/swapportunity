"""
Kwenta 🧮

"""
from loguru import logger
from kwenta import Kwenta

from dxsp.protocols import DexClient


class DexKwenta(DexClient):
    """
    A DexClient using kwenta-python library

    More info
    https://github.com/Kwenta/kwenta-python-sdk

    """

    async def get_quote(self, buy_address=None, symbol=None, amount=1):
        """ """
        #pass
        try:
            kwenta = Kwenta(
                network_id=10,
                provider_rpc=self.rpc,
                wallet_address=self.wallet_address,
                private_key=self.private_key,
            )
            symbol = await self.replace_instrument(symbol)
            sell_token = await self.contract_utils.get_data(symbol=symbol)
            asset = 'ETH'
            #asset = sell_token.symbol
            market = kwenta.markets[asset]
            logger.info("market: {}", market)
    
            quote = kwenta.get_current_asset_price(asset)
            logger.info("quote: {}", quote)
            return quote
        except Exception as error:
            logger.debug(error)


    async def make_swap(self, sell_address, buy_address, amount):
        """ """
        pass

        # kwenta = Kwenta(
        #     network_id=10,
        #     provider_rpc="https://optimism.llamarpc.com",
        #     wallet_address=self.wallet_address,
        #     private_key=self.private_key,
        # )
        # symbol = self.contract_utils.get_token_symbol(buy_address)
        # logger.debug(f"Symbol: {symbol}\n")
        # # get the market info for the asset
        # market = kwenta.markets[symbol]
        # logger.debug(f"Market: {market}\n")

        # # check margin balance
        # margin_balance_before = kwenta.get_accessible_margin(symbol)
        # logger.debug(f"Starting margin balance: {margin_balance_before}\n")

        # # transfer margin to the market
        # transfer_margin = kwenta.transfer_margin(symbol, 100, execute_now=True)
        # logger.debug(f"Transfer tx: {transfer_margin}\n")

        # # wait for the transfer to be mined
        # kwenta.web3.eth.wait_for_transaction_receipt(transfer_margin)
        # logger.debug("Transfer transaction confirmed\n")
        # await asyncio.sleep(10)

        # # check margin balance again
        # margin_balance_after = kwenta.get_accessible_margin(symbol)
        # logger.debug(f"Ending margin balance: {margin_balance_after}\n")

        # # submit an order
        # open_position = kwenta.modify_position(
        # symbol,
        # size_delta=0.5,
        # execute_now=True)
        # logger.debug(f"Open position tx: {open_position}\n")

        # # wait for the transfer to be mined
        # kwenta.web3.eth.wait_for_transaction_receipt(open_position)
        # logger.debug("Order transaction confirmed\n")
        # await asyncio.sleep(2)

        # # check the order status
        # order_before = kwenta.check_delayed_orders(symbol)
        # logger.debug(f"Order before: {order_before}\n")
        # await asyncio.sleep(20)

        # # check the open position
        # position = kwenta.get_current_position(symbol)
        # logger.debug(f"Position: {position}\n")

        # # check the order status again
        # order_after = kwenta.check_delayed_orders(symbol)
        # logger.debug(f"Order after: {order_after}\n")
