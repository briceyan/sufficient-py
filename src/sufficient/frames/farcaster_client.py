import json
import os
import requests


class FarcasterClient:
    def __init__(self, hub_ep=None, neynar_ep=None, neynar_api_ep=None):
        self._hub_ep = "https://nemes.farcaster.xyz:2281/v1" if not hub_ep else hub_ep
        self._neynar_ep = "https://api.neynar.com/v2" if not neynar_ep else neynar_ep
        self._neynar_api_key = "NEYNAR_API_DOCS" if neynar_api_ep == None else neynar_api_ep

    def verify_message(self, hex_data):
        url = f"{self._hub_ep}/validateMessage"
        data = bytes.fromhex(hex_data)
        header = {'Content-Type': 'application/octet-stream'}
        resp = requests.post(url, headers=header, data=data)
        if resp.ok:
            json = resp.json()
            if json["valid"]:
                return json["message"]
        return None

    def get_user(self, fid):
        users = self.get_users_bulk([fid])
        if users and len(users) > 0:
            return users[0]
        return None

    def get_users_bulk(self, fids):
        csv = ",".join(map(str, fids))
        url = f"{self._neynar_ep}/farcaster/user/bulk?fids={csv}"
        headers = {
            "accept": "application/json",
            "api_key": self._neynar_api_key
        }
        resp = requests.get(url, headers=headers)
        if resp.ok:
            json = resp.json()
            return json["users"]
        return None

    def get_casts_recent(self, casts):
        csv = ",".join(casts)
        sort_type = "recent"
        url = f"{self._neynar_ep}/farcaster/casts?casts={csv}&sort={sort_type}"
        headers = {
            "accept": "application/json",
            "api_key": self._neynar_api_key
        }
        resp = requests.get(url, headers=headers)
        if resp.ok:
            json = resp.json()
            return json["result"]["casts"]
        return None

    def fetch_image(self, url):
        resp = requests.get(url)
        if resp.ok:
            return resp.content
        return None
