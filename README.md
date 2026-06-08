# ASTRA v0.5

A local-first intelligent desktop assistant created by Ashwanth.

## Overview

ASTRA is a personal AI assistant designed to bring advanced intelligence to existing desktop and laptop operating systems. The long-term vision is to create a digital intelligence that makes computers feel alive through natural interaction, contextual awareness, automation, memory, and intelligent assistance.

Version 0.5 represents the first major milestone where ASTRA can hear, think, speak, see, and understand what is happening on the screen.

---

## Features

### Voice Interaction

* Wake word activation
* Natural voice conversations
* Speech-to-text using Faster Whisper
* Text-to-speech using Microsoft Edge TTS
* Sleep mode support

Example:

User:
Astra

ASTRA:
Yes?

---

### Conversational Intelligence

* Local LLM-powered reasoning
* Multi-turn conversations
* Context-aware responses
* Runtime conversation memory
* Personal assistant behavior

---

### Application Launcher

ASTRA can launch installed desktop applications.

Examples:

* Open Chrome
* Open PyCharm
* Open Spotify
* Launch Edge

---

### Web Launcher

ASTRA can open commonly used websites directly.

Supported websites:

* YouTube
* ChatGPT
* GitHub
* Claude
* Instagram
* Google
* Sanfoundry

Examples:

* Open GitHub
* Open ChatGPT
* Open YouTube

---

### Internet Search

Examples:

* Search NVIDIA
* Search VLSI Design
* Search Python Inheritance

ASTRA automatically opens the search in the default browser.

---

### YouTube Integration

Examples:

* Play Believer
* Play Faded
* Play Shape of You

Current capabilities:

* Opens matching YouTube videos
* Starts media playback
* Automatically enters sleep mode after playback starts

---

### Screen Vision

Powered by:

* Qwen2.5-VL 7B
* EasyOCR

Capabilities:

* Full desktop screenshot analysis
* Multi-window understanding
* Application recognition
* Workspace understanding
* Activity recognition

Examples:

* Detects PyCharm
* Detects ChatGPT
* Detects GitHub
* Detects browser windows
* Detects development environments

---

### OCR Integration

EasyOCR is used to extract text visible on screen.

Benefits:

* Improves screen understanding accuracy
* Reads visible UI text
* Enhances vision model performance

Pipeline:

Screenshot
→ OCR
→ Vision Model
→ Screen Understanding

---

### Screen Awareness Commands

Examples:

* Describe the screen
* Read my screen
* What is on my screen
* Look at my screen

ASTRA can summarize visible applications and explain what the user appears to be doing.

---

### Utilities

Time

Example:

* What time is it?

Date

Example:

* What is today's date?

---

## Technology Stack

### AI Models

* Llama 3.1 8B
* Qwen2.5-VL 7B

### Speech

* Faster Whisper
* Edge TTS

### Vision

* EasyOCR
* Qwen2.5-VL

### Desktop Automation

* PyAutoGUI
* Python

### Core Language

* Python

---

## Current Architecture

ASTRA v0.5

Voice Input
↓
Whisper STT
↓
Intent Processing
↓
Llama Intelligence
↓
Tool Execution
↓
Edge TTS Speech Output

Additional Modules

* Screen Vision
* OCR
* App Launcher
* Web Search
* YouTube Integration

---

## Current Limitations

* No persistent memory across restarts
* No internet intelligence routing
* No autonomous workflows
* No browser state monitoring
* No coding assistant integration
* No terminal awareness
* No file awareness
* No OS-level contextual memory

---

## Future Roadmap

### ASTRA v0.6

* Persistent memory
* Intent router
* File awareness
* Terminal awareness
* Coding assistant foundation

### ASTRA v0.7

* Internet intelligence
* Live web search
* Tool routing
* Advanced browser control

### ASTRA v0.8

* Autonomous actions
* Workflow automation
* Context-based assistance
* Multi-step task execution

### Long-Term Vision

Create a local-first digital intelligence capable of understanding the computer, user workflows, applications, files, and environment in a human-like manner while maintaining privacy and deep operating system integration.

---

## Project Status

Version: v0.5

Status: Functional Prototype

Capabilities:

✓ Hear

✓ Think

✓ Speak

✓ See

✓ Read Screen

✓ Open Applications

✓ Search Web

✓ Play Media

✓ Understand Workspace Context

---

Created by Ashwanth

"Building the digital ecosystem for future computers."
