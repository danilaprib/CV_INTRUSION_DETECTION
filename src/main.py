import cv2
import os
import numpy as np


def main():
    global is_paused
    video_path = './data/walk.mp4'
    window_name = 'Intruder Detection System'
    
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, handle_click)

    rewind_time = 1000
    saved_frame_counter = 0

    window_height = 480
    window_width = 640

    cap = cv2.VideoCapture(video_path)
    
    while (True):
        if not is_paused:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_MSEC, 0)
                ret, frame = cap.read()
                if not ret:
                    break

        resized_frame = cv2.resize(frame, (window_width, window_height))  
        button_color = (0, 255, 0) if not is_paused else (0, 0, 255)
        button_text = "PLAYING" if not is_paused else "PAUSED"
        
        cv2.rectangle(resized_frame, (10, 10), (110, 50), button_color, -1)
        cv2.putText(resized_frame, button_text, (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        cv2.imshow(window_name, resized_frame)

        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('p'):
            is_paused = not is_paused
        elif key == ord('f') and not is_paused:
            current_pos = cap.get(cv2.CAP_PROP_POS_MSEC)
            cap.set(cv2.CAP_PROP_POS_MSEC, current_pos + rewind_time)
            print(f'Fast forwarded {rewind_time / 1000} second(s)')  
        elif key == ord('r') and not is_paused:
            current_pos = cap.get(cv2.CAP_PROP_POS_MSEC)
            cap.set(cv2.CAP_PROP_POS_MSEC, current_pos - rewind_time)
            print(f'Rewinded {rewind_time / 1000} second(s)')
        elif key == ord('s'):
            if not os.path.exists('outputs'):
                os.makedirs('outputs')
            if (saved_frame_counter == 0):
                cv2.imwrite('outputs/saved_frame.jpg', resized_frame)
                saved_frame_counter += 1
            else:
                cv2.imwrite(f'outputs/saved_frame({saved_frame_counter}).jpg', resized_frame)
                saved_frame_counter += 1
            print(f'Frame ({saved_frame_counter}) saved to outputs folder.')
            
    # FIXED: These lines are now outside the while loop block
    cap.release()
    cv2.destroyAllWindows() 

if __name__ == "__main__":
    main()