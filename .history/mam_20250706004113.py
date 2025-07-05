import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from collections import defaultdict
import requests
from io import BytesIO
import threading

# --- 데이터 ---
# 매머드커피 공식 웹사이트 메뉴 데이터
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

# --- 디자인 설정 ---
BG_COLOR = "#2E2E2E"
FRAME_COLOR = "#3E3E3E"
TEXT_COLOR = "#F0F0F0"
ACCENT_COLOR = "#FFC107"  # 노란색 계열 포인트 컬러
FONT_FAMILY = "맑은 고딕"
FONT_TITLE = (FONT_FAMILY, 20, "bold")
FONT_H1 = (FONT_FAMILY, 16, "bold")
FONT_BODY = (FONT_FAMILY, 11)
FONT_BUTTON = (FONT_FAMILY, 12, "bold")

class CoffeeOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mammoth Coffee Order System")
        self.root.geometry("420x750")
        self.root.configure(bg=BG_COLOR)
        # 창 크기 조절 불가
        self.root.resizable(False, False)

        # 데이터
        self.orders = {}
        self.drink_counts = defaultdict(int)
        
        # UI 상태
        self.selected_drink = None
        self.selected_drink_button = None
        
        # 이미지 캐시
        self.image_cache = {} # PIL Image 객체 캐시
        self.photo_cache = {} # ImageTk.PhotoImage 객체 캐시

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """UI에 사용될 ttk 위젯 스타일을 설정합니다."""
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # 기본 설정
        style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=FONT_BODY, borderwidth=0)
        
        # 프레임
        style.configure('TFrame', background=FRAME_COLOR)
        
        # 라벨
        style.configure('TLabel', background=FRAME_COLOR, foreground=TEXT_COLOR)
        style.configure('Title.TLabel', background=BG_COLOR, font=FONT_TITLE)
        style.configure('Header.TLabel', background=FRAME_COLOR, font=FONT_H1)
        
        # 버튼
        style.configure('TButton', font=FONT_BUTTON, padding=10)
        style.map('TButton',
                  background=[('active', '#555555')],
                  foreground=[('active', TEXT_COLOR)])
                  
        # Accent 버튼 (주요 동작 버튼)
        style.configure('Accent.TButton', foreground='#1E1E1E', background=ACCENT_COLOR)
        style.map('Accent.TButton',
                  background=[('active', '#FFD54F'), ('disabled', '#787878')],
                  foreground=[('disabled', '#A0A0A0')])

        # 메뉴 버튼
        style.configure('Menu.TButton', background=FRAME_COLOR, font=(FONT_FAMILY, 10),
                        width=12, padding=5, relief='flat')
        style.map('Menu.TButton',
                  background=[('active', '#5A5A5A')])

        # 선택된 메뉴 버튼
        style.configure('Selected.Menu.TButton', background='#5A5A5A',
                        relief='solid', borderwidth=2, bordercolor=ACCENT_COLOR)


        # 입력 필드
        style.configure('TEntry', fieldbackground='#5A5A5A', foreground=TEXT_COLOR, 
                        insertcolor=TEXT_COLOR, borderwidth=1, padding=5)
        
        # 콤보박스
        style.configure('TCombobox', fieldbackground='#5A5A5A', background='#5A5A5A', 
                        arrowcolor=TEXT_COLOR, foreground=TEXT_COLOR, padding=5)
        self.root.option_add('TCombobox*Listbox.background', '#5A5A5A')
        self.root.option_add('TCombobox*Listbox.foreground', TEXT_COLOR)
        self.root.option_add('TCombobox*Listbox.selectBackground', ACCENT_COLOR)
        self.root.option_add('TCombobox*Listbox.selectForeground', BG_COLOR)
        
        # 라디오 버튼
        style.configure('TRadiobutton', background=FRAME_COLOR, font=FONT_BODY)
        style.map('TRadiobutton',
                  background=[('active', FRAME_COLOR)],
                  indicatorcolor=[('selected', ACCENT_COLOR), ('!selected', '#888888')])
                  
        # 레이블 프레임
        style.configure('TLabelFrame', background=FRAME_COLOR, bordercolor='#5A5A5A')
        style.configure('TLabelFrame.Label', background=FRAME_COLOR, foreground=TEXT_COLOR, font=FONT_BODY)

        # 스크롤바
        style.configure('Vertical.TScrollbar', troughcolor=FRAME_COLOR, background='#5A5A5A', arrowcolor=TEXT_COLOR)
        style.map('Vertical.TScrollbar', background=[('active', '#6A6A6A')])


    def create_widgets(self):
        """메인 위젯들을 생성하고 배치합니다."""
        main_frame = ttk.Frame(self.root, padding=15, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 1. 헤더
        try:
            img_path = os.path.join("images", "mammoth_main.png")
            main_img = Image.open(img_path).resize((380, 100), Image.Resampling.LANCZOS)
            self.main_photo = ImageTk.PhotoImage(main_img)
            header_label = tk.Label(main_frame, image=self.main_photo, bg=FRAME_COLOR)
        except Exception:
            header_label = ttk.Label(main_frame, text="MAMMOTH COFFEE", style='Title.TLabel', anchor='center')
        header_label.pack(fill=tk.X, pady=(0, 20))

        # 2. 주문자 정보
        name_frame = ttk.LabelFrame(main_frame, text="주문자 이름", padding=10)
        name_frame.pack(fill=tk.X, pady=5)
        self.name_entry = ttk.Entry(name_frame, font=FONT_BODY, width=20)
        self.name_entry.pack(fill=tk.X, expand=True)

        # 3. 메뉴 선택
        menu_select_frame = ttk.LabelFrame(main_frame, text="메뉴 선택", padding=10)
        menu_select_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 3-1. 카테고리 & 온도
        cat_temp_frame = ttk.Frame(menu_select_frame, style='TFrame')
        cat_temp_frame.pack(fill=tk.X, pady=(0, 10))
        cat_temp_frame.columnconfigure(0, weight=1)
        cat_temp_frame.columnconfigure(1, weight=1)

        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(cat_temp_frame, textvariable=self.category_var,
                                     values=list(MENU.keys()), state="readonly", font=FONT_BODY)
        category_combo.set("카테고리 선택")
        category_combo.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)

        self.temperature_var = tk.StringVar(value="ICE")
        temp_frame = ttk.Frame(cat_temp_frame, style='TFrame')
        temp_frame.grid(row=0, column=1, sticky='ew', padx=(5, 0))
        ttk.Radiobutton(temp_frame, text="ICE", variable=self.temperature_var, value="ICE").pack(side=tk.LEFT, expand=True)
        ttk.Radiobutton(temp_frame, text="HOT", variable=self.temperature_var, value="HOT").pack(side=tk.LEFT, expand=True)
        
        # 3-2. 메뉴 이미지 스크롤 영역
        self.canvas = tk.Canvas(menu_select_frame, bg=FRAME_COLOR, highlightthickness=0, height=200)
        scrollbar = ttk.Scrollbar(menu_select_frame, orient="vertical", command=self.canvas.yview, style='Vertical.TScrollbar')
        self.scrollable_frame = ttk.Frame(self.canvas, style='TFrame')
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 4. 주문 추가 버튼
        self.add_order_btn = ttk.Button(main_frame, text="내 주문 추가하기", style='Accent.TButton', command=self.add_order, state='disabled')
        self.add_order_btn.pack(fill=tk.X, pady=10, ipady=5)

        # 5. 주문 현황
        status_frame = ttk.LabelFrame(main_frame, text="현재 주문 현황", padding=(10, 5))
        status_frame.pack(fill=tk.X, pady=5)
        self.status_text = tk.Text(status_frame, height=6, width=40, font=(FONT_FAMILY, 10), 
                                   bg='#2A2A2A', fg=TEXT_COLOR, relief='flat', highlightthickness=0)
        self.status_text.pack(fill=tk.X)
        self.update_status_display()
        
        # 6. 하단 버튼
        bottom_frame = ttk.Frame(main_frame, style='TFrame')
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.columnconfigure(1, weight=1)
        
        ttk.Button(bottom_frame, text="초기화", command=self.reset_orders).grid(row=0, column=0, sticky='ew', padx=(0,5))
        ttk.Button(bottom_frame, text="전체 주문 완료", command=self.show_final_order).grid(row=0, column=1, sticky='ew', padx=(5,0))

    def on_category_selected(self, event=None):
        """카테고리 선택 시, 해당 메뉴 이미지를 스레드로 로드합니다."""
        category = self.category_var.get()
        if not category or category == "카테고리 선택":
            return
        
        # 이전 선택 초기화
        self.select_drink(None, None) 
        
        # 메뉴 표시 영역 초기화
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # 로딩 메시지 표시
        loading_label = ttk.Label(self.scrollable_frame, text="메뉴를 불러오는 중...", font=FONT_BODY, style='TLabel')
        loading_label.pack(pady=20)
        self.root.update_idletasks() # UI 업데이트 강제

        # 스레드에서 이미지 로딩 시작
        threading.Thread(target=self.load_images_threaded, args=(category, loading_label), daemon=True).start()

    def load_images_threaded(self, category, loading_label):
        """백그라운드 스레드에서 메뉴 이미지를 로드하고 GUI에 표시합니다."""
        drinks = MENU.get(category, [])
        menu_widgets = []
        
        for drink in drinks:
            # 이미지 로드 (로컬 -> 웹 시뮬레이션)
            if drink in self.photo_cache:
                img = self.photo_cache[drink]
            else:
                pil_img = self.get_menu_image_from_source(drink)
                img = ImageTk.PhotoImage(pil_img)
                self.photo_cache[drink] = img # PhotoImage 캐싱

            # 메뉴 버튼 생성
            btn = ttk.Button(self.scrollable_frame, text=drink, image=img, compound=tk.TOP,
                             style='Menu.TButton')
            btn.image = img # 참조 유지
            btn['command'] = lambda b=btn, d=drink: self.select_drink(b, d)
            menu_widgets.append(btn)
        
        # 로딩이 끝나면 메인 스레드에서 위젯 배치
        self.root.after(0, self.populate_menu_grid, menu_widgets, loading_label)
        
    def get_menu_image_from_source(self, menu_name):
        """로컬 파일이나 웹에서 메뉴 이미지를 가져옵니다."""
        # 1. 로컬 이미지 확인
        local_path = os.path.join("images", f"{menu_name}.png")
        if os.path.exists(local_path):
            return Image.open(local_path).resize((90, 90), Image.Resampling.LANCZOS)
        
        # 2. 캐시 확인
        if menu_name in self.image_cache:
            return self.image_cache[menu_name]
            
        # 3. 웹에서 이미지 가져오기 (예: Placeholder 사용)
        try:
            # 실제로는 크롤링이나 API를 통해 이미지 URL을 가져와야 함
            # 여기서는 Unsplash의 검색 기능을 이용한 예시 URL
            url = f"https://source.unsplash.com/150x150/?{menu_name.split(' ')[0]}+drink"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            pil_img = Image.open(BytesIO(response.content)).resize((90, 90), Image.Resampling.LANCZOS)
        except (requests.RequestException, IOError):
            # 실패 시 기본 이미지 생성
            pil_img = Image.new('RGB', (90, 90), color='#5A5A5A')
            # 여기에 기본 아이콘을 그릴 수도 있음 (PIL.ImageDraw)
        
        self.image_cache[menu_name] = pil_img # PIL Image 캐싱
        return pil_img
        
    def populate_menu_grid(self, widgets, loading_label):
        """메인 스레드에서 메뉴 버튼들을 그리드에 배치합니다."""
        loading_label.destroy() # 로딩 메시지 제거
        
        max_cols = 3
        for i, widget in enumerate(widgets):
            row = i // max_cols
            col = i % max_cols
            widget.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
    def select_drink(self, button_widget, drink_name):
        """음료를 선택하고 시각적 피드백을 줍니다."""
        # 이전에 선택된 버튼이 있다면 스타일 초기화
        if self.selected_drink_button:
            self.selected_drink_button.configure(style='Menu.TButton')
            
        self.selected_drink = drink_name
        self.selected_drink_button = button_widget
        
        if self.selected_drink_button:
            # 새로 선택된 버튼에 'Selected' 스타일 적용
            self.selected_drink_button.configure(style='Selected.Menu.TButton')
            self.add_order_btn.config(state='normal')
        else:
            # 선택 해제 시
            self.add_order_btn.config(state='disabled')

    def add_order(self):
        """사용자 주문을 리스트에 추가합니다."""
        name = self.name_entry.get().strip()
        drink = self.selected_drink
        temperature = self.temperature_var.get()
        
        if not name:
            messagebox.showwarning("입력 오류", "주문자 이름을 입력해주세요.", parent=self.root)
            return
        if not drink:
            messagebox.showwarning("선택 오류", "음료를 선택해주세요.", parent=self.root)
            return
        
        # 추가 요청사항 팝업 (기존 로직 유지)
        if messagebox.askyesno("추가 요청", "추가 요청사항이 있습니까?", parent=self.root):
            req_window = tk.Toplevel(self.root)
            req_window.title("추가 요청사항")
            req_window.geometry("300x150")
            req_window.configure(bg=BG_COLOR)
            ttk.Label(req_window, text="요청사항을 입력하세요:", background=BG_COLOR).pack(pady=10)
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
        """주문 정보를 저장하고 UI를 초기화합니다."""
        self.orders[name] = (drink, temperature, request)
        self.drink_counts[(drink, temperature)] += 1
        
        # UI 초기화
        self.name_entry.delete(0, tk.END)
        self.select_drink(None, None) # 선택 해제
        self.category_var.set("카테고리 선택")
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.update_status_display()
        messagebox.showinfo("주문 완료", f"{name}님의 주문이 추가되었습니다: {drink} ({temperature})", parent=self.root)

    def update_status_display(self):
        """현재 주문 현황 텍스트 박스를 업데이트합니다."""
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        
        if not self.orders:
            self.status_text.insert(tk.END, "아직 주문이 없습니다.")
        else:
            # 누적 주문 현황
            self.status_text.insert(tk.END, "📊 누적 주문 현황\n")
            sorted_counts = sorted(self.drink_counts.items(), key=lambda item: item[1], reverse=True)
            for (drink, temp), count in sorted_counts:
                self.status_text.insert(tk.END, f"  • {drink} ({temp}) : {count}잔\n")
            
            self.status_text.insert(tk.END, f"\n총 주문자: {len(self.orders)}명")

        self.status_text.config(state='disabled')

    def show_final_order(self):
        """최종 주문 내역을 새 창에 표시합니다."""
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

        # 내용 생성
        final_text = "☕ 매머드커피 최종 주문서 ☕\n"
        final_text += "=" * 40 + "\n\n"

        summary = defaultdict(int)
        for (drink, temp), count in self.drink_counts.items():
            key = f"{drink} ({temp})"
            summary[key] += count

        if summary:
            final_text += "📋 주문 요약\n"
            final_text += "-" * 40 + "\n"
            for item, count in sorted(summary.items()):
                final_text += f" • {item}: {count}잔\n"
            final_text += "\n"

        total_drinks = sum(self.drink_counts.values())
        final_text += f"📊 총 음료 수: {total_drinks}잔\n"
        final_text += f"👥 총 주문자 수: {len(self.orders)}명\n\n"
        final_text += "=" * 40 + "\n\n"

        final_text += "📝 개인별 상세 주문\n"
        final_text += "-" * 40 + "\n"
        for name, (drink, temp, req) in sorted(self.orders.items()):
            req_str = f" (요청: {req})" if req else ""
            final_text += f" • {name}: {drink} ({temp}){req_str}\n"

        text_widget.insert(tk.END, final_text)
        text_widget.configure(state='disabled')

    def reset_orders(self):
        """모든 주문 내역을 초기화합니다."""
        if messagebox.askyesno("초기화 확인", "모든 주문 내역을 삭제하고 초기화하시겠습니까?", parent=self.root):
            self.orders.clear()
            self.drink_counts.clear()
            self.select_drink(None, None)
            self.update_status_display()
            self.name_entry.delete(0, tk.END)
            self.category_var.set("카테고리 선택")
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            messagebox.showinfo("완료", "모든 데이터가 초기화되었습니다.", parent=self.root)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = CoffeeOrderApp(app_root)
    app_root.mainloop()