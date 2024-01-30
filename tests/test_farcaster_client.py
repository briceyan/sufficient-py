from sufficient.frames import FarcasterClient


untrusted_data = {
    "untrustedData":    {
        "fid": 219187,
        "url": "https://3be4974cca45.ngrok.app/",
        "messageHash": "0x8b66528b75fa5aecd147e2a971afdee3057236b5",
        "timestamp": 1706533881000,
        "network": 1,
        "buttonIndex": 2,
        "castId": {
            "fid": 219187,
            "hash": "0x3611f313bb969ef44035631ec2dcbb3952bf4a54"
        }
    },
    "trustedData": {
        "messageBytes": "0a4f080d10b3b00d18f9fba42e200182013f0a1f68747470733a2f2f3362653439373463636134352e6e67726f6b2e6170702f10021a1a08b3b00d12143611f313bb969ef44035631ec2dcbb3952bf4a5412148b66528b75fa5aecd147e2a971afdee3057236b518012240a6c915640f57f2b839d5a6710bc68b51f30d2264c20fe4d0174ff4d02cea349d560fc7fc92acbfabfd11e1e36d3bb675b9f62684ad003314c7cb55dbbbb24b0a280132205f63ad6da952c2dd37191283bb4672aff6ea8738d9ec986687283be803f7b040"
    }
}

verify_resp = {
    "valid": True,
    "message": {
        "data": {
            "type": "MESSAGE_TYPE_FRAME_ACTION",
            "fid": 21828,
            "timestamp": 96774342,
            "network": "FARCASTER_NETWORK_MAINNET",
            "frameActionBody": {
                "url": "aHR0cDovL2V4YW1wbGUuY29t",
                "buttonIndex": 1,
                "castId": {
                    "fid": 21828,
                    "hash": "0x1fd48ddc9d5910046acfa5e1b91d253763e320c3"
                }
            }
        },
        "hash": "0x230a1291ae8e220bf9173d9090716981402bdd3d",
        "hashScheme": "HASH_SCHEME_BLAKE3",
        "signature": "8IyQdIav4cMxFWW3onwfABHHS9IroWer6Lowo16AjL6uZ0rve3TTFhxhhuSOPMTYQ8XsncHc6ca3FUetzALJDA==",
        "signer": "0x196a70ac9847d59e039d0cfcf0cde1adac12f5fb447bb53334d67ab18246306c"
    }
}


class TestFarcasterClient:
    def test_verify_message(self):
        c = FarcasterClient()
        r = c.verify_message(untrusted_data["trustedData"]["messageBytes"])
        print(r)

    def test_get_users(self):
        c = FarcasterClient()
        r = c.get_users_bulk([21828, 227193])
        print(r)

    def test_get_user(self):
        c = FarcasterClient()
        r = c.get_user(227193)
        print(r)

    def test_get_casts_recent(self):
        c = FarcasterClient()
        r = c.get_casts_recent(["0x8c828e5f011ead03300dde7a45d52405cec01aab",
                                "0xe1ae75b7184d8080241b90100861c3d7e20e5609"])
        print(r)
