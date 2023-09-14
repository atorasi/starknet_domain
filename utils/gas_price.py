from web3 import Web3
import asyncio

from utils import script_exceptions, logger
from config import ETHER_RPC, NEED_GAS

@script_exceptions
async def wait_for_gas(index) -> int:
    logger.info(f'Acc.{index} : Waiting for gas. . .')
    while True:
        w3 = Web3(Web3.HTTPProvider(ETHER_RPC))
        gas = w3.eth.gas_price
        if gas / 1_000_000_000 > NEED_GAS:
            await asyncio.sleep(10)
        
        logger.success(f"Acc.{index} : Right gas. Starting work. . .")
        return gas
    
