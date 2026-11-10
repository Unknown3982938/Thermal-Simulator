"""Scientific Calculator (Tkinter) for Thermo Lab 3D.

Run:  python scientific_calculator.py      (Python 3.8+, no extra packages)
Type with the keyboard (Enter = evaluate, Esc = clear) or click the keys.
"""
import tkinter as tk

from calc_engine import CalcError, Calculator

BG, FIELD, ACCENT, ERROR = "#0b1226", "#16213f", "#ffb347", "#ff6b6b"
COLORS = {"num": ("#1f2d52", "#e9f0ff"), "fn": ("#2a3d68", "#cfe0ff"),
          "op": ("#3b5286", "#ffffff"), "eq": ("#ff6a2a", "#ffffff")}

# (label, action, style) - same layout as the in-browser panel
KEYS = [
    ("Deg", "mode", "fn"), ("sin", "sin(", "fn"), ("cos", "cos(", "fn"), ("tan", "tan(", "fn"), ("AC", "ac", "op"),
    ("sin⁻¹", "asin(", "fn"), ("cos⁻¹", "acos(", "fn"), ("tan⁻¹", "atan(", "fn"), ("(", "(", "fn"), (")", ")", "fn"),
    ("ln", "ln(", "fn"), ("log", "log(", "fn"), ("√", "sqrt(", "fn"), ("x²", "^2", "fn"), ("xʸ", "^", "fn"),
    ("π", "pi", "fn"), ("e", "e", "fn"), ("n!", "!", "fn"), ("1/x", "1/(", "fn"), ("⌫", "del", "op"),
    ("7", "7", "num"), ("8", "8", "num"), ("9", "9", "num"), ("÷", "/", "op"), ("Ans", "ans", "fn"),
    ("4", "4", "num"), ("5", "5", "num"), ("6", "6", "num"), ("×", "*", "op"), ("EXP", "*10^(", "fn"),
    ("1", "1", "num"), ("2", "2", "num"), ("3", "3", "num"), ("−", "-", "op"), ("abs", "abs(", "fn"),
    ("0", "0", "num"), (".", ".", "num"), ("±", "neg", "fn"), ("+", "+", "op"), ("=", "eq", "eq"),
]


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Thermo Lab 3D - Scientific Calculator")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.calc = Calculator()

        self.entry = tk.Entry(self, font=("Consolas", 16), bg=FIELD, fg="white", insertbackground="white",
                              relief="flat", justify="right")
        self.entry.grid(row=0, column=0, columnspan=5, sticky="ew", padx=10, pady=(10, 2), ipady=8)
        self.result = tk.Label(self, text="0", anchor="e", font=("Consolas", 24, "bold"), bg=BG, fg=ACCENT)
        self.result.grid(row=1, column=0, columnspan=5, sticky="ew", padx=12)
        self.history = tk.Listbox(self, height=3, bg=FIELD, fg="#9db0d3", relief="flat", highlightthickness=0,
                                  font=("Consolas", 10), activestyle="none")
        self.history.grid(row=2, column=0, columnspan=5, sticky="ew", padx=10, pady=6)
        self.history.bind("<Double-Button-1>", self.recall)

        for i, (label, action, style) in enumerate(KEYS):
            bg, fg = COLORS[style]
            btn = tk.Button(self, text=label, width=6, height=2, bg=bg, fg=fg, relief="flat", bd=0,
                            activebackground=ACCENT, font=("Segoe UI", 11, "bold"),
                            command=lambda a=action: self.press(a))
            btn.grid(row=3 + i // 5, column=i % 5, padx=3, pady=3, sticky="nsew")
            if action == "mode":
                self.mode_btn = btn
        tk.Label(self, text="Double-click history to reuse  |  Enter = evaluate, Esc = clear",
                 bg=BG, fg="#6f82a8", font=("Segoe UI", 8)).grid(row=12, column=0, columnspan=5, pady=(2, 8))

        self.bind("<Return>", lambda _e: self.press("eq"))
        self.bind("<Escape>", lambda _e: self.press("ac"))
        self.entry.focus_set()

    def insert(self, text):
        self.entry.insert(self.entry.index(tk.INSERT), text)
        self.entry.focus_set()

    def recall(self, _event):
        picked = self.history.curselection()
        if picked:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.calc.history[picked[0]][0])

    def press(self, action):
        if action == "ac":
            self.entry.delete(0, tk.END)
            self.result.config(text="0", fg=ACCENT)
        elif action == "del":
            pos = self.entry.index(tk.INSERT)
            if pos > 0:
                self.entry.delete(pos - 1, pos)
        elif action == "mode":
            self.calc.angle_mode = "rad" if self.calc.angle_mode == "deg" else "deg"
            self.mode_btn.config(text="Deg" if self.calc.angle_mode == "deg" else "Rad")
        elif action == "neg":
            text = self.entry.get()
            wrapped = text.startswith("-(") and text.endswith(")")
            self.entry.delete(0, tk.END)
            self.entry.insert(0, text[2:-1] if wrapped else "-(" + text + ")")
        elif action == "eq":
            expr = self.entry.get()
            try:
                self.result.config(text=self.calc.calculate(expr), fg=ACCENT)
                self.history.insert(0, f"{expr} = {self.calc.history[-1][1]}")
                self.calc.history.insert(0, self.calc.history.pop())   # keep order matching the listbox
            except CalcError as err:
                self.result.config(text=str(err), fg=ERROR)
        else:
            self.insert(action)


if __name__ == "__main__":
    CalculatorApp().mainloop()
