import cv2
import numpy as np

class Preprocessor:
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=True)
        self.clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        self.sharpen_kernel = np.array([
            [ 0, -1,  0],
            [-1,  5, -1],
            [ 0, -1,  0]
        ], dtype=np.float32)

    def enhance(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        
        if mean_brightness < 80:
            equalized = self.clahe.apply(gray)
            enhanced = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
            enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)
        else:
            sharpened = cv2.filter2D(frame, -1, self.sharpen_kernel)
            enhanced = cv2.GaussianBlur(sharpened, (5, 5), 0)
            
        return enhanced
    
    def segment(self, enhanced_frame):
        raw_mask = self.bg_subtractor.apply(enhanced_frame)
        _, binary_mask = cv2.threshold(raw_mask, 200, 255, cv2.THRESH_BINARY)
        return binary_mask