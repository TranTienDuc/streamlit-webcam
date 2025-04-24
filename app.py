import threading
import time
import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2

st.set_page_config(page_title="Webcam App", layout="wide")

lock = threading.Lock()
img_container = {"img": None}

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    imgout = cv2.flip(img,0)
    with lock:
        img_container["img"] = imgout
    return av.VideoFrame.from_ndarray(img, format="bgr24")

col1, col2 = st.columns(2)

ctx = None
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

with col2:
    image_placeholder = st.empty()

if ctx:
    while ctx.state.playing:
        with lock:
            img = img_container["img"]
        if img is not None:
            image_placeholder.image(img, channels="BGR", caption="Processed Frame (Flipped)")
        time.sleep(0.05)
        
