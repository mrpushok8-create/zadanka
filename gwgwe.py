import tkinter as tk
from tkinter import messagebox
import time
from dataclasses import dataclass
from typing import Callable

# ============================================================================
# КОНСТАНТЫ И КОНФИГУРАЦИЯ
# ============================================================================

@dataclass
class UIConfig:
    """Конфигурация пользовательского интерфейса"""
    TITLE = "Управление светодиодами"
    SIZE = "350x280"
    BG_COLOR = "#1a1b2e"
    
    # Цвета кнопок (фон, текст)
    BLUE_BTN = ("#2563eb", "#dbeafe")
    RED_BTN = ("#dc2626", "#fee2e2")
    GREEN_BTN = ("#16a34a", "#dcfce7")
    GRAY_BTN = ("#4b5563", "#f3f4f6")
    
    # Шрифты
    FONT_HEADER = ("Arial", 22, "bold")
    FONT_LABEL = ("Calibri", 11)
    FONT_BUTTON = ("Calibri", 10, "bold")
    
    # Размеры и отступы
    BTN_PADDING = (15, 8)
    ENTRY_WIDTH = 15
    SLIDER_LENGTH = 180

# ============================================================================
# МОДЕЛЬ ДАННЫХ И ЛОГИКА
# ============================================================================

class LEDModel:
    """Модель для управления светодиодами"""
    
    # Пины Arduino (закомментировано для тестирования)
    PINS = {"blue": 3, "red": 5}
    
    @staticmethod
    def control_led(pin: int, duration: float, intensity: int) -> None:
        """
        Управление светодиодом (эмуляция).
        
        Args:
            pin: Номер пина Arduino
            duration: Время свечения в секундах
            intensity: Яркость 0-100%
        """
        brightness = intensity / 100.0
        # Реальный код для Arduino:
        # board.digital[pin].write(brightness)
        # time.sleep(duration)
        # board.digital[pin].write(0)
        
        print(f"LED {pin}: {duration} сек, {intensity}%")
        time.sleep(duration)  # Эмуляция задержки

# ============================================================================
# КОМПОНЕНТЫ ИНТЕРФЕЙСА
# ============================================================================

class LabeledControl(tk.Frame):
    """Виджет с меткой и элементом управления"""
    
    def __init__(self, parent, label_text: str, control_widget, **kwargs):
        super().__init__(parent, bg=UIConfig.BG_COLOR)
        self.label = self._create_label(label_text)
        self.control = control_widget(self, **kwargs)
        self._pack_components()
    
    def _create_label(self, text: str) -> tk.Label:
        return tk.Label(
            self,
            text=text,
            font=UIConfig.FONT_LABEL,
            fg="#e5e7eb",
            bg=UIConfig.BG_COLOR
        )
    
    def _pack_components(self) -> None:
        self.label.pack(side='left')
        self.control.pack(side='right')

class LEDButton(tk.Button):
    """Специализированная кнопка для управления светодиодами"""
    
    def __init__(self, parent, text: str, colors: tuple, command: Callable):
        bg_color, fg_color = colors
        super().__init__(
            parent,
            text=text,
            font=UIConfig.FONT_BUTTON,
            bg=bg_color,
            fg=fg_color,
            relief="flat",
            padx=UIConfig.BTN_PADDING[0],
            pady=UIConfig.BTN_PADDING[1],
            cursor="hand2",
            command=command
        )

# ============================================================================
# ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ
# ============================================================================

