# 🛡️ Smart Environment: Intrusion Detection

## 🎯 Project Objective
This system detects motion specifically within predefined restricted areas of a video feed. [cite_start]It follows the mandatory 5-stage Computer Vision pipeline to produce an automatic, interpretable "ALARM" result[cite: 3, 12, 13].

## 👥 Team Roles & Responsibilities
* [cite_start]**Lead CV Engineer:** Integrates all modules and implements **Detect** and **Decide**[cite: 6].
* [cite_start]**Image Processing Specialist:** Handles **Enhance** and **Segment** stages[cite: 6].
* [cite_start]**Morphology & Report Lead:** Manages **Clean** stage and technical documentation[cite: 6].

## 🛠 5-Stage Pipeline Mapping
1.  [cite_start]**Enhance (`preprocessing.py`):** Denoising and CLAHE[cite: 14].
2.  [cite_start]**Segment (`preprocessing.py`):** Background Subtraction to isolate motion[cite: 15].
3.  [cite_start]**Clean (`filtering.py`):** Morphological operations to refine the mask[cite: 16].
4.  [cite_start]**Detect (`analytics.py`):** Drawing bounding boxes around moving targets[cite: 17].
5.  [cite_start]**Decide (`analytics.py`):** Checking if targets enter restricted zones[cite: 18].

## 📂 Project Structure
* [cite_start]`/data`: Source videos (`walk.mp4`, `thieves.mp4`, `intruder.mp4`).
* [cite_start]`/outputs`: Mandatory stage-by-stage results for 3 test images[cite: 19, 20].
* `/src`: All Python source files.

## 🚀 How to Run
1.  `pip install -r requirements.txt`
2.  `python src/main.py`