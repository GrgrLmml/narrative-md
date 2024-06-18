import asyncio
import io
import tempfile
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from pydub import AudioSegment
from openai import OpenAI

from config.config import OPEN_AI_API_KEY, logger
from utils.calls import new_questionnaire


# Global variables to store samples and accumulated time
samples = np.array([], dtype=np.int16)
accumulated_time = 0.0
SAMPLE_TIME = 5.0  # Time in seconds
OVERLAP_TIME = 1.0  # Time in seconds
prev_segment = 'There is no previous segment.'

client = OpenAI(api_key=OPEN_AI_API_KEY)


def audio_callback(audio_frame):
    global samples, accumulated_time, prev_segment

    # Convert the audio frame to an ndarray and ensure it's the right type
    data = audio_frame.to_ndarray().astype(np.int16)
    frame_time = data.shape[1] / (2 * audio_frame.sample_rate)
    accumulated_time += frame_time

    # Append new data to the existing samples
    samples = np.concatenate((samples, data.ravel()))

    # print(f"audio_frame received: {data.shape}, {audio_frame.sample_rate}, {audio_frame.format}, {accumulated_time}")

    if accumulated_time >= SAMPLE_TIME:
        samples_to_retain = int(OVERLAP_TIME * 2 * audio_frame.sample_rate)
        audio_segment = AudioSegment(
            data=samples.tobytes(),  # Raw audio data
            sample_width=2,  # 16-bit PCM
            frame_rate=2 * audio_frame.sample_rate,  # Sample rate from the frame
            channels=1,  # Mono audio
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
            audio_segment.export(tmpfile.name, format='mp3', bitrate='128k')  # Export audio to MP3 format
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=open(tmpfile.name, "rb"),
                language="en",
                prompt=f"Transcribe the following audio segment. To guide you I provide your with the previous segment: {prev_segment}. Also bear in mind that there is a 1s overlap between segments.",
            )
            prev_segment = transcription.text
            logger.info(f"Transcription: {prev_segment}")

        samples = samples[-samples_to_retain:]
        accumulated_time = OVERLAP_TIME


def render_screen():
    st.title("narrative-md demo")

    if st.session_state.get("project") is None:
        project = st.text_input("Enter project name")
        questions = st.text_area(label="Sample questions (feel free to modify)",
                                 value="""What is your reason for coming today? (open question)
    Do you smoke yes/no? (boolean)
    If yes, how many cigarettes per day (number) and what age did you start (number)
    How did your weight change last month? (multiple choice, stable, lost weight gained weight)
    Can you currently walk 2 km without fatigue yes/no? (boolean)
    List the medications you are presently taking? (list)
    How tall are you? (number)""", height=200)
        click = st.button("Start", disabled=st.session_state.get("project", "") != "")
        if click:
            st.session_state.project = project
            asyncio.run(new_questionnaire({"name": project, "questions": questions}))
            st.rerun()
    else:
        project = st.session_state.project
        st.markdown(f"Project: {project}")
        webrtc_streamer(key="sample", mode=WebRtcMode.SENDONLY, sendback_video=False, sendback_audio=True,
                        audio_frame_callback=audio_callback, media_stream_constraints={
                "audio": True,
                "video": False
            })

    # st.write(st.session_state.num_frames)


render_screen()
