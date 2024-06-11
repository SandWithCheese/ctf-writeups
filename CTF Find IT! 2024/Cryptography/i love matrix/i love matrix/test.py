import numpy as np

# Create a matrix with complex eigenvalues and eigenvectors
A = np.array([[1, -2], [2, 1]])

# Calculate eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# Reconstruct the original matrix using eigenvalues and eigenvectors
reconstructed_A = np.dot(
    np.dot(eigenvectors, np.diag(eigenvalues)), np.linalg.inv(eigenvectors)
)

print("Original matrix:")
print(A)

print("\nReconstructed matrix:")
print(reconstructed_A)

print("\nEigenvalues:")
print(eigenvalues)

print("\nEigenvectors:")
print(eigenvectors)

print("Arrays equal:", np.allclose(A, reconstructed_A))
