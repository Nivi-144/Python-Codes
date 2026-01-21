import sympy as sp

# Define the symbol
x = sp.symbols('x')

# Define the expression
expression = (x**2 + 2*x + 1) / (x + 1)

# Simplify the expression
simplified_expr = sp.simplify(expression)

# Display results
print("Original Expression:")
print(expression)

print("\nSimplified Expression:")
print(simplified_expr)
