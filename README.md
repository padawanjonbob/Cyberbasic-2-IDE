CyberBasic 2 IDE

CyberBasic 2 IDE is a lightweight development environment built with Tkinter for the CyberBasic 2 programming language. It provides a dark-themed interface, syntax highlighting, file navigation, and the ability to run CyberBasic programs directly within the editor.

Features

Syntax highlighting for keywords, functions, strings, and comments is supported with real-time updates.

A project explorer sidebar allows opening folders and navigating files.

An integrated console displays program output when running CyberBasic code.

Customizable themes are available, including built-in themes such as Dracula and Classic Dark, along with a color editor with color wheel.

The editor includes line numbers, current line highlighting, and undo and redo support.

Keyboard shortcuts are available. Ctrl + S saves files and F5 runs code.

Project Structure

cyberbasic-ide/

main.py is the main controller and application entry point.
ide_ui.py contains UI layout and components.
highlighter.py implements the syntax highlighting engine.
cyberbasic_config.py stores keywords, themes, and configuration.
cyberbasic.exe is the required CyberBasic runtime.

Requirements

Python version 3.8 or higher is required.

The application is designed for Windows and uses pywinstyles for native styling.

The CyberBasic runtime executable cyberbasic.exe must be present.

Installation

Clone the repository using:

git clone https://github.com/padawanjonbob/cyberbasic-2-IDE.git

Change into the project directory:

cd cyberbasic-ide

Install dependencies:

pip install pywinstyles

Ensure that cyberbasic.exe is located in the project root directory.

Usage

Run the IDE with:

python main.py or CB2IDE.exe

To run a program, open or create a .bas file and press F5. Output will appear in the built-in console.

Customization

Themes can be changed from the View menu under Themes.

Colors can be customized from the View menu under Customize Colors. Editable elements include background, text, keywords, functions, comments, and strings.

Syntax Highlighting

The CyberHighlighter module uses regular expressions to parse and highlight code.

It supports keyword highlighting, function detection, string literals, and comments using both double slash and REM syntax.

Contributing

Contributions are welcome. Suggestions and improvements can be submitted through issues or pull requests.

License

This project is licensed under the MIT License or another license of your choice.

Credits

This project is built using Tkinter and styled with pywinstyles.
