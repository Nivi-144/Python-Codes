import sympy as sp
x,y=sp.symbols('x y')
expr=(x+y)**2
expanded_expr=sp.expand
print("Expanded Expression:",expanded_expr)
factored_expr=sp.factor(expr)
print("Factored Expresion:",factored_expr)
simplified_expr=sp.simplify((x**2+2*x*y)/(x+y))
print("Simplified Expression :",simplified_expr)
equation=sp.Eq(x**2+2*8,0)
solution=sp.solve(equation,x)
print("Solutions for the equation:",solution)