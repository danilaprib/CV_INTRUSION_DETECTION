import cv2
import os
import numpy as np

from preprocessing import Preprocessor
import filtering
import analytics

is_paused = False
should_ff = False   
should_rewind = False
should_quit = False
should_save = False
pipeline_stage = 0  # 0: Original, 1: Enhanced, 2: Segmented Mask, 3: Cleaned Mask, 4: Final Analytics Output
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
    global is_paused, should_ff, should_rewind, should_quit
    
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

def main():
    global is_paused, should_ff, should_rewind, should_quit, should_save, pipeline_stage, saved_frame_counter
    video_path = './data/walk.mp4'
    window_name = 'Intruder Detection System'
    
    cv2.namedWindow(window_name)
    
    preprocessor = Preprocessor()
    rewind_time = 1000
    window_height = 480
    window_width = 640

    cap = cv2.VideoCapture(video_path)
    
    while True:
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
            
        cv2.setMouseCallback(window_name, handle_click)

        if should_quit: 
            break
        
        if should_ff:
            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + rewind_time)
            print(f'Fast forwarded {rewind_time / 1000} second(s)')
            should_ff = False
        if should_rewind:
            cap.set(cv2.CAP_PROP_POS_MSEC, max(0, cap.get(cv2.CAP_PROP_POS_MSEC) - rewind_time))
            print(f'Rewinded {rewind_time / 1000} second(s)')
            should_rewind = False

        if not is_paused:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_MSEC, 0)
                ret, frame = cap.read()
                if not ret: 
                    break

        original_resized = cv2.resize(frame, (window_width, window_height))  
        
        enhanced_frame = preprocessor.enhance(original_resized)
        segmented_mask = preprocessor.segment(enhanced_frame)
        cleaned_mask = filtering.clean_mask(segmented_mask)
        final_output = analytics.detect_and_decide(original_resized.copy(), cleaned_mask)

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
            display_frame = final_output
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

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): 
            trigger_quit()
        elif key == ord('p'): 
            toggle_pause()
        elif key == ord('r'): 
            rewind_video()
        elif key == ord('f'): 
            fast_forward_video()
        elif key == ord('j'): 
            cycle_pipeline_stage()
        elif key == ord('s'): 
            trigger_save_frame()
            
    cap.release()
    cv2.destroyAllWindows() 

if __name__ == "__main__":
    main()