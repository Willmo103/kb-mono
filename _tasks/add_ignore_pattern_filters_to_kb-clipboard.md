# Task: Add Ignore Pattern Filters to `kb-clipboard`

## Problem Statement / Motivation
Currently, `kb-clipboard` continuously monitors the system clipboard and logs all captured text, files, and image data into the SQLite database. However, this captures highly sensitive information (e.g., passwords, API keys, private tokens, personal identifiers) or repeated automated noise (e.g., specific CLI command outputs, logs) that a developer does not want stored in a persistent SQLite database.

We need a flexible, lightweight filtering system to automatically ignore and discard clipboard records that match specific user-defined patterns, and a clean configuration interface inside the Electron desktop application.

---

## Technical Requirements

### 1. Configuration File
- The ignore patterns will be defined in a simple text file located at:
  `~/.kb/configs/clipboard_ignore.txt`
- The file format should follow these rules:
  - One pattern per line.
  - Empty lines are ignored.
  - Lines starting with `#` are treated as comments and ignored.
  - Each line represents a regular expression (regex) to check against the clipboard content.

### 2. Filtering Logic in the Python Watcher
- Modifying `kb_clipboard/watcher.py`:
  - Read/compile the patterns from `~/.kb/configs/clipboard_ignore.txt`.
  - To prevent continuous file I/O overhead on every poll (e.g., 5 times a second), the watcher should cache the compiled patterns and only reload them if the file's modification time (`mtime`) has changed.
  - Invalid regex patterns must be caught, reported, and ignored without crashing the watcher process.
- **Matching Content**:
  - **Text Content**: Check if the string matches any compiled regex pattern.
  - **File Content**: Check if the absolute file path or filename matches any compiled regex pattern.
  - If a match is found:
    - Log a message to stdout/stderr: `f"Skipped clipboard item matching pattern: '{pattern}'"` (do **not** print the sensitive content itself).
    - Bypass database insertion and update.

### 3. Desktop UI & Backend Integration

#### A. Main Process IPC Handlers (`desktop/main.js`)
Implement two new handlers to allow safe reading and writing of the ignore patterns configuration file:
- `get-ignore-patterns`:
  - Returns the contents of `~/.kb/configs/clipboard_ignore.txt` as a single string. If the file or directory does not exist, return an empty string.
- `save-ignore-patterns`:
  - Accepts a string containing the text of the ignore patterns.
  - Ensures the directory `~/.kb/configs` exists, then writes the string to `clipboard_ignore.txt` using UTF-8 encoding.

#### B. Preload Script Exposure (`desktop/preload.js`)
Expose the new IPC handlers to the renderer process via `contextBridge` in `window.api`:
- `getIgnorePatterns: () => ipcRenderer.invoke('get-ignore-patterns')`
- `saveIgnorePatterns: (content) => ipcRenderer.invoke('save-ignore-patterns', content)`

#### C. React UI Component (`desktop/src/App.jsx`)
- Import the `Settings` icon from `lucide-react`.
- Add a new "Settings" button to the header next to the "Export" and "Clear" buttons.
- Create a `SettingsModal` state/component:
  - Loads the existing patterns from the config file using `getIgnorePatterns` when opened.
  - Displays a clean, scrollable `<textarea>` element with monospace font styling (`font-mono`) fitting the app's retro theme.
  - Includes a quick guidelines panel or text explaining the rules (e.g., one regex per line, `#` for comments).
  - Provides a "Save" button that writes changes back to the disk using `saveIgnorePatterns` and displays a success notification (`showStatus`).
  - Provides a "Cancel" or "Close" button to discard changes.

### 4. Verification & Testing
- Update `tests/test_watcher_logic.py` to add comprehensive test coverage:
  - Verify that matching text content is skipped.
  - Verify that non-matching text content is processed and saved.
  - Verify that file paths/filenames matching patterns are skipped.
  - Verify that comments and blank lines are ignored.
  - Verify that invalid regexes do not cause the parser or watcher to crash.
