import sys

def calc(expr):
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expr):
        raise ValueError("Invalid characters in expression")
    return eval(expr)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(calc(" ".join(sys.argv[1:])))
    else:
        print("Usage: python calc.py <expression>")
        print("Example: python calc.py '(2 + 3) * 4'")
