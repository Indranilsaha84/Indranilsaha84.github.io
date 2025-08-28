import tkinter as tk
from tkinter import Toplevel, Listbox, Scrollbar, Button, Frame
from tkinter import ttk
import math
import ast

# A dictionary to map AST nodes to actual math functions for safe evaluation
ALLOWED_OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
    ast.USub: lambda a: -a,
}

def safe_eval(expression):
    """
    A safe replacement for eval(). It parses the expression and evaluates
    only allowed mathematical operations.
    """
    try:
        # Replace user-friendly symbols with Python operators
        expression = expression.replace('^', '**').replace('×', '*').replace('÷', '/')
        tree = ast.parse(expression, mode='eval')
    except (SyntaxError, ValueError):
        raise SyntaxError("Invalid Syntax")

    def _eval_node(node):
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num): # For older Python versions
            return node.n
        elif isinstance(node, ast.BinOp):
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            op_func = ALLOWED_OPERATORS.get(type(node.op))
            if op_func:
                return op_func(left, right)
            else:
                raise SyntaxError(f"Unsupported operator: {type(node.op)}")
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            operand = _eval_node(node.operand)
            return ALLOWED_OPERATORS[ast.USub](operand)
        else:
            raise SyntaxError("Unsupported expression")

    return _eval_node(tree)

