from arizon_usb_apiserver.client.api.default import get_status_v1_arizon_status_get, get_force_v1_arizon_force_get, toggle_force_v1_arizon_force_put

from arizon_usb_apiserver.client import Client

if __name__ == '__main__':
    client = Client(base_url="http://127.0.0.1:8080", timeout=5, verify_ssl=False)
    print(get_status_v1_arizon_status_get.sync_detailed(client=client))
    print(toggle_force_v1_arizon_force_put.sync_detailed(client=client, flag=True))
    print(get_force_v1_arizon_force_get.sync_detailed(client=client))
