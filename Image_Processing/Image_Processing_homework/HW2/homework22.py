import numpy as np
import matplotlib.pyplot as plt

# Kích thước ảnh
W, H = 256, 256

def read_bin_image(path: str, width: int = W, height: int = H) -> np.ndarray:
    with open(path, "rb") as f:
        arr = np.fromfile(f, dtype=np.uint8, count=width*height)
    return arr.reshape((height, width))

# (1) Đọc ảnh gốc
lady = read_bin_image("ladybin.sec", W, H)

# (2) Histogram ảnh gốc
plt.figure("N22DCCN019",figsize=(12, 5))

plt.subplot(2, 2, 1)
plt.imshow(lady, cmap="gray", vmin=0, vmax=255)
plt.title("Ảnh gốc")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.hist(lady.ravel(), bins=256, range=(0, 255), color='black')
plt.title("Histogram ảnh gốc")

# (3) Kéo giãn tương phản toàn thang
f_min, f_max = lady.min(), lady.max()
stretched = ((lady - f_min) / (f_max - f_min) * 255).astype(np.uint8)

# (4) Histogram ảnh sau khi kéo giãn
plt.subplot(2, 2, 3)
plt.imshow(stretched, cmap="gray", vmin=0, vmax=255)
plt.title("Ảnh sau kéo giãn")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.hist(stretched.ravel(), bins=256, range=(0, 255), color='black')
plt.title("Histogram sau kéo giãn")

plt.tight_layout()
plt.show()