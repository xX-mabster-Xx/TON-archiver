import asyncio
from pytonconnect import TonConnect
import json

async def connect(connector: TonConnect):
    wallets_list = connector.get_wallets()
    loop = asyncio.get_running_loop()
        
    i = 0
    for wallet in wallets_list:
        i += 1
        print(f'{i}: {wallet["name"]}')
    chosen = ''
    while not chosen.isdecimal() or int(chosen) > len(wallets_list) or int(chosen) < 1:
        chosen = await loop.run_in_executor(None, input, f"Choose wallet to connect[1-{i}]: ")
    generated_url = await connector.connect(wallets_list[int(chosen)-1])
    print('generated_url:', generated_url)


async def main():
    connector = TonConnect(manifest_url='https://raw.githubusercontent.com/xX-mabster-Xx/TON-archiver/refs/heads/main/manifest.json')
    is_connected = await connector.restore_connection()
    print('is_connected:', is_connected)
    wallets_list = connector.get_wallets()
    # print(json.dumps(wallets_list, indent=4))

    def status_changed(wallet_info):
        print('wallet_info:', wallet_info)
        unsubscribe()

    def status_error(e):
        print('connect_error:', e)

    unsubscribe = connector.on_status_change(status_changed, status_error)



    for i in range(120):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                print('Connected with address:', connector.account.address)
            break


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())