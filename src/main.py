import argparse
import cv2
import os
import config
from preprocessing import Preprocessor
from events import EventLogger
from controls import KeyPoller
import filtering
import analytics

is_paused = False
should_ff = False
should_rewind = False
should_quit = False
should_save = False
pipeline_stage = 0
saved_frame_counter = 0

def toggle_pause():
    global is_paused
    is_paused = not is_paused

def rewind_video():
    global should_rewind
    if not is_paused:
        should_rewind = True

def fast_forward_video():
    global should_ff
    if not is_paused:
        should_ff = True

def cycle_pipeline_stage():
    global pipeline_stage
    pipeline_stage = (pipeline_stage + 1) % 5
    print(f"Jumped to Pipeline Stage: {pipeline_stage}")

def trigger_save_frame():
    global should_save
    should_save = True

def trigger_quit():
    global should_quit
    should_quit = True

def handle_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 <= x <= 95 and 10 <= y <= 40:
            trigger_save_frame()
        elif 105 <= x <= 215 and 10 <= y <= 40:
            toggle_pause()
        elif 225 <= x <= 315 and 10 <= y <= 40:
            rewind_video()
        elif 325 <= x <= 415 and 10 <= y <= 40:
            fast_forward_video()
        elif 425 <= x <= 505 and 10 <= y <= 40:
            trigger_quit()
        elif 515 <= x <= 630 and 10 <= y <= 40:
            cycle_pipeline_stage()

def resolve_video_path(video):
    if os.path.exists(video):
        return video
    in_data = os.path.join('data', video)
    if os.path.exists(in_data):
        return in_data
    return video

def select_zone(window_name, frame):
    x, y, w, h = cv2.selectROI(window_name, frame, showCrosshair=True, fromCenter=False)
    if w == 0 or h == 0:
        return None
    return (x, y, x + w, y + h)

def main(video_path=config.VIDEO_PATH):
    global should_save, saved_frame_counter, should_ff, should_rewind
    window_name = 'Intruder Detection System'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, handle_click)
    preprocessor = Preprocessor()
    logger = EventLogger()
    poller = KeyPoller(window_name)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: could not open video '{video_path}'")
        cv2.destroyAllWindows()
        return
    restricted_zone = config.zone_for_video(video_path)
    original_resized = None
    enhanced_frame = None
    segmented_mask = None
    cleaned_mask = None
    final_output = None
    while True:
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
        if should_quit:
            break
        if should_ff:
            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + config.REWIND_MS)
            print(f'Fast forwarded {config.REWIND_MS / 1000} second(s)')
            should_ff = False
        if should_rewind:
            cap.set(cv2.CAP_PROP_POS_MSEC, max(0, cap.get(cv2.CAP_PROP_POS_MSEC) - config.REWIND_MS))
            print(f'Rewinded {config.REWIND_MS / 1000} second(s)')
            should_rewind = False
        if not is_paused:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_MSEC, 0)
                ret, frame = cap.read()
                if not ret:
                    break
            original_resized = cv2.resize(frame, (config.WINDOW_W, config.WINDOW_H))
            enhanced_frame = preprocessor.enhance(original_resized)
            segmented_mask = preprocessor.segment(enhanced_frame)
            cleaned_mask = filtering.clean_mask(segmented_mask)
            final_output, intrusion_detected, info = analytics.detect_and_decide(
                original_resized.copy(), cleaned_mask, restricted_zone)
            logger.update(intrusion_detected, info)
        if original_resized is None:
            cv2.waitKey(1)
            continue
        if pipeline_stage == 0:
            display_frame = original_resized.copy()
            stage_label = "0: ORIGINAL"
        elif pipeline_stage == 1:
            display_frame = enhanced_frame.copy()
            stage_label = "1: ENHANCED"
        elif pipeline_stage == 2:
            display_frame = cv2.cvtColor(segmented_mask, cv2.COLOR_GRAY2BGR)
            stage_label = "2: SEGMENTED"
        elif pipeline_stage == 3:
            display_frame = cv2.cvtColor(cleaned_mask, cv2.COLOR_GRAY2BGR)
            stage_label = "3: CLEANED"
        elif pipeline_stage == 4:
            display_frame = final_output.copy()
            stage_label = "4: FINAL DECISION"
        if should_save:
            if not os.path.exists('outputs'):
                os.makedirs('outputs')
            filename = f'outputs/saved_frame_{saved_frame_counter}.jpg'
            cv2.imwrite(filename, display_frame)
            print(f'Saved visual frame state to {filename}')
            saved_frame_counter += 1
            should_save = False
        cv2.rectangle(display_frame, (10, 10), (95, 40), (255, 128, 0), -1)
        cv2.putText(display_frame, "SAVE", (28, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        play_color = (0, 255, 0) if not is_paused else (0, 0, 255)
        play_text = "PLAYING" if not is_paused else "PAUSED"
        cv2.rectangle(display_frame, (105, 10), (215, 40), play_color, -1)
        cv2.putText(display_frame, play_text, (130, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.rectangle(display_frame, (225, 10), (315, 40), (100, 100, 100), -1)
        cv2.putText(display_frame, "REWIND", (245, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.rectangle(display_frame, (325, 10), (415, 40), (100, 100, 100), -1)
        cv2.putText(display_frame, "FF >>", (350, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.rectangle(display_frame, (425, 10), (505, 40), (0, 0, 150), -1)
        cv2.putText(display_frame, "QUIT", (448, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.rectangle(display_frame, (515, 10), (630, 40), (200, 50, 50), -1)
        cv2.putText(display_frame, stage_label, (525, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow(window_name, display_frame)
        # Poll physical keys so shortcuts work under any keyboard layout.
        pressed = poller.poll(cv2.waitKey(1))
        if 'q' in pressed:
            trigger_quit()
        if 'p' in pressed:
            toggle_pause()
        if 'r' in pressed:
            rewind_video()
        if 'f' in pressed:
            fast_forward_video()
        if 'j' in pressed:
            cycle_pipeline_stage()
        if 's' in pressed:
            trigger_save_frame()
        if 'z' in pressed:
            if original_resized is not None:
                new_zone = select_zone(window_name, original_resized)
                if new_zone is not None:
                    restricted_zone = new_zone
                    print(f"New restricted zone for {os.path.basename(video_path)}: {restricted_zone}")
                    print(f"  paste into config.RESTRICTED_ZONES -> "
                          f"'{os.path.basename(video_path)}': {restricted_zone},")
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classical CV intrusion detection")
    parser.add_argument(
        "-v", "--video",
        default=config.VIDEO_PATH,
        help="path to a video file, or a bare filename inside data/ "
             f"(default: {config.VIDEO_PATH})",
    )
    args = parser.parse_args()
    print(f"OpenCV Version: {cv2.__version__}")
    main(resolve_video_path(args.video))
