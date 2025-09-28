import requests
from collections import defaultdict

def get_eth_balance(address, api_key):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&apikey={api_key}"
    result = requests.get(url).json()
    if result.get("status") == "1":
        return int(result["result"]) / 1e18
    return 0

def get_btc_balance(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    result = requests.get(url).text
    return int(result) / 1e8

def fetch_balances(addresses: dict, eth_api_key: str):
    report = defaultdict(dict)
    for chain, addrs in addresses.items():
        for addr in addrs:
            if chain == "ethereum":
                bal = get_eth_balance(addr, eth_api_key)
                report[chain][addr] = bal
            elif chain == "bitcoin":
                bal = get_btc_balance(addr)
                report[chain][addr] = bal
    return report

def find_dust(report, dust_thresholds):
    dust = defaultdict(dict)
    for chain, addrs in report.items():
        threshold = dust_thresholds.get(chain, 0.0001)
        for addr, amount in addrs.items():
            if 0 < amount < threshold:
                dust[chain][addr] = amount
    return dust

if __name__ == "__main__":
    # Пример использования
    addresses = {
        "ethereum": ["0x742d35Cc6634C0532925a3b844Bc454e4438f44e"],
        "bitcoin": ["1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY"]
    }
    api_key = "YourEtherscanAPIKey"
    dust_thresholds = {"ethereum": 0.005, "bitcoin": 0.001}
    balances = fetch_balances(addresses, api_key)
    dust = find_dust(balances, dust_thresholds)
    print("Dust found:")
    for chain, addr_dict in dust.items():
        for addr, amt in addr_dict.items():
            print(f"{chain}: {addr} – {amt}")
