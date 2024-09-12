import tkinter as tk

def holzzack(n):
    return n % 2 == 0

def click(entry,text2):    #매개변수 entry,text2
    n = int(entry.get())    #entry(글자입력칸)에 입력한 값 받아오기
    if holzzack(n):
        text2.config(text=f"{n}은 짝수 입니다.", fg="red")    #config는 위젯 속성을 변경해줌
    else:
        text2.config(text=f"{n}은 홀수 입니다.", fg="blue")

def main():
    window = tk.Tk()    #화면 만들기
    window.title("홀짝")    #화면 이름
    window.geometry("400x200")    #화면 크기

    #위젯: Label, Button, Entry(글자입력칸)
    #위치 설정: pack은 쌓는 방식, grid는 행과 열로 배치하는 방식
    text1 = tk.Label(window, text="숫자를 입력하세요", font=("Arial", 16, "bold"))    #라벨 생성
    text1.pack(pady=10)    #라벨을 윈도우에 배치 / pady는 세로 여백 (가로여백은 padx)

    entry = tk.Entry(window, width=30)    #글자입력칸 생성
    # entry = tk.Text(window, height=2, width=40)    #Entry는 세로길이 조절 x, Text 사용하면 세로길이 조절 가능.
    entry.pack()    #entry를 윈도우에 배치

    # text2 = tk.Label(window, text="")    #순서대로 출력: text2를 먼저 쓰면 결과값이 확인 버튼 위에 나옴.
    # text2.pack()

    button = tk.Button(window, text="확인", command=lambda:click(entry,text2), bg="#800020", fg="white", font=("Arial", 14, "bold"))
                                          #command 버튼을 눌렀을 때 실행될 함수    #lambda를 통해 click함수 호출 & entry,text2인자를 받음.
    button.pack(pady=10)

    text2 = tk.Label(window, text="", font=("Arial", 14, "bold"))
    text2.pack(pady=10)

    window.mainloop()    #창 실행

if __name__ == '__main__':
    main()
