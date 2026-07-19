# Gesture-Driven Virtual Painting System

This project is a computer vision application that lets you paint in the air using hand gestures. By tracking your hand movements through a webcam, the system turns your fingers into a digital paintbrush, allowing you to draw directly on your screen without touching any physical hardware.

## How It Works

The system processes a live video feed from your webcam and uses machine learning to identify your hand and track its movements. It switches between two primary interaction modes based on which fingers you hold up:

1. **Selection Mode (Two Fingers Up)**: When you hold up both your index and middle fingers, the brush stops drawing. You can move your hand to the top of the screen to choose a new color or select the eraser tool.
2. **Drawing Mode (One Finger Up)**: When you hold up only your index finger, the system tracks its tip and draws a continuous line on the digital canvas.

## Features

- **Real-Time Hand Tracking**: Uses advanced vision models to find and track your hand with zero lag.
- **Gesture Control**: Seamlessly switch between drawing and menu selection just by changing your finger positions.
- **Customizable Palette**: Includes multiple brush colors and a built-in digital eraser.
- **Clean Interface**: Features a dynamic on-screen display that shows your current color and brush settings.

## System Workflow

1. **Video Ingestion**: Captures frame-by-frame video from the local webcam.
2. **Landmark Detection**: Processes each frame to find the exact coordinates of your fingertips.
3. **State Evaluation**: Checks your finger configuration to determine if you are choosing a tool or actively drawing.
4. **Canvas Rendering**: Overlays the painted lines onto the live camera stream in real time.
