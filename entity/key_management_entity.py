import requests
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class KeyManagementEntity:
    account_id: str
    kme_id: str
    ca_cert: Path
    client_cert: tuple[Path, Path]
    headers: dict[str, str] = field(
        default_factory=lambda: {"Accept": "application/json"}
    )
    base_url: str = field(init=False)

    def __post_init__(self):
        self.base_url = f"https://{self.kme_id}.acct-{self.account_id}.etsi-qkd-api.qukaydee.com/api/v1/keys"

    def get_status(self, sae_id: str):
        url = f"{self.base_url}/{sae_id}/status"
        response = requests.get(
            url, headers=self.headers, verify=self.ca_cert, cert=self.client_cert
        )
        return response.status_code, response.json()

    def get_key(self, sae_id: str, number: int, size: int):
        url = f"{self.base_url}/{sae_id}/enc_keys?number={number}&size={size}"
        response = requests.get(
            url, headers=self.headers, verify=self.ca_cert, cert=self.client_cert
        )
        return response.status_code, response.json()

    def get_key_with_id(self, sae_id: str, key_id: str):
        url = f"{self.base_url}/{sae_id}/dec_keys?key_ID={key_id}"
        response = requests.get(
            url, headers=self.headers, verify=self.ca_cert, cert=self.client_cert
        )
        return response.status_code, response.json()
