# Windows Application Blocker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[繁體中文](README_zh.md)

A Windows application that helps you manage blocked applications through a user-friendly GUI interface. It utilizes Windows Registry to prevent specific applications from running.

## 📋 Features

- Block specific applications from running on Windows
- Easy-to-use graphical interface
- Support for both manual input and file selection
- Multi-language support (English/Traditional Chinese)
- Multiple selection for batch deletion
- Real-time list updates
- Automatic system language detection

## 📸 Screenshots

![Main Window Interface](https://github.com/user-attachments/assets/3e1446d8-4547-4fc3-aa6e-9451a8918c16)
![Execution Prevention Demo](https://github.com/user-attachments/assets/2aa3a050-1b50-454f-8e2c-f18c850c7fe1)

## 💻 Installation

1. Download the [latest release](https://github.com/jmsch23280866/Windows-Blocklist-Manager/releases/latest) from the releases page
2. Run the executable as administrator
3. The program will automatically configure necessary registry settings

## 📖 Usage

### Adding Applications to Block List
- Type the application name directly (e.g., notepad.exe)
- Or use the "Browse" button to select an executable file
- Press Enter or click "Add" button to add to block list

### Removing Applications from Block List
- Select one or multiple items from the list
- Press Delete key or click "Remove Selected" button
- Confirm the deletion in the popup dialog

## ⚙️ Technical Details

- Built with Python and Tkinter
- Uses Windows Registry to implement blocking functionality
### How It Works

This tool works by modifying the Windows Registry key:

```
HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun
```
to prevent specific applications from running.
- Requires administrator privileges to modify system settings
- Supports Windows 10/11

## 📋 System Requirements

- Windows 10 or later
- Administrator privileges
- Python 3.x (if running from source)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🤝 Contributing

Issues and Pull Requests are welcome to help improve this project!

## 👨‍💻 Author

Agent_E04 ([@jmsch23280866](https://github.com/jmsch23280866))

## 🤖 AI Assistance Statement

This project was developed with assistance from Claude AI and ChatGPT, including code optimization suggestions and documentation writing.

## 📝 Changelog

### v2 (2025-01-13)
- Added multi-language system (English/Traditional Chinese)
- Added multiple selection for batch deletion
- Added deletion confirmation dialog
- Improved UI layout and design
- Added keyboard shortcut support
- Added scrollbar functionality
- Code refactoring for better stability

### v1.2 (2025-01-10)
- Improved system policy configuration
- Added duplicate item checking
- Enhanced error handling

### v1.1 (2025-01-10)
- Added file browsing functionality
- Added input field placeholder text
- Improved interface layout

### v1 (2025-01-10)
- Initial release
- Basic blocking functionality
- Simple GUI interface
- Basic add/remove functions

## 🙏 Acknowledgments

Special thanks to [CyberCPU Tech](https://youtu.be/z-4YYzWb-GQ) for the inspiration from their video.
