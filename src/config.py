import os

WINDOW_W = 640
WINDOW_H = 480
VIDEO_PATH = './data/walk.mp4'
REWIND_MS = 1000

MOG2_HISTORY = 500
MOG2_VAR_THRESHOLD = 25
MOG2_DETECT_SHADOWS = True

CLAHE_CLIP_LIMIT = 3.0
CLAHE_TILE_GRID_SIZE = (8, 8)

SEGMENT_THRESHOLD = 200

LOW_LIGHT_ENTER = 70
LOW_LIGHT_EXIT = 90

KERNEL_SIZE = (5, 5)

DEFAULT_RESTRICTED_ZONE = (0, 0, WINDOW_W, WINDOW_H)
RESTRICTED_ZONES = {
    # 'walk.mp4': (x1, y1, x2, y2),
    # 'thieves.mp4': (x1, y1, x2, y2),
    # 'intruder.mp4': (x1, y1, x2, y2),
}
MIN_CONTOUR_AREA = 400

def zone_for_video(video_path):
    return RESTRICTED_ZONES.get(os.path.basename(video_path), DEFAULT_RESTRICTED_ZONE)

EVENTS_LOG_PATH = 'outputs/events.csv'
