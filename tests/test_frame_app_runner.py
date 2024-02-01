from sufficient.frames import FrameAppRunner
from .frame_apps import gm as gm_app
import os


class TestFrameAppRunner:
    def test_main_page_meta(self):
        app_path = gm_app.__file__
        app_dir = os.path.dirname(app_path)
        static_dir = os.path.join(app_dir, "static")
        templates_dir = os.path.join(app_dir,  "templates")
        data_dir = os.path.join(app_dir,  "data")

        host = "http://localhost:5000"
        app = FrameAppRunner(gm_app, static_dir,
                             templates_dir, data_dir=data_dir)
        framelet = app.start()
        print(framelet, host)
        html = app.gen_frame_html(framelet, host)
        print(html)
        html = app.gen_frame_html(framelet, host, og=True)
        print(html)

    # def test_main_page_click_button_1(self):
    #     app = FrameAppRunner(gm_app, "http://localhost:3000")
    #     frame_meta = app.click("PageHome", untrusted_data)
    #     html = app.gen_frame_html(frame_meta)
    #     print(html)


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
