import random
import asyncio
import string

from starknet_py.net.account.account import Account
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.signer.stark_curve_signer import KeyPair

from utils import script_exceptions, logger
from config import STARKNET_RPC

class StarkNet:
    def __init__(self, index: int, private_key: str, address: hex) -> None:
        self.volume = 0
        self.index = index
        self.private_key = private_key

        self.full_node_client = FullNodeClient(STARKNET_RPC)
        
        self.account = Account(
            client=self.full_node_client,
            address=address,
            key_pair=KeyPair.from_private_key(key=int(self.private_key, 16)),
            chain=StarknetChainId.MAINNET,
        )
    
    @staticmethod
    def generate_random_hex_string():
        max_value = 3618502788666131213697322783095070105623107215331596699973092056135872020481
        hex_chars = string.hexdigits[:-6]
        random_hex = ''.join(random.choices(hex_chars, k=64))
        random_int = int(random_hex, 16)
        random_int %= max_value
        return "0x" + format(random_int, 'x')

    @script_exceptions
    async def send_calls_transaction(self, calls: list, wait: bool) -> None:
        tx_response = await self.account.execute(
            calls=calls,
            nonce=await self.account.get_nonce(),
            auto_estimate=True
        )
        if wait:
            await self.account.client.wait_for_tx(tx_response.transaction_hash)
        else:
            await asyncio.sleep(random.randint(90, 120))
        logger.success(f'Acc.{self.index} : https://starkscan.co/tx/{hex(tx_response.transaction_hash)}')
        

            
