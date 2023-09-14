import asyncio

from client.starknet import StarkNet


with open('addresses.txt', 'r') as file:
    address = [key.strip() for key in file]
    
with open('private_keys.txt', 'r') as file:
    private = [key.strip() for key in file]


async def main():
    for index, (key, adr) in enumerate(zip(private, address), start=1):
        client = StarkNet(index, key, adr)
        await client.mint_domain()

if __name__ == '__main__':
    asyncio.run(main())
