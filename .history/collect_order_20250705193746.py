import sys

# 중요 조건: 웹사이트를 실시간으로 가져오지 않고, 메뉴를 코드에 미리 넣어줍니다.
# 제공된 HTML 구조를 분석하여 메뉴 데이터를 딕셔너리 형태로 정리했습니다.
MENU = {
    "커피": [
        "아메리카노", "꿀 커피", "카페 라떼", "카푸치노", "바닐라 라떼",
        "카라멜 마키아토", "카페 모카", "돌체 라떼", "아샷추 아이스티"
    ],
    "콜드브루": [
        "콜드브루", "콜드브루 라떼", "돌체 콜드브루 라떼", "아몬드 크림 콜드브루"
    ],
    "논커피": [
        "초코 라떼", "그린티 라떼", "딸기 크림 라떼", "고구마 라떼", "옥수수 라떼"
    ],
    "티·에이드": [
        "복숭아 아이스티", "리얼 레몬티", "자몽 티 / 에이드", "블루레몬 티 / 에이드",
        "청포도 에이드", "수박 주스"
    ],
    "프라페·블렌디드": [
        "코코넛 커피 스무디", "딸기 스무디", "플레인 요거트 스무디",
        "쿠앤크 프라페", "자바칩 프라페", "피스타치오 프라페"
    ]
}

def display_menu():
    """
    터미널에 보기 좋게 메뉴판을 출력하고, 선택 가능한 전체 음료 리스트를 반환합니다.
    """
    print("\n" + "=" * 40)
    print("      ☕ 매머드커피 음료 메뉴판 ☕")
    print("=" * 40)
    
    all_drinks = []
    item_number = 1
    
    for category, items in MENU.items():
        print(f"\n----- [ {category} ] -----")
        for item in items:
            # 메뉴명과 번호를 함께 출력
            print(f"  {item_number:2d}. {item}")
            all_drinks.append(item)
            item_number += 1
            
    print("\n" + "=" * 40)
    return all_drinks

def get_josa(word):
    """
    단어의 마지막 글자에 받침이 있는지 여부에 따라 '을' 또는 '를'을 반환합니다.
    """
    last_char = word[-1]
    # 한글 유니코드 범위 (가 ~ 힣)
    if '가' <= last_char <= '힣':
        # 받침 유무 확인: (ord(글자) - 44032) % 28
        has_jongseong = (ord(last_char) - 44032) % 28 != 0
        return '을' if has_jongseong else '를'
    # 한글이 아닐 경우 기본값 반환
    return '을(를)'

def main():
    """
    프로그램의 메인 로직을 실행합니다.
    """
    # {이름: 선택한 메뉴} 형식으로 주문을 저장할 딕셔너리
    orders = {}
    
    # 메뉴판을 한 번 출력하고, 선택 가능한 음료 목록을 생성
    all_drinks = display_menu()
    
    print("\n안녕하세요! 음료 주문 취합을 시작합니다.")

    while True:
        # 핵심 기능: 사용자의 이름을 입력받습니다.
        name = input(">> 주문하실 분의 이름을 입력하세요 (완료하려면 '완료' 또는 '종료' 입력): ")

        # 중요 조건: 입력 종료 조건 확인
        if name == '완료' or name == '종료':
            print("\n주문 입력을 마감합니다.")
            break
        
        if not name.strip(): # 공백만 입력한 경우
            print("이름을 정확히 입력해주세요.")
            continue

        # 핵심 기능: 사용자가 음료 메뉴를 선택하도록 안내합니다.
        while True:
            try:
                choice_str = input(f">> {name}님, 원하시는 음료의 번호를 선택하세요: ")
                choice_num = int(choice_str)

                if 1 <= choice_num <= len(all_drinks):
                    chosen_drink = all_drinks[choice_num - 1]
                    
                    # 핵심 기능: 결과 저장
                    orders[name] = chosen_drink
                    
                    print(f"✅ {name}님, '{chosen_drink}' 선택 완료!\n")
                    break
                else:
                    print(f"❌ 잘못된 번호입니다. 1번부터 {len(all_drinks)}번 사이의 번호를 입력해주세요.")
            
            except ValueError:
                print("❌ 숫자로만 입력해주세요.")
            except Exception as e:
                print(f"오류가 발생했습니다: {e}")

    # 핵심 기능: 최종 결과 출력
    print("\n" + "*" * 40)
    print("           📋 최종 주문 내역 📋")
    print("*" * 40)

    if not orders:
        print("\n주문 내역이 없습니다.")
    else:
        for name, drink in orders.items():
            josa = get_josa(drink)
            print(f"✔️ {name}님은 {drink}{josa} 선택했습니다.")
            
    print("\n" + "*" * 40)
    print("프로그램을 종료합니다. 이용해주셔서 감사합니다.")


if __name__ == "__main__":
    main()