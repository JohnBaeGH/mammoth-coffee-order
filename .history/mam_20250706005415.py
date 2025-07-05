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
        # 창 높이를 늘려 모든 버튼이 보이도록 수정
        self.root.geometry("420x800")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        # 데이터
        self.orders = {}
        self.drink_counts = defaultdict(int)
        
        # UI 상태
        self.selected_drink = None
        self.selected_drink_button = None
        
        # 이미지 캐시
        self.image_cache = {}
        self.photo_cache = {}

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # 기본 설정
        style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_BODY, borderwidth=0, focusthickness=0)
        
        # 프레임
        style.configure('TFrame', background=BG_COLOR)
        style.configure('Card.TFrame', background=FRAME_COLOR, relief='solid', borderwidth=1, bordercolor='#E9ECEF')

        # 라벨
        style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure('Card.TLabel', background=FRAME_COLOR)
        style.configure('Header.TLabel', font=FONT_H1, background=FRAME_COLOR)
        
        # 버튼
        style.configure('TButton', font=FONT_BUTTON, padding=10, relief='flat', background='#E9ECEF')
        style.map('TButton', background=[('active', '#DEE2E6')])
                  
        # Accent 버튼 (주요 동작 버튼)
        style.configure('Accent.TButton', foreground=FRAME_COLOR, background=ACCENT_COLOR)
        style.map('Accent.TButton',
                  background=[('active', '#0095CC'), ('disabled', DISABLED_COLOR)],
                  foreground=[('disabled', '#6C757D')])

        # 메뉴 버튼
        style.configure('Menu.TButton', background=FRAME_COLOR, font=(FONT_FAMILY, 10),
                        width=12, padding=5, relief='flat', borderwidth=1, bordercolor='#E9ECEF')
        style.map('Menu.TButton', background=[('active', '#F1F3F5')])

        # 선택된 메뉴 버튼
        style.configure('Selected.Menu.TButton', background='#E3F2FD',
                        relief='solid', borderwidth=2, bordercolor=ACCENT_COLOR)

        # 입력 필드
        style.configure('TEntry', fieldbackground=FRAME_COLOR, foreground=TEXT_COLOR, 
                        insertcolor=TEXT_COLOR, borderwidth=1, relief='solid', padding=8, bordercolor='#CED4DA')
        
        # 콤보박스
        style.configure('TCombobox', fieldbackground=FRAME_COLOR, background=FRAME_COLOR, 
                        arrowcolor=TEXT_COLOR, foreground=TEXT_COLOR, padding=8, relief='solid', bordercolor='#CED4DA')
        self.root.option_add('TCombobox*Listbox.background', FRAME_COLOR)
        self.root.option_add('TCombobox*Listbox.foreground', TEXT_COLOR)
        self.root.option_add('TCombobox*Listbox.selectBackground', ACCENT_COLOR)
        self.root.option_add('TCombobox*Listbox.selectForeground', FRAME_COLOR)
        
        # 라디오 버튼
        style.configure('TRadiobutton', background=FRAME_COLOR, font=FONT_BODY)
        style.map('TRadiobutton',
                  indicatorcolor=[('selected', ACCENT_COLOR), ('!selected', '#ADB5BD')])
                  
        # 레이블 프레임
        style.configure('TLabelFrame', background=BG_COLOR, bordercolor='#DEE2E6')
        style.configure('TLabelFrame.Label', background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_H1)

        # 스크롤바
        style.configure('Vertical.TScrollbar', troughcolor=BG_COLOR, background='#DEE2E6', arrowcolor=TEXT_COLOR)
        style.map('Vertical.TScrollbar', background=[('active', '#ADB5BD')])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 1. 헤더
        try:
            img_path = os.path.join("images", "mammoth_main.png")
            main_img = Image.open(img_path).resize((380, 100), Image.Resampling.LANCZOS)
            self.main_photo = ImageTk.PhotoImage(main_img)
            header_label = tk.Label(main_frame, image=self.main_photo, bg=BG_COLOR)
        except Exception:
            header_label = ttk.Label(main_frame, text="Mammoth Coffee", font=FONT_TITLE, anchor='center')
        header_label.pack(fill=tk.X, pady=(0, 20))

        # 2. 주문자 정보
        name_frame = ttk.LabelFrame(main_frame, text="주문자 이름", padding=15)
        name_frame.pack(fill=tk.X, pady=5)
        self.name_entry = ttk.Entry(name_frame, font=FONT_BODY, width=20)
        self.name_entry.pack(fill=tk.X, expand=True)

        # 3. 메뉴 선택
        menu_select_frame = ttk.LabelFrame(main_frame, text="음료 선택", padding=15)
        menu_select_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 3-1. 카테고리 & 온도
        cat_temp_frame = tk.Frame(menu_select_frame, background=FRAME_COLOR)
        cat_temp_frame.pack(fill=tk.X, pady=(0, 15))
        cat_temp_frame.columnconfigure(0, weight=1)
        cat_temp_frame.columnconfigure(1, weight=1)

        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(cat_temp_frame, textvariable=self.category_var,
                                     values=list(MENU.keys()), state="readonly", font=FONT_BODY)
        category_combo.set("카테고리 선택")
        category_combo.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)

        self.temperature_var = tk.StringVar(value="ICE")
        temp_frame = tk.Frame(cat_temp_frame, background=FRAME_COLOR)
        temp_frame.grid(row=0, column=1, sticky='ew', padx=(5, 0))
        ttk.Radiobutton(temp_frame, text="ICE", variable=self.temperature_var, value="ICE").pack(side=tk.LEFT, expand=True)
        ttk.Radiobutton(temp_frame, text="HOT", variable=self.temperature_var, value="HOT").pack(side=tk.LEFT, expand=True)
        
        # 3-2. 메뉴 이미지 스크롤 영역
        canvas_frame = tk.Frame(menu_select_frame, background=FRAME_COLOR)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(canvas_frame, bg=FRAME_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview, style='Vertical.TScrollbar')
        self.scrollable_frame = tk.Frame(self.canvas, background=FRAME_COLOR)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5, padx=(0,5))
        
        # 4. 주문 추가 버튼
        self.add_order_btn = ttk.Button(main_frame, text="내 주문 완료", style='Accent.TButton', command=self.add_order, state='disabled')
        self.add_order_btn.pack(fill=tk.X, pady=10, ipady=5)

        # 5. 현재 주문 현황
        status_frame = ttk.LabelFrame(main_frame, text="현재 주문 현황", padding=15)
        status_frame.pack(fill=tk.X, pady=5)
        self.status_text = tk.Text(status_frame, height=5, font=(FONT_FAMILY, 10), 
                                   bg='#F1F3F5', fg=TEXT_COLOR, relief='flat', highlightthickness=0,
                                   borderwidth=1, wrap='word')
        self.status_text.pack(fill=tk.X, expand=True)
        self.update_status_display()
        
        # 6. 하단 버튼 (초기화, 전체 주문)
        bottom_frame = tk.Frame(main_frame, background=FRAME_COLOR)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        
        # '모든 인원 주문 완료' 버튼 항상 보이도록 추가
        self.all_order_btn = ttk.Button(bottom_frame, text="모든 인원 주문 완료", command=self.show_final_order)
        self.all_order_btn.grid(row=0, column=1, sticky='ew', padx=(5,0))

        # 초기화 버튼
        self.reset_btn = ttk.Button(bottom_frame, text="초기화", command=self.reset_orders)
        self.reset_btn.grid(row=0, column=0, sticky='ew', padx=(0,5))

    # --- 나머지 메소드는 이전 '세련된 GUI' 버전과 대부분 동일합니다 ---
    # (단, 팝업창 배경색 등 일부 디자인 요소만 수정)
    def on_category_selected(self, event=None):
        category = self.category_var.get()
        if not category or category == "카테고리 선택": return
        self.select_drink(None, None) 
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        loading_label = ttk.Label(self.scrollable_frame, text="메뉴를 불러오는 중...", font=FONT_BODY, style='Card.TLabel')
        loading_label.pack(pady=20)
        self.root.update_idletasks()
        threading.Thread(target=self.load_images_threaded, args=(category, loading_label), daemon=True).start()

    def load_images_threaded(self, category, loading_label):
        drinks = MENU.get(category, [])
        menu_widgets = []
        for drink in drinks:
            if drink in self.photo_cache:
                img = self.photo_cache[drink]
            else:
                pil_img = self.get_menu_image_from_source(drink)
                img = ImageTk.PhotoImage(pil_img)
                self.photo_cache[drink] = img
            btn = ttk.Button(self.scrollable_frame, text=drink, image=img, compound=tk.TOP, style='Menu.TButton')
            btn.image = img
            btn['command'] = lambda b=btn, d=drink: self.select_drink(b, d)
            menu_widgets.append(btn)
        self.root.after(0, self.populate_menu_grid, menu_widgets, loading_label)
        
    def get_menu_image_from_source(self, menu_name):
        local_path = os.path.join("images", f"{menu_name}.png")
        if os.path.exists(local_path):
            return Image.open(local_path).resize((90, 90), Image.Resampling.LANCZOS)
        if menu_name in self.image_cache: return self.image_cache[menu_name]
        try:
            url = f"https://source.unsplash.com/150x150/?{menu_name.split(' ')[0]}+drink,beverage"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            pil_img = Image.open(BytesIO(response.content)).resize((90, 90), Image.Resampling.LANCZOS)
        except (requests.RequestException, IOError):
            pil_img = Image.new('RGB', (90, 90), color=FRAME_COLOR)
        self.image_cache[menu_name] = pil_img
        return pil_img
        
    def populate_menu_grid(self, widgets, loading_label):
        loading_label.destroy()
        max_cols = 3
        for i, widget in enumerate(widgets):
            row, col = divmod(i, max_cols)
            widget.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
    def select_drink(self, button_widget, drink_name):
        if self.selected_drink_button:
            self.selected_drink_button.configure(style='Menu.TButton')
        self.selected_drink = drink_name
        self.selected_drink_button = button_widget
        if self.selected_drink_button:
            self.selected_drink_button.configure(style='Selected.Menu.TButton')
            self.add_order_btn.config(state='normal')
        else:
            self.add_order_btn.config(state='disabled')

    def add_order(self):
        name = self.name_entry.get().strip()
        drink = self.selected_drink
        temperature = self.temperature_var.get()
        if not name:
            messagebox.showwarning("입력 오류", "주문자 이름을 입력해주세요.", parent=self.root)
            return
        if not drink:
            messagebox.showwarning("선택 오류", "음료를 선택해주세요.", parent=self.root)
            return
        
        if messagebox.askyesno("추가 요청", "추가 요청사항이 있습니까?", parent=self.root):
            req_window = tk.Toplevel(self.root)
            req_window.title("추가 요청사항")
            req_window.geometry("300x150")
            req_window.configure(bg=BG_COLOR)
            ttk.Label(req_window, text="요청사항을 입력하세요:").pack(pady=10)
            req_entry = ttk.Entry(req_window, width=40)
            req_entry.pack(pady=5, padx=10, fill=tk.X)
            def submit_req():
                req = req_entry.get().strip()
                self._finalize_order(name, drink, temperature, req)
                req_window.destroy()
            ttk.Button(req_window, text="확인", command=submit_req, style='Accent.TButton').pack(pady=10)
            req_window.transient(self.root)
            req_window.grab_set()
            self.root.wait_window(req_window)
        else:
            self._finalize_order(name, drink, temperature, "")

    def _finalize_order(self, name, drink, temperature, request):
        self.orders[name] = (drink, temperature, request)
        self.drink_counts[(drink, temperature)] += 1
        self.name_entry.delete(0, tk.END)
        self.select_drink(None, None)
        self.category_var.set("카테고리 선택")
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        self.update_status_display()
        messagebox.showinfo("주문 완료", f"{name}님의 주문이 추가되었습니다: {drink} ({temperature})", parent=self.root)

    def update_status_display(self):
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        if not self.orders:
            self.status_text.insert(tk.END, "아직 주문이 없습니다.")
        else:
            self.status_text.insert(tk.END, "📊 누적 주문 현황\n")
            sorted_counts = sorted(self.drink_counts.items(), key=lambda item: item[1], reverse=True)
            for (drink, temp), count in sorted_counts:
                self.status_text.insert(tk.END, f"  • {drink} ({temp}) : {count}잔\n")
            self.status_text.insert(tk.END, f"\n총 주문자: {len(self.orders)}명")
        self.status_text.config(state='disabled')

    def show_final_order(self):
        if not self.orders:
            messagebox.showinfo("알림", "주문 내역이 없습니다.", parent=self.root)
            return

        final_window = tk.Toplevel(self.root)
        final_window.title("최종 주문 내역")
        final_window.geometry("500x600")
        final_window.configure(bg=BG_COLOR)

        text_widget = tk.Text(final_window, wrap=tk.WORD, font=FONT_BODY,
                              bg=FRAME_COLOR, fg=TEXT_COLOR, relief='flat', padx=15, pady=15)
        text_widget.pack(fill=tk.BOTH, expand=True)

        final_text = "☕ 매머드커피 최종 주문서 ☕\n" + "=" * 40 + "\n\n"
        summary = defaultdict(int)
        for (drink, temp), count in self.drink_counts.items():
            summary[f"{drink} ({temp})"] += count
        if summary:
            final_text += "📋 주문 요약\n" + "-" * 40 + "\n"
            for item, count in sorted(summary.items()):
                final_text += f" • {item}: {count}잔\n"
            final_text += "\n"
        total_drinks = sum(self.drink_counts.values())
        final_text += f"📊 총 음료 수: {total_drinks}잔\n"
        final_text += f"👥 총 주문자 수: {len(self.orders)}명\n\n" + "=" * 40 + "\n\n"
        final_text += "📝 개인별 상세 주문\n" + "-" * 40 + "\n"
        for name, (drink, temp, req) in sorted(self.orders.items()):
            req_str = f" (요청: {req})" if req else ""
            final_text += f" • {name}: {drink} ({temp}){req_str}\n"

        text_widget.insert(tk.END, final_text)
        text_widget.configure(state='disabled')

    def reset_orders(self):
        if messagebox.askyesno("초기화 확인", "모든 주문 내역을 삭제하고 초기화하시겠습니까?", parent=self.root):
            self.orders.clear()
            self.drink_counts.clear()
            self.select_drink(None, None)
            self.update_status_display()
            self.name_entry.delete(0, tk.END)
            self.category_var.set("카테고리 선택")
            for widget in self.scrollable_frame.winfo_children(): widget.destroy()
            messagebox.showinfo("완료", "모든 데이터가 초기화되었습니다.", parent=self.root)

if __name__ == "__main__":
    app_root = tk.Tk()
    app = CoffeeOrderApp(app_root)
    app_root.mainloop()