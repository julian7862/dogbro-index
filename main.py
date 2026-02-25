import shioaji as sj
from src.utils.config import config

print(sj.__version__)

def main():
    api = sj.Shioaji(simulation=True)
    api.login(
        api_key=config.api_key,
        secret_key=config.secret_key,
        fetch_contract=False
    )
    api.activate_ca(
        ca_path=config.ca_cert_path,
        ca_passwd=config.ca_password,
    )
    print("login and activate ca success")
    print(list(api.Contracts.Options.TXO.items())[:3])

if __name__ == "__main__":
    main()
