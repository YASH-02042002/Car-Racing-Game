# 🏎️ RetroRacer: Autonomous 2D Vehicle AI & Game Engine

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)
![PyInstaller](https://img.shields.io/badge/Deployment-Standalone_.exe-orange.svg)
![AI](https://img.shields.io/badge/AI-Heuristic_Auto_Pilot-black.svg)

## 📌 Overview
RetroRacer is a production-grade 2D arcade racing engine built entirely from scratch in Python. Moving beyond a standard game loop, this project utilizes a custom **State Machine** architecture to seamlessly manage UI flows and game states. Furthermore, it integrates a **Heuristic AI Auto-Pilot** capable of real-time spatial awareness, autonomous obstacle evasion, and objective tracking without human intervention.

## ✨ Key Engineering Features
* **Heuristic AI Auto-Pilot:** Implements a real-time, distance-based algorithm that calculates proximity thresholds of oncoming obstacles. It dynamically shifts vectors for evasion while simultaneously tracking coordinate paths to maximize coin collection.
* **State Machine Orchestration:** A robust routing node that cleanly manages 6 independent game states (Menu, Settings, Garage, Playing, Paused, Game Over), eliminating logic overlap and ensuring zero-latency transitions.
* **Algorithmic Environment Generation:** Features an infinite-scrolling background with dynamic day/night logic triggers, applying modular color-shifting without relying on heavy external image assets.
* **Production Deployment:** Compiled and packaged via PyInstaller into a standalone executable (`.exe`), allowing users to run the application with zero Python environment dependencies.

## 🏗️ System Architecture
1. **Event Listener:** Keyboard inputs and OS events are captured via Pygame's event queue.
2. **State Router:** Analyzes the current game state and routes processing to the appropriate logic block (e.g., Garage Selection vs. Active Race).
3. **Execution Engine:** 
   * *Manual Mode:* Translates user input into physical coordinate updates.
   * *AI Mode:* Bypasses user input, calculates bounding-box proximities, and autonomously applies optimal movement vectors.
4. **Render Pipeline:** Computes real-time theme colors, HUD updates, and sprite blitting, finally pushing the frame buffer to the display at 60 FPS.

## 🚀 Tech Stack
* **Core Language:** Python 3.11+
* **Game Engine Library:** Pygame (Rendering, Collision Detection, Audio Mixing)
* **Packaging & Deployment:** PyInstaller
* **Architecture Design:** Object-Oriented Programming (OOP), Finite State Machines (FSM)

## 💻 Local Installation & Setup

**1. Clone the repository**
```bash
git clone (https://github.com/YASH-02042002/Car-Racing-Game)
cd CarRacingGame
```
**2. Install dependencies**
```bash
pip install pygame
```
## ⚡Running the Application
```bash
pip install pygame
```

