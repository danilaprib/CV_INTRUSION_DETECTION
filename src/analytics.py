import cv2
import config

def detect_and_decide(frame, cleaned_mask, zone=None):
    if zone is None:
        zone = config.DEFAULT_RESTRICTED_ZONE
    zone_x1, zone_y1, zone_x2, zone_y2 = zone
    intrusion_detected = False
    info = {'bbox': None}
    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area < config.MIN_CONTOUR_AREA:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        if not (x + w < zone_x1 or x > zone_x2 or y + h < zone_y1 or y > zone_y2):
            intrusion_detected = True
            if info['bbox'] is None:
                info['bbox'] = (x, y, w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "INTRUDER", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(frame, "OBJECT", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
    zone_color = (0, 0, 255) if intrusion_detected else (255, 255, 0)
    cv2.rectangle(frame, (zone_x1, zone_y1), (zone_x2, zone_y2), zone_color, 2, cv2.LINE_AA)
    label_x = max(zone_x1 - 30, 5)
    label_y = max(zone_y1 - 8, 15)
    cv2.putText(frame, "RESTRICTED AREA", (label_x, label_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, zone_color, 1, cv2.LINE_AA)
    if intrusion_detected:
        cv2.rectangle(frame, (0, 440), (640, 480), (0, 0, 180), -1)
        cv2.putText(frame, "INTRUSION DETECTED", (180, 465),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    else:
        cv2.rectangle(frame, (0, 440), (640, 480), (40, 40, 40), -1)
        cv2.putText(frame, "MONITORING", (220, 465),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    return frame, intrusion_detected, info
