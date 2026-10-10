# Data Module (`data/`)

This directory contains dataset files, knowledge bases, and reference data used by the **Smart Virtual Assistant** (`CSC10014`).

---

## 📁 Directory Structure & Datasets

### 1. `offices.csv`
Contains campus office and department directory data used by the assistant's rule-based routing engine (`src/assistant/rules.py`).

- **Expected Schema**:
  | Column | Type | Description | Example |
  | :--- | :--- | :--- | :--- |
  | `name` | `string` | Lowercase / common name of the office | `training office` |
  | `room` | `string` | Room number or building location | `A.102 (Building A)` |
  | `hours` | `string` | Operating schedule | `07:30 - 11:30, 13:00 - 16:30 (Mon - Fri)` |

- **Sample CSV Format**:
  ```csv
  name,room,hours
  training office,A.102,07:30 - 11:30 and 13:00 - 16:30 (Mon - Fri)
  student affairs,B.101,08:00 - 11:30 and 13:30 - 17:00 (Mon - Fri)
  library,Building C,07:30 - 19:00 (Mon - Sat)
  ```

> [!NOTE]
> If maintaining project team member information, consider storing it in a dedicated file such as `team.csv` or `members.csv` (`name,id`) to avoid conflicting with the assistant's office lookup engine.

---

## 📋 Data Management Guidelines

1. **File Format & Encoding**:
   - All text datasets must be encoded in **UTF-8**.
   - Standard delimiter is comma (`,`). Wrap fields containing commas in double quotes (`"`).
   - Ensure files include a header row matching the fields expected by backend loaders.

2. **Naming Conventions**:
   - Use snake_case or kebab-case for file names (e.g., `offices.csv`, `faqs.csv`, `intents.json`).

3. **Security & Privacy**:
   - Never commit sensitive information (e.g., private student records, personal API keys, or access tokens).
   - For testing large or private datasets, store sample mock data here and add private data files to `.gitignore`.