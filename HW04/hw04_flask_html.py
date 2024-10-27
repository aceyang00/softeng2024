from flask import Flask, request
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html lang="kr">
<head>
    <meta charset="UTF-8">
    <title>사귄 날짜 계산기</title>
    <style>
        h2 {color: #FF69B4}
        button:hover {background-color: #FF1493}
    </style>
</head>
<body>
    <form method="GET" action="/calculate">
        <h2>사귄 날짜 계산기</h2>
        <label>사귀기로 한 날짜 (YYYY-MM-DD):
           <input type="text" name="start_date">
        </label><br>       
        <label>확인할 날짜 (YYYY-MM-DD):
            <input type="text" name="target_date">
        </label><br>             
        <button type="submit">계산하기</button>      
    </form>

    <form method="GET" action="/D-day">
        <h2>100일이 되기 위해 사귀어야 하는 날짜 계산기</h2>
        <label>100일째가 되는 날짜 (YYYY-MM-DD):
            <input type="text" name="check_date">
        </label><br>
        <button type="submit">계산하기</button>
    </form>    
</body>
</html>"""

@app.route('/calculate/')
def cal():
    start_date = request.args.get('start_date')
    target_date = request.args.get('target_date')

    if start_date and target_date:
        try:
            start_d = datetime.strptime(start_date, '%Y-%m-%d')
            target_d = datetime.strptime(target_date, '%Y-%m-%d')
            day_diff = (target_d - start_d).days + 1  # 당일부터 1일이기 때문
            return f"사귄지 {day_diff}일째 되는 날입니다."
        except ValueError:
            return "'YYYY-MM-DD' 형식으로 입력해주세요."
    else:
        return "날짜를 입력해주세요."


@app.route('/D-day/')
def goback():
    check_date = request.args.get('check_date')

    if check_date:
        try:
            check_d = datetime.strptime(check_date, '%Y-%m-%d')
            goback_date = check_d - timedelta(days=99)  # 100일 맞추려면 99일전에 사귀어야함.
            return f"{check_date}에 100일이 되려면 {goback_date.strftime('%Y-%m-%d')}에 사귀어야 합니다."
        except ValueError:
            return "'YYYY-MM-DD' 형식으로 입력해주세요."
    else:
        return "날짜를 입력해주세요."

app.run(debug=True)  # 소스코드를 새로저장할때마다 자동으로 새로 띄워줌 = 새로고침만 하면됨.
