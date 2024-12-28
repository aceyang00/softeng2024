from gtts import gTTS
import os
from time import sleep

def text_to_speech(text, language='ko'):
    try:
        tts = gTTS(text=text, lang=language)    # 텍스트를 음성으로 변환
        tts.save("speech.mp3")    # 임시 파일로 저장
        os.system("mpg321 speech.mp3")    # mp3 파일 재생
        # 재생 완료 후 임시 파일 삭제
        sleep(2)  # 재생이 완료될 때까지 잠시 대기
        os.system("rm speech.mp3")
        return True
    except Exception as e:
        print(f"에러가 발생했습니다: {str(e)}")
        return False
# 테스트용 메시지
# text_to_speech("안녕하세요 반갑습니다")
text_to_speech("Hello, how are you?", 'en')