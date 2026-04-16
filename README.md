# shinescript

**Shinescript** is a modern, interpreted, statically-typed programming language designed to combine the readability and simplicity of Python with the familiar structure of C-style languages (curly braces and explicit typing).

It is built to be fast, expressive, and easy to learn for both beginners and experienced developers.

---

## Quick Start

### Hello World
```shinescript
prints("Hello, Shinescript!");
```

### Variables & Types
Shinescript enforces static typing to ensure code reliability. Supported types include `int`, `float`, `str`, and `bool`.

```shinescript
int age = 25;
float price = 19.99;
str name = "Zelix";
bool isAwesome = true;

prints(name, " is ", age, " years old.");
```

### Functions
Define reusable logic with the `func` keyword. Parameters must specify their types.

```shinescript
func greet(str nickname, int level) {
    prints("Welcome back, ", nickname, "!");
    prints("Your current level is: ", level);
}

greet("Adventurer", 10);
```

### Control Flow

#### If/Else
```shinescript
int score = 85;

if (score >= 90) {
    prints("Grade: A");
} else {
    if (score >= 80) {
        prints("Grade: B");
    } else {
        prints("Keep trying!");
    }
}
```

#### While Loop
```shinescript
int count = 5;
while (count > 0) {
    prints("T-minus: ", count);
    count = count - 1;
}
prints("Liftoff!");
```

#### For Loop
Shinescript supports C-style for loops, creating a specific block scope for the loop variable.
```shinescript
for (int i = 0; i < 5; i = i + 1) {
    prints("Iteration: ", i);
}
```

---

## Standard Library

Shinescript comes with a lightweight but powerful set of built-in functions:

| Function | Description | Example |
| :--- | :--- | :--- |
| `prints(...)` | Output multiple values to the console. | `prints("Log: ", 123);` |
| `inputs(prompt)` | Prompt the user for input and return a string. | `str s = inputs("Name? ");` |

---

## Setup & Execution

### Prerequisites
- Python 3.8+
- A computer that can run better than potato(idk never tested on potato. probably works)

---

## Installation (Windows, Linux, & Mac)

The recommended way to install Shinescript globally across any operating system is by using Python's package manager (`pip`). This will automatically set up the `shines` command in your terminal.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/lanierc/shinescript.git](https://github.com/lanierc/shinescript.git)
   cd shinescript
   ```

2. **Install using pip:**
   ```bash
   pip install .
   ```
   *Note: If you get a "command not found" error after installation, make sure your Python Scripts folder is added to your system's PATH.*

### Alternative Installation (Linux Only)
ShineScript also comes with an automated installation bash script specifically for Linux environments.

1. **Grant execution permissions to the installer:**
   ```bash
   chmod +x install.sh
   ```

2. **Run the installer as root:**
   ```bash
   sudo ./install.sh
   ```

## Project Structure

* `shines/`: The core engine of the language (Lexer, Parser, Interpreter, and `main.py`).
* `setup.py` / `install.sh`: Automated setup scripts for cross-platform and Linux environments.
* `examples/`: Sample scripts to help you get started with the syntax.

## Core Philosophy

* **Approachability:** Maintain the low learning curve found in Python.
* **Standardization:** Enforce general programming standards to ensure code quality and maintainability.
* **Portability:** Designed to run seamlessly across Windows, Linux, and macOS systems.

---

### Running Shinescript
Once installed, you can run Shinescript files from anywhere using the provided global command:

```bash
shines file_to_run.ss
```
*(You can use `.ss` or `.shn` file extensions)*

---

## VS Code Extension
For the best experience, use the **Shinescript VS Code Extension**, which provides:
- Full Syntax Highlighting
- Play Button for native execution
- Bracket matching & Auto-completion

---

## 📄 License
Shinescript is open-source software licensed under the **MIT License**.
```
