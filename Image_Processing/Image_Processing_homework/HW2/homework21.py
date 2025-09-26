import numpy as np
import matplotlib.pyplot as plt

# Step (a) - Load raw image
filename = "Mammogram.bin"
img = np.fromfile(filename, dtype=np.uint8)
img = img.reshape((256, 256))

# Display original
plt.imshow(img, cmap='gray')
plt.title("Original Mammogram")
plt.show()

# Plot histogram
plt.hist(img.ravel(), bins=256, range=[0,256])
plt.title("Histogram")
plt.show()

# Thresholding (manual or Otsu’s method)
threshold = 40  # <-- adjust if needed
binary = np.where(img > threshold, 255, 0).astype(np.uint8)

plt.imshow(binary, cmap='gray')
plt.title("Binary Image (Thresholding)")
plt.show()

# Step (b) - Approximate contour extraction
contour = np.zeros_like(binary)

# 8-neighborhood offsets
neighbors = [(-1,-1), (-1,0), (-1,1), 
             (0,-1),          (0,1), 
             (1,-1),  (1,0),  (1,1)]

rows, cols = binary.shape
for i in range(1, rows-1):
    for j in range(1, cols-1):
        if binary[i,j] == 255:
            # Check if any neighbor is background
            if any(binary[i+di, j+dj] == 0 for di,dj in neighbors):
                contour[i,j] = 255

plt.imshow(contour, cmap='gray')
plt.title("Contour Image")
plt.show()
