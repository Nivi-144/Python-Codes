import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)/np.cos(x)
plt.plot(x, y, label='Tan(x)', color='orange')
plt.title('Tan Graph')
plt.xlabel('x values')
plt.ylabel('tan(x)')
plt.legend()
plt.grid(True)
plt.show()
