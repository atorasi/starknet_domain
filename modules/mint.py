import random
import asyncio

from starknet_py.contract import Contract

from client.starknet import StarkNet
from config import SLEEP_ACCS_MIN, SLEEP_ACCS_MAX, SLEEP
from utils import script_exceptions, logger, abi_read


class MintStarkDomain(StarkNet):
    def __init__(self, index: int, private_key: str, address: hex) -> None:
        super().__init__(index, private_key, address)
        
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