class master:
    def __init__(self, master):
        self.master = master
        master.title("master calculator")

        # --- Color Palette ---
        self.colors = {
            "blue": "#004CFF",
            "sky_blue": "#6E7AE6",
            "red": "#FF2A00",
            "parrot_green": "#04FF00",
            "display_bg": "#FFFFFF",
            "white": "#000000", # Corrected white color for text
            "black": "#000000"
        }
        
        master.configure(bg=self.colors["blue"])

        # History data storage
        self.history_data = []
        
        # --- Configure ttk Style for Buttons ---
        style = ttk.Style()
        style.configure("TButton", 
                        padding=6, 
                        font=('Arial', 14, 'bold'),
                        borderwidth=0,
                        relief="flat")

        # Display Entry Widget
        self.display = tk.Entry(master, width=40, borderwidth=10, justify="right", 
                                font=('Arial', 20, 'bold'), 
                                bg=self.colors["display_bg"], fg=self.colors["black"])
        self.display.grid(row=0, column=0, columnspan=6, padx=10, pady=20)

        # Button Layout
        buttons = [
            ('sin', 1, 0, self.colors["blue"]), ('cos', 1, 1, self.colors["blue"]), ('tan', 1, 2, self.colors["blue"]), 
            ('log₁₀', 1, 3, self.colors["blue"]), ('ln', 1, 4, self.colors["blue"]), ('History', 1, 5, self.colors["black"]),
            
            ('7', 2, 0, self.colors["sky_blue"]), ('8', 2, 1, self.colors["sky_blue"]), ('9', 2, 2, self.colors["sky_blue"]), 
            ('÷', 2, 3, self.colors["parrot_green"]), ('xʸ', 2, 4, self.colors["blue"]), ('AC', 2, 5, self.colors["red"]),
            
            ('4', 3, 0, self.colors["sky_blue"]), ('5', 3, 1, self.colors["sky_blue"]), ('6', 3, 2, self.colors["sky_blue"]), 
            ('×', 3, 3, self.colors["parrot_green"]), ('√', 3, 4, self.colors["blue"]), ('C', 3, 5, self.colors["red"]),
            
            ('1', 4, 0, self.colors["sky_blue"]), ('2', 4, 1, self.colors["sky_blue"]), ('3', 4, 2, self.colors["sky_blue"]), 
            ('-', 4, 3, self.colors["parrot_green"]), ('(', 4, 4, self.colors["sky_blue"]), (')', 4, 5, self.colors["sky_blue"]),
            
            ('0', 5, 0, self.colors["sky_blue"]), ('.', 5, 1, self.colors["sky_blue"]), ('±', 5, 2, self.colors["sky_blue"]), 
            ('+', 5, 3, self.colors["parrot_green"]), ('=', 5, 4, self.colors["parrot_green"], 2)
        ]

        for (text, row, col, color, *span) in buttons:
            self.create_button(text, row, col, span[0] if span else 1, color)

        # Initialize display
        self.display.insert(0, "0")

    def create_button(self, text, row, col, colspan, color):
        text_color = self.colors["white"] if color in [self.colors["blue"], self.colors["red"], self.colors["parrot_green"], self.colors["black"]] else self.colors["black"]
        
        button_font = ('Freestyle script ', 14, 'bold')
        if text in ['sin', 'cos', 'tan', 'log₁₀', 'ln']:
            button_font = ('Freestyle script', 12, )

        # Use a unique style for each button to set its color
        style_name = f"{text}.TButton"
        style = ttk.Style()
        style.configure(style_name, 
                        padding=10,
                        font=button_font,
                        background=color,
                        foreground=text_color)
        style.map(style_name,
                  background=[('active', color)],
                  foreground=[('active', text_color)])

        button = ttk.Button(self.master, text=text, style=style_name,
                           command=lambda t=text: self.on_button_click(t))
        button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)
        self.master.grid_columnconfigure(col, weight=1)
        self.master.grid_rowconfigure(row, weight=1)

    def on_button_click(self, char):
        current_text = self.display.get()

        if char == 'History':
            self.show_history()
            return
        
        if char == 'AC':
            self.reset_calculator()
        elif char == 'C':
            if len(current_text) > 1:
                self.display.delete(len(current_text) - 1, tk.END)
            else:
                self.display.delete(0, tk.END)
                self.display.insert(0, "0")
        elif char == '=':
            self.calculate_result()
        elif char in "0123456789.()":
            if current_text == "0" and char != '.':
                self.display.delete(0, tk.END)
            self.display.insert(tk.END, char)
        elif char in ('+', '-', '×', '÷'):
            # Append operator, ensuring no duplicates
            if current_text and current_text[-1] not in ('+', '-', '×', '÷'):
                 self.display.insert(tk.END, char)
        elif char == 'xʸ':
            # Use ^ for power, as it's handled by safe_eval
            if current_text and current_text[-1] not in ('+', '-', '×', '÷', '^'):
                self.display.insert(tk.END, '^')
        elif char == '±':
            if current_text != "0":
                if current_text.startswith('-'):
                    self.display.delete(0)
                else:
                    self.display.insert(0, '-')
        elif char in ('sin', 'cos', 'tan', 'log₁₀', 'ln', '√'):
            self.handle_single_operand_function(char, current_text)

    def show_history(self):
        history_window = Toplevel(self.master)
        history_window.title("Calculation History")
        history_window.geometry("300x400")
        history_window.configure(bg=self.colors["blue"])

        frame = Frame(history_window, bg=self.colors["blue"])
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = Listbox(frame, yscrollcommand=scrollbar.set, bg=self.colors["display_bg"], 
                          font=('Arial', 14))
        for item in self.history_data:
            listbox.insert(tk.END, item)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        def clear_history():
            self.history_data.clear()
            listbox.delete(0, tk.END)

        clear_button = Button(history_window, text="Clear History", command=clear_history,
                              bg=self.colors["red"], fg=self.colors["white"], 
                              font=('Arial', 12, 'bold'))
        clear_button.pack(pady=5)

    def reset_calculator(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")

    def handle_single_operand_function(self, func, text):
        try:
            # This function should only operate if the display contains a valid number
            value = float(text)
            result = 0
            if func == 'sin': result = math.sin(math.radians(value))
            elif func == 'cos': result = math.cos(math.radians(value))
            elif func == 'tan': result = math.tan(math.radians(value))
            elif func == 'log₁₀': result = math.log10(value)
            elif func == 'ln': result = math.log(value)
            elif func == '√': result = math.sqrt(value)
            
            final_result_str = str(round(result, 10))
            self.display.delete(0, tk.END)
            self.display.insert(0, final_result_str)
            self.history_data.append(f"{func}({value}) = {final_result_str}")
        except (ValueError, OverflowError):
            self.display_error("Invalid Input")

    def calculate_result(self):
        expression = self.display.get()
        try:
            result = safe_eval(expression)
            final_result_str = str(round(result, 10))
            self.history_data.append(f"{expression} = {final_result_str}")
            self.display.delete(0, tk.END)
            self.display.insert(0, final_result_str)
        except ZeroDivisionError:
            self.display_error("Division by Zero")
        except Exception:
            self.display_error("Error")

    def display_error(self, message):
        self.display.delete(0, tk.END)
        self.display.insert(0, message)

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = master(root)
    root.mainloop()