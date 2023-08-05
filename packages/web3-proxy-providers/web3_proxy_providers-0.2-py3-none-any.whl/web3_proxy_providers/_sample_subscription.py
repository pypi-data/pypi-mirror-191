import sys
import asyncio
import logging
from Crypto.Hash import keccak
from python_socks import ProxyType

from web3 import Web3
from web3.eth import AsyncEth
from web3_proxy_providers import AsyncSubscriptionWebsocketWithProxyProvider


async def main(loop: asyncio.AbstractEventLoop):
    provider = AsyncSubscriptionWebsocketWithProxyProvider(
        loop,
        endpoint_uri='wss://eth-mainnet.g.alchemy.com/v2/rVCgqIgyl9A_k0ekaiPwAS7q8s5tx1ls',
        proxy_type=ProxyType.SOCKS5,
        proxy_host='localhost',
        proxy_port=9088,
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    provider.logger.addHandler(handler)
    provider.logger.setLevel(logging.DEBUG)
    w3 = Web3(
        provider,
        modules={'eth': (AsyncEth,)},
        middlewares=[]
    )
    block_number = await w3.eth.get_block_number()
    print(f'Block number is {block_number}')

    async def callback(subs_id: str, json_result):
        print(json_result)

    pair_addresses = [
        '0x5cac3899499612e4eb3cd828ce9acf5c15163953',
        '0x21b8065d10f73ee2e260e5b47d3344d3ced7596e',
        '0xb4e16d0168e52d35cacd2c6185b44281ec28c9dc',
        '0xae461ca67b15dc8dc81ce7615e0320da1a9ab8d5',
        '0x7d7e813082ef6c143277c71786e5be626ec77b20',
        '0x61b62c5d56ccd158a38367ef2f539668a06356ab',
        '0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852',
        '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11',
    ]
    k = keccak.new(data=b'Swap(address,uint256,uint256,uint256,uint256,address)', digest_bits=256)
    swap_topic = "0x" + k.hexdigest()

    # subscription_id = await provider.subscribe(['alchemy_minedTransactions'], callback)
    subscription_id = await provider.subscribe(
        [
            'logs',
            {
                "address": pair_addresses,
                "topics": [swap_topic]
            }
        ],
        callback
    )
    print(f'Subscribed with id {subscription_id}')

    await asyncio.sleep(30)
    await provider.unsubscribe(subscription_id)


if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    async_loop.run_until_complete(
        main(async_loop)
    )
    async_loop.run_forever()
