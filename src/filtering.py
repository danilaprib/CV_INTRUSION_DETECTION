import cv2
import config

def clean_mask(binary_mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, config.KERNEL_SIZE)
    opened_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)
    cleaned_mask = cv2.morphologyEx(opened_mask, cv2.MORPH_CLOSE, kernel)
    return cleaned_mask
