# 과제 #07 템플릿이용

#### 1.

![화면 캡처 2024-10-05 142353](https://github.com/user-attachments/assets/07d4f770-506f-46ec-84c1-dd6ac9ad9151) 

-html 파일은 templates 폴더에, css와 images는 static 폴더로 옮김.
 
#### 2.
![화면 캡처 2024-10-05 142433](https://github.com/user-attachments/assets/2daa00d6-127e-48b5-85c8-e2d0f46197c2)

-layout.html에 공통으로 사용하는 코드를 모아둠. ex) h1 폰트, 배경, 경로지정

#### 3.
![화면 캡처 2024-10-05 142414](https://github.com/user-attachments/assets/c2d3c164-d055-4a59-b9a7-9bee0e253bea)

- {% extends 'layout.html' %} : layout 템플릿을 불러와서 각 페이지별로 필요한 것만 사용.
-  {{ url_for('static', filename='images/smart_farm.jpg') }} : 이미지 경로
-  {{ url_for('index') }} : 주소 경로

*hw06을 진행할 때 페이지마다 따로 디자인을 해서 공통부분을 활용하기 어려웠음.
-> 처음부터 템플릿을 이용한다면 더 쉽게 홈페이지를 만들 수 있다.
