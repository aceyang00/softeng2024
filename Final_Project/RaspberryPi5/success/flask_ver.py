from flask import Flask, jsonify, render_template
from threading import Thread
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt
from collections import deque
import os
from gpiozero import OutputDevice, InputDevice
import time

class DHT11:
    MAX_DELAY_COUNT = 100
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
                if delay_count > self.MAX_DELAY_COUNT:
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

# Flask 애플리케이션 생성
app = Flask(__name__)
# DHT11 데이터 저장을 위한 변수 설정
sensor_data = {
    "temperature": deque(maxlen=100),
    "humidity": deque(maxlen=100),
    "timestamps": deque(maxlen=100)}
# 센서 데이터 수집 스레드
class SensorThread(Thread):
    def __init__(self, dht11_sensor):
        super().__init__()
        self.dht11_sensor = dht11_sensor
        self.running = True
    def run(self):
        while self.running:
            humidity, temperature = self.dht11_sensor.read_data()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sensor_data["temperature"].append(temperature)
            sensor_data["humidity"].append(humidity)
            sensor_data["timestamps"].append(timestamp)
            sleep(2)
    def stop(self):
        self.running = False
# DHT11 객체 생성
dht11 = DHT11(18)
# 센서 스레드 시작
sensor_thread = SensorThread(dht11)
sensor_thread.start()

@app.route("/api/data", methods=["GET"])
def api_data():
    """센서 데이터를 JSON 형태로 반환."""
    return jsonify({
        "temperature": list(sensor_data["temperature"]),
        "humidity": list(sensor_data["humidity"]),
        "timestamps": list(sensor_data["timestamps"])})
@app.route("/data", methods=["GET"])
def data_page():
    """웹 페이지에서 그래프를 확인할 수 있도록 HTML 제공."""
    plt.figure(figsize=(10, 5))     # 그래프 생성
    # 온도 그래프
    plt.subplot(2, 1, 1)
    plt.plot(sensor_data["timestamps"], sensor_data["temperature"], label="Temperature (°C)")
    plt.title("Temperature Over Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45, fontsize=8)
    plt.legend()
    # 습도 그래프
    plt.subplot(2, 1, 2)
    plt.plot(sensor_data["timestamps"], sensor_data["humidity"], label="Humidity (%)", color="orange")
    plt.title("Humidity Over Time")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45, fontsize=8)
    plt.legend()
    # 그래프 저장
    if not os.path.exists("static"):
        os.mkdir("static")
    graph_path = "static/graph.png"
    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()
    return render_template("graph.html", graph_path=graph_path)
# HTML 템플릿 생성
graph_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sensor Data Graph</title>
</head>
<body>
    <h1>Sensor Data Graph</h1>
    <img src="/{{ graph_path }}" alt="Sensor Data Graph">
</body>
</html>
'''
# HTML 파일 저장
if not os.path.exists("templates"):
    os.mkdir("templates")
with open("templates/graph.html", "w") as f:
    f.write(graph_html)

if __name__ == "__main__":
    try:
        print("Flask 서버가 실행 중입니다. http://<Your-IP>:5000/data 에 접속하세요.")
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print("\n서버를 종료합니다...")
    finally:
        sensor_thread.stop()
        sensor_thread.join()