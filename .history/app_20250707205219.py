from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from collections import defaultdict
import os
from datetime import datetime
import threading

app = Flask(__name__)
app.secret_key = 'mammoth_coffee_secret_key_2024'

# 전역 주문 저장소 (다중 사용자 지원)
global_orders = {}
global_drink_counts = defaultdict(int)
orders_lock = threading.Lock()  # 스레드 안전성을 위한 락

# 메뉴 데이터
MENU = {
    "커피": [
        "아메리카노", "꿀 커피", "아몬드 아메리카노", "아샷추 아이스티", "카페 라떼", 
        "카푸치노", "꿀 라떼", "아몬드 라떼", "바닐라 라떼", "꿀바나 라떼", 
        "카라멜 마키아토", "카페 모카", "티라미수 라떼", "헤이즐넛 커피", 
        "코코넛 사이공 라떼", "헤이즐넛 모카", "돌체 라떼", "달고나 카페라떼", 
        "믹스 커피", "디카페인 아메리카노", "디카페인 꿀 커피", "디카페인 아몬드 아메리카노", 
        "디카페인 꿀 라떼", "디카페인 카푸치노", "디카페인 카페 라떼", 
        "디카페인 아몬드 라떼", "디카페인 바닐라 라떼", "디카페인 카라멜 마키아토", 
        "디카페인 카페 모카", "디카페인 티라미수 라떼", "디카페인 꿀바나 라떼", 
        "디카페인 헤이즐넛 커피", "디카페인 코코넛 사이공 라떼", "디카페인 헤이즐넛 모카", 
        "디카페인 돌체 라떼", "디카페인 달고나 카페라떼", "디카페인 아샷추 아이스티"
    ],
    "콜드브루": [
        "콜드브루", "콜드브루 라떼", "돌체 콜드브루 라떼", "아몬드 크림 콜드브루", 
        "레몬토닉 콜드브루", "코코넛 크림 콜드브루 라떼", "디카페인 콜드브루", 
        "디카페인 콜드브루 라떼", "디카페인 돌체 콜드브루 라떼", 
        "디카페인 아몬드 크림 콜드브루", "디카페인 레몬토닉 콜드브루", 
        "디카페인 코코넛 크림 콜드브루 라떼"
    ],
    "논커피": [
        "그린티 라떼", "초코 라떼", "딸기 크림 라떼", "차이티 라떼", 
        "콩가루 라떼", "옥수수 라떼", "고구마 라떼", "메론바나 라떼"
    ],
    "티": [
        "리얼 레몬티", "페퍼민트티", "캐모마일티", "레몬&오렌지티", "얼그레이티", 
        "페퍼민트 라임티", "오렌지 아일랜드티", "우롱 밀크티", "복숭아 아이스티", 
        "라임레몬 깔라만시티", "라임티", "유자티", "자몽티", "제주 한라봉티", "제주청귤티"
    ],
    "에이드": [
        "매머드 파워드링크", "제로 체리콕 에이드", "제로 복숭아 아이스티", 
        "블루레몬 에이드", "청포도 에이드", "수박 주스", "자몽 에이드", 
        "라임레몬 깔라만시 에이드", "라임 에이드", "유자 에이드", "자몽 에이드", 
        "제주 한라봉 에이드", "제주청귤 에이드"
    ],
    "프라페·블렌디드": [
        "코코넛 커피 스무디", "딸기 스무디", "플레인 요거트 스무디", 
        "쿠앤크 프라페", "자바칩 프라페", "피스타치오 프라페"
    ]
}

@app.route('/')
def index():
    return render_template('index.html', menu=MENU)

@app.route('/add_order', methods=['POST'])
def add_order():
    name = request.form.get('name', '').strip()
    drink = request.form.get('drink', '').strip()
    temperature = request.form.get('temperature', 'ICE')
    request_note = request.form.get('request_note', '').strip()
    
    if not name or not drink:
        return jsonify({'success': False, 'message': '이름과 음료를 모두 입력해주세요.'})
    
    with orders_lock:
        # 기존 주문이 있으면 카운트 감소
        if name in global_orders:
            old_drink, old_temp, _ = global_orders[name]
            old_key = f"{old_drink}|{old_temp}"
            global_drink_counts[old_key] -= 1
            if global_drink_counts[old_key] == 0:
                del global_drink_counts[old_key]
        
        # 새 주문 추가
        global_orders[name] = (drink, temperature, request_note)
        new_key = f"{drink}|{temperature}"
        global_drink_counts[new_key] += 1
    
    return jsonify({
        'success': True, 
        'message': f'{name}님의 주문이 추가되었습니다! ({drink} {temperature})',
        'orders': dict(global_orders),
        'drink_counts': dict(global_drink_counts)
    })

@app.route('/delete_order/<name>')
def delete_order(name):
    with orders_lock:
        if name in global_orders:
            drink, temp, _ = global_orders[name]
            key = f"{drink}|{temp}"
            
            global_drink_counts[key] -= 1
            if global_drink_counts[key] == 0:
                del global_drink_counts[key]
            
            del global_orders[name]
            flash(f'{name}님의 주문이 삭제되었습니다.', 'success')
    return redirect(url_for('index'))

@app.route('/reset_orders')
def reset_orders():
    with orders_lock:
        global_orders.clear()
        global_drink_counts.clear()
    flash('모든 주문이 초기화되었습니다.', 'success')
    return redirect(url_for('index'))

@app.route('/get_orders')
def get_orders():
    """실시간 주문 현황을 JSON으로 반환"""
    with orders_lock:
        return jsonify({
            'orders': dict(global_orders),
            'drink_counts': dict(global_drink_counts),
            'total_people': len(global_orders),
            'total_drinks': sum(global_drink_counts.values())
        })

@app.route('/final_order')
def final_order():
    with orders_lock:
        if not global_orders:
            flash('주문 내역이 없습니다.', 'error')
            return redirect(url_for('index'))
        
        # 주문 요약 생성
        hot_orders = {}
        ice_orders = {}
        
        for key, count in global_drink_counts.items():
            if '|' in key:
                drink, temp = key.split('|', 1)
                if temp == "HOT":
                    hot_orders[drink] = count
                elif temp == "ICE":
                    ice_orders[drink] = count
        
        total_drinks = sum(global_drink_counts.values())
        total_people = len(global_orders)
        
        # 현재 시간 추가
        current_time = datetime.now()
        
        return render_template('final_order.html', 
                             orders=global_orders,
                             hot_orders=hot_orders,
                             ice_orders=ice_orders,
                             total_drinks=total_drinks,
                             total_people=total_people,
                             current_time=current_time)

@app.route('/images/<filename>')
def serve_image(filename):
    """이미지 파일을 제공하는 라우트"""
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 