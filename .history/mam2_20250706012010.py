import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from collections import defaultdict
import requests
from io import BytesIO
import threading

# 매머드커피 공식 웹사이트 메뉴 데이터 (https://mmthcoffee.com/sub/menu/list_coffee.php)
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

# 메뉴 이미지 자동 매핑 함수 (메뉴명과 파일명이 완전히 일치한다고 가정)
def get_menu_image(menu_name):
    img_path = os.path.join("images", f"{menu_name}.png")
    if os.path.exists(img_path):
        img = Image.open(img_path).resize((100, 100))
        return ImageTk.PhotoImage(img)
    return None

class CoffeeOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("☕ 매머드커피 주문 시스템 ☕")
        self.root.geometry("420x750")  # 모바일 친화적 세로형
        
        # 현대적 컬러 팔레트
        self.colors = {
            'primary': '#FF6B35',      # 매머드커피 시그니처 오렌지
            'primary_hover': '#E55A2B', # 오렌지 호버
            'secondary': '#FFF8F5',    # 따뜻한 화이트
            'accent': '#FFE5D9',       # 연한 오렌지
            'text_primary': '#2D3436',  # 진한 회색
            'text_secondary': '#636E72', # 중간 회색
            'background': '#FFFFFF',    # 순백색
            'card_bg': '#FEFEFE',      # 카드 배경
            'border': '#E8E8E8',       # 연한 테두리
            'success': '#00B894',      # 성공 컬러
            'error': '#E17055'         # 에러 컬러
        }
        
        self.root.configure(bg=self.colors['background'])
        
        # 주문 데이터 저장
        self.orders = {}  # {이름: (음료, 온도, 요청사항)}
        self.drink_counts = defaultdict(int)  # {(음료, 온도): 개수}
        
        # 이미지 캐시
        self.image_cache = {}
        self.photo_cache = {}
        
        # 스타일 설정
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """현대적인 ttk 스타일을 설정합니다."""
        style = ttk.Style()
        
        # 메인 프레임 스타일
        style.configure('Card.TFrame', 
                       background=self.colors['card_bg'],
                       relief='flat',
                       borderwidth=1)
        
        # 라벨 스타일
        style.configure('Title.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['text_primary'],
                       font=('맑은 고딕', 18, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['text_secondary'],
                       font=('맑은 고딕', 11))
        
        style.configure('Label.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_primary'],
                       font=('맑은 고딕', 12))
        
        style.configure('Small.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_secondary'],
                       font=('맑은 고딕', 10))
        
        # 버튼 스타일
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('맑은 고딕', 11, 'bold'),
                       focuscolor='none',
                       borderwidth=0,
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['primary_hover']),
                           ('pressed', self.colors['primary_hover'])])
        
        style.configure('Secondary.TButton',
                       background=self.colors['secondary'],
                       foreground=self.colors['text_primary'],
                       font=('맑은 고딕', 10),
                       focuscolor='none',
                       borderwidth=1,
                       relief='flat')
        
        style.map('Secondary.TButton',
                 background=[('active', self.colors['accent']),
                           ('pressed', self.colors['accent'])])
        
        # 입력 필드 스타일
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['background'],
                       borderwidth=2,
                       relief='flat',
                       font=('맑은 고딕', 12))
        
        # 콤보박스 스타일
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['background'],
                       borderwidth=2,
                       relief='flat',
                       font=('맑은 고딕', 12))
        
        # 라디오 버튼 스타일 (토글 버튼처럼 보이게)
        style.configure('Toggle.TRadiobutton',
                       background=self.colors['secondary'],
                       foreground=self.colors['text_primary'],
                       font=('맑은 고딕', 11),
                       focuscolor='none',
                       borderwidth=1,
                       relief='flat')
        
        style.map('Toggle.TRadiobutton',
                 background=[('selected', self.colors['primary']),
                           ('active', self.colors['accent'])],
                 foreground=[('selected', 'white')])
        
        # LabelFrame 스타일
        style.configure('Modern.TLabelframe',
                       background=self.colors['card_bg'],
                       borderwidth=0,
                       relief='flat')
        
        style.configure('Modern.TLabelframe.Label',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_primary'],
                       font=('맑은 고딕', 13, 'bold'))
        
    def create_card_frame(self, parent, title="", **kwargs):
        """카드 스타일의 프레임을 생성합니다."""
        card = tk.Frame(parent, bg=self.colors['card_bg'], relief='flat', bd=0, **kwargs)
        
        # 그림자 효과를 위한 테두리
        border_frame = tk.Frame(parent, bg=self.colors['border'], height=2)
        
        if title:
            title_label = tk.Label(card, text=title, 
                                 bg=self.colors['card_bg'],
                                 fg=self.colors['text_primary'],
                                 font=('맑은 고딕', 13, 'bold'))
            title_label.pack(anchor='w', padx=15, pady=(15, 10))
            
        return card
        
    def setup_ui(self):
        # 메인 컨테이너
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 상단 헤더
        header_frame = tk.Frame(main_container, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 로고/메인 이미지
        try:
            main_img = Image.open(os.path.join("images", "mammoth_main.png")).resize((360, 100))
            self.main_photo = ImageTk.PhotoImage(main_img)
            img_label = tk.Label(header_frame, image=self.main_photo, 
                               bg=self.colors['background'], borderwidth=0)
            img_label.pack()
        except Exception as e:
            # 이미지가 없을 경우 텍스트로 대체
            logo_frame = tk.Frame(header_frame, bg=self.colors['primary'], height=80)
            logo_frame.pack(fill=tk.X, pady=10)
            logo_frame.pack_propagate(False)
            
            logo_label = tk.Label(logo_frame, text="MAMMOTH COFFEE", 
                                bg=self.colors['primary'], fg='white',
                                font=('맑은 고딕', 20, 'bold'))
            logo_label.pack(expand=True)

        # 타이틀
        title_label = tk.Label(header_frame, text="☕ 매머드커피 주문 시스템 ☕", 
                             bg=self.colors['background'], fg=self.colors['text_primary'],
                             font=('맑은 고딕', 18, 'bold'))
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(header_frame, text="음료를 선택하고 주문을 진행하세요!", 
                                bg=self.colors['background'], fg=self.colors['text_secondary'],
                                font=('맑은 고딕', 11))
        subtitle_label.pack()

        # 주문자 정보 카드
        name_card = self.create_card_frame(main_container, "👤 주문자 정보")
        name_card.pack(fill=tk.X, pady=(0, 15))
        
        name_inner = tk.Frame(name_card, bg=self.colors['card_bg'])
        name_inner.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        name_label = tk.Label(name_inner, text="이름", 
                            bg=self.colors['card_bg'], fg=self.colors['text_primary'],
                            font=('맑은 고딕', 12))
        name_label.pack(anchor='w', pady=(0, 5))
        
        self.name_entry = tk.Entry(name_inner, font=('맑은 고딕', 12), 
                                 bg=self.colors['background'], fg=self.colors['text_primary'],
                                 relief='solid', bd=1, highlightthickness=0)
        self.name_entry.pack(fill=tk.X, ipady=8)
        self.name_entry.bind('<Return>', lambda e: self.show_menu_selection())

        # 음료 선택 카드
        menu_card = self.create_card_frame(main_container, "☕ 음료 선택")
        menu_card.pack(fill=tk.X, pady=(0, 15))
        
        menu_inner = tk.Frame(menu_card, bg=self.colors['card_bg'])
        menu_inner.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # 카테고리 선택
        category_label = tk.Label(menu_inner, text="카테고리", 
                                bg=self.colors['card_bg'], fg=self.colors['text_primary'],
                                font=('맑은 고딕', 12))
        category_label.pack(anchor='w', pady=(0, 5))
        
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(menu_inner, textvariable=self.category_var, 
                                    values=list(MENU.keys()), state="readonly", 
                                    font=('맑은 고딕', 12), style='Modern.TCombobox')
        category_combo.pack(fill=tk.X, ipady=5, pady=(0, 15))
        category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)
        
        # 온도 선택
        temp_label = tk.Label(menu_inner, text="온도", 
                            bg=self.colors['card_bg'], fg=self.colors['text_primary'],
                            font=('맑은 고딕', 12))
        temp_label.pack(anchor='w', pady=(0, 5))
        
        self.temperature_var = tk.StringVar(value="ICE")
        temp_frame = tk.Frame(menu_inner, bg=self.colors['card_bg'])
        temp_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 토글 버튼 스타일의 라디오 버튼
        ice_btn = tk.Radiobutton(temp_frame, text="🧊 ICE", variable=self.temperature_var, 
                               value="ICE", bg=self.colors['secondary'], 
                               fg=self.colors['text_primary'], font=('맑은 고딕', 11),
                               selectcolor=self.colors['primary'], relief='flat',
                               bd=0, padx=20, pady=8, indicatoron=0)
        ice_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        hot_btn = tk.Radiobutton(temp_frame, text="🔥 HOT", variable=self.temperature_var, 
                               value="HOT", bg=self.colors['secondary'], 
                               fg=self.colors['text_primary'], font=('맑은 고딕', 11),
                               selectcolor=self.colors['primary'], relief='flat',
                               bd=0, padx=20, pady=8, indicatoron=0)
        hot_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 주문 완료 버튼
        order_btn = tk.Button(menu_inner, text="🛒 내 주문 완료", command=self.add_order,
                            bg=self.colors['primary'], fg='white', 
                            font=('맑은 고딕', 12, 'bold'),
                            relief='flat', bd=0, pady=12, cursor='hand2')
        order_btn.pack(fill=tk.X, pady=(5, 0))
        
        # 호버 효과
        def on_enter(e):
            order_btn.config(bg=self.colors['primary_hover'])
        def on_leave(e):
            order_btn.config(bg=self.colors['primary'])
        order_btn.bind("<Enter>", on_enter)
        order_btn.bind("<Leave>", on_leave)

        # 메뉴 이미지 선택 카드
        image_card = self.create_card_frame(main_container, "📋 메뉴 선택")
        image_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 스크롤 가능한 메뉴 영역
        canvas_frame = tk.Frame(image_card, bg=self.colors['card_bg'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['card_bg'], 
                              highlightthickness=0, height=200)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['card_bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 현재 주문 현황 카드
        status_card = self.create_card_frame(main_container, "📊 현재 주문 현황")
        status_card.pack(fill=tk.X, pady=(0, 15))
        
        status_inner = tk.Frame(status_card, bg=self.colors['card_bg'])
        status_inner.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.status_text = tk.Text(status_inner, height=6, 
                                 bg=self.colors['background'], fg=self.colors['text_primary'],
                                 font=('맑은 고딕', 11), relief='solid', bd=1,
                                 highlightthickness=0, wrap=tk.WORD)
        self.status_text.pack(fill=tk.X)

        # 하단 버튼들
        button_frame = tk.Frame(main_container, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        final_btn = tk.Button(button_frame, text="🎯 모든 인원 주문 완료", 
                            command=self.show_final_order,
                            bg=self.colors['success'], fg='white', 
                            font=('맑은 고딕', 11, 'bold'),
                            relief='flat', bd=0, pady=10, cursor='hand2')
        final_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        reset_btn = tk.Button(button_frame, text="🔄 초기화", command=self.reset_orders,
                            bg=self.colors['error'], fg='white', 
                            font=('맑은 고딕', 11),
                            relief='flat', bd=0, pady=10, cursor='hand2')
        reset_btn.pack(side=tk.RIGHT)
        
        # 버튼 호버 효과
        def create_hover_effect(button, normal_color, hover_color):
            def on_enter(e):
                button.config(bg=hover_color)
            def on_leave(e):
                button.config(bg=normal_color)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        create_hover_effect(final_btn, self.colors['success'], '#00A085')
        create_hover_effect(reset_btn, self.colors['error'], '#D63031')
        
        # 초기 상태 업데이트
        self.update_status_display()
        
    def on_category_selected(self, event=None):
        """카테고리가 선택되었을 때 메뉴 이미지를 표시합니다."""
        category = self.category_var.get()
        if category in MENU:
            self.display_menu_images(category)
            
    def display_menu_images(self, category):
        """선택된 카테고리의 메뉴 이미지들을 표시합니다."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        drinks = MENU[category]
        row = 0
        col = 0
        max_cols = 2  # 한 줄에 2개씩
        
        for drink in drinks:
            # 메뉴 아이템 카드
            item_card = tk.Frame(self.scrollable_frame, bg=self.colors['background'], 
                               relief='solid', bd=1, padx=10, pady=10)
            item_card.grid(row=row, column=col, padx=8, pady=8, sticky='ew')
            
            # 이미지 표시
            img = get_menu_image(drink)
            if img:
                img_label = tk.Label(item_card, image=img, bg=self.colors['background'])
                img_label.image = img  # 참조 유지
            else:
                img_label = tk.Label(item_card, text="🥤", font=('맑은 고딕', 24),
                                   bg=self.colors['background'])
            img_label.pack(pady=(0, 8))
            
            # 메뉴명 라벨
            name_label = tk.Label(item_card, text=drink, font=('맑은 고딕', 10, 'bold'), 
                                bg=self.colors['background'], fg=self.colors['text_primary'],
                                wraplength=100, justify=tk.CENTER)
            name_label.pack(pady=(0, 8))
            
            # 선택 버튼
            select_btn = tk.Button(item_card, text="선택", 
                                 command=lambda d=drink: self.select_drink(d),
                                 bg=self.colors['primary'], fg='white', 
                                 font=('맑은 고딕', 9, 'bold'),
                                 relief='flat', bd=0, pady=6, cursor='hand2')
            select_btn.pack(fill=tk.X)
            
            # 버튼 호버 효과
            def create_select_hover(btn):
                def on_enter(e):
                    btn.config(bg=self.colors['primary_hover'])
                def on_leave(e):
                    btn.config(bg=self.colors['primary'])
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
            
            create_select_hover(select_btn)
            
            # 그리드 설정
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # 컬럼 가중치 설정
        for i in range(max_cols):
            self.scrollable_frame.columnconfigure(i, weight=1)
                
    def select_drink(self, drink_name):
        """음료를 선택합니다."""
        self.drink_var = drink_name
        messagebox.showinfo("선택 완료", f"'{drink_name}'을(를) 선택했습니다!", icon='info')
        
    def add_order(self):
        """주문을 추가합니다."""
        name = self.name_entry.get().strip()
        drink = getattr(self, 'drink_var', None)
        temperature = self.temperature_var.get()
        
        if not name:
            messagebox.showerror("오류", "이름을 입력해주세요.", icon='error')
            return
        if not drink:
            messagebox.showerror("오류", "음료를 선택해주세요.", icon='error')
            return
            
        # 추가 요청사항 입력 여부 확인
        if messagebox.askyesno("추가 요청사항", "추가 요청사항이 있나요?", icon='question'):
            self.show_request_dialog(name, drink, temperature)
        else:
            self._finalize_order(name, drink, temperature, "")

    def show_request_dialog(self, name, drink, temperature):
        """요청사항 입력 대화상자를 표시합니다."""
        req_window = tk.Toplevel(self.root)
        req_window.title("추가 요청사항 입력")
        req_window.geometry("400x200")
        req_window.configure(bg=self.colors['background'])
        req_window.transient(self.root)
        req_window.grab_set()
        
        # 중앙 정렬
        req_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        main_frame = tk.Frame(req_window, bg=self.colors['background'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="📝 추가 요청사항", 
                             bg=self.colors['background'], fg=self.colors['text_primary'],
                             font=('맑은 고딕', 14, 'bold'))
        title_label.pack(pady=(0, 15))
        
        desc_label = tk.Label(main_frame, text="음료에 대한 특별한 요청사항을 입력해주세요", 
                            bg=self.colors['background'], fg=self.colors['text_secondary'],
                            font=('맑은 고딕', 10))
        desc_label.pack(pady=(0, 10))
        
        req_entry = tk.Entry(main_frame, font=('맑은 고딕', 12), 
                           bg=self.colors['background'], fg=self.colors['text_primary'],
                           relief='solid', bd=1, highlightthickness=0)
        req_entry.pack(fill=tk.X, ipady=8, pady=(0, 20))
        req_entry.focus()
        
        def submit_req():
            req = req_entry.get().strip()
            self._finalize_order(name, drink, temperature, req)
            req_window.destroy()
        
        def cancel_req():
            req_window.destroy()
        
        req_entry.bind('<Return>', lambda e: submit_req())
        
        button_frame = tk.Frame(main_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X)
        
        confirm_btn = tk.Button(button_frame, text="확인", command=submit_req,
                              bg=self.colors['primary'], fg='white', 
                              font=('맑은 고딕', 11, 'bold'),
                              relief='flat', bd=0, pady=8, cursor='hand2')
        confirm_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(button_frame, text="취소", command=cancel_req,
                             bg=self.colors['secondary'], fg=self.colors['text_primary'], 
                             font=('맑은 고딕', 11),
                             relief='flat', bd=0, pady=8, cursor='hand2')
        cancel_btn.pack(side=tk.RIGHT)
        
        req_window.wait_window()

    def _finalize_order(self, name, drink, temperature, request):
        """주문을 완료 처리합니다."""
        self.orders[name] = (drink, temperature, request)
        self.drink_counts[(drink, temperature)] += 1
        self.name_entry.delete(0, tk.END)
        self.drink_var = None
        self.category_var.set('')
        
        # 메뉴 표시 영역 초기화
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.update_status_display()
        messagebox.showinfo("주문 완료", f"✅ {name}님의 주문이 완료되었습니다!\n\n🥤 {drink} ({temperature})", icon='info')
        
    def update_status_display(self):
        """현재 주문 현황을 업데이트합니다."""
        self.status_text.delete(1.0, tk.END)
        
        if not self.orders:
            self.status_text.insert(tk.END, "🔍 아직 주문이 없습니다.\n위에서 음료를 선택하고 주문해주세요!")
            return
            
        # 개별 주문 내역
        self.status_text.insert(tk.END, "👥 개별 주문 내역\n")
        self.status_text.insert(tk.END, "─" * 40 + "\n")
        
        for name, (drink, temp, req) in self.orders.items():
            req_str = f" | 📝 {req}" if req else ""
            temp_icon = "🧊" if temp == "ICE" else "🔥"
            self.status_text.insert(tk.END, f"• {name}: {drink} {temp_icon}{req_str}\n")
            
        # 누적 주문 현황
        self.status_text.insert(tk.END, f"\n📊 누적 주문 현황\n")
        self.status_text.insert(tk.END, "─" * 40 + "\n")
        
        for (drink, temp), count in self.drink_counts.items():
            temp_icon = "🧊" if temp == "ICE" else "🔥"
            self.status_text.insert(tk.END, f"• {drink} {temp_icon}: {count}잔\n")
            
        # 총 주문 수
        total_orders = len(self.orders)
        total_drinks = sum(self.drink_counts.values())
        self.status_text.insert(tk.END, f"\n🎯 총 주문자: {total_orders}명 | 총 음료: {total_drinks}잔\n")
        
    def show_final_order(self):
        """최종 주문 내역을 매장 주문용으로 표시합니다."""
        if not self.orders:
            messagebox.showinfo("알림", "📋 주문 내역이 없습니다.", icon='info')
            return
            
        final_window = tk.Toplevel(self.root)
        final_window.title("📋 최종 주문 내역 (매장 주문용)")
        final_window.geometry("900x700")
        final_window.configure(bg=self.colors['background'])
        
        # 중앙 정렬
        final_window.geometry("+%d+%d" % (self.root.winfo_rootx() - 100, self.root.winfo_rooty() - 50))
        
        main_frame = tk.Frame(final_window, bg=self.colors['background'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 헤더
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], pady=15)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = tk.Label(header_frame, text="☕ 매머드커피 최종 주문서 ☕", 
                              bg=self.colors['primary'], fg='white',
                              font=('맑은 고딕', 18, 'bold'))
        header_label.pack()
        
        # 텍스트 영역
        text_frame = tk.Frame(main_frame, bg=self.colors['background'])
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('맑은 고딕', 12),
                            bg=self.colors['background'], fg=self.colors['text_primary'],
                            relief='solid', bd=1, highlightthickness=0)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # 주문 내역 작성
        text_widget.insert(tk.END, "🏪 매장 주문용 정리 내역\n")
        text_widget.insert(tk.END, "=" * 60 + "\n\n")
        
        hot_orders = defaultdict(int)
        ice_orders = defaultdict(int)
        
        for drink, temp in self.drink_counts.keys():
            count = self.drink_counts[(drink, temp)]
            if temp == "HOT":
                hot_orders[drink] += count
            else:
                ice_orders[drink] += count
        
        if hot_orders:
            text_widget.insert(tk.END, "🔥 HOT 음료 주문:\n")
            text_widget.insert(tk.END, "-" * 40 + "\n")
            for drink, count in sorted(hot_orders.items()):
                text_widget.insert(tk.END, f"• {drink} ×{count}잔\n")
            text_widget.insert(tk.END, "\n")
        
        if ice_orders:
            text_widget.insert(tk.END, "🧊 ICE 음료 주문:\n")
            text_widget.insert(tk.END, "-" * 40 + "\n")
            for drink, count in sorted(ice_orders.items()):
                text_widget.insert(tk.END, f"• {drink} ×{count}잔\n")
            text_widget.insert(tk.END, "\n")
        
        total_drinks = sum(self.drink_counts.values())
        text_widget.insert(tk.END, f"📊 주문 요약:\n")
        text_widget.insert(tk.END, f"   총 음료 수: {total_drinks}잔\n")
        text_widget.insert(tk.END, f"   총 주문자: {len(self.orders)}명\n")
        text_widget.insert(tk.END, "\n" + "=" * 60 + "\n")
        
        text_widget.insert(tk.END, "📝 개별 주문 내역 (참고용):\n")
        text_widget.insert(tk.END, "-" * 40 + "\n")
        
        for name, (drink, temp, req) in self.orders.items():
            req_str = f" | 요청: {req}" if req else ""
            temp_icon = "🧊" if temp == "ICE" else "🔥"
            text_widget.insert(tk.END, f"• {name}: {drink} {temp_icon}{req_str}\n")
        
        text_widget.configure(state=tk.DISABLED)
        
    def reset_orders(self):
        """모든 주문을 초기화합니다."""
        if messagebox.askyesno("초기화 확인", "🔄 모든 주문을 초기화하시겠습니까?\n이 작업은 되돌릴 수 없습니다.", icon='warning'):
            self.orders.clear()
            self.drink_counts.clear()
            
            # 메뉴 표시 영역 초기화
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            self.name_entry.delete(0, tk.END)
            self.category_var.set('')
            if hasattr(self, 'drink_var'):
                delattr(self, 'drink_var')
                
            self.update_status_display()
            messagebox.showinfo("초기화 완료", "✅ 모든 주문이 초기화되었습니다.", icon='info')
            
    def show_menu_selection(self):
        """이름 입력 후 메뉴 선택으로 포커스를 이동합니다."""
        if self.name_entry.get().strip():
            # 카테고리 콤보박스로 포커스 이동
            pass

def main():
    """GUI 애플리케이션을 실행합니다."""
    root = tk.Tk()
    app = CoffeeOrderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()