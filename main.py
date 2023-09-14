import asyncio

from modules.mint import MintStarkDomain
from utils import wait_for_gas

with open('wallets\\addresses.txt', 'r') as file:
    address = [key.strip() for key in file]
    
with open('wallets\private_keys.txt', 'r') as file:
    private = [key.strip() for key in file]


async def main():
    for index, (key, adr) in enumerate(zip(private, address), start=1):
        await wait_for_gas(index)
        client = MintStarkDomain(index, key, adr)
        await client.mint_domain()


if __name__ == '__main__':
    asyncio.run(main())
