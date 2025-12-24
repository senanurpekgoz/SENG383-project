# Coding Tools Evaluation Report

**Student:** Sena Nur Pekgöz
**Projects:** KidTask (Java) & BeePlan (Python)
**Tools Evaluated:** Cursor (AI Code Editor) & GitHub Copilot (VS Code Extension)

---

## 1. Introduction
This report evaluates the efficiency, accuracy, and usability of two AI-assisted coding tools used during the development of the **KidTask** (Java GUI) and **BeePlan** (Python Algorithm) projects. The goal is to analyze how these tools contributed to the software development lifecycle, specifically in GUI implementation and algorithmic logic construction.

## 2. Tool Analysis: Cursor
**Used for:** KidTask (Java Swing GUI & Data Structures)

### Efficiency & Workflow
Cursor provided a significant speed advantage, particularly in generating "boilerplate" code.
* **GUI Generation:** Writing Java Swing code manually is often verbose and repetitive. Cursor's "Composer" feature (`Cmd/Ctrl + I`) allowed for the generation of entire class structures (e.g., `MainFrame`, `TaskPanel`) from a single natural language prompt.
* **Context Awareness:** Cursor demonstrated a strong understanding of the entire project context. When a file was accidentally deleted, the tool was able to reconstruct the project structure based on the chat history, saving hours of work.

### Accuracy & Limitations
* **Strengths:** Highly accurate in creating standard class hierarchies (Inheritance) and file I/O operations.
* **Weaknesses:** It occasionally struggled with environment setup (e.g., Java path configurations), requiring manual intervention in the terminal.

**Verdict:** Excellent for initializing projects and managing multi-file architecture.

---

## 3. Tool Analysis: GitHub Copilot
**Used for:** BeePlan (Python Backtracking Algorithm)

### Efficiency & Workflow
GitHub Copilot functioned as an intelligent autocomplete assistant rather than a project generator.
* **Algorithmic Logic:** For the BeePlan project, Copilot was instrumental in implementing the backtracking algorithm. By writing a comment describing the constraint (e.g., `# Check if Friday 13:20 is free`), Copilot suggested the correct logic block immediately.
* **Refactoring:** The "Chat" feature was highly effective for "Clean Coding." It successfully refactored complex constraint checks into readable helper functions and added necessary `try-except` blocks for error handling.

### Accuracy & Limitations
* **Strengths:** Extremely precise with Python syntax and standard libraries (like `json` or `PyQt5`). It significantly reduced syntax errors.
* **Weaknesses:** It relies heavily on the quality of the comments/docstrings provided. If the constraint rule was not described clearly in the comment, the suggested logic was sometimes generic rather than project-specific.

**Verdict:** Superior for logic implementation, refactoring, and line-by-line coding assistance.

---

## 4. Comparative Conclusion

| Feature | Cursor (KidTask) | GitHub Copilot (BeePlan) |
| :--- | :--- | :--- |
| **Primary Strength** | Generating entire files/projects from scratch. | Real-time code completion and logic refinement. |
| **Best Use Case** | GUI Design, Scaffolding, Recovery. | Algorithms, Refactoring, Unit Testing. |
| **User Experience** | Acts as a standalone IDE (Context-heavy). | Acts as a plugin (Unobtrusive assistant). |

### Final Thoughts
For **GUI-heavy tasks** like KidTask, **Cursor** proved to be more efficient as it could visualize and generate the component structure in bulk. However, for **logic-heavy tasks** like BeePlan, **GitHub Copilot** offered a more granular control, ensuring that specific scheduling rules were implemented correctly line-by-line.

Both tools significantly reduced development time compared to manual coding, but they serve different stages of the development workflow effectively.
