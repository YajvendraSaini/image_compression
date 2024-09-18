import cv2
import numpy as np
from PIL import Image
import io

def compress_image(input_path, max_size_kb=10):
    # Read the image in color
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)

    # Resize to a smaller resolution if needed
    img = cv2.resize(img, (320, 240))

    # Start with quality 95 and decrease until size is under 10KB
    quality = 95
    while True:
        # Encode image to JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', img, encode_param)

        # Check size
        size_kb = len(encimg) / 1024
        if size_kb <= max_size_kb:
            break

        quality -= 5
        if quality < 5:
            raise ValueError("Cannot compress image to under 10KB")

    # Convert compressed image to bytes
    image_bytes = encimg.tobytes()

    return image_bytes, quality

# Usage
input_image = "input_image.jpg"  # Update this path if you renamed the image
compressed_image, final_quality = compress_image(input_image)
print(f"Compressed image size: {len(compressed_image) / 1024:.2f} KB")
print(f"Final JPEG quality: {final_quality}")

# Save compressed image (for testing)
with open("compressed_image.jpg", "wb") as f:
    f.write(compressed_image)

def upscale_image(image_bytes, target_size=(1280, 960)):
    # Reconstruct image from bytes
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Upscale
    upscaled = cv2.resize(img, target_size, interpolation=cv2.INTER_CUBIC)

    return upscaled

# Usage
upscaled_image = upscale_image(compressed_image)
cv2.imwrite("upscaled_image.jpg", upscaled_image)
