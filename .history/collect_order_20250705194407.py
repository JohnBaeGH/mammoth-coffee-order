import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from collections import defaultdict

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

class CoffeeOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("☕ 매머드커피 주문 시스템 ☕")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')
        
        # 주문 데이터 저장
        self.orders = {}  # {이름: (음료, 온도)}
        self.drink_counts = defaultdict(int)  # {(음료, 온도): 개수}
        
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="☕ 매머드커피 주문 시스템 ☕", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 이름 입력 프레임
        name_frame = ttk.LabelFrame(main_frame, text="주문자 정보", padding="10")
        name_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(name_frame, text="이름:").grid(row=0, column=0, padx=(0, 5))
        self.name_entry = ttk.Entry(name_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=(0, 10))
        self.name_entry.bind('<Return>', lambda e: self.show_menu_selection())
        
        # 메뉴 선택 프레임
        self.menu_frame = ttk.LabelFrame(main_frame, text="음료 선택", padding="10")
        self.menu_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 카테고리 선택
        ttk.Label(self.menu_frame, text="카테고리:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(self.menu_frame, textvariable=self.category_var, 
                                     values=list(MENU.keys()), state="readonly", width=20)
        category_combo.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        category_combo.bind('<<ComboboxSelected>>', self.on_category_selected)
        
        # 음료 선택
        ttk.Label(self.menu_frame, text="음료:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.drink_var = tk.StringVar()
        self.drink_combo = ttk.Combobox(self.menu_frame, textvariable=self.drink_var, 
                                       state="readonly", width=20)
        self.drink_combo.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        # 온도 선택
        ttk.Label(self.menu_frame, text="온도:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.temperature_var = tk.StringVar(value="ICE")
        temp_frame = ttk.Frame(self.menu_frame)
        temp_frame.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        
        ttk.Radiobutton(temp_frame, text="ICE", variable=self.temperature_var, 
                       value="ICE").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(temp_frame, text="HOT", variable=self.temperature_var, 
                       value="HOT").pack(side=tk.LEFT)
        
        # 주문 버튼
        order_btn = ttk.Button(self.menu_frame, text="주문 추가", 
                              command=self.add_order)
        order_btn.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        # 현재 주문 현황
        self.status_frame = ttk.LabelFrame(main_frame, text="현재 주문 현황", padding="10")
        self.status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_text = tk.Text(self.status_frame, height=8, width=70)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(self.status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="주문 완료", 
                  command=self.show_final_order).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="초기화", 
                  command=self.reset_orders).pack(side=tk.LEFT)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        self.menu_frame.columnconfigure(1, weight=1)
        self.status_frame.columnconfigure(0, weight=1)
        
        # 초기 상태 업데이트
        self.update_status_display()
        
    def on_category_selected(self, event=None):
        """카테고리가 선택되었을 때 음료 목록을 업데이트합니다."""
        category = self.category_var.get()
        if category in MENU:
            self.drink_combo['values'] = MENU[category]
            self.drink_var.set('')  # 음료 선택 초기화
            
    def add_order(self):
        """주문을 추가합니다."""
        name = self.name_entry.get().strip()
        drink = self.drink_var.get()
        temperature = self.temperature_var.get()
        
        if not name:
            messagebox.showerror("오류", "이름을 입력해주세요.")
            return
            
        if not drink:
            messagebox.showerror("오류", "음료를 선택해주세요.")
            return
            
        # 주문 추가
        self.orders[name] = (drink, temperature)
        self.drink_counts[(drink, temperature)] += 1
        
        # 입력 필드 초기화
        self.name_entry.delete(0, tk.END)
        self.drink_var.set('')
        self.category_var.set('')
        
        # 상태 업데이트
        self.update_status_display()
        
        messagebox.showinfo("성공", f"{name}님의 주문이 추가되었습니다!\n{drink} ({temperature})")
        
    def update_status_display(self):
        """현재 주문 현황을 업데이트합니다."""
        self.status_text.delete(1.0, tk.END)
        
        if not self.orders:
            self.status_text.insert(tk.END, "아직 주문이 없습니다.")
            return
            
        # 개별 주문 내역
        self.status_text.insert(tk.END, "📋 개별 주문 내역:\n")
        self.status_text.insert(tk.END, "-" * 40 + "\n")
        
        for name, (drink, temp) in self.orders.items():
            self.status_text.insert(tk.END, f"• {name}: {drink} ({temp})\n")
            
        # 누적 주문 현황
        self.status_text.insert(tk.END, "\n📊 누적 주문 현황:\n")
        self.status_text.insert(tk.END, "-" * 40 + "\n")
        
        for (drink, temp), count in self.drink_counts.items():
            self.status_text.insert(tk.END, f"• {drink} ({temp}): {count}잔\n")
            
        # 총 주문 수
        total_orders = len(self.orders)
        self.status_text.insert(tk.END, f"\n총 주문자 수: {total_orders}명\n")
        
    def show_final_order(self):
        """최종 주문 내역을 매장 주문용으로 표시합니다."""
        if not self.orders:
            messagebox.showinfo("알림", "주문 내역이 없습니다.")
            return
            
        # 새 창 생성
        final_window = tk.Toplevel(self.root)
        final_window.title("📋 최종 주문 내역 (매장 주문용)")
        final_window.geometry("600x500")
        
        # 텍스트 위젯
        text_widget = tk.Text(final_window, wrap=tk.WORD, font=('Arial', 12))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(final_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # 매장 주문용 정리
        text_widget.insert(tk.END, "☕ 매머드커피 주문 내역 ☕\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        # 온도별로 정리
        hot_orders = defaultdict(int)
        ice_orders = defaultdict(int)
        
        for drink, temp in self.drink_counts.keys():
            count = self.drink_counts[(drink, temp)]
            if temp == "HOT":
                hot_orders[drink] += count
            else:
                ice_orders[drink] += count
        
        # HOT 음료
        if hot_orders:
            text_widget.insert(tk.END, "🔥 HOT 음료:\n")
            text_widget.insert(tk.END, "-" * 30 + "\n")
            for drink, count in sorted(hot_orders.items()):
                text_widget.insert(tk.END, f"• {drink} {count}잔\n")
            text_widget.insert(tk.END, "\n")
            
        # ICE 음료
        if ice_orders:
            text_widget.insert(tk.END, "🧊 ICE 음료:\n")
            text_widget.insert(tk.END, "-" * 30 + "\n")
            for drink, count in sorted(ice_orders.items()):
                text_widget.insert(tk.END, f"• {drink} {count}잔\n")
            text_widget.insert(tk.END, "\n")
            
        # 총계
        total_drinks = sum(self.drink_counts.values())
        text_widget.insert(tk.END, f"📊 총 음료 수: {total_drinks}잔\n")
        text_widget.insert(tk.END, f"👥 총 주문자 수: {len(self.orders)}명\n")
        
        # 개별 주문 내역 (참고용)
        text_widget.insert(tk.END, "\n" + "=" * 50 + "\n")
        text_widget.insert(tk.END, "📝 개별 주문 내역 (참고용):\n")
        text_widget.insert(tk.END, "-" * 30 + "\n")
        
        for name, (drink, temp) in self.orders.items():
            text_widget.insert(tk.END, f"• {name}: {drink} ({temp})\n")
            
        # 읽기 전용으로 설정
        text_widget.configure(state=tk.DISABLED)
        
    def reset_orders(self):
        """모든 주문을 초기화합니다."""
        if messagebox.askyesno("확인", "모든 주문을 초기화하시겠습니까?"):
            self.orders.clear()
            self.drink_counts.clear()
            self.update_status_display()
            
    def show_menu_selection(self):
        """이름 입력 후 메뉴 선택으로 포커스를 이동합니다."""
        if self.name_entry.get().strip():
            self.menu_frame.focus_set()

def main():
    """GUI 애플리케이션을 실행합니다."""
    root = tk.Tk()
    app = CoffeeOrderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()