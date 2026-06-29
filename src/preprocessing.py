import cv2
import numpy as np
import config

class Preprocessor:
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=config.MOG2_HISTORY,
            varThreshold=config.MOG2_VAR_THRESHOLD,
            detectShadows=config.MOG2_DETECT_SHADOWS,
        )
        self.clahe = cv2.createCLAHE(
            clipLimit=config.CLAHE_CLIP_LIMIT,
            tileGridSize=config.CLAHE_TILE_GRID_SIZE,
        )
        self.sharpen_kernel = np.array([
            [ 0, -1,  0],
            [-1,  5, -1],
            [ 0, -1,  0]
        ], dtype=np.float32)
        self.low_light = False

    def enhance(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray)
        if self.low_light:
            if mean_brightness > config.LOW_LIGHT_EXIT:
                self.low_light = False
        else:
            if mean_brightness < config.LOW_LIGHT_ENTER:
                self.low_light = True
        if self.low_light:
            equalized = self.clahe.apply(gray)
            enhanced = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
            enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)
        else:
            sharpened = cv2.filter2D(frame, -1, self.sharpen_kernel)
            enhanced = cv2.GaussianBlur(sharpened, (5, 5), 0)

        return enhanced

    def segment(self, enhanced_frame):
        raw_mask = self.bg_subtractor.apply(enhanced_frame)
        _, binary_mask = cv2.threshold(raw_mask, config.SEGMENT_THRESHOLD, 255, cv2.THRESH_BINARY)
        
        return binary_mask
