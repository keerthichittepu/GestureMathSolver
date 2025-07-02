# 🤖✋ GestureMathSolver — Your Hands Are the Calculator!

> 🎯 Control a calculator using just your fingers!  
> Built using 💡 AI + Computer Vision + Python — this app detects hand gestures to solve math expressions **live on your webcam**, speaks the result, and visualizes your progress.  

---


## 🌟 What Makes It Awesome?

✨ **No buttons, no keyboard — just your hands!**  
📷 Detects hand gestures in real-time using MediaPipe + OpenCV  
🧠 Smart logic for digits, symbols & evaluation  
🗣 Speaks out the result with natural TTS voice  
📈 Shows a **bar chart** of how many problems you solved today  
📁 Saves all your expressions + results in a `.csv` file for analysis  
🎮 Great for demos, classrooms, accessibility, and tech reels!

---

## ✋ Gesture-to-Action Table

| 🖐️ **Gesture (Fingers)**      | 🎯 **What It Does**          | 🧠 **Interpreted As**      |
|------------------------------|------------------------------|----------------------------|
| 🤚 0 fingers                 | Add `0`                     | Digit `0`                  |
| ☝️ 1 to 5 fingers            | Add `1` to `5`              | Digits `1`–`5`             |
| ✋ 5 fingers + ✌️ 1 finger    | Add `6`                     | Digit `6`                  |
| ✋ 5 fingers + ✌️ 2 fingers   | Add `7`                     | Digit `7`                  |
| ✋ 5 fingers + 🤟 3 fingers   | Add `8`                     | Digit `8`                  |
| ✋ 5 fingers + ✋ 4 fingers    | Add `9`                     | Digit `9`                  |
| ☝️ 1 + ☝️ 1 fingers (2 hands) | Add `+`                     | Addition                   |
| ☝️ 1 + ✌️ 2 fingers           | Add `−`                     | Subtraction                |
| ☝️ 1 + 🤟 3 fingers           | Add `×`                     | Multiplication             |
| ☝️ 1 + ✋ 4 fingers           | Add `÷`                     | Division                   |
| 👊 + 👊 (2 fists)             | Solve expression            | `=` Evaluate               |
| ✌️ + ✌️ (2 fingers both hands)| Delete last character       | `del`                      |
| ✋ + ✋ (5 fingers both hands) | Clear full input            | `clear`                    |
| 👈👈 Index finger pinch       | Quit the app                | `exit`                     |

---

## ⚙️ How to Setup & Run

### 🧩 Prerequisites

- Python 3.8 or above
- Git Bash or terminal
- Webcam

### 📦 Installation

```bash
git clone https://github.com/keerthichittepu/GestureMathSolver.git
cd GestureMathSolver
python -m venv venv
source venv/Scripts/activate     # For Windows
pip install -r requirements.txt

▶️ Run the App
bash
Copy
Edit
python gesture_math_solver.py
Webcam window opens — now use your fingers to enter math expressions and see the magic!

👩‍🏫 Who Is This For?
🎓 Students learning AI / OpenCV / MediaPipe
🧏 Accessibility & Assistive Tech Builders
📲 AR/VR Developers looking for gesture control
📹 Creators who want viral tech demos on Reels/YouTube
🧠 Anyone curious about hands-free interactive systems!

🔚 Final Thoughts
This project is a great example of how Computer Vision + AI + Python can create intuitive, magical experiences.

No need for a mouse. No need for voice commands.
Just lift your fingers, and your screen responds. 🧞‍♂️

👩‍💻 Built With ❤️ by
Chittepu Sree Keerthi Reddy
🎓 IIIT Bhubaneswar | 🌍 India
🔗 LinkedIn
🔗 GitHub

