import tkinter as tk

# 온도(섭씨 => 화씨)
def c2f(temp_c):
    return temp_c * 9 / 5 + 32

# 길이 (인치 => 센티미터)
def in_to_cm(inch):
    return inch * 2.54

# 열 에너지 (칼로리 => 줄)
def heat_J(cal):
    return cal * 4.1868

def convert_temp(entry_temp, text_result_temp):
    temp_c_str = entry_temp.get()
    if temp_c_str.replace('.', '', 1).isdigit() and temp_c_str.count('.') <= 1:
        temp_c = float(temp_c_str)
        temp_f = c2f(temp_c)
        text_result_temp.config(text=f"{temp_c:.2f}℃ => {temp_f:.2f}℉")
    else:
        text_result_temp.config(text="유효한 섭씨 온도를 입력하세요.")

def convert_length(entry_inch, text_result_inch):
    inch_str = entry_inch.get()
    if inch_str.isdigit():
        inch = int(inch_str)
        cm = in_to_cm(inch)
        text_result_inch.config(text=f"{inch} inch는 {cm:.2f} cm 입니다.")
    else:
        text_result_inch.config(text="유효한 인치 값을 입력하세요.")

def convert_heat(entry_cal, text_result_heat):
    cal_str = entry_cal.get()
    if cal_str.isdigit():
        cal = int(cal_str)
        joules = heat_J(cal)
        text_result_heat.config(text=f"물 {cal} g을 1℃ 올리는데 필요한 열 에너지는 {joules:.4f} J입니다.")
    else:
        text_result_heat.config(text="유효한 물의 양을 입력하세요.")

def reset(entry, text_result):
    entry.delete(0, tk.END)  # 입력 초기화
    text_result.config(text="")  # 결과 라벨 초기화

def main():
    window = tk.Tk()  # 화면 만들기
    window.title("단위 변환기")  # 화면 이름
    window.geometry("400x600")  # 화면 크기

    # 섭씨 온도 입력
    text_temp = tk.Label(window, text="섭씨온도를 입력하세요.(정수~소수 2자리)")
    text_temp.pack(pady=5)
    entry_temp = tk.Entry(window)
    entry_temp.pack()
    text_result_temp = tk.Label(window, text="")
    text_result_temp.pack(pady=5)
    button_check_temp = tk.Button(window, text="확인", command=lambda: convert_temp(entry_temp, text_result_temp))
    button_check_temp.pack(pady=5)
    button_reset_temp = tk.Button(window, text="초기화", command=lambda: reset(entry_temp, text_result_temp))
    button_reset_temp.pack(pady=5)

    # 인치 입력
    text_inch = tk.Label(window, text="inch를 입력하세요. (정수)")
    text_inch.pack(pady=5)
    entry_inch = tk.Entry(window)
    entry_inch.pack()
    text_result_inch = tk.Label(window, text="")
    text_result_inch.pack(pady=5)
    button_check_inch = tk.Button(window, text="확인", command=lambda: convert_length(entry_inch, text_result_inch))
    button_check_inch.pack(pady=5)
    button_reset_inch = tk.Button(window, text="초기화", command=lambda: reset(entry_inch, text_result_inch))
    button_reset_inch.pack(pady=5)

    # 열 에너지 입력
    text_cal = tk.Label(window, text="물 몇 g? (정수)")
    text_cal.pack(pady=5)
    entry_cal = tk.Entry(window)
    entry_cal.pack()
    text_result_heat = tk.Label(window, text="")
    text_result_heat.pack(pady=5)
    button_check_cal = tk.Button(window, text="확인", command=lambda: convert_heat(entry_cal, text_result_heat))
    button_check_cal.pack(pady=5)
    button_reset_cal = tk.Button(window, text="초기화", command=lambda: reset(entry_cal, text_result_heat))
    button_reset_cal.pack(pady=5)

    window.mainloop()  # 창 실행

if __name__ == '__main__':
    main()
