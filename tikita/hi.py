import cv2
import matplotlib.pyplot as plt

# Đọc ảnh (đưa đường dẫn ảnh của bạn vào)
image = cv2.imread("brain.jpg", cv2.IMREAD_GRAYSCALE)

# Tính histogram với OpenCV
hist = cv2.calcHist([image], [0], None, [256], [0, 256])

# Vẽ histogram
plt.figure(figsize=(8,5))
plt.title("Gray Level Histogram")
plt.xlabel("Gray level (0-255)")
plt.ylabel("Pixel count")
plt.plot(hist, color='black')
plt.xlim([0, 256])
plt.show()