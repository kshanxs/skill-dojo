# Code Styling & Comment Polishing

Good comments explain what the code cannot say itself. Cut comments that repeat the code, and keep the ones that record a reason or a trap.

---

## 1. Comment Clean-up Rules

When polishing mixed-mode source code or programming documentation:

### Rule 1: Eliminate the Obvious
Never comment on what a line of code does unless it is highly complex or counter-intuitive. Only explain the **Why** or the **Gotchas**.
- [Incorrect] **Robotic AI Commenting:**
  ```python
  # Check if the user is authenticated
  if user.is_authenticated():
      # Get the user's profile from the database
      profile = get_profile(user.id)
      # Return the profile
      return profile
  ```
- [Correct] **Keep only what the code cannot say:**
  ```python
  if user.is_authenticated():
      return get_profile(user.id)
  ```
  Add a "why" comment only if you know the reason. Never invent one.

### Rule 2: Match the Project's Comment Style
Follow the casing, length, and tone already used in the codebase. Prefer short, direct wording.
- [Incorrect] `# In the event that the database connection fails, throw a custom exception.`
- [Correct] `# Raise if the database connection fails.`

### Rule 3: Docstrings State Facts You Can Verify
Keep the project's docstring format. Describe assumptions, side effects, errors, and complexity only when you have confirmed them from the code. Do not remove parameter documentation that the project requires.

---

## 2. Terminology & Syntax Protection

> [!IMPORTANT]
> **Code Block Immunity**
> When editing code comment prose, you must protect the surrounding code syntax perfectly:
> - **Code Executability:** Never modify a single line of functional code, variable declaration, import, method signature, or logic.
> - **Syntax Match:** Keep the target language comment tokens intact (e.g., `#` for Python, `//` or `/* */` for JS/Go, `--` for SQL).
> - **Backtick Isolation:** Protect inline backticks (`` ` ``) inside comments representing variables or method names. Do not translate or synonymize those terms.
