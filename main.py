import asyncio
from client.starknet import StarkNet


with open('addresses.txt', 'r') as file:
    addresses = [key.strip() for key in file]
    
with open('private_keys.txt', 'r') as file:
    stark_keys = [key.strip() for key in file]

async def main():
    for index, (key, address) in enumerate(zip(stark_keys, addresses), start=1):
        client = StarkNet(index, key, address)
        await client.mint_domain()

if __name__ == '__main__':
    asyncio.run(main())
