import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label, filedialog

def display_image(title, image):
    plt.figure(figsize=(7,7))
    if len(image.shape) == 2:
        plt.imshow(image, cmap="gray")
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Edge Detection & Filtering App")
        self.image = None
        self.gray = None

        Label(root, text="Upload an image to begin").pack()
        Button(root, text="Upload Image", command=self.upload_image).pack(pady=5)
        Button(root, text="Sobel Edge Detection", command=self.sobel).pack(pady=5)
        Button(root, text="Canny Edge Detection", command=self.canny).pack(pady=5)
        Button(root, text="Laplacian Edge Detection", command=self.laplacian).pack(pady=5)
        Button(root, text="Gaussian Blur", command=self.gaussian).pack(pady=5)
        Button(root, text="Median Filter", command=self.median).pack(pady=5)

    def upload_image(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if path:
            self.image = cv2.imread(path)
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            display_image("Original Image", self.image)

    def sobel(self):
        if self.gray is None:
            return
        sx = cv2.Sobel(self.gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(self.gray, cv2.CV_64F, 0, 1, ksize=3)
        sx = cv2.convertScaleAbs(sx)
        sy = cv2.convertScaleAbs(sy)
        combined = cv2.bitwise_or(sx, sy)
        display_image("Sobel Edge Detection", combined)

    def canny(self):
        if self.gray is None:
            return
        edges = cv2.Canny(self.gray, 100, 200)
        display_image("Canny Edge Detection", edges)

    def laplacian(self):
        if self.gray is None:
            return
        lap = cv2.Laplacian(self.gray, cv2.CV_64F)
        lap = cv2.convertScaleAbs(lap)
        display_image("Laplacian Edge Detection", lap)

    def gaussian(self):
        if self.image is None:
            return
        blur = cv2.GaussianBlur(self.image, (5, 5), 0)
        display_image("Gaussian Blur", blur)

    def median(self):
        if self.image is None:
            return
        med = cv2.medianBlur(self.image, 5)
        display_image("Median Filter", med)

root = Tk()
app = ImageApp(root)
root.mainloop()
