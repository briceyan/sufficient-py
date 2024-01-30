from sufficient.frames.frame_app_runner import FrameAppRunner
from sufficient.examples import example, degen
import os


class TestFrameAppRunner:
    # def test_on_start(self):
    #     app = FrameAppRunner(example)
    #     html = app.on_start()
    #     print(html)

    # def test_to_picture(self):
    #     app = FrameAppRunner(example)
    #     r = app.to_picture(
    #         "PageHome", "7b2263617374223a20302c2022636173746572223a2022222c20226163746f72223a20302c2022616374696f6e223a20307d_7b7d")
    #     print(r)

    def test_on_click(self):
        app = FrameAppRunner(example)
        r = app.on_click("PageNext", untrusted_data)
        print(r)

    def test_next_picture(self):
        app = FrameAppRunner(example)
        r = app.to_picture("PageNext","7b2263617374223a2022307833363131663331336262393639656634343033353633316563326463626233393532626634613534222c2022636173746572223a203231393138372c20226163746f72223a203231393138372c2022616374696f6e223a20327d_7b7d")
        print(r)


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
