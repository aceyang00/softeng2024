import tkinter as tk

def holzzack(n):
    return n % 2 == 0

def click(entry,text2):
    n = int(entry.get())
    return text2.config(text=f"1부터 {n}까지 짝수의 합은 {sum([i for i in range(1,n+1) if holzzack(i)])} 입니다.")

def main():
    window = tk.Tk()
    window.title("짝수합 구하기")
    window.geometry("400x250")
    window.config(bg="white")

    text1 = tk.Label(window, text="숫자를 입력하세요", bg="white", fg="gold", font=("Arial", 14, "bold"))
    text1.pack(pady=10)

    entry = tk.Entry(window, width=35)
    entry.pack(pady=10)

    button = tk.Button(window, text="확인", command=lambda: click(entry, text2), bg="#800020", fg="white", font=("Arial", 14, "bold"))
    button.pack(pady=10)

    text2 = tk.Label(window, text="", bg="white", fg="gold", font=("Arial", 14, "bold"))
    text2.pack(pady=10)

    window.mainloop()

if __name__ == '__main__':
    main()
