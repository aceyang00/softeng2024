import tkinter as tk

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num):    #1과 자기 자신은 범위에서 제외
        if num % i == 0:
            return False
    return True

def click(entry,text2):
    n = int(entry.get())
    return text2.config(text=f"1부터 {n}중에 소수는 {[i for i in range(2,n+1) if is_prime(i)]} 입니다.")

def main():
    window = tk.Tk()
    window.title("소수 구하기")
    window.geometry("400x250")
    window.resizable(True, False)    # False: 창 크기 고정/ True: 창 크기 변경 가능
    window.config(bg="black")

    text1 = tk.Label(window, text="숫자를 입력하세요", bg="black", fg="gold", font=("Arial", 14, "bold"))
    text1.pack(pady=10)

    entry = tk.Entry(window, width=35)
    entry.pack(pady=10)

    button = tk.Button(window, text="확인", command=lambda:click(entry,text2), bg="#800020", fg="white", font=("Arial", 14, "bold"))
    button.pack(pady=10)

    text2 = tk.Label(window, text="", bg="black", fg="gold", font=("Arial", 14, "bold"))
    text2.pack(pady=10)

    window.mainloop()

if __name__ == '__main__':
    main()
