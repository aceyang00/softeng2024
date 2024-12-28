from gpiozero import Button, LED
from time import sleep
import pyaudio
import wave
import urllib3
import json
import base64
import os
import time
import subprocess
from datetime import datetime
import threading
from gtts import gTTS

# GPIO 설정
button = Button(23, pull_up=False)
led = LED(2)

# 전역 변수 설정
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
ACCESS_KEY = "092c787b-0cda-4cdc-8a54-5e4bd7874e1a"

# 녹음 관련 전역 변수
recording = False
frames = []
audio_thread = None
p = None
stream = None

def get_device_info():
    """사용 가능한 오디오 장치 정보를 출력하고 확인하는 함수"""
    global p
    if p is None:
        p = pyaudio.PyAudio()
    info = p.get_default_input_device_info()
    # print("\n기본 입력 장치 정보:")
    # print(f"장치 이름: {info['name']}")
    # print(f"지원 샘플레이트: {int(info['defaultSampleRate'])}Hz")
    return info

def convert_sample_rate(input_file, output_file, target_rate=16000):
    """sox를 사용하여 오디오 파일의 샘플레이트를 변환하는 함수"""
    try:
        subprocess.run(['sox', input_file, '-r', str(target_rate), output_file, 'gain', '-3'], check=True)
        print(f"샘플레이트를 {target_rate}Hz로 변환했습니다.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"샘플레이트 변환 중 오류 발생: {str(e)}")
        return False
    except FileNotFoundError:
        print("sox가 설치되어 있지 않습니다. 'sudo apt-get install sox' 명령으로 설치해주세요.")
        return False

def record_audio_thread():
    """별도 스레드에서 실행될 녹음 함수"""
    global recording, frames, p, stream
    device_info = get_device_info()
    device_sample_rate = int(device_info['defaultSampleRate'])
    if p is None:
        p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=device_sample_rate,
                    input=True,
                    input_device_index=0,
                    frames_per_buffer=CHUNK)
    frames = []
    while recording:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        except Exception as e:
            print(f"녹음 중 오류 발생: {str(e)}")
            break
    stream.stop_stream()
    stream.close()

def convert_speech_to_text(audio_file_path):
    """ETRI Open API를 사용하여 음성을 텍스트로 변환하는 함수"""
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    languageCode = "korean"
    try:
        with open(audio_file_path, "rb") as file:
            audioContents = base64.b64encode(file.read()).decode("utf8")
        requestJson = {
            "argument": {
                "language_code": languageCode,
                "audio": audioContents}}
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": ACCESS_KEY},
            body=json.dumps(requestJson))
        response_data = json.loads(response.data.decode('utf-8'))
        if response.status == 200:
            recognized_text = response_data.get('return_object', {}).get('recognized', '')
            return recognized_text
        else:
            print(f"Error: API 응답 코드 {response.status}")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def text_to_speech(text, language='ko'):
    """텍스트를 음성으로 변환하여 재생하는 함수"""
    try:
        tts = gTTS(text=text, lang=language)
        tts.save("speech.mp3")
        os.system("mpg321 speech.mp3")
        sleep(2)
        os.remove("speech.mp3")
        return True
    except Exception as e:
        print(f"에러가 발생했습니다: {str(e)}")
        return False

def save_and_convert_audio():
    """녹음된 오디오를 저장하고 텍스트로 변환 및 음성 출력하는 함수"""
    global frames, p
    if not frames:
        return
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_audio_file = f"temp_audio_{timestamp}.wav"
    converted_audio_file = f"converted_{temp_audio_file}"
    try:
        wf = wave.open(temp_audio_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        if convert_sample_rate(temp_audio_file, converted_audio_file):
            result_text = convert_speech_to_text(converted_audio_file)
            if result_text:
                print("\n인식된 텍스트:")
                print(result_text)
                text_to_speech(result_text)
            else:
                print("텍스트 변환에 실패했습니다.")
    finally:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
        if os.path.exists(converted_audio_file):
            os.remove(converted_audio_file)
        print("* 임시 녹음 파일들이 삭제되었습니다.")

def button_pressed():
    """버튼이 눌렸을 때 LED를 켜고 녹음을 시작하는 함수"""
    global recording, audio_thread
    led.on()
    print("LED ON")
    print("녹음을 시작합니다...")
    recording = True
    audio_thread = threading.Thread(target=record_audio_thread)
    audio_thread.start()

def button_released():
    """버튼에서 손을 뗐을 때 LED를 끄고 녹음을 종료하는 함수"""
    global recording, audio_thread, p
    led.off()
    print("LED OFF")
    print("녹음을 종료합니다...")
    recording = False
    if audio_thread:
        audio_thread.join()
    save_and_convert_audio()

# 버튼 이벤트 설정
button.when_pressed = button_pressed
button.when_released = button_released

try:
    print("프로그램이 시작되었습니다.")
    print("버튼을 누르고 있는 동안 녹음이 진행됩니다.")
    print("버튼에서 손을 떼면 녹음이 종료되고 텍스트로 변환 및 음성으로 출력됩니다.")
    print("프로그램을 종료하려면 Ctrl+C를 누르세요.")
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    print("\n프로그램을 종료합니다...")
finally:
    recording = False
    if audio_thread and audio_thread.is_alive():
        audio_thread.join()
    if stream:
        stream.stop_stream()
        stream.close()
    if p:
        p.terminate()
    button.close()
    led.close()