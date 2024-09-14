import tkinter as tk

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def click(entry, text_result):
    n = int(entry.get())
    result = factorial(n)
    text_result.config(text=f"{n}! = {result}", fg="lightgreen")

def main():
    window = tk.Tk()
    window.title("팩토리얼 계산기")
    window.geometry("400x250")
    window.config(bg="#1e1e1e")

    title_label = tk.Label(window, text="숫자를 입력하세요", font=("Arial", 18), bg="#1e1e1e", fg="#ffffff")
    title_label.pack(pady=20)

    entry = tk.Entry(window, font=("Arial", 14), width=15, bg="#2e2e2e", fg="#ffffff", insertbackground="white")
    entry.pack(pady=10)

    button = tk.Button(window, text="확인", command=lambda: click(entry, text_result), bg="#ff6347", fg="white", font=("Arial", 14))
    button.pack(pady=10)

    text_result = tk.Label(window, text="", font=("Arial", 14), bg="#1e1e1e", fg="lightgreen")
    text_result.pack(pady=20)

    window.mainloop()

if __name__ == '__main__':
    main()
