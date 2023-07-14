"""
0️⃣x
"""
from dxsp.config import settings
from dxsp.main import DexSwap
from dxsp.utils.utils import get ,get_sign

class DexSwapZeroX(DexSwap):
    async def get_quote(self, buy_address, sell_address, amount=1):
        try:
            out_amount = amount * (10 ** await self.contract_utils.get_token_decimals(sell_address))
            url = f"{settings.dex_0x_url}/swap/v1/quote?buyToken={str(buy_address)}&sellToken={str(sell_address)}&sellAmount={str(out_amount)}"
            headers = {"0x-api-key": settings.dex_0x_api_key}
            response = await get(url, params=None, headers=headers)
            if response:
                quote = float(response['guaranteedPrice'])
                return quote
        except Exception as error:
            raise ValueError(f"Quote failed {error}") 

    async def get_swap(self, buy_address, sell_address, amount):
        swap_order = await self.get_quote(buy_address, sell_address, amount)
        return await get_sign(swap_order)