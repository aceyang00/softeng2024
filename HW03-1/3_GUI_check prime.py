import tkinter as tk

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def click(entry, text_result):
    n = int(entry.get())
    if is_prime(n):
        text_result.config(text=f"{n}은(는) 소수입니다.", fg="green")
    else:
        text_result.config(text=f"{n}은(는) 소수가 아닙니다.", fg="red")

def main():
    window = tk.Tk()
    window.title("소수 판별기")
    window.geometry("400x250")
    window.config(bg="#f4f4f4")

    title_label = tk.Label(window, text="숫자를 입력하세요", font=("Arial", 18), bg="#f4f4f4", fg="#333333")
    title_label.pack(pady=20)

    entry = tk.Entry(window, font=("Arial", 14), width=15)
    entry.pack(pady=10)

    button = tk.Button(window, text="확인", command=lambda: click(entry, text_result), bg="#008CBA", fg="white", font=("Arial", 14))
    button.pack(pady=10)

    text_result = tk.Label(window, text="", font=("Arial", 14), bg="#f4f4f4")
    text_result.pack(pady=20)

    window.mainloop()

if __name__ == '__main__':
    main()
