import tkinter as tk
from tkinter import messagebox
import time
from types import SimpleNamespace
from functools import partial

# ============================================================================
# КОНСТАНТЫ (именованные кортежи для скорости)
# ============================================================================

_CFG = SimpleNamespace(
    # Окно
    TITLE="LED Controller",
    SIZE="320x260",
    BG="#1a1b2e",
    FG="#ffffff",
    
    # Цвета кнопок (фон, текст)
    COL_BLUE=("#2563eb", "#dbeafe"),
    COL_RED=("#dc2626", "#fee2e2"),
    COL_GREEN=("#16a34a", "#dcfce7"),
    COL_GRAY=("#4b5563", "#f3f4f6"),
    
    # Цвета элементов
    ENTRY_BG="#2d3748",
    SLIDER_BG="#374151",
    TEXT_COL="#e5e7eb",
    
    # Пины (синий, красный)
    PINS=(3, 5),
    
    # Размеры
    ENTRY_W=12,
    SLIDER_L=160,
    BTN_W=14
)

# ============================================================================
# ГЛОБАЛЬНЫЕ КОМПОНЕНТЫ (минимизация создания объектов)
# ============================================================================

# Единый стиль для меток
_label_style = {
    'bg': _CFG.BG,
    'fg': _CFG.TEXT_COL,
    'font': ('Calibri', 11)
}

# Единый стиль для полей ввода
_entry_style = {
    'width': _CFG.ENTRY_W,
    'bg': _CFG.ENTRY_BG,
    'fg': _CFG.FG,
    'insertbackground': 'white',
    'relief': 'flat',
    'font': ('Calibri', 11)
}

# Стиль для слайдера
_slider_style = {
    'from_': 0,
    'to': 100,
    'orient': tk.HORIZONTAL,
    'length': _CFG.SLIDER_L,
    'bg': _CFG.BG,
    'fg': _CFG.FG,
    'troughcolor': _CFG.SLIDER_BG,
    'highlightthickness': 0
}

# ============================================================================
# ФУНКЦИИ СОЗДАНИЯ ВИДЖЕТОВ (вместо классов)
# ============================================================================

def create_label(parent, text, **kwargs):
    """Создание метки с предустановленным стилем"""
    style = _label_style.copy()
    style.update(kwargs)
    return tk.Label(parent, text=text, **style)

def create_entry(parent, **kwargs):
    """Создание поля ввода"""
    style = _entry_style.copy()
    style.update(kwargs)
    widget = tk.Entry(parent, **style)
    widget.insert(0, "1.0")
    return widget

def create_slider(parent, **kwargs):
    """Создание слайдера"""
    style = _slider_style.copy()
    style.update(kwargs)
    widget = tk.Scale(parent, **style)
    widget.set(50)
    return widget

def create_button(parent, text, colors, command, width=_CFG.BTN_W):
    """Создание кнопки"""
    bg, fg = colors
    return tk.Button(
        parent,
        text=text,
        font=('Calibri', 10, 'bold'),
        bg=bg,
        fg=fg,
        relief='flat',
        width=width,
        cursor='hand2',
        command=command
    )

# ============================================================================
# БИЗНЕС-ЛОГИКА
# ============================================================================

def control_led(pin, duration, intensity):
    """Управление светодиодом (эмуляция)"""
    # board.digital[pin].write(intensity / 100.0)
    # time.sleep(duration)
    # board.digital[pin].write(0)
    time.sleep(duration)  # Эмуляция задержки
    print(f"PIN {pin}: {duration}s, {intensity}%")

# ============================================================================
# ОБРАБОТЧИКИ СОБЫТИЙ (замыкания для скорости)
# ============================================================================

def make_led_handler(pin_idx, time_widget, slider_widget, button_widget):
    """Создание обработчика для светодиода"""
    def handler():
        button_widget.config(state=tk.DISABLED)
        button_widget.update_idletasks()
        
        try:
            duration = float(time_widget.get())
            if duration <= 0:
                raise ValueError("Длительность должна быть > 0")
                
            brightness = slider_widget.get()
            control_led(_CFG.PINS[pin_idx], duration, brightness)
            
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            button_widget.config(state=tk.NORMAL)
    
    return handler

def show_help():
    """Показать справку"""
    messagebox.showinfo(
        "Справка",
        "LED Controller v2.0\n\n"
        "Управление светодиодами Arduino\n"
        "Оптимизированная версия"
    )

# ============================================================================
# ПОСТРОЕНИЕ ИНТЕРФЕЙСА (одна функция для минимизации накладных расходов)
# ============================================================================

def build_gui():
    """Создание всего интерфейса"""
    root = tk.Tk()
    root.title(_CFG.TITLE)
    root.geometry(_CFG.SIZE)
    root.configure(bg=_CFG.BG)
    root.resizable(False, False)
    
    # Заголовок
    tk.Label(
        root,
        text="LED CONTROLLER",
        font=('Arial', 20, 'bold'),
        fg=_CFG.FG,
        bg=_CFG.BG
    ).pack(pady=10)
    
    # Контейнер для элементов управления
    controls = tk.Frame(root, bg=_CFG.BG)
    controls.pack(pady=5, padx=15, fill='x')
    
    # Поле ввода времени
    create_label(controls, "Время (сек):").grid(row=0, column=0, sticky='w', pady=5)
    time_entry = create_entry(controls)
    time_entry.grid(row=0, column=1, sticky='e', pady=5)
    
    # Слайдер яркости
    create_label(controls, "Яркость (%):").grid(row=1, column=0, sticky='w', pady=5)
    brightness_slider = create_slider(controls)
    brightness_slider.grid(row=1, column=1, sticky='e', pady=5)
    
    # Контейнер для кнопок светодиодов
    led_buttons = tk.Frame(root, bg=_CFG.BG)
    led_buttons.pack(pady=10)
    
    # Кнопки светодиодов
    blue_btn = create_button(
        led_buttons,
        "СИНИЙ LED",
        _CFG.COL_BLUE,
        None,  # Заполнится позже
        16
    )
    blue_btn.grid(row=0, column=0, padx=3)
    
    red_btn = create_button(
        led_buttons,
        "КРАСНЫЙ LED",
        _CFG.COL_RED,
        None,  # Заполнится позже
        16
    )
    red_btn.grid(row=0, column=1, padx=3)
    
    # Привязка обработчиков (после создания всех виджетов)
    blue_btn.config(command=make_led_handler(0, time_entry, brightness_slider, blue_btn))
    red_btn.config(command=make_led_handler(1, time_entry, brightness_slider, red_btn))
    
    # Контейнер для служебных кнопок
    util_buttons = tk.Frame(root, bg=_CFG.BG)
    util_buttons.pack(pady=5)
    
    # Служебные кнопки
    create_button(
        util_buttons,
        "СПРАВКА",
        _CFG.COL_GREEN,
        show_help
    ).pack(side='left', padx=3)
    
    create_button(
        util_buttons,
        "ВЫХОД",
        _CFG.COL_GRAY,
        root.quit
    ).pack(side='left', padx=3)
    
    # Настройка весов колонок для выравнивания
    controls.grid_columnconfigure(0, weight=1)
    controls.grid_columnconfigure(1, weight=1)
    
    return root

# ============================================================================
# ТОЧКА ВХОДА (минималистичная)
# ============================================================================

def main():
    """Запуск приложения"""
    app = build_gui()
    app.mainloop()

if __name__ == "__main__":
    main()
