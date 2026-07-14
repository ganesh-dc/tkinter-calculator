import tkinter as tk
from tkinter import font
import math

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator Pro")
        self.root.geometry("500x750")
        self.root.resizable(False, False)
        
        # Variable to store expression
        self.expression = ""
        self.history = []
        
        # Color scheme - Modern Dark Theme
        self.bg_color = "#1e1e1e"
        self.display_bg = "#2d2d2d"
        self.display_fg = "#00ff41"
        self.button_bg = "#3a3a3a"
        self.button_hover = "#4a4a4a"
        self.operator_bg = "#ff6b35"
        self.operator_hover = "#ff8557"
        self.equal_bg = "#4CAF50"
        self.equal_hover = "#66bb6a"
        
        self.root.configure(bg=self.bg_color)
        
        # Create title
        self.create_title()
        
        # Create display
        self.create_display()
        
        # Create history panel
        self.create_history_panel()
        
        # Create scientific buttons
        self.create_scientific_buttons()
        
        # Create main calculator buttons
        self.create_main_buttons()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
    
    def create_title(self):
        """Create title bar"""
        title_frame = tk.Frame(self.root, bg=self.operator_bg)
        title_frame.pack(fill="x", padx=0, pady=0)
        
        title_label = tk.Label(
            title_frame,
            text="🧮 Advanced Calculator Pro",
            font=("Arial", 18, "bold"),
            bg=self.operator_bg,
            fg="white"
        )
        title_label.pack(pady=10)
    
    def create_display(self):
        """Create the display screen"""
        display_frame = tk.Frame(self.root, bg=self.bg_color)
        display_frame.pack(pady=15, padx=15, fill="both")
        
        # Input display
        self.display = tk.Entry(
            display_frame,
            font=("Arial", 28, "bold"),
            justify=tk.RIGHT,
            bd=0,
            bg=self.display_bg,
            fg=self.display_fg,
            relief=tk.FLAT
        )
        self.display.pack(fill="both", ipady=20)
        
        # Result display
        self.result_display = tk.Entry(
            display_frame,
            font=("Arial", 16),
            justify=tk.RIGHT,
            bd=0,
            bg=self.display_bg,
            fg="#888888",
            relief=tk.FLAT
        )
        self.result_display.pack(fill="both", ipady=10, pady=(5, 0))
    
    def create_history_panel(self):
        """Create history panel"""
        history_frame = tk.LabelFrame(
            self.root,
            text="History",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg="white",
            bd=1
        )
        history_frame.pack(padx=15, pady=5, fill="x")
        
        # History listbox
        self.history_listbox = tk.Listbox(
            history_frame,
            height=3,
            font=("Arial", 9),
            bg=self.display_bg,
            fg=self.display_fg,
            bd=0
        )
        self.history_listbox.pack(fill="both", padx=5, pady=5)
        self.history_listbox.bind('<Button-1>', self.load_from_history)
    
    def create_scientific_buttons(self):
        """Create scientific function buttons"""
        sci_frame = tk.Frame(self.root, bg=self.bg_color)
        sci_frame.pack(padx=15, pady=5, fill="x")
        
        scientific_buttons = [
            ("sin", lambda: self.scientific_operation("sin")),
            ("cos", lambda: self.scientific_operation("cos")),
            ("tan", lambda: self.scientific_operation("tan")),
            ("log", lambda: self.scientific_operation("log")),
            ("ln", lambda: self.scientific_operation("ln")),
            ("π", lambda: self.add_to_expression(str(math.pi))),
            ("e", lambda: self.add_to_expression(str(math.e))),
            ("!", lambda: self.scientific_operation("!")),
        ]
        
        for btn_text, cmd in scientific_buttons:
            btn = tk.Button(
                sci_frame,
                text=btn_text,
                font=("Arial", 11, "bold"),
                bg="#5a4a8a",
                fg="white",
                relief=tk.FLAT,
                bd=0,
                command=cmd,
                padx=8,
                pady=8
            )
            btn.pack(side=tk.LEFT, fill="both", expand=True, padx=2, pady=2)
    
    def create_main_buttons(self):
        """Create main calculator buttons"""
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(padx=15, pady=10, fill="both", expand=True)
        
        # Button layout - organized like professional calculator
        buttons = [
            ["C", "←", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", "^"],
        ]
        
        for row in buttons:
            button_row = tk.Frame(buttons_frame, bg=self.bg_color)
            button_row.pack(fill="both", expand=True, pady=3)
            
            for btn_text in row:
                self.create_button(button_row, btn_text)
    
    def create_button(self, parent, text):
        """Create individual button with hover effect"""
        # Determine button type and colors
        if text == "=":
            bg_color = self.equal_bg
            fg_color = "white"
            btn_type = "equal"
        elif text in ["/", "*", "-", "+", "^"]:
            bg_color = self.operator_bg
            fg_color = "white"
            btn_type = "operator"
        elif text in ["C", "←"]:
            bg_color = "#e74c3c"
            fg_color = "white"
            btn_type = "clear"
        elif text == "%":
            bg_color = self.operator_bg
            fg_color = "white"
            btn_type = "operator"
        else:
            bg_color = self.button_bg
            fg_color = "white"
            btn_type = "number"
        
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 16, "bold"),
            bg=bg_color,
            fg=fg_color,
            relief=tk.FLAT,
            bd=0,
            command=lambda: self.on_button_click(text),
            activebackground=self.button_hover,
            activeforeground=fg_color,
            padx=15,
            pady=15
        )
        button.pack(side=tk.LEFT, fill="both", expand=True, padx=2, pady=2)
    
    def add_to_expression(self, value):
        """Add value to expression"""
        self.expression += str(value)
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)
        self.update_result_preview()
    
    def on_button_click(self, char):
        """Handle button clicks"""
        if char == "C":
            # Clear everything
            self.expression = ""
            self.display.delete(0, tk.END)
            self.result_display.delete(0, tk.END)
        
        elif char == "←":
            # Delete last character
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)
            self.update_result_preview()
        
        elif char == "=":
            # Calculate result
            self.calculate_result()
        
        elif char == "^":
            # Power operation
            self.expression += "**"
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)
            self.update_result_preview()
        
        else:
            # Add character to expression
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)
            self.update_result_preview()
    
    def scientific_operation(self, operation):
        """Handle scientific operations"""
        try:
            if not self.expression:
                return
            
            value = float(self.expression)
            
            if operation == "sin":
                result = math.sin(math.radians(value))
            elif operation == "cos":
                result = math.cos(math.radians(value))
            elif operation == "tan":
                result = math.tan(math.radians(value))
            elif operation == "log":
                result = math.log10(value)
            elif operation == "ln":
                result = math.log(value)
            elif operation == "!":
                result = math.factorial(int(value))
            
            self.expression = str(round(result, 10))
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)
            self.result_display.delete(0, tk.END)
            
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")
            self.expression = ""
    
    def update_result_preview(self):
        """Show live preview of result"""
        try:
            if self.expression:
                result = eval(self.expression.replace("^", "**"))
                self.result_display.delete(0, tk.END)
                self.result_display.insert(tk.END, f"= {round(result, 8)}")
            else:
                self.result_display.delete(0, tk.END)
        except:
            self.result_display.delete(0, tk.END)
    
    def calculate_result(self):
        """Calculate and store result"""
        try:
            if not self.expression:
                return
            
            result = eval(self.expression.replace("^", "**"))
            result = round(result, 10)
            
            # Add to history
            history_item = f"{self.expression} = {result}"
            self.history.append(history_item)
            self.history_listbox.insert(0, history_item)
            
            # Keep only last 10 items
            if len(self.history) > 10:
                self.history.pop()
                self.history_listbox.delete(10, tk.END)
            
            # Update display
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.result_display.delete(0, tk.END)
            self.expression = str(result)
            
        except ZeroDivisionError:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Cannot divide by 0")
            self.expression = ""
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")
            self.expression = ""
    
    def load_from_history(self, event):
        """Load calculation from history"""
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            # Extract the expression part (before =)
            expr = item.split(" = ")[0]
            self.expression = expr
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, expr)
            self.update_result_preview()
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        char = event.char
        
        # Handle number and operator keys
        if char in "0123456789+-*/.":
            self.on_button_click(char)
        elif char == "=":
            self.calculate_result()
        elif event.keysym == "BackSpace":
            self.on_button_click("←")
        elif event.keysym == "Delete":
            self.on_button_click("C")
        elif char == "^":
            self.on_button_click("^")
        elif char == "%":
            self.on_button_click("%")

def main():
    root = tk.Tk()
    calculator = AdvancedCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()