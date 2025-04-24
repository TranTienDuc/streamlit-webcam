import threading
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2

st.set_page_config(page_title="Webcam App", layout="wide")

lock = threading.Lock()
img_container = {"imgin": None}

def video_frame_callback(frame):
    imgin = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["imgin"] = imgin
    return

col1, col2 = st.columns(2)

with col1:
    ctx = webrtc_streamer(
                key="sample",
                mode=WebRtcMode.SENDRECV,
                media_stream_constraints={"video": True, "audio": False},
                video_frame_callback=video_frame_callback,
                rtc_configuration= 
                {
                    "iceServers": [{"urls": ["stun:stun.relay.metered.ca:80"]},
                                   {"urls": ["turn:asia.relay.metered.ca:80"],
                                    "username": "5f056e7d0dc59e50e3deeaa6",
                                    "credential": "ktMeHfTxMPOhP6v+",
                                   },
                                   {"urls": ["turn:asia.relay.metered.ca:80?transport=tcp"],
                                    "username": "5f056e7d0dc59e50e3deeaa6",
                                    "credential": "ktMeHfTxMPOhP6v+",
                                   },
                                   {"urls": ["turn:asia.relay.metered.ca:443"],
                                    "username": "5f056e7d0dc59e50e3deeaa6",
                                    "credential": "ktMeHfTxMPOhP6v+",
                                   },
                                   {"urls": ["turns:asia.relay.metered.ca:443?transport=tcp"],
                                    "username": "5f056e7d0dc59e50e3deeaa6",
                                    "credential": "ktMeHfTxMPOhP6v+",
                                   },
                                   ]
                },
                async_processing=True
          )

imgout_place = col2.empty()

while ctx.state.playing:
    with lock:
        imgin = img_container["imgin"]
    if imgin is None:
        continue

    # Đặt chương trình đóng khung khuôn mặt ở đây
    imgout = cv2.flip(imgin,1)

    imgout_place.image(imgout,channels='BGR')
