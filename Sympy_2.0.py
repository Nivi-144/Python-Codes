import sympy as sp
x,y=sp.symbols('x y')
expr=(x+y)**2
expanded_expr=sp.expand
sp.plot(x**2-4,(x,-5,5),title="Plot of x^2",xlabel="x",ylabel="y")
diff_expr=sp.diff(x**3*x**2+5*x+7,x)
print("Derivative of x^3+3x^2+5x+7",diff_expr)
integral_expr=sp.integrate(x**3+3*x**2+5*x+7,x)
print("Integral of x^3+3x^2+5x+7",integral_expr)