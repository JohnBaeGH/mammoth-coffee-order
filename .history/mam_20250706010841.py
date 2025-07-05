import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from collections import defaultdict
import requests
from io import BytesIO
import threading

# --- 데이터 (기존과 동일) ---
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


# --- 밝고 발랄한 디자인 설정 ---
BG_COLOR = "#F8F9FA"       # 부드러운 흰색 배경
FRAME_COLOR = "#FFFFFF"     # 카드형 UI를 위한 순백색
TEXT_COLOR = "#343A40"      # 가독성 높은 진한 회색 텍스트
ACCENT_COLOR = "#00AEEF"     # 상쾌한 하늘색 포인트
DISABLED_COLOR = "#CED4DA"   # 비활성화된 요소 색상
FONT_FAMILY = "맑은 고딕"
FONT_TITLE = (FONT_FAMILY, 20, "bold")
FONT_H1 = (FONT_FAMILY, 14, "bold")
FONT_BODY = (FONT_FAMILY, 11)
FONT_BUTTON = (FONT_FAMILY, 11, "bold")

class CoffeeOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mammoth Coffee Order System")
        self.root.geometry("420x800")
        self.root.configure(bg="#F8F9FA")
        self.orders = {}
        self.drink_counts = defaultdict(int)
        self.selected_drink = None
        self.selected_drink_button = None
        self.image_cache = {}
        self.photo_cache = {}
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#F8F9FA")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 헤더 이미지
        try:
            img_path = os.path.join("images", "mammoth_main.png")
            main_img = Image.open(img_path).resize((380, 100), Image.Resampling.LANCZOS)
            self.main_photo = ImageTk.PhotoImage(main_img)
            header_label = tk.Label(main_frame, image=self.main_photo, bg="#F8F9FA")
        except Exception:
            header_label = tk.Label(main_frame, text="MAMMOTH COFFEE", font=("Arial", 20, "bold"), bg="#F8F9FA")
        header_label.pack(fill=tk.X, pady=(0, 20))

        # 주문자 정보
        name_frame = tk.LabelFrame(main_frame, text="주문자 이름", bg="#F8F9FA", padx=10, pady=10)
        name_frame.pack(fill=tk.X, pady=5)
        self.name_entry = tk.Entry(name_frame, font=("Arial", 13), width=20)
        self.name_entry.pack(fill=tk.X, expand=True)

        # 메뉴 선택
        menu_select_frame = tk.LabelFrame(main_frame, text="음료 선택", bg="#F8F9FA", padx=10, pady=10)
        menu_select_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 카테고리 & 온도
        cat_temp_frame = tk.Frame(menu_select_frame, bg="#F1F3F5")
        cat_temp_frame.pack(fill=tk.X, pady=(0, 10))
        cat_temp_frame.columnconfigure(0, weight=1)
        cat_temp_frame.columnconfigure(1, weight=1)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(cat_temp_frame, textvariable=self.category_var,
                                     values=list(MENU.keys()), state="readonly", font=("Arial", 12))
        category_combo.set("카테고리 선택")
        category_combo.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)
        self.temperature_var = tk.StringVar(value="ICE")
        temp_frame = tk.Frame(cat_temp_frame, bg="#F1F3F5")
        temp_frame.grid(row=0, column=1, sticky='ew', padx=(5, 0))
        ttk.Radiobutton(temp_frame, text="ICE", variable=self.temperature_var, value="ICE").pack(side=tk.LEFT, expand=True)
        ttk.Radiobutton(temp_frame, text="HOT", variable=self.temperature_var, value="HOT").pack(side=tk.LEFT, expand=True)

        # 메뉴 이미지 스크롤 영역
        self.canvas = tk.Canvas(menu_select_frame, bg="#F1F3F5", highlightthickness=0, height=200)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(menu_select_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F1F3F5")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # 주문 추가 버튼
        self.add_order_btn = ttk.Button(main_frame, text="내 주문 완료", command=self.add_order, state='normal')
        self.add_order_btn.pack(fill=tk.X, pady=10, ipady=5)

        # 주문 현황
        status_frame = tk.LabelFrame(main_frame, text="현재 주문 현황", bg="#F8F9FA", padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.status_text = tk.Text(status_frame, height=8, width=40, font=('Arial', 12), bg='#F1F3F5', fg='#222', relief='flat', highlightthickness=0)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_status_display()

        # 하단 버튼 프레임
        bottom_frame = tk.Frame(main_frame, bg="#F1F3F5")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        self.reset_btn = ttk.Button(bottom_frame, text="초기화", command=self.reset_orders)
        self.reset_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=5)
        self.all_order_btn = ttk.Button(bottom_frame, text="모든 인원 주문 완료", command=self.show_final_order)
        self.all_order_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0), ipady=5)

    def on_category_selected(self, event=None):
        category = self.category_var.get()
        if not category or category == "카테고리 선택":
            return
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        drinks = MENU[category]
        row = 0
        col = 0
        max_cols = 2
        for drink in drinks:
            menu_item_frame = tk.Frame(self.scrollable_frame, bg="#F1F3F5")
            menu_item_frame.grid(row=row, column=col, padx=4, pady=6, sticky=(tk.W, tk.E))
            img = self.get_menu_image(drink)
            if img:
                img_label = tk.Label(menu_item_frame, image=img, bg="#F1F3F5")
                img_label.image = img
            else:
                img_label = tk.Label(menu_item_frame, text="🍹", font=('Arial', 18), bg="#F1F3F5")
            img_label.grid(row=0, column=0, pady=(0, 3))
            name_label = tk.Label(menu_item_frame, text=drink, font=('Arial', 11), wraplength=80, justify=tk.CENTER, bg="#F1F3F5")
            name_label.grid(row=1, column=0, pady=(0, 3))
            select_btn = ttk.Button(menu_item_frame, text="선택", command=lambda d=drink: self.select_drink(d), width=8)
            select_btn.grid(row=2, column=0)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def get_menu_image(self, menu_name):
        img_path = os.path.join("images", f"{menu_name}.png")
        if os.path.exists(img_path):
            img = Image.open(img_path).resize((80, 80))
            return ImageTk.PhotoImage(img)
        return None

    def select_drink(self, drink_name):
        self.selected_drink = drink_name
        # 추가로 버튼 활성화 등 필요시 구현

    def add_order(self):
        name = self.name_entry.get().strip()
        drink = self.selected_drink
        temperature = self.temperature_var.get()
        if not name:
            tk.messagebox.showerror("오류", "이름을 입력해주세요.")
            return
        if not drink:
            tk.messagebox.showerror("오류", "음료를 선택해주세요.")
            return
        request = ""
        if tk.messagebox.askyesno("추가 요청사항", "추가 요청사항이 있나요?"):
            req_window = tk.Toplevel(self.root)
            req_window.title("추가 요청사항 입력")
            req_window.geometry("350x150")
            tk.Label(req_window, text="추가 요청사항을 입력하세요:").pack(pady=10)
            req_entry = tk.Entry(req_window, width=40)
            req_entry.pack(pady=5)
            def submit_req():
                nonlocal request
                request = req_entry.get().strip()
                self._finalize_order(name, drink, temperature, request)
                req_window.destroy()
            tk.Button(req_window, text="확인", command=submit_req).pack(pady=10)
            req_window.transient(self.root)
            req_window.grab_set()
            req_window.wait_window()
        else:
            self._finalize_order(name, drink, temperature, request)

    def _finalize_order(self, name, drink, temperature, request):
        self.orders[name] = (drink, temperature, request)
        self.drink_counts[(drink, temperature)] += 1
        self.name_entry.delete(0, tk.END)
        self.selected_drink = None
        self.category_var.set('')
        self.update_status_display()
        tk.messagebox.showinfo("성공", f"{name}님의 주문이 추가되었습니다!\n{drink} ({temperature})")

    def update_status_display(self):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        if not self.orders:
            self.status_text.insert(tk.END, "아직 주문이 없습니다.")
        else:
            for name, (drink, temp, req) in self.orders.items():
                req_str = f" | 요청: {req}" if req else ""
                self.status_text.insert(tk.END, f"{name}: {drink} ({temp}){req_str}\n")
        self.status_text.config(state=tk.DISABLED)

    def reset_orders(self):
        self.orders.clear()
        self.drink_counts.clear()
        self.update_status_display()

    def show_final_order(self):
        # ... 기존 최종 주문 내역 출력 코드 ...
        pass

if __name__ == "__main__":
    app_root = tk.Tk()
    app = CoffeeOrderApp(app_root)
    app_root.mainloop()