# 라즈베리파이 센서 연결 완성
from gpiozero import Button, LED, OutputDevice, InputDevice, TonalBuzzer
from gpiozero.tones import Tone
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
from googletrans import Translator
translator = Translator()

class DHT11():
    MAX_DELAY_COUINT = 100
    BIT_1_DELAY_COUNT = 10
    BITS_LEN = 40
    def __init__(self, pin, pull_up=False):
        self._pin = pin
        self._pull_up = pull_up
    def read_data(self):
        bit_count = 0
        delay_count = 0
        bits = ""
        # -------------- send start --------------
        gpio = OutputDevice(self._pin)
        gpio.off()
        time.sleep(0.02)
        gpio.close()
        gpio = InputDevice(self._pin, pull_up=self._pull_up)
        # -------------- wait response --------------
        while gpio.value == 1:
            pass
        # -------------- read data --------------
        while bit_count < self.BITS_LEN:
            while gpio.value == 0:
                pass
            while gpio.value == 1:
                delay_count += 1
                if delay_count > self.MAX_DELAY_COUINT:
                    break
            if delay_count > self.BIT_1_DELAY_COUNT:
                bits += "1"
            else:
                bits += "0"
            delay_count = 0
            bit_count += 1
        # -------------- verify --------------
        humidity_integer = int(bits[0:8], 2)
        humidity_decimal = int(bits[8:16], 2)
        temperature_integer = int(bits[16:24], 2)
        temperature_decimal = int(bits[24:32], 2)
        check_sum = int(bits[32:40], 2)
        _sum = humidity_integer + humidity_decimal + temperature_integer + temperature_decimal
        if check_sum != _sum:
            humidity = 0.0
            temperature = 0.0
        else:
            humidity = float(f'{humidity_integer}.{humidity_decimal}')
            temperature = float(f'{temperature_integer}.{temperature_decimal}')
        return humidity, temperature
    @staticmethod
    def calculate_vpd(temperature, humidity):
        svp = 0.6108 * 2.71828 ** ((17.27 * temperature) / (temperature + 237.3))
        avp = svp * (humidity / 100.0)
        vpd = svp - avp
        return vpd

# GPIO 설정
button1 = Button(23, pull_up=False, bounce_time=0.05)  # 음성인식용 버튼
led1 = LED(2, active_high=False)  # 음성인식용 LED
button2 = Button(14, pull_up=False, bounce_time=0.05)   # 번역(한글->영어) 버튼
led2 = LED(4)  # 번역 LED
button3 = Button(15, pull_up=False, bounce_time=0.05)    # 번역(영어->한글) 버튼  #삭제
button4 = Button(17, pull_up=False, bounce_time=0.05)    # 5개국어 전환 버튼    #삭제
button5 = Button(26, pull_up=False, bounce_time=0.05)  # 창문 제어용 버튼
led3 = LED(24)  # 창문 상태 LED
button6 = Button(19, pull_up=False, bounce_time=0.05)  # 차광막 제어용 버튼
led4 = LED(12)  # 차광막 상태 LED

dht11 = DHT11(18)
buzzer = TonalBuzzer(25)

# 엘리제를 위하여 음계
notes = [('E5', 0.3),  # 미
    ('D#5', 0.3),  # 레#
    ('E5', 0.3),  # 미
    ('D#5', 0.3),  # 레#
    ('E5', 0.3),  # 미
    ('B4', 0.3),  # 시
    ('D5', 0.3),  # 레
    ('C5', 0.3),  # 도
    ('A4', 0.5),  # 라

    ('C4', 0.3),  # 도
    ('E4', 0.3),  # 미
    ('A4', 0.3),  # 라
    ('B4', 0.5),  # 시

    ('E4', 0.3),  # 미
    ('G#4', 0.3),  # 솔#
    ('B4', 0.3),  # 시
    ('C5', 0.5),  # 도
    # ('E5', 0.3),  # 미 # ('D#5', 0.3),  # 레# # ('E5', 0.3),  # 미 # ('D#5', 0.3),  # 레# # ('E5', 0.3),  # 미
    # ('B4', 0.3),  # 시 # ('D5', 0.3),  # 레 # ('C5', 0.3),  # 도 # ('A4', 0.5),  # 라
]

