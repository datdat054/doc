import numpy as np
import matplotlib.pyplot as plt

# --- Đọc file nhị phân ---
W, H = 256, 256
def read_bin_image(path: str, width=W, height=H) -> np.ndarray:
    with open(path, "rb") as f:
        arr = np.fromfile(f, dtype=np.uint8, count=width*height)
    return arr.reshape((height, width))

# Đọc ảnh gốc
img = read_bin_image("actontBinbin.sec")

# --- (1) Tạo template chữ T ---
TemplRows, TemplCols = 47, 15
template = np.zeros((TemplRows, TemplCols), dtype=np.uint8)

# hàng 11–16 full ngang
template[10:16, :] = 255
# hàng 17–37: cột 7–10
template[16:37, 6:10] = 255

# --- (2) Tính M2 (J1) ---
J1 = np.zeros_like(img, dtype=np.int32)
row_half, col_half = TemplRows//2, TemplCols//2

for row in range(row_half, H-row_half):
    for col in range(col_half, W-col_half):
        window = img[row-row_half:row+row_half+1, col-col_half:col+col_half+1]
        if window.shape == template.shape:
            J1[row, col] = np.sum(window == template)

# --- (3) Full-scale stretch J1 ---
min_val, max_val = J1.min(), J1.max()
J1_stretched = ((J1 - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# --- (4) Ngưỡng hóa J1 để tạo J2 ---
counts = np.sort(J1.ravel())[::-1]   # sắp giảm dần
tau = 678  # ngưỡng = giá trị lớn thứ 2
J2 = np.where(J1 >= tau, 255, 0).astype(np.uint8)

print(f"Threshold τ = {tau}")

# --- Hiển thị ---
plt.figure("N22DCCN019",figsize=(12, 6))

plt.subplot(1, 3, 1)
plt.imshow(img, cmap="gray")
plt.title("Ảnh gốc actontBin.bin")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(J1_stretched, cmap="gray")
plt.title("J1 = M2(i,j)")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(J2, cmap="gray")
plt.title(f"J2; τ = {tau}")
plt.axis("off")

plt.tight_layout()
plt.show()