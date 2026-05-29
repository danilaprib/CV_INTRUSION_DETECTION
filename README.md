# 🛡️ Smart Environment: Intrusion Detection

## 🎯 Project Objective
This system detects motion specifically within predefined restricted areas of a video feed. It follows the mandatory 5-stage Computer Vision pipeline to produce an automatic, interpretable "ALARM" result.

## 👥 Team Roles & Responsibilities
* **Lead CV Engineer:** Integrates all modules and implements **Detect** and **Decide**.
* **Image Processing Specialist:** Handles **Enhance** and **Segment** stages.
* **Morphology & Report Lead:** Manages **Clean** stage and technical documentation.

## 🛠 5-Stage Pipeline Mapping
1.  **Enhance (`preprocessing.py`):** Denoising and CLAHE.
2.  **Segment (`preprocessing.py`):** Background Subtraction to isolate motion.
3.  **Clean (`filtering.py`):** Morphological operations to refine the mask.
4.  **Detect (`analytics.py`):** Drawing bounding boxes around moving targets.
5.  **Decide (`analytics.py`):** Checking if targets enter restricted zones.

## 📂 Project Structure
* `/data`: Source videos (`walk.mp4`, `thieves.mp4`, `intruder.mp4`).
* `/outputs`: Mandatory stage-by-stage results for 3 test images
* `/src`: All Python source files.

## 🚀 How to Run
1.  `pip install -r requirements.txt`
2.  `download CV_VIDEOS.rar and upload the videos to 'data' folder`
3.  `python src/main.py`