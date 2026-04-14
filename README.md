# shinescript

**Shinescript** is a modern, statically-typed programming language designed to combine the readability and simplicity of Python with the familiar structure of C-style languages (curly braces and explicit typing).

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
prints("Liftoff! 🚀");
```

---

## 🛠 Standard Library

Shinescript comes with a lightweight but powerful set of built-in functions:

| Function | Description | Example |
| :--- | :--- | :--- |
| `prints(...)` | Output multiple values to the console. | `prints("Log: ", 123);` |
| `inputs(prompt)` | Prompt the user for input and return a string. | `str s = inputs("Name? ");` |

---

## 🏗 Setup & Execution

### Prerequisites
- Python 3.8+
Certainly! A professional, English `README.md` is essential if you want your programming language to be recognized globally by other developers. 

Here is a polished version tailored for **ShineScript**:

---

## 🚀 Installation (Linux)

ShineScript comes with an automated installation script that sets up the environment and creates a global terminal command (`shines`) for you.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/shinescript.git
   cd shinescript
   ```

2. **Grant execution permissions to the installer:**
   ```bash
   chmod +x install.sh
   ```

3. **Run the installer as root:**
   ```bash
   sudo ./install.sh
   ```

## 📂 Project Structure

* `shines/`: The core engine of the language (Lexer, Parser, and `main.py`).
* `install.sh`: Automated setup script for Linux environments.
* `examples/`: Sample scripts to help you get started with the syntax.

## 🛠️ Core Philosophy

* **Approachability:** Maintain the low learning curve found in Python.
* **Standardization:** Enforce general programming standards to ensure code quality and maintainability.
* **Portability:** Designed to run seamlessly across Linux systems.

---

### Running Shinescript
You can run Shinescript files using the provided interpreter:

```bash
shines file_to_run.ss/.shn
```

---

## 🎨 VS Code Extension
For the best experience, use the **Shinescript VS Code Extension**, which provides:
- 🌈 Full Syntax Highlighting
- Play Button for native execution
- Bracket matching & Auto-completion

---

## 📄 License
Shinescript is open-source software licensed under the **MIT License**.