def play_fur_elise():
    """엘리제를 위하여 연주 함수"""
    try:
        for note, duration in notes:
            buzzer.play(Tone(note))
            sleep(duration)
    finally:
        buzzer.stop()

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

# LED 상태 변수
led3_state = False  # 창문 상태
led4_state = False  # 차광막 상태

def get_device_info():
    global p
    if p is None:
        p = pyaudio.PyAudio()
    info = p.get_default_input_device_info()
    return info

def convert_sample_rate(input_file, output_file, target_rate=16000):
    try:
        subprocess.run(['sox', input_file, '-r', str(target_rate), output_file, 'gain', '-6'], check=True)
        print(f"샘플레이트를 {target_rate}Hz로 변환했습니다.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"샘플레이트 변환 중 오류 발생: {str(e)}")
        return False
    except FileNotFoundError:
        print("sox가 설치되어 있지 않습니다. 'sudo apt-get install sox' 명령으로 설치해주세요.")
        return False

def record_audio_thread():
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
            headers={"Content-Type": "application/json; charset=UTF-8",
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

def control_window(command):
    global led3_state
    if command == 'open':
        led3_state = True
        led3.on()
        return "측창을 열었습니다."
    else:
        led3_state = False
        led3.off()
        return "측창을 닫았습니다."

def control_shade(command):
    global led4_state
    if command == 'open':
        led4_state = True
        led4.on()
        return "차광막 닫힙니다."
    else:
        led4_state = False
        led4.off()
        return "차광막 열립니다."

def process_text_response(text):
    humidity, temperature = dht11.read_data()
    if '날씨' in text or '온도' in text:
        if temperature > 28:
            return f"현재 온도는 {temperature:.1f}°C 입니다. 온도를 낮춰 주세요."
        elif temperature <16:
            return f"현재 온도는 {temperature:.1f}°C 입니다. 온도를 높혀 주세요."
        else:
            return f"현재 온도는 {temperature:.1f}°C 입니다."
    elif '습도' in text:
        return f"현재 습도는 {humidity:.1f}%입니다."
    elif 'vpd' in text.lower() or '브이피디' in text or '브이PD' in text:
        vpd = DHT11.calculate_vpd(temperature, humidity)
        if vpd > 1.5:
            return f"현재 VPD는 {vpd:.2f} kPa입니다. 가습을 해주세요."
        elif vpd <0.8:
            return f"현재 VPD는 {vpd:.2f} kPa입니다. 제습을 해주세요."
        else:
            return f"현재 VPD는 {vpd:.2f} kPa입니다."
    elif '측창' in text or '창문' in text:
        if '열어' in text:
            return control_window('open')
        elif '닫아' in text:
            return control_window('close')
    elif '차광막' in text:
        if '쳐' in text or '처' in text or '닫아' in text:
            return control_shade('open')
        elif '걷어' in text or '열어' in text:
            return control_shade('close')
    elif '부저' in text or '장갑' in text or '영양제' in text or '마스크' in text:
        threading.Thread(target=play_fur_elise).start()
        return "재고가 1개 남았습니다."
    elif '멋진직업' in text or '멋진 직업' in text:
        return "그것은 정우성의 dm 메시지 입니다"
    elif '{"reason": "ERROR_WHILE_EVAL_PRONSCORE"}' in text:
        return "죄송합니다. 다시 말씀해주세요."
    else:
        return "현재 개발중입니다."

def text_to_speech(text, language='ko'):
    try:
        if not text or len(text.strip()) == 0:
            print("음성 변환할 텍스트가 없습니다.")
            tts = gTTS(text="다시 말씀해주세요.", lang=language)
            tts.save("speech.mp3")
            os.system("mpg321 speech.mp3")
            sleep(2)
            os.remove("speech.mp3")
            return False
        tts = gTTS(text=text, lang=language)
        tts.save("speech.mp3")
        os.system("mpg321 speech.mp3")
        sleep(2)
        os.remove("speech.mp3")
        return True
    except Exception as e:
        print(f"에러가 발생했습니다: {str(e)}")
        tts = gTTS(text="다시 말씀해주세요.", lang=language)
        tts.save("speech.mp3")
        os.system("mpg321 speech.mp3")
        sleep(2)
        os.remove("speech.mp3")
        return False

def save_and_convert_audio():
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
                response_text = process_text_response(result_text)
                text_to_speech(response_text)
            else:
                print("텍스트 변환에 실패했습니다.")
    finally:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
        if os.path.exists(converted_audio_file):
            os.remove(converted_audio_file)
        print("* 임시 녹음 파일들이 삭제되었습니다.")

def button1_pressed():
    """음성인식 버튼이 눌렸을 때의 동작"""
    global recording, audio_thread
    led1.on()
    print("LED1 ON")
    print("녹음을 시작합니다...")
    recording = True
    audio_thread = threading.Thread(target=record_audio_thread)
    audio_thread.start()

def button1_released():
    """음성인식 버튼에서 손을 뗐을 때의 동작"""
    global recording, audio_thread, p
    led1.off()
    print("LED1 OFF")
    print("녹음을 종료합니다...")
    recording = False
    if audio_thread:
        audio_thread.join()
    save_and_convert_audio()

def button2_pressed():
    """번역용 버튼이 눌렸을 때의 동작"""
    global recording, audio_thread
    led2.on()
    print("LED2 ON")
    print("번역을 위한 녹음을 시작합니다...")
    recording = True
    audio_thread = threading.Thread(target=record_audio_thread)
    audio_thread.start()

def button2_released():
    """번역용 버튼에서 손을 뗐을 때의 동작"""
    global recording, audio_thread, p
    led2.off()
    print("LED2 OFF")
    print("녹음을 종료합니다...")
    recording = False
    if audio_thread:
        audio_thread.join()
    translate_and_save_audio()

def translate_and_save_audio():
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
                print("\n인식된 한국어:")
                print(result_text)
                # Google Translate API 사용
                translated = translator.translate(result_text, dest='en')
                print("\n영어 번역:")
                print(translated.text)
                # 영어로 음성 출력
                text_to_speech(translated.text, 'en')
    finally:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
        if os.path.exists(converted_audio_file):
            os.remove(converted_audio_file)

def button5_pressed():
    """창문 제어 버튼이 눌렸을 때의 동작"""
    global led3_state
    led3_state = not led3_state
    if led3_state:
        led3.on()
        print("측창 열림")
        text_to_speech("측창이 열립니다.")
    else:
        led3.off()
        print("측창 닫힘")
        text_to_speech("측창이 닫힙니다.")

def button6_pressed():
    """차광막 제어 버튼이 눌렸을 때의 동작"""
    global led4_state
    led4_state = not led4_state
    if led4_state:
        led4.on()
        print("차광막 내려감")
        text_to_speech("차광막 닫힙니다")
    else:
        led4.off()
        print("차광막 올라감")
        text_to_speech("차광막 열립니다")

# 버튼 이벤트 설정
button1.when_pressed = button1_pressed
button1.when_released = button1_released
button2.when_pressed = button2_pressed
button2.when_released = button2_released
button5.when_pressed = button5_pressed
button6.when_pressed = button6_pressed

try:
    print("프로그램이 시작되었습니다.")
    print("버튼1: 음성인식 (누르고 있는 동안 녹음)")
    print("버튼2: 번역 (한국어->영어)")
    print("버튼5: 측창 제어 (토글)")
    print("버튼6: 차광막 제어 (토글)")
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
    buzzer.stop()
    buzzer.close()
    button1.close()
    led1.close()
    button2.close()
    led2.close()
    button3.close()
    button5.close()
    led3.close()
    button6.close()
    led4.close()