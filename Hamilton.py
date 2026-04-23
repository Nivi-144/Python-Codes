import numpy as np
H=np.array([[1,0.5],[0.5,2])
print("Hamiltonian Matrix:")
print(H)
eigenvalues,eigenvectors=np.linal.eig(H)
print("\nEigenvalues:")
print(eigenvvalues)
print("\nEigenvectors:")
print(eigenvectors)
