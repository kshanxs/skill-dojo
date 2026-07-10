# Code Styling & Comment Polishing

AI-generated code is highly detectable by its comments and docstrings. AI writing tends to be verbose, stating the obvious, and using highly predictable academic syntax inside comment blocks.

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
- [Correct] **Clean Human Commenting:**
  ```python
  if user.is_authenticated():
      # fetch profile directly to minimize DB join overhead
      return get_profile(user.id)
  ```

### Rule 2: Keep Developer Comments Direct & Informal
In production code, human developers write short, lowercase, and direct comments. AI writes formal, grammatically perfect sentence structures.
- [Incorrect] **AI Comment:** `# In the event that the database connection fails, throw a custom exception.`
- [Correct] **Human Comment:** `# bail if DB connection fails`

### Rule 3: docstring Humanisation
Ensure docstrings describe performance trade-offs, input assumptions, and complexity rather than just restating the parameters.
- [Incorrect] **AI Docstring:**
  ```python
  """
  Calculates the factorial of a number.
  
  Parameters:
  n (int): The number to calculate factorial for.
  
  Returns:
  int: The factorial result.
  """
  ```
- [Correct] **Human Docstring:**
  ```python
  """
  Calculates factorial using iterative DP to prevent stack overflows on large n.
  Complexity: O(n) time, O(1) space.
  """
  ```

---

## 2. Terminology & Syntax Protection

> [!CRITICAL]
> **Code Block Immunity**
> When editing code comment prose, you must protect the surrounding code syntax perfectly:
> - **Code Executability:** Never modify a single line of functional code, variable declaration, import, method signature, or logic.
> - **Syntax Match:** Keep the target language comment tokens intact (e.g., `#` for Python, `//` or `/* */` for JS/Go, `--` for SQL).
> - **Backtick Isolation:** Protect inline backticks (` ` ) inside comments representing variables or method names. Do not translate or synonymize those terms.
