import random
import asyncio
import string

from starknet_py.net.account.account import Account
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.contract import Contract

from utils import script_exceptions, logger, abi_read
from config import STARKNET_RPC, SLEEP_ACCS_MIN, SLEEP_ACCS_MAX, SLEEP


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
    
    def generate_random_hex_string(self):
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
        
    @script_exceptions
    async def mint_domain(self) -> None:
        logger.info(f'Acc.{self.index} : Start Minting Domain')
        contract_id = Contract(
            address=0x05DBDEDC203E92749E2E746E2D40A768D966BD243DF04A6B712E222BC040A9AF,
            abi=abi_read('abies\\nameservice.json'),
            provider=self.account,
        )
        contract_token = Contract(    
            address=0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7,
            abi=abi_read('abies\stark_token.json'),
            provider=self.account,
        )
        contract_domain = Contract(    
            address=0x06ac597f8116f886fa1c97a23fa4e08299975ecaf6b598873ca6792b9bbfb678,
            abi=abi_read('abies\domain.json'),
            provider=self.account,
        )
        
        calls = [
            contract_id.functions["mint"].prepare(
                nft_data := random.randint(400000, 20000000)
            ),
            contract_token.functions['approve'].prepare(
                int("0x6ac597f8116f886fa1c97a23fa4e08299975ecaf6b598873ca6792b9bbfb678", 16),
                599178082191783
            ),
            contract_domain.functions['buy_discounted'].prepare(
                nft_data,
                domain := nft_data * random.randint(12700, 92318),
                'Q',
                0,
                self.account.address,
                1,
                int(self.generate_random_hex_string(), 16)
            ),
            contract_domain.functions['set_address_to_domain'].prepare(
                [
                    domain
                ]
            ),
        ]
        
        logger.info(f'Acc.{self.index} : Transaction Was Sent. Waiting Confirmation')
        await self.send_calls_transaction(calls=calls, wait=False)
        if SLEEP:
            await asyncio.sleep(random.randint(SLEEP_ACCS_MIN, SLEEP_ACCS_MAX))
            
