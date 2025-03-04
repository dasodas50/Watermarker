# Video Watermarker GUI

## Overview

The Video Watermarker GUI is a Python application that allows you to apply watermarks to videos using a graphical user interface. It leverages FFmpeg to process videos and apply text-based watermarks. The application is divided into two main scripts:

- `Watermarker_GUI.py`: This script provides a user-friendly GUI for managing videos and watermark application.
- `watermarker.py`: This script handles the actual processing of videos to add watermarks using FFmpeg.

## Features

- **User Management**: Add, search, and delete users to personalize watermarks.
- **File Management**: Select and manage video files for watermarking.
- **Drag-and-Drop Support**: Easily add files with drag-and-drop functionality.
- **Multithreaded Processing**: Watermark videos concurrently for efficient processing.
- **Cross-Platform**: Designed for use on Windows, with potential for adaptation on other platforms.

## Installation

### Prerequisites

1. **Python 3.7+**: Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).
2. **FFmpeg**: Ensure FFmpeg is installed and accessible in your system's PATH. You can download it from [FFmpeg.org](https://ffmpeg.org/download.html).(or just put FFmpeg in the same folder as watermarker.py) 
3. **TkinterDnD2**: Install via pip using:
   ```bash
   pip install tkinterdnd2
   ```

### Clone the Repository

```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository
```

### Setup

1. Install necessary Python packages and FFmpeg:

2. Adjust the `OUTPUT_FOLDER` in `Watermarker_GUI.py` to specify where the watermarked videos will be saved.

## Usage

1. Run the GUI application:
   ```bash
   python Watermarker_GUI.py
   ```
   Or, you can rename `Watermarker_GUI.py` to `Watermarker_GUI.**pyw**` and start it as a usual application, which will prevent a command prompt window from opening alongside your app on Windows. Just double-click the `Watermarker_GUI.pyw` file to run the application directly.

2. **User Management**:
   - Add Users: Use the input field and button in the GUI to add new users to the list.
   - Search Users: Use the search bar to filter and find specific users quickly.
   - Select and Delete Users: Highlight and delete user(s) from the list using the delete button. You can select multiple users at once using `CTRL` (to select non-contiguous users) or `Shift` (to select a range of users).
   - Directly Edit `users.json`: For advanced management, you can directly modify the `users.json` file located in the same directory as the script. This file stores the user data in JSON format, and you can manually add, update, or remove entries. Be sure to follow JSON syntax rules when editing this file.
     
3. **File Management**:
   - Add Files: Drag and drop videos into the application or use the file dialog to select them manually.
   - View Files: All selected files will be displayed in the list box for easy management.
   - Delete Files: To remove file(s) from the list, select them and press the backspace key. This will effectively delete them from the list of files set for watermarking.
    
4. **Apply Watermark**:
   - Select user(s) and file(s) for watermarking.
   - Click "Start Watermarker" to begin processing.

## Customization

- Modify Watermark Properties: You can customize the watermark properties like font size, color, position, and transparency in the `watermarker.py` script. This requires some knowledge of FFmpeg commands and syntax. FFmpeg is a powerful tool for video processing, but modifications should be made carefully to ensure they are syntactically correct and meet your requirements. You might want to consult [FFmpeg's documentation](https://ffmpeg.org/documentation.html) for more details and examples on how to adjust the drawtext filter or other FFmpeg options.
- Adapt the application for non-Windows platforms by adjusting subprocess command handling.

## Troubleshooting

- Ensure FFmpeg is properly installed and available in the system PATH.
- Check for error messages in the command line/window for details if video processing fails.
- Verify that input and output directories have appropriate permissions.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any features or bug fixes.
