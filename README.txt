Interactive Image Processing Toolkit
CSE3113/CSE3214 Introduction to Digital Image Processing
Optional Project - Spring 2026

Student Name Surname: TODO
Student ID: TODO

How to run:
1. Install Python 3.
2. Install required libraries:
   pip install -r requirements.txt
3. Run the program:
   python image_processing_toolkit.py

Implemented features:
- Load image from file
- Display original and processed images side by side
- Display histograms of original and processed images
- Point processing:
  1. Negative transformation
  2. Log transformation
  3. Gamma transformation
  4. Contrast stretching
  5. Bitplane slicing
- Histogram operation:
  1. Histogram equalization
- Spatial filtering:
  1. Mean filter
  2. Gaussian filter
  3. Median filter
  4. Laplacian filter
  5. Sobel edge detection
  6. Prewitt edge detection
  7. Unsharp masking
- Thresholding:
  1. Manual/global thresholding
  2. Otsu thresholding
- Extra:
  1. Gaussian noise
  2. Salt and pepper noise
  3. Save processed image
  4. Use processed result as new input

Notes:
- Parameter 1 is used for gamma value, filter kernel/sigma, sharpening amount, and noise strength.
- Threshold / Bitplane is used for manual thresholding and bitplane slicing.
