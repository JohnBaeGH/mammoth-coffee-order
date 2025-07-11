# ☕ 매머드커피 주문 시스템

매머드커피의 음료 주문을 취합하고 관리하는 GUI 기반 주문 시스템입니다. [매머드커피 공식 웹사이트](https://mmthcoffee.com/sub/menu/list_coffee.php)의 모든 메뉴를 포함하고 있습니다.

## 🚀 주요 기능

1. **이미지 기반 메뉴 선택**: 직관적인 이미지 인터페이스로 음료 선택
2. **완전한 메뉴 구성**: 매머드커피 공식 웹사이트의 모든 메뉴 포함
3. **온도 선택**: ICE/HOT 음료 온도 선택 가능
4. **실시간 주문 현황**: 누적 주문 현황을 실시간으로 확인
5. **매장 주문용 정리**: 최종 주문을 매장에서 주문하기 쉽게 정리

## 📋 메뉴 구성

### 🥤 32oz
- 매머드 커피, 아이스티, 아샷추 아이스티, 스노우 매머드 커피, 허니베리 홍초 에이드, 패션 오렌지 아이스티, 디카페인 매머드 커피, 디카페인 아샷추 아이스티, 디카페인 스노우 매머드 커피

### ☕ 커피
- 아메리카노, 꿀 커피, 아몬드 아메리카노, 아샷추 아이스티, 카페 라떼, 카푸치노, 꿀 라떼, 아몬드 라떼, 바닐라 라떼, 꿀바나 라떼, 카라멜 마키아토, 카페 모카, 티라미수 라떼, 헤이즐넛 커피, 코코넛 사이공 라떼, 헤이즐넛 모카, 돌체 라떼, 달고나 카페라떼, 믹스 커피
- **디카페인**: 아메리카노, 꿀 커피, 아몬드 아메리카노, 꿀 라떼, 카푸치노, 카페 라떼, 아몬드 라떼, 바닐라 라떼, 카라멜 마키아토, 카페 모카, 티라미수 라떼, 꿀바나 라떼, 헤이즐넛 커피, 코코넛 사이공 라떼, 헤이즐넛 모카, 돌체 라떼, 달고나 카페라떼, 아샷추 아이스티

### 🧊 콜드브루
- 콜드브루, 콜드브루 라떼, 돌체 콜드브루 라떼, 아몬드 크림 콜드브루, 레몬토닉 콜드브루, 코코넛 크림 콜드브루 라떼
- **디카페인**: 콜드브루, 콜드브루 라떼, 돌체 콜드브루 라떼, 아몬드 크림 콜드브루, 레몬토닉 콜드브루, 코코넛 크림 콜드브루 라떼
- **원액**: 매머드 콜드브루 원액, 매머드 콜드브루 디카페인 원액

### 🥛 논커피
- 그린티 라떼, 초코 라떼, 딸기 크림 라떼, 차이티 라떼, 콩가루 라떼, 옥수수 라떼, 고구마 라떼, 메론바나 라떼

### 🍵 티·에이드
- 매머드 파워드링크, 제로 체리콕 에이드, 제로 복숭아 아이스티, 리얼 레몬티, 페퍼민트티, 캐모마일티, 레몬&오렌지티, 얼그레이티, 페퍼민트 라임티, 오렌지 아일랜드티, 우롱 밀크티, 복숭아 아이스티, 자몽 티/에이드, 블루레몬 티/에이드, 청포도 에이드, 수박 주스

### 🥤 프라페·블렌디드
- 코코넛 커피 스무디, 딸기 스무디, 플레인 요거트 스무디, 쿠앤크 프라페, 자바칩 프라페, 피스타치오 프라페

### 🍰 푸드
- **쿠키/베이커리**: 매머드 초콜릿 칩 쿠키, 우유 크림 크로슈, 초코 덮인 크로슈, 바삭 한입 페스츄리 약과, 쫀득 한입 고구마말랭이, 근대골목 생크림 단팥빵, 근대골목 단팥빵, 꿀 우유 크림 도넛, 미니 매머드 빵, 바나나 쿠키, 브라우니 쿠키, 매머드 크룽지, 매머드 고메버터 플레인 스콘, 매머드 고메버터 초코 스콘, 바닐라 비스킷 슈, 허니브레드, 플레인 베이글, 블루베리 베이글
- **케이크**: 끼리 플레인 치즈 스틱 케이크, 끼리 쿠키앤 크림 치즈 스틱 케이크, 매머드 초코 파운드 케이크, 바스크 치즈 케이크, 매머드 레몬 파운드 케이크, 매머드 마카다미아 쿠키, 마스카포네 티라미수, 폭탄 카스테라, 밀크 크레이프, 클래식 치즈 케이크, 제리의 치즈 케이크, 쇼콜라 아메르 케이크, 당근 케이크
- **마카롱**: 미니 쁘띠 마카롱, 바닐라 마카롱, 초콜릿 마카롱, 망고 마카롱, 민트초코 마카롱, 라즈베리 마카롱, 블루베리 마카롱
- **샌드위치**: 햄&치즈 대만식 샌드위치, 카야 대만식 샌드위치, 잉글리쉬 머핀 샌드위치, 멜팅 치즈 샌드위치, 베이컨 치즈 샌드위치, 에그 샐러드 샌드위치, 튜나 샌드위치, 클럽 샌드위치
- **세트 메뉴**: 베이컨 치즈 샌드위치 세트, 에그 샐러드 샌드위치 세트, 튜나 샌드위치 세트, 클럽 샌드위치 세트
- **기타**: 매머드 렐리시 핫도그, 매머드 미트 칠리 핫도그, 매머드 렐리시 핫도그 세트, 매머드 미트 칠리 핫도그 세트, 크로플, 치즈 크로플, 에그 타르트

### 🥤 RTD (Ready To Drink)
- 뽀로로(보리차), 뽀로로(밀크), 뽀로로(딸기), 뽀로로(사과), 아쿠아파나(병), 골드메달 애플주스(병), 로리나(핑크레몬), 창소다워터, 분다버그(망고), 분다버그(진저비어), 분다버그(핑크자몽), 매머드 탄산수

### 🛍️ MD (Merchandise)
- 매머드 캡슐 커피, 매머드 캡슐 커피 디카페인, 매머드 캡슐 커피 다크 로스트, 매머드 콜드브루 스틱커피, 매머드 매트블랙 콜드 텀블러, 매머드 리유저블 핫 컵

## 🛠️ 설치 및 실행

### 1. 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 2. 프로그램 실행
```bash
python collect_order.py
```

## 📖 사용법

1. **이름 입력**: 주문자의 이름을 입력합니다.
2. **카테고리 선택**: 원하는 음료 카테고리를 선택합니다.
3. **이미지 기반 메뉴 선택**: 해당 카테고리의 메뉴 이미지들을 확인하고 원하는 메뉴를 클릭하여 선택합니다.
4. **온도 선택**: ICE 또는 HOT을 선택합니다.
5. **주문 추가**: "주문 추가" 버튼을 클릭하여 주문을 등록합니다.
6. **주문 완료**: 모든 주문이 끝나면 "주문 완료" 버튼을 클릭하여 최종 주문 내역을 확인합니다.

## 📊 출력 예시

### 실시간 주문 현황
```
📋 개별 주문 내역:
------------------------------------------------------------
• 김철수: 아메리카노 (ICE)
• 이영희: 카페 라떼 (HOT)
• 박민수: 아메리카노 (ICE)

📊 누적 주문 현황:
------------------------------------------------------------
• 아메리카노 (ICE): 2잔
• 카페 라떼 (HOT): 1잔

총 주문자 수: 3명
```

### 최종 주문 내역 (매장 주문용)
```
☕ 매머드커피 주문 내역 ☕
============================================================

🧊 ICE 음료:
----------------------------------------
• 아메리카노 2잔

🔥 HOT 음료:
----------------------------------------
• 카페 라떼 1잔

📊 총 음료 수: 3잔
👥 총 주문자 수: 3명
```

## 🔧 기능 설명

- **이미지 기반 선택**: 메뉴를 이미지로 표시하여 직관적인 선택 가능
- **완전한 메뉴**: 매머드커피 공식 웹사이트의 모든 메뉴 포함
- **초기화**: 모든 주문을 초기화할 수 있습니다.
- **실시간 업데이트**: 주문이 추가될 때마다 현황이 자동으로 업데이트됩니다.
- **매장 주문용 정리**: 같은 음료를 여러 명이 주문한 경우 개수로 정리하여 매장에서 주문하기 쉽게 표시합니다.
- **스크롤 가능한 메뉴**: 많은 메뉴를 스크롤하여 확인할 수 있습니다.

## 📝 시스템 요구사항

- Python 3.6 이상
- tkinter (대부분의 Python 설치에 포함됨)
- Pillow (이미지 처리용)
- requests (웹 요청용)

## 🎯 개발 목적

이 시스템은 단체 주문이나 회의 주문 시 음료 주문을 체계적으로 관리하고, 매장에서 주문하기 쉽게 정리하는 것을 목적으로 개발되었습니다. 매머드커피의 모든 메뉴를 포함하여 완전한 주문 관리가 가능합니다.

## 📄 참고 자료

- [매머드커피 공식 웹사이트](https://mmthcoffee.com/sub/menu/list_coffee.php) 