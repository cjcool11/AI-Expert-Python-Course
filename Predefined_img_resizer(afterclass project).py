import cv2

sizes = {
    "small": (320, 240),
    "medium": (640, 480),
    "large": (1280, 720)
}

image_path = "input.jpg"
image = cv2.imread(image_path)

if image is None:
    raise ValueError("Image not found")

for label, (w, h) in sizes.items():
    resized = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
    cv2.imshow(f"{label} {w}x{h}", resized)
    cv2.imwrite(f"output_{label}.jpg", resized)

cv2.waitKey(0)
cv2.destroyAllWindows()