class LEDControlApp:
    """Основной класс приложения"""
    
    def __init__(self):
        self.root = self._create_window()
        self.model = LEDModel()
        self._setup_variables()
        self._create_ui()
    
    def _create_window(self) -> tk.Tk:
        """Создание и настройка главного окна"""
        root = tk.Tk()
        root.title(UIConfig.TITLE)
        root.geometry(UIConfig.SIZE)
        root.configure(bg=UIConfig.BG_COLOR)
        root.resizable(False, False)
        return root
    
    def _setup_variables(self) -> None:
        """Инициализация переменных"""
        self.active_buttons = set()
    
    def _create_ui(self) -> None:
        """Создание интерфейса"""
        self._create_header()
        self._create_control_panel()
        self._create_button_panel()
    
    def _create_header(self) -> None:
        """Создание заголовка"""
        header = tk.Label(
            self.root,
            text="УПРАВЛЕНИЕ СВЕТОДИОДАМИ",
            font=UIConfig.FONT_HEADER,
            fg="#ffffff",
            bg=UIConfig.BG_COLOR
        )
        header.pack(pady=15)
    
    def _create_control_panel(self) -> None:
        """Создание панели управления"""
        panel = tk.Frame(self.root, bg=UIConfig.BG_COLOR)
        panel.pack(pady=10, padx=20, fill='x')
        
        # Поле ввода времени
        self.time_entry = tk.Entry(
            panel,
            width=UIConfig.ENTRY_WIDTH,
            font=UIConfig.FONT_LABEL,
            bg="#2d3748",
            fg="#ffffff",
            insertbackground="white",
            relief="flat"
        )
        self.time_entry.insert(0, "1.0")
        
        time_control = LabeledControl(
            panel,
            "Длительность (сек):",
            lambda p: self.time_entry
        )
        time_control.pack(fill='x', pady=5)
        
        # Слайдер яркости
        self.brightness_var = tk.IntVar(value=50)
        self.brightness_slider = tk.Scale(
            panel,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=UIConfig.SLIDER_LENGTH,
            variable=self.brightness_var,
            bg=UIConfig.BG_COLOR,
            fg="#ffffff",
            troughcolor="#374151",
            highlightthickness=0
        )
        
        brightness_control = LabeledControl(
            panel,
            "Уровень яркости:",
            lambda p: self.brightness_slider
        )
        brightness_control.pack(fill='x', pady=10)
    
    def _create_button_panel(self) -> None:
        """Создание панели кнопок"""
        button_frame = tk.Frame(self.root, bg=UIConfig.BG_COLOR)
        button_frame.pack(pady=20, padx=20)
        
        # Кнопки светодиодов
        self.blue_btn = LEDButton(
            button_frame,
            "СИНИЙ СВЕТОДИОД",
            UIConfig.BLUE_BTN,
            lambda: self._activate_led("blue")
        )
        self.blue_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.red_btn = LEDButton(
            button_frame,
            "КРАСНЫЙ СВЕТОДИОД",
            UIConfig.RED_BTN,
            lambda: self._activate_led("red")
        )
        self.red_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Панель служебных кнопок
        service_frame = tk.Frame(self.root, bg=UIConfig.BG_COLOR)
        service_frame.pack(pady=10)
        
        LEDButton(
            service_frame,
            "СПРАВКА",
            UIConfig.GREEN_BTN,
            self._show_help
        ).pack(side='left', padx=5)
        
        LEDButton(
            service_frame,
            "ВЫХОД",
            UIConfig.GRAY_BTN,
            self.root.quit
        ).pack(side='left', padx=5)
    
    # ============================================================================
    # ОБРАБОТЧИКИ СОБЫТИЙ
    # ============================================================================
    
    def _activate_led(self, color: str) -> None:
        """Активация светодиода"""
        button_map = {
            "blue": (self.blue_btn, LEDModel.PINS["blue"]),
            "red": (self.red_btn, LEDModel.PINS["red"])
        }
        
        if color not in button_map:
            return
        
        button, pin = button_map[color]
        
        # Блокировка кнопки на время выполнения
        self._toggle_button(button, False)
        
        try:
            duration = self._get_duration()
            brightness = self.brightness_var.get()
            
            # Вызов модели для управления светодиодом
            self.model.control_led(pin, duration, brightness)
            
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            self._toggle_button(button, True)
    
    def _get_duration(self) -> float:
        """Получение и валидация длительности"""
        try:
            value = float(self.time_entry.get())
            if value <= 0:
                raise ValueError("Длительность должна быть больше 0")
            return value
        except ValueError:
            raise ValueError("Введите корректное число для времени")
    
    def _toggle_button(self, button: tk.Button, enabled: bool) -> None:
        """Изменение состояния кнопки"""
        state = tk.NORMAL if enabled else tk.DISABLED
        button.config(state=state)
        self.root.update_idletasks()
    
    def _show_help(self) -> None:
        """Показать справочную информацию"""
        help_text = (
            "Программа управления светодиодами v1.0\n\n"
            "Функциональные возможности:\n"
            "• Управление синим и красным светодиодами\n"
            "• Регулировка длительности свечения\n"
            "• Плавная регулировка яркости\n\n"
            "Разработка: 2026 год"
        )
        messagebox.showinfo("Справка", help_text)
    
    def run(self) -> None:
        """Запуск основного цикла приложения"""
        self.root.mainloop()

# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================

def main():
    """Основная функция приложения"""
    app = LEDControlApp()
    app.run()

if __name__ == "__main__":
    main()