from flask import Flask, render_template
#import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/edu')
def edu():
    return render_template('edu.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/blog')
def blog():
    posts = [
        {'title': '첫 번째 글', 'content': '이것은 첫 번째 블로그 글입니다.'},
        {'title': '두 번째 글', 'content': '이것은 두 번째 블로그 글입니다.'},
        {'title': '세 번째 글', 'content': '이것은 세 번째 블로그 글입니다.'},
        {'title': '네 번째 글', 'content': '이것은 네 번째 블로그 글입니다.'},
        {'title': '다섯 번째 글', 'content': '이것은 다섯 번째 블로그 글입니다.'},
        {'title': '여섯 번째 글', 'content': '이것은 여섯 번째 블로그 글입니다.'},
        {'title': '일곱 번째 글', 'content': '이것은 일곱 번째 블로그 글입니다.'},
    ]
    return render_template('blog.html', posts=posts)
    #return render_template('blog.html', title="blog post", posts=posts)  #페이지마다 제목 변경하려면 title이라는 변수 사용

# <csv파일에 13개의 데이터를 작성해둠. 불러오려 했는데 실패. ParserError뜨면서 blog.html 화면 안열림.>
"""@app.route('/blog')
def blog():
    df = pd.read_csv('blog_content.csv', encoding='utf-8')  
    posts = []
    for i, row in df.iterrows():
        posts.append({'title': row['title'], 'content': row['content']})
    return render_template('blog.html', posts=posts)"""

if __name__ == '__main__':
    app.run(debug=True)
