import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from collections import defaultdict
import requests
from io import BytesIO
import threading

# --- 기존 메뉴 데이터 (변경 없음) ---
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

# --- 기존 이미지 로드 함수 (변경 없음) ---
def get_menu_image(menu_name):
    img_path = os.path.join("images", f"{menu_name}.png")
    if os.path.exists(img_path):
        # 카드에 맞게 이미지 크기 조정
        img = Image.open(img_path).resize((120, 120), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    return None

class CoffeeOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MAMMOTH COFFEE KIOSK")
        self.root.geometry("420x800") # 모바일 키오스크 비율
        self.root.configure(bg='#FFFFFF')
        self.root.resizable(False, False)

        # --- 스타일링을 위한 변수 정의 ---
        self.FONT_TITLE = ("맑은 고딕", 20, "bold")
        self.FONT_HEADER = ("맑은 고딕", 14, "bold")
        self.FONT_BODY = ("맑은 고딕", 11)
        self.FONT_BODY_BOLD = ("맑은 고딕", 11, "bold")
        
        self.COLOR_PRIMARY = "#FF7A00" # 매머드커피 오렌지
        self.COLOR_SECONDARY = "#FFE0B2" # 밝은 오렌지
        self.COLOR_BACKGROUND = "#FFFFFF"
        self.COLOR_TEXT = "#333333"
        self.COLOR_SUBTEXT = "#666666"
        self.COLOR_BORDER = "#EEEEEE"

        # --- 기존 데이터 변수 (변경 없음) ---
        self.orders = {}
        self.drink_counts = defaultdict(int)
        self.image_cache = {}
        self.photo_cache = {}
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """GUI 위젯들의 스타일을 설정합니다."""
        style = ttk.Style()
        style.theme_use('clam')

        # 전체적인 위젯 스타일 설정
        style.configure('.', 
                        background=self.COLOR_BACKGROUND, 
                        foreground=self.COLOR_TEXT, 
                        font=self.FONT_BODY)
        
        # 메인 프레임
        style.configure('Main.TFrame', background=self.COLOR_BACKGROUND)

        # 섹션 '카드' 프레임 스타일
        style.configure('Card.TFrame', 
                        background=self.COLOR_BACKGROUND,
                        relief='solid', 
                        borderwidth=1,
                        bordercolor=self.COLOR_BORDER)
        
        # 라벨 스타일
        style.configure('TLabel', foreground=self.COLOR_TEXT)
        style.configure('Header.TLabel', font=self.FONT_HEADER, foreground=self.COLOR_TEXT)
        style.configure('Title.TLabel', font=self.FONT_TITLE, foreground=self.COLOR_PRIMARY)
        style.configure('Sub.TLabel', font=self.FONT_BODY, foreground=self.COLOR_SUBTEXT)
        
        # 입력창(Entry) 및 콤보박스 스타일
        style.configure('TEntry', 
                        fieldbackground=self.COLOR_BACKGROUND,
                        bordercolor=self.COLOR_BORDER,
                        insertcolor=self.COLOR_PRIMARY,
                        padding=(10, 8))
        style.map('TEntry',
                  bordercolor=[('focus', self.COLOR_PRIMARY)])
        
        style.configure('TCombobox', 
                        fieldbackground=self.COLOR_BACKGROUND,
                        bordercolor=self.COLOR_BORDER,
                        arrowcolor=self.COLOR_PRIMARY,
                        selectbackground=self.COLOR_SECONDARY,
                        padding=(10, 8))

        # 메인 액션 버튼 스타일 (주문 완료, 최종 확인 등)
        style.configure('Accent.TButton', 
                        background=self.COLOR_PRIMARY, 
                        foreground='white',
                        font=self.FONT_BODY_BOLD,
                        padding=(20, 12),
                        bordercolor=self.COLOR_PRIMARY,
                        relief='flat')
        style.map('Accent.TButton',
                  background=[('active', self.COLOR_SECONDARY), ('!disabled', self.COLOR_PRIMARY)],
                  relief=[('pressed', 'sunken')])
        
        # 보조 버튼 스타일 (초기화)
        style.configure('Secondary.TButton', 
                        background=self.COLOR_BACKGROUND,
                        foreground=self.COLOR_PRIMARY,
                        font=self.FONT_BODY_BOLD,
                        padding=(15, 12),
                        bordercolor=self.COLOR_PRIMARY,
                        borderwidth=1,
                        relief='solid')
        style.map('Secondary.TButton',
                  background=[('active', self.COLOR_SECONDARY)])

        # 메뉴 선택 버튼 스타일
        style.configure('Select.TButton',
                        font=("맑은 고딕", 9, "bold"),
                        padding=(8, 5))

        # 온도 선택 토글 버튼 스타일
        style.configure('Toggle.TRadiobutton',
                        font=self.FONT_BODY_BOLD,
                        padding=(20, 10),
                        relief='flat',
                        indicatorrelief='flat',
                        indicatormargin=-1,
                        indicatordiameter=-1)
        style.map('Toggle.TRadiobutton',
                  background=[('selected', self.COLOR_PRIMARY), ('!selected', '#E0E0E0')],
                  foreground=[('selected', 'white'), ('!selected', self.COLOR_SUBTEXT)])

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=(20, 15), style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 상단 로고 및 타이틀 ---
        header_frame = ttk.Frame(main_frame, style='Main.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        try:
            main_img_pil = Image.open(os.path.join("images", "mammoth_main.png")).resize((280, 75), Image.Resampling.LANCZOS)
            self.main_photo = ImageTk.PhotoImage(main_img_pil)
            img_label = tk.Label(header_frame, image=self.main_photo, bg=self.COLOR_BACKGROUND)
            img_label.pack()
        except Exception:
            img_label = ttk.Label(header_frame, text="MAMMOTH COFFEE", style='Title.TLabel')
            img_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="오늘의 커피, 매머드에서 주문하세요!", style='Sub.TLabel')
        subtitle_label.pack(pady=(5, 0))

        # --- 주문자 정보 카드 ---
        name_card = ttk.Frame(main_frame, style='Card.TFrame', padding=15)
        name_card.pack(fill=tk.X, pady=8)
        
        ttk.Label(name_card, text="주문자 이름", style='Header.TLabel').pack(anchor='w')
        self.name_entry = ttk.Entry(name_card, width=20, font=self.FONT_BODY)
        self.name_entry.pack(fill=tk.X, pady=(8, 0))
        self.name_entry.bind('<Return>', lambda e: self.show_menu_selection())

        # --- 메뉴 선택 카드 ---
        menu_card = ttk.Frame(main_frame, style='Card.TFrame', padding=15)
        menu_card.pack(fill=tk.X, pady=8)

        ttk.Label(menu_card, text="음료 선택", style='Header.TLabel').pack(anchor='w')
        
        # 카테고리
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(menu_card, textvariable=self.category_var, 
                                     values=list(MENU.keys()), state="readonly", font=self.FONT_BODY)
        category_combo.pack(fill=tk.X, pady=(8, 10))
        category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)
        
        # 온도 선택
        self.temperature_var = tk.StringVar(value="ICE")
        temp_frame = ttk.Frame(menu_card, style='Card.TFrame')
        temp_frame.pack(fill=tk.X, pady=(0, 10))
        temp_frame.columnconfigure(0, weight=1)
        temp_frame.columnconfigure(1, weight=1)

        ttk.Radiobutton(temp_frame, text="ICE 🧊", variable=self.temperature_var, value="ICE", style='Toggle.TRadiobutton').grid(row=0, column=0, sticky='ew')
        ttk.Radiobutton(temp_frame, text="HOT 🔥", variable=self.temperature_var, value="HOT", style='Toggle.TRadiobutton').grid(row=0, column=1, sticky='ew')
        
        # 주문 버튼
        order_btn = ttk.Button(menu_card, text="내 주문 담기", command=self.add_order, style='Accent.TButton')
        order_btn.pack(fill=tk.X, pady=(8, 0))
        
        # --- 메뉴 이미지 스크롤 영역 ---
        self.image_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=0)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=8)
        
        self.canvas = tk.Canvas(self.image_frame, bg=self.COLOR_BACKGROUND, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.image_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Main.TFrame', padding=(15, 10))
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 초기 안내 메시지
        self.initial_menu_prompt = ttk.Label(self.scrollable_frame, text="음료 카테고리를 선택해주세요!", font=self.FONT_BODY, foreground=self.COLOR_SUBTEXT)
        self.initial_menu_prompt.pack(pady=50)

        # --- 하단 버튼 ---
        button_frame = ttk.Frame(main_frame, style='Main.TFrame')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        button_frame.columnconfigure(0, weight=2)
        button_frame.columnconfigure(1, weight=1)

        ttk.Button(button_frame, text="전체 주문 완료", command=self.show_final_order, style='Accent.TButton').grid(row=0, column=0, sticky='ew', padx=(0, 5))
        ttk.Button(button_frame, text="초기화", command=self.reset_orders, style='Secondary.TButton').grid(row=0, column=1, sticky='ew', padx=(5, 0))
        
        self.update_status_display() # 초기화면에서는 숨김
            
    def display_menu_images(self, category):
        """선택된 카테고리의 메뉴 이미지를 세련된 카드로 표시합니다."""
        if self.initial_menu_prompt:
            self.initial_menu_prompt.destroy()
            self.initial_menu_prompt = None

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        drinks = MENU[category]
        
        for i, drink in enumerate(drinks):
            row, col = divmod(i, 2)
            
            # 메뉴 아이템 카드
            card = ttk.Frame(self.scrollable_frame, style='Card.TFrame', padding=10)
            card.grid(row=row, column=col, padx=5, pady=6, sticky='nsew')
            self.scrollable_frame.columnconfigure(col, weight=1)

            # 이미지
            img = get_menu_image(drink)
            if img:
                img_label = tk.Label(card, image=img, bg=self.COLOR_BACKGROUND)
                img_label.image = img
            else:
                img_label = tk.Label(card, text="🥤", font=("맑은 고딕", 40), bg=self.COLOR_BACKGROUND)
            img_label.pack(pady=(0, 10))
            
            # 메뉴명
            name_label = ttk.Label(card, text=drink, font=self.FONT_BODY, wraplength=130, justify=tk.CENTER)
            name_label.pack(pady=(0, 10), fill=tk.X)
            
            # 선택 버튼
            select_btn = ttk.Button(card, text="선택", style='Select.TButton', command=lambda d=drink: self.select_drink(d))
            select_btn.pack()

            # 호버 효과
            def on_enter(e, c=card):
                c.configure(style='Card.Hover.TFrame')
            def on_leave(e, c=card):
                c.configure(style='Card.TFrame')

            # 스타일 정의가 필요함 (여기서는 간단하게 구현)
            # card.bind("<Enter>", on_enter)
            # card.bind("<Leave>", on_leave)
    
    # --- 아래 로직은 기존 코드와 거의 동일 ---
            
    def on_category_selected(self, event=None):
        category = self.category_var.get()
        if category in MENU:
            self.display_menu_images(category)

    def select_drink(self, drink_name):
        self.drink_var = drink_name
        # 더 나은 사용자 경험을 위해 messagebox 대신 시각적 피드백 제공
        # 예: 선택된 카드를 강조 표시 (추가 구현 필요)
        # 우선 기존 방식 유지
        messagebox.showinfo("음료 선택", f"'{drink_name}'이(가) 선택되었습니다.\n온도를 확인하고 '내 주문 담기'를 눌러주세요.", parent=self.root)
        
    def add_order(self):
        name = self.name_entry.get().strip()
        drink = getattr(self, 'drink_var', None)
        temperature = self.temperature_var.get()
        
        if not name:
            messagebox.showerror("오류", "주문자 이름을 입력해주세요.", parent=self.root)
            return
        if not drink:
            messagebox.showerror("오류", "음료를 먼저 선택해주세요.", parent=self.root)
            return
        
        if messagebox.askyesno("추가 요청사항", "추가 요청사항이 있나요?", parent=self.root):
            req_window = tk.Toplevel(self.root)
            req_window.title("추가 요청사항 입력")
            req_window.geometry("350x150")
            req_window.transient(self.root)
            req_window.grab_set()
            
            ttk.Label(req_window, text="추가 요청사항을 입력하세요:", padding=10).pack()
            req_entry = ttk.Entry(req_window, width=40)
            req_entry.pack(pady=5, padx=10, fill='x')
            req_entry.focus()
            
            def submit_req():
                req = req_entry.get().strip()
                self._finalize_order(name, drink, temperature, req)
                req_window.destroy()
            ttk.Button(req_window, text="확인", command=submit_req, style='Accent.TButton').pack(pady=10)
            req_window.wait_window()
        else:
            self._finalize_order(name, drink, temperature, "")

    def _finalize_order(self, name, drink, temperature, request):
        if name in self.orders:
            if not messagebox.askyesno("주문 수정", f"{name}님은 이미 주문 내역이 있습니다. 덮어쓰시겠습니까?", parent=self.root):
                return
            
            # 기존 주문 카운트 감소
            old_drink, old_temp, _ = self.orders[name]
            self.drink_counts[(old_drink, old_temp)] -= 1
            if self.drink_counts[(old_drink, old_temp)] == 0:
                del self.drink_counts[(old_drink, old_temp)]

        self.orders[name] = (drink, temperature, request)
        self.drink_counts[(drink, temperature)] += 1
        
        self.name_entry.delete(0, tk.END)
        self.drink_var = None
        
        self.update_status_display()
        messagebox.showinfo("주문 완료", f"{name}님의 주문이 추가되었습니다!\n{drink} ({temperature})", parent=self.root)
        
    def update_status_display(self):
        # 이번 UI에서는 현재 주문 현황을 최종 확인 창에서만 보여주므로 이 함수는 비워두거나
        # 별도의 상태 표시줄이 필요할 때 사용합니다.
        # 여기서는 기능 유지를 위해 코드는 남겨둡니다.
        pass

    def show_final_order(self):
        if not self.orders:
            messagebox.showinfo("알림", "주문 내역이 없습니다.", parent=self.root)
            return
            
        final_window = tk.Toplevel(self.root)
        final_window.title("📋 최종 주문 내역")
        final_window.geometry("500x600")
        final_window.configure(bg=self.COLOR_BACKGROUND)

        text_widget = tk.Text(final_window, wrap=tk.WORD, 
                              font=self.FONT_BODY, 
                              bg=self.COLOR_BACKGROUND, 
                              padx=20, pady=20, 
                              borderwidth=0,
                              highlightthickness=0)
        text_widget.pack(fill=tk.BOTH, expand=True)

        # 텍스트 스타일 태그 설정
        text_widget.tag_configure("title", font=self.FONT_TITLE, foreground=self.COLOR_PRIMARY, justify='center', spacing3=20)
        text_widget.tag_configure("header", font=self.FONT_HEADER, foreground=self.COLOR_TEXT, spacing1=15, spacing3=5)
        text_widget.tag_configure("item", font=self.FONT_BODY, spacing1=2, spacing3=2)
        text_widget.tag_configure("total", font=self.FONT_BODY_BOLD, spacing1=15)
        text_widget.tag_configure("separator", foreground=self.COLOR_BORDER, justify='center', spacing1=10, spacing3=10)

        # --- 주문 내역 텍스트 생성 ---
        text_widget.insert(tk.END, "매머드커피 최종 주문서\n", "title")
        
        # 누적 주문
        hot_orders = {k[0]: v for k, v in self.drink_counts.items() if k[1] == "HOT"}
        ice_orders = {k[0]: v for k, v in self.drink_counts.items() if k[1] == "ICE"}
        
        text_widget.insert(tk.END, "주문 요약\n", "header")
        if ice_orders:
            text_widget.insert(tk.END, "🧊 ICE 음료\n", "item")
            for drink, count in sorted(ice_orders.items()):
                text_widget.insert(tk.END, f"  • {drink}: {count}잔\n", "item")
        if hot_orders:
            text_widget.insert(tk.END, "\n🔥 HOT 음료\n", "item")
            for drink, count in sorted(hot_orders.items()):
                text_widget.insert(tk.END, f"  • {drink}: {count}잔\n", "item")

        total_drinks = sum(self.drink_counts.values())
        text_widget.insert(tk.END, f"\n총 음료: {total_drinks}잔\n", "total")
        text_widget.insert(tk.END, f"총 인원: {len(self.orders)}명\n", "total")
        text_widget.insert(tk.END, "─" * 40 + "\n", "separator")

        # 개별 주문
        text_widget.insert(tk.END, "개별 주문 내역\n", "header")
        for name, (drink, temp, req) in sorted(self.orders.items()):
            req_str = f" (요청: {req})" if req else ""
            text_widget.insert(tk.END, f"• {name}: {drink} ({temp}){req_str}\n", "item")

        text_widget.configure(state=tk.DISABLED)

    def reset_orders(self):
        if messagebox.askyesno("초기화 확인", "모든 주문 내역을 삭제하고 처음부터 다시 시작하시겠습니까?", parent=self.root):
            self.orders.clear()
            self.drink_counts.clear()
            self.name_entry.delete(0, tk.END)
            self.category_var.set('')
            self.drink_var = None
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.initial_menu_prompt = ttk.Label(self.scrollable_frame, text="음료 카테고리를 선택해주세요!", font=self.FONT_BODY, foreground=self.COLOR_SUBTEXT)
            self.initial_menu_prompt.pack(pady=50)
            messagebox.showinfo("완료", "모든 주문이 초기화되었습니다.", parent=self.root)

    def show_menu_selection(self):
        if self.name_entry.get().strip():
            self.category_var.set('') # 포커스 이동 대신 콤보박스 초기화
            # 사용자가 자연스럽게 다음 단계로 넘어가도록 유도

def main():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    root = tk.Tk()
    app = CoffeeOrderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()