import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------------------------------------------------
# CSE3113/CSE3214 Introduction to Digital Image Processing
# Optional Project - Interactive Image Processing Toolkit
# Name Surname: Illia Bredikhin
# Student ID: 2503015008
# ------------------------------------------------------------

class ImageProcessingToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Image Processing Toolkit")
        self.root.geometry("1250x760")

        self.original_image = None
        self.processed_image = None
        self.original_tk = None
        self.processed_tk = None

        self.create_widgets()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root, padding=8)
        top_frame.pack(fill="x")

        title = ttk.Label(
            top_frame,
            text="Name Surname: Illia Bredikhin    Student ID: 2503015008",
            font=("Arial", 12, "bold")
        )
        title.pack(side="left", padx=5)

        ttk.Button(top_frame, text="Load Image", command=self.load_image).pack(side="right", padx=5)
        ttk.Button(top_frame, text="Reset", command=self.reset_image).pack(side="right", padx=5)
        ttk.Button(top_frame, text="Save Processed", command=self.save_processed).pack(side="right", padx=5)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(side="left", fill="y", padx=8, pady=8)

        image_frame = ttk.Frame(main_frame)
        image_frame.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        self.original_label = ttk.Label(image_frame, text="Original Image", anchor="center")
        self.original_label.grid(row=0, column=0, padx=8, pady=5)
        self.processed_label = ttk.Label(image_frame, text="Processed Image", anchor="center")
        self.processed_label.grid(row=0, column=1, padx=8, pady=5)

        self.original_canvas = ttk.Label(image_frame, background="white")
        self.original_canvas.grid(row=1, column=0, padx=8, pady=5)
        self.processed_canvas = ttk.Label(image_frame, background="white")
        self.processed_canvas.grid(row=1, column=1, padx=8, pady=5)

        hist_frame = ttk.Frame(image_frame)
        hist_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=8)
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(8, 2.6))
        self.fig.tight_layout()
        self.hist_canvas = FigureCanvasTkAgg(self.fig, master=hist_frame)
        self.hist_canvas.get_tk_widget().pack(fill="both", expand=True)

        ttk.Label(control_frame, text="Operation:").pack(anchor="w")
        self.operation = tk.StringVar(value="Negative transformation")
        operations = [
            "Negative transformation",
            "Log transformation",
            "Gamma transformation",
            "Contrast stretching",
            "Bitplane slicing",
            "Histogram equalization",
            "Mean filter",
            "Gaussian filter",
            "Median filter",
            "Laplacian filter",
            "Sobel edge detection",
            "Prewitt edge detection",
            "Unsharp masking",
            "Manual thresholding",
            "Otsu thresholding",
            "Add Gaussian noise",
            "Add Salt & Pepper noise"
        ]
        self.operation_box = ttk.Combobox(control_frame, textvariable=self.operation, values=operations, state="readonly", width=28)
        self.operation_box.pack(anchor="w", pady=5)

        ttk.Label(control_frame, text="Parameter 1").pack(anchor="w", pady=(10, 0))
        self.param1 = tk.DoubleVar(value=1.0)
        self.param1_scale = ttk.Scale(control_frame, from_=0.1, to=10.0, variable=self.param1, orient="horizontal", length=220)
        self.param1_scale.pack(anchor="w")
        self.param1_label = ttk.Label(control_frame, textvariable=self.param1)
        self.param1_label.pack(anchor="w")

        ttk.Label(control_frame, text="Threshold / Bitplane").pack(anchor="w", pady=(10, 0))
        self.param2 = tk.IntVar(value=128)
        self.param2_scale = ttk.Scale(control_frame, from_=0, to=255, variable=self.param2, orient="horizontal", length=220)
        self.param2_scale.pack(anchor="w")
        self.param2_label = ttk.Label(control_frame, textvariable=self.param2)
        self.param2_label.pack(anchor="w")

        ttk.Button(control_frame, text="Apply Operation", command=self.apply_operation).pack(fill="x", pady=15)
        ttk.Button(control_frame, text="Use Processed as Input", command=self.use_processed_as_input).pack(fill="x", pady=3)

        info = (
            "Parameter guide:\n"
            "Gamma: parameter 1\n"
            "Filters: parameter 1 = kernel/sigma\n"
            "Manual threshold: Threshold value\n"
            "Bitplane: Threshold/Bitplane 0-7"
        )
        ttk.Label(control_frame, text=info, justify="left").pack(anchor="w", pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )
        if not path:
            return
        self.original_image = Image.open(path).convert("RGB")
        self.processed_image = self.original_image.copy()
        self.update_display()

    def reset_image(self):
        if self.original_image is None:
            return
        self.processed_image = self.original_image.copy()
        self.update_display()

    def save_processed(self):
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            self.processed_image.save(path)

    def use_processed_as_input(self):
        if self.processed_image is None:
            return
        self.original_image = self.processed_image.copy()
        self.update_display()

    def pil_to_cv_gray(self, image):
        arr = np.array(image.convert("RGB"))
        return cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    def apply_operation(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first.")
            return

        op = self.operation.get()
        img_rgb = np.array(self.original_image.convert("RGB"))
        gray = self.pil_to_cv_gray(self.original_image)
        p1 = float(self.param1.get())
        p2 = int(self.param2.get())

        try:
            if op == "Negative transformation":
                result = 255 - img_rgb
                self.processed_image = Image.fromarray(result.astype(np.uint8))

            elif op == "Log transformation":
                c = 255 / np.log(1 + np.max(img_rgb))
                result = c * np.log(1 + img_rgb.astype(np.float32))
                self.processed_image = Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))

            elif op == "Gamma transformation":
                gamma = max(p1, 0.1)
                norm = img_rgb.astype(np.float32) / 255.0
                result = 255 * (norm ** gamma)
                self.processed_image = Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))

            elif op == "Contrast stretching":
                result = np.zeros_like(img_rgb)
                for c in range(3):
                    channel = img_rgb[:, :, c]
                    min_v, max_v = np.min(channel), np.max(channel)
                    result[:, :, c] = ((channel - min_v) / (max_v - min_v + 1e-6) * 255)
                self.processed_image = Image.fromarray(result.astype(np.uint8))

            elif op == "Bitplane slicing":
                bit = max(0, min(7, p2))
                result = ((gray >> bit) & 1) * 255
                self.processed_image = Image.fromarray(result.astype(np.uint8)).convert("RGB")

            elif op == "Histogram equalization":
                ycrcb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2YCrCb)
                ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
                result = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
                self.processed_image = Image.fromarray(result.astype(np.uint8))

            elif op == "Mean filter":
                k = self.make_odd_kernel(p1)
                result = cv2.blur(img_rgb, (k, k))
                self.processed_image = Image.fromarray(result.astype(np.uint8))

            elif op == "Gaussian filter":
                k = self.make_odd_kernel(p1)
                result = cv2.GaussianBlur(img_rgb, (k, k), sigmaX=max(p1, 0.1))
                self.processed_image = Image.fromarray(result.astype(np.uint8))

            elif op == "Median filter":
                k = self.make_odd_kernel(p1)
                result = cv2.medianBlur(img_rgb, k)
                self.processed_image = Image.fromarray(result.astype(np.uint8))

            elif op == "Laplacian filter":
                lap = cv2.Laplacian(gray, cv2.CV_64F)
                result = np.uint8(np.clip(np.abs(lap), 0, 255))
                self.processed_image = Image.fromarray(result).convert("RGB")

            elif op == "Sobel edge detection":
                sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
                sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
                result = np.sqrt(sx ** 2 + sy ** 2)
                self.processed_image = Image.fromarray(np.clip(result, 0, 255).astype(np.uint8)).convert("RGB")

            elif op == "Prewitt edge detection":
                kernelx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
                kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                x = cv2.filter2D(gray, -1, kernelx)
                y = cv2.filter2D(gray, -1, kernely)
                result = cv2.addWeighted(x, 0.5, y, 0.5, 0)
                self.processed_image = Image.fromarray(result.astype(np.uint8)).convert("RGB")

            elif op == "Unsharp masking":
                blur = cv2.GaussianBlur(img_rgb, (5, 5), 1.0)
                amount = max(p1, 0.1)
                result = cv2.addWeighted(img_rgb, 1 + amount, blur, -amount, 0)
                self.processed_image = Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))

            elif op == "Manual thresholding":
                _, result = cv2.threshold(gray, p2, 255, cv2.THRESH_BINARY)
                self.processed_image = Image.fromarray(result.astype(np.uint8)).convert("RGB")

            elif op == "Otsu thresholding":
                _, result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                self.processed_image = Image.fromarray(result.astype(np.uint8)).convert("RGB")

            elif op == "Add Gaussian noise":
                noise = np.random.normal(0, p1 * 10, img_rgb.shape)
                result = img_rgb.astype(np.float32) + noise
                self.processed_image = Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))

            elif op == "Add Salt & Pepper noise":
                result = img_rgb.copy()
                amount = min(max(p1 / 100, 0.001), 0.1)
                random_matrix = np.random.rand(img_rgb.shape[0], img_rgb.shape[1])
                result[random_matrix < amount / 2] = 0
                result[random_matrix > 1 - amount / 2] = 255
                self.processed_image = Image.fromarray(result.astype(np.uint8))

            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed: {e}")

    def make_odd_kernel(self, value):
        k = int(round(value))
        k = max(3, min(k, 15))
        if k % 2 == 0:
            k += 1
        return k

    def resize_for_display(self, image, max_size=(430, 330)):
        img = image.copy()
        img.thumbnail(max_size)
        return img

    def update_display(self):
        if self.original_image is not None:
            show_original = self.resize_for_display(self.original_image)
            self.original_tk = ImageTk.PhotoImage(show_original)
            self.original_canvas.configure(image=self.original_tk)

        if self.processed_image is not None:
            show_processed = self.resize_for_display(self.processed_image)
            self.processed_tk = ImageTk.PhotoImage(show_processed)
            self.processed_canvas.configure(image=self.processed_tk)

        self.update_histograms()

    def update_histograms(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_title("Original Histogram")
        self.ax2.set_title("Processed Histogram")

        if self.original_image is not None:
            gray = self.pil_to_cv_gray(self.original_image)
            self.ax1.hist(gray.ravel(), bins=256, range=(0, 255))

        if self.processed_image is not None:
            gray = self.pil_to_cv_gray(self.processed_image)
            self.ax2.hist(gray.ravel(), bins=256, range=(0, 255))

        self.fig.tight_layout()
        self.hist_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingToolkit(root)
    root.mainloop()
