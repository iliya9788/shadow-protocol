# Shadow Protocol — CS50 Final Project

**Shadow Protocol** is an interactive cyberpunk, terminal-based adventure game built as the Final Project for **Harvard CS50x**.  
The player takes the role of an undercover operative infiltrating a classified network, uncovering hidden messages, bypassing firewalls, decoding encrypted data, and ultimately deciding the fate of a suppressed truth.

This project was developed by **Iliya** and **Diana**.

---

# What Is Shadow Protocol?

Shadow Protocol is a **web-based CLI (Command Line Interface) game**, played entirely through typed commands.  
The project features:

- A multi-stage narrative  
- A real-time command parser  
- A detection (TRACE) system  
- Two moral endings (LOYAL / REBEL)  
- Terminal-style UI with animations  
- Sounds, glitch effects, shaking alerts  
- A cinematic intro and ending sequences  

It is designed to feel like a real cyber-intrusion simulation.

---

# Story Summary

You are **Agent X-17**, a covert operative from Division-71.

A silent encrypted whisper reaches your secure terminal:

> “If you reach the CORE… do not trust what they tell you.”

You breach the network, navigate unstable nodes, dodge active security traces, and recover corrupted messages from a vanished agent.  
The deeper you go, the more you uncover evidence that **Division-71 itself may be hiding something catastrophic**.

At the end of your journey, you face a critical moral decision:

### LOYAL  
Destroy the evidence and obey the orders of Division-71.

### REBEL  
Expose the truth and trigger the collapse of a corrupt system.

Both endings are fully implemented with cinematic HTML sequences, glitch animations, sound effects, and narration.

---

# Gameplay Overview

Players interact entirely through typed commands such as:

scan network
connect node_04 --auth
bypass node_5c
decode VEhFIFRSVVRIIElTIElOIFRIRSBDT1JF
disconnect


The game transitions through multiple stages using Flask session states.

---

# Game Stages

### **Stage 1 — Network Breach**
- `scan network`  
- connect to encrypted node  
- passcode authentication  
- intro to the narrative

---

### **Stage 2 — Firewall Node + TRACE System**
- `scan firewalls`  
- choose the correct path  
- wrong choices trigger TRACE  
- 5-second countdown → DETECTED page  
- cinematic alert, shaking screen, alarm sound  

---

### **Stage 3 — Echo Chamber**
- Encrypted Base64 message  
- Player must decode the sentence:  
  `"THE TRUTH IS IN THE CORE"`  
- Unlocks access to Stage 4  

---

### **Stage 4 — THE CORE**
- Access to classified files  
- Confront the truth  
- Final moral decision:  
  - `destroy evidence` (LOYAL)  
  - `reveal truth` (REBEL)

---

### **Ending — REBEL**
A glitch-heavy cinematic sequence where the system collapses, alarms distort, and the truth is released.

### **Ending — LOYAL**
A long, emotionally heavy, classified letter from Division-71 acknowledging the agent’s sacrifice — a calm, golden, military-style ending.

---

# Technical Architecture

### **Backend:** Python (Flask)  
### **Frontend:** HTML, CSS, JavaScript (Vanilla)  
### **Session State Machine:** Controls all game progression  
### **Database:** SQLite (prepared but optional)  

Central gameplay logic lives in:

/api/command

Where each command is parsed, validated, and responded to depending on the player’s current state.

---

# Project Structure

shadow-protocol/
│── app.py
│── requirements.txt
│── README.md
│── database/
│ └── game.db
│── static/
│ ├── css/style.css
│ └── js/terminal.js
│── templates/
│ ├── index.html
│ ├── terminal.html
│ ├── detected.html
│ ├── ending_rebel.html
│ └── ending_loyal.html


---

# ⚙ How to Run Locally

### 1️ Install Flask:
pip install flask

### 2️ Start the Flask server:
python app.py

### 3️ Open the browser:
http://127.0.0.1:5000

---

# Demonstration Video

A full gameplay walkthrough will be added here:
https://youtu.be/P3slS6Uf2wc

---

## Team

### **Iliya (Lead Developer & Game Designer)**  
Primary creator of Shadow Protocol.  
Responsible for:
- Full backend architecture (Flask)
- All game logic and state machine
- Story writing and worldbuilding
- Terminal command system
- TRACE detection mechanism
- Narrative endings (LOYAL & REBEL)
- Overall project structure and implementation  
Iliya handled the majority of development and system design.

### **Diana (Frontend & UI/UX Contributor)**  
Contributed to:
- CSS styling and layout
- Terminal visual design
- Frontend improvements and polishing
- Small adjustments to HTML structure

### **Ailar (Testing & Feedback Contributor)**  
Helped with:
- Gameplay testing
- Debugging command sequences
- Identifying flow issues
- Providing user-experience feedback

---

# AI Assistance Disclosure (Required for Honesty)

Some parts of the project — including:

- Story ideas  
- README structuring  
- Terminal JS animations  
- HTML/CSS glitch effects  
- Bug fixing guidance  
- And small code improvement suggestions  

were developed with the help of **ChatGPT** and **two additional AI programming assistants**.

All final code was reviewed, edited, and integrated manually by the project creators (Iliya & Diana).

This disclosure ensures compliance with CS50's Academic Honesty guidelines.

---

# License

This project was created as part of **Harvard CS50x**.  
All code is original unless otherwise noted, and all AI assistance has been disclosed.

