import csv
import os
from datetime import datetime
import config


class EventLogger:
    def __init__(self, log_path=config.EVENTS_LOG_PATH):
        self.log_path = log_path
        self.active = False
        self.start_time = None
        out_dir = os.path.dirname(self.log_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if not os.path.exists(self.log_path) or os.path.getsize(self.log_path) == 0:
            with open(self.log_path, 'a', newline='') as f:
                csv.writer(f).writerow(['timestamp', 'event', 'duration_s', 'bbox'])

    def update(self, detected, info=None):
        now = datetime.now()
        if detected and not self.active:
            self.active = True
            self.start_time = now
            bbox = info.get('bbox') if info else None
            self._write(now, 'INTRUSION_START', '', bbox)
        elif not detected and self.active:
            duration = (now - self.start_time).total_seconds() if self.start_time else 0.0
            self.active = False
            self.start_time = None
            self._write(now, 'INTRUSION_END', f'{duration:.1f}', None)

    def _write(self, when, event, duration_s, bbox):
        bbox_str = '' if bbox is None else 'x'.join(str(v) for v in bbox)
        timestamp = when.strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_path, 'a', newline='') as f:
            csv.writer(f).writerow([timestamp, event, duration_s, bbox_str])
        print(f'[{timestamp}] {event}'
              + (f' (duration {duration_s}s)' if duration_s else '')
              + (f' bbox={bbox_str}' if bbox_str else ''))
