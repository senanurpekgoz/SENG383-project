# Coding Tools Evaluation Report

**Student:** Ceren Kızılay
**Projects:** KidTask (Java) & BeePlan (Python)
**Tools Evaluated:**GitHub Copilot & Cursor (Coding Phase)

---

## 1. Introduction
This report evaluates the efficiency, accuracy, and usability of AI-assisted tools from the perspective of Student B. The focus is on KidTask (Algorithm & Error Handling) and BeePlan (GUI & Data Structures), analyzing how specific tools facilitate complex logic implementation versus interface construction.

## 2. Tool Analysis: Cursor
**Used for:** BeePlan (Python GUI & Data Structures)

### Efficiency & Workflow
 
* **GUI Development:Copilot was used to generate the Python-based GUI components. It excelled at suggesting property settings for layout widgets based on naming conventions
* **Real-time Autocomplete: Unlike full-file generation, Copilot’s strength lay in predicting the next line of code for data structure initialization, maintaining a fluid "flow" state during development.

### Accuracy & Limitations
* **Strengths:** High precision in Python syntax and seamless integration as a VS Code extension, making it unobtrusive.
* **Weaknesses:** Requires high-quality context; if the previous GUI components weren't well-structured, the suggestions became repetitive or irrelevant.

**Verdict:** Superior for incremental UI development and rapid data structure prototyping.

---

## 3. Tool Analysis: GitHub Copilot
**Used for:** KidTask (Java Algorithm, Clean Coding & Error Handling)

### Efficiency & Workflow
**Complex Logic Implementation:** Cursor was utilized to build the core algorithmic logic and error-handling mechanisms for KidTask.

**Refactoring & Clean Code:** Using the @file or @folder context, Cursor was able to analyze existing code and suggest refactoring patterns to ensure "Clean Coding" standards were met.
### Accuracy & Limitations
* **Strengths:** Exceptional at understanding multi-file dependencies, which is crucial for Java's object-oriented structure. It successfully implemented robust try-catch blocks and validation logic.
* **Weaknesses:** Occasionally suggested over-engineered solutions for simple logic, necessitating manual simplification.
**Verdict:** Excellent for deep logic implementation and maintaining code quality across a project.

---

## 4. Comparative Conclusion

|Feature,GitHub Copilot (BeePlan),Cursor (KidTask)
Primary Task,GUI Implementation & Data Structures ,Algorithms & Clean Coding 
Primary Strength,"Fast, line-by-line autocomplete.",Context-aware logic and refactoring.
User Experience,Seamless plugin assistant.,Powerful standalone AI IDE.
Target Quality,Usability & Speed.,Trustworthiness & Logic Accuracy.
