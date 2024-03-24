# TimeTracker App Documentation

## Overview
<img src="TimeTracker/src/timer.ico">
The **TimeTracker** app is a text-based user interface (TUI) Python application built on the **Textual** framework. It allows users to track their training sessions or any other activities. Users can input details such as the training title, number of sets, number of exercises per set, and the time per exercise in seconds. The app then saves this information to a `./src/progression.json` file.

## Installation

1. **Prerequisites** (only if you want to run it using python, otherwise just run the .exe file):
    - Ensure you have Python installed.
    - Install the required frameworks:
        - **Textual**: A Rapid Application Development framework for Python. It enables building sophisticated user interfaces with a simple Python API. You can run Textual apps in both the terminal and a web browser. Visit the <a href="https://textual.textualize.io/guide/">Textual Documentation</a> for more details, install it using ```pip install textual```.
        - **Pyglet**: A Python library for creating games and multimedia applications. Install it using ```pip install pyglet```.

2. **Download and Run**:
    - Clone the repository or download the source code.
    - Navigate to the project directory.
    - Run the app using either of the following methods:
        - **Console**: Execute ```python main3.py``` in the terminal.
        - **Executable (Windows)**: Use the provided `main3.exe` generated with PyInstaller. This standalone executable includes all necessary files (e.g., `./src/progression.json`, `src/src/start.wav`, `src/ping.mp3.wav` ,...).

## Usage

1. **Input Details**:
    - Launch the app.
    - Enter the training title, number of sets, number of exercises per set, and exercise duration (in seconds).

2. **Progression Tracking**:
    - Completed activities are saved to the `./src/progression.json` file.
    - To view your progression, use the `DataTable` class from the `Textual.widgets` package.

3. **Screenshots**:
    - Take a screenshot of your progression table.
    - Save it as `progression.svg`.
    - Open the SVG file in a web browser to visualize your progress!.

## Authors

- **Darghal Mohammed** <mrdrgh2003@gmail.com>

Feel free to reach out if you have any questions or need further assistance!

THANKS TO THE <a href="https://textual.textualize.io/">TEXTUAL FRAMEWORK</a> TEAM!!❤️✨
