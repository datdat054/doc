import numpy as np
import matplotlib.pyplot as plt

# --- 1. Hàm đọc file nhị phân ---
W, H = 256, 256


def read_bin_image(path: str, width=W, height=H) -> np.ndarray:
    with open(path, "rb") as f:
        arr = np.fromfile(f, dtype=np.uint8, count=width * height)
    return arr.reshape((height, width))


# --- 2. Đọc ảnh gốc ---
img = read_bin_image("johnnybin.sec")


# --- 3. Histogram Equalization ---
def histogram_equalization(image: np.ndarray):
    # Bước 1: đếm tần suất xuất hiện của các mức xám
    hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 256])

    # Bước 2: tính phân phối tích lũy (CDF)
    cdf = hist.cumsum()
    cdf_normalized = cdf * 255 / cdf[-1]  # scale về [0,255]

    # Bước 3: ánh xạ pixel theo CDF
    img_equalized = np.interp(image.flatten(), bins[:-1], cdf_normalized)
    img_equalized = img_equalized.reshape(image.shape).astype(np.uint8)

    return img_equalized, hist, cdf, cdf_normalized


# Thực hiện equalization
equalized, hist, cdf, cdf_normalized = histogram_equalization(img)

# --- 4. Vẽ kết quả ---
plt.figure("N22DCCN019",figsize=(12, 8))

# Ảnh gốc
plt.subplot(2, 2, 1)
plt.imshow(img, cmap="gray", vmin=0, vmax=255)
plt.title("Ảnh gốc (johnny.bin)")
plt.axis("off")

# Histogram ảnh gốc
plt.subplot(2, 2, 2)
plt.hist(img.ravel(), bins=256, range=(0, 255), color="black")
plt.title("Histogram ảnh gốc")

# Ảnh sau equalization
plt.subplot(2, 2, 3)
plt.imshow(equalized, cmap="gray", vmin=0, vmax=255)
plt.title("Ảnh sau Histogram Equalization")
plt.axis("off")

# Histogram ảnh sau equalization
plt.subplot(2, 2, 4)
plt.hist(equalized.ravel(), bins=256, range=(0, 255), color="black")
plt.title("Histogram sau equalization")

plt.tight_layout()
plt.show()