"""Scientific calculator engine for Thermo Lab 3D.

Shared by the Tkinter desktop app (scientific_calculator.py) and by the
in-browser calculator panel (calc_toggle.js), which runs this same file
through Pyodide. No eval(): input is parsed with ast and only whitelisted
operations and functions can run.
"""
import ast
import json
import math
import operator
import re


class CalcError(Exception):
    """A user-facing calculator error (bad syntax, domain error, ...)."""


SYMBOLS = {"×": "*", "÷": "/", "−": "-", "^": "**", "π": "pi", "√": "sqrt", "²": "**2", "³": "**3"}
BINARY = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
          ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
NAMES = r"(?:pi\b|tau\b|ans\b|exp\(|[a-df-z]\w*\(|e\b(?!\s*[+\-]?\d)|\()"
IMPLICIT = re.compile(r"(?<=[\d)])\s*(?=" + NAMES + ")")
IMPLICIT_AFTER_PAREN = re.compile(r"(?<=\))\s*(?=\d)")
SQRT_NUMBER = re.compile(r"sqrt\s*(\d+(?:\.\d+)?)")


def _int(x):
    if float(x) != int(x) or x < 0:
        raise CalcError("Needs a non-negative whole number")
    return int(x)


def _fact(x):
    n = _int(x)
    if n > 170:
        raise CalcError("Factorial too large (max 170)")
    return math.factorial(n)


def _factorials(expr):
    """Rewrite postfix n! and (expr)! into fact(...)."""
    while "!" in expr:
        i = expr.index("!")
        j = i
        if i > 0 and expr[i - 1] == ")":
            depth = 0
            j = i - 1
            while j >= 0:
                depth += (expr[j] == ")") - (expr[j] == "(")
                if depth == 0:
                    break
                j -= 1
            if j < 0:
                raise CalcError("Unbalanced parentheses")
        else:
            while j > 0 and (expr[j - 1].isdigit() or expr[j - 1] == "."):
                j -= 1
            if j == i:
                raise CalcError("Misplaced !")
        expr = expr[:j] + "fact(" + expr[j:i] + ")" + expr[i + 1:]
    return expr


def prepare(expr):
    for symbol, plain in SYMBOLS.items():
        expr = expr.replace(symbol, plain)
    expr = _factorials(expr.lower().strip())
    expr = SQRT_NUMBER.sub(r"sqrt(\1)", expr)
    expr = IMPLICIT.sub("*", expr)
    return IMPLICIT_AFTER_PAREN.sub("*", expr)


def format_number(x):
    if isinstance(x, int) and abs(x) < 10 ** 15:
        return str(x)
    try:
        x = float(x)
    except OverflowError:
        raise CalcError("Number too large")
    if not math.isfinite(x):
        raise CalcError("Number too large")
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return f"{x:.12g}"


class Calculator:
    def __init__(self, angle_mode="deg"):
        self.angle_mode = angle_mode      # "deg" or "rad"
        self.ans = 0
        self.history = []                 # [(expression, result_text), ...]

    # ----- functions & constants -----
    def _functions(self):
        deg = self.angle_mode == "deg"
        to_rad = (lambda x: math.radians(x)) if deg else (lambda x: x)
        from_rad = (lambda x: math.degrees(x)) if deg else (lambda x: x)
        clean = lambda v: 0.0 if abs(v) < 1e-15 else v

        def tan(x):
            a = to_rad(x)
            if abs(math.cos(a)) < 1e-12:
                raise CalcError("tan is undefined here")
            return clean(math.tan(a))

        return {
            "sin": lambda x: clean(math.sin(to_rad(x))), "cos": lambda x: clean(math.cos(to_rad(x))), "tan": tan,
            "asin": lambda x: from_rad(math.asin(x)), "acos": lambda x: from_rad(math.acos(x)),
            "atan": lambda x: from_rad(math.atan(x)),
            "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
            "ln": math.log, "log": lambda x, base=10: math.log(x, base), "log2": math.log2,
            "sqrt": math.sqrt, "cbrt": lambda x: math.copysign(abs(x) ** (1 / 3), x),
            "exp": math.exp, "abs": abs, "fact": _fact,
            "ncr": lambda n, r: math.comb(_int(n), _int(r)), "npr": lambda n, r: math.perm(_int(n), _int(r)),
            "floor": math.floor, "ceil": math.ceil, "round": round,
        }

    def _constants(self):
        return {"pi": math.pi, "e": math.e, "tau": math.tau, "ans": self.ans}

    # ----- evaluation -----
    def _eval(self, node, funcs, consts):
        if isinstance(node, ast.Expression):
            return self._eval(node.body, funcs, consts)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id in consts:
            return consts[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = self._eval(node.operand, funcs, consts)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and type(node.op) in BINARY:
            left = self._eval(node.left, funcs, consts)
            right = self._eval(node.right, funcs, consts)
            if isinstance(node.op, ast.Pow) and abs(right) > 10000:
                raise CalcError("Exponent too large")
            try:
                return BINARY[type(node.op)](left, right)
            except ZeroDivisionError:
                raise CalcError("Division by zero")
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in funcs and not node.keywords):
            return funcs[node.func.id](*[self._eval(a, funcs, consts) for a in node.args])
        raise CalcError("Unsupported expression")

    def evaluate(self, expr):
        if not expr or not expr.strip():
            raise CalcError("Enter an expression")
        try:
            tree = ast.parse(prepare(expr), mode="eval")
            result = self._eval(tree, self._functions(), self._constants())
        except CalcError:
            raise
        except SyntaxError:
            raise CalcError("Syntax error")
        except OverflowError:
            raise CalcError("Number too large")
        except (ValueError, TypeError):
            raise CalcError("Math domain error")
        if isinstance(result, complex):
            raise CalcError("Result is not a real number")
        return result

    def calculate(self, expr):
        """Evaluate, store Ans + history, and return the formatted result text."""
        result = self.evaluate(expr)
        text = format_number(result)
        self.ans = result
        self.history.append((expr, text))
        return text


# ----- entry point used by the browser panel (Pyodide) -----
_web = Calculator()


def web_eval(expr, mode="deg"):
    _web.angle_mode = "rad" if mode == "rad" else "deg"
    try:
        return json.dumps({"ok": True, "text": _web.calculate(expr)})
    except CalcError as err:
        return json.dumps({"ok": False, "text": str(err)})
