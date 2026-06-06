---
name: collect-user-inputs
description: Collects structured user feedback and inputs using static HTML pages and saves them locally as JSON.
---
# Collect User Inputs Skill

This skill allows agents to generate interactive, self-contained HTML forms, present them to the user, and collect structured data (such as API specifications, database tables, or project requirements) saved directly to the local workspace as JSON.

---

## Why Use This Skill?

Text-based chat can be inefficient for gathering highly structured, multidimensional information (like table columns, API payloads, or lists of features). An interactive UI lets the user visually edit pre-filled proposals, add or delete fields, and configure settings dynamically.

---

## Workflow Steps

### Step 1: Identify the Input Template
Choose or customize one of the pre-built templates in [templates](file:///c:/Users/Will/Desktop/will_mono/.agents/skills/collect-user-inputs/templates/):
1. **API Designer Template** (`api_design.html`): Perfect for mapping out REST/GraphQL endpoints, request headers, query parameters, and payload tables.
2. **Project Requirements Template** (`project_requirements.html`): Gather app metadata, tech stacks, dependencies, and feature lists.
3. **Base Form Template** (`base_form.html`): Standard boilerplate with full styling and JavaScript for custom forms.

### Step 2: Pre-Fill and Generate the HTML File
1. Read the template contents using the `view_file` tool.
2. Replace template placeholders (or pre-fill forms with your own proposed schema/names).
3. Write the resulting HTML file to `scratch/<task_name>_form.html` in the workspace.
4. If there is existing data, you can pre-populate a companion JSON file at `scratch/<task_name>_data.json` which the HTML page can load automatically.

### Step 3: Direct the User to Open the Form
Instruct the user to:
1. Open `scratch/<task_name>_form.html` in their web browser (double-click the file or open it directly).
2. Interact with the form (modify fields, add columns, add endpoints, etc.).
3. Click **"Save JSON"** to select/create a file in the workspace (suggesting `scratch/<task_name>_data.json`) using the File System Access API.
4. (Fallback) If the browser does not support local saving, click **"Download JSON"**, then place the downloaded file into `scratch/<task_name>_data.json` inside the workspace.

### Step 4: Read the Generated JSON
Once the user notifies you that they have completed and saved the form:
1. Read the JSON file at `scratch/<task_name>_data.json` using the `view_file` tool.
2. Use this structured data to proceed with code generation, API building, or project setup.
3. If further iterations are needed, update the HTML page with the new state and repeat the process.

---

## Design and Styling Standards

To align with the user's styling preferences (as defined in [GEMINI.md](file:///c:/Users/Will/Desktop/will_mono/GEMINI.md)), all generated forms must implement:

1. **Default Color Palette**: Solarized light (`solarized-light`).
   - Background: `#fdf6e3` (soft cream/tan)
   - Secondary Background/Cards: `#eee8d5` (warm light gray)
   - Primary Text: `#586e75` (muted blue-gray)
   - Accents: `#268bd2` (solarized blue), `#cb4b16` (retro orange), `#b58900` (muted yellow), `#859900` (green).
2. **Dark Theme Palette**: Retro dark (`retro-dark`), enabled automatically via:
   ```css
   @media (prefers-color-scheme: dark) { ... }
   ```
   - Background: `#002b36` (deep dark teal)
   - Secondary Background/Cards: `#073642`
   - Primary Text: `#93a1a1` (light blue-gray)
3. **No Theme Selectors**: The layout must react automatically to system themes without bulky selectors.
4. **Zoom Friendly Layout**: Use flexible grid/flexbox layouts and a clean readable font (e.g. `Outfit` or `Inter` from Google Fonts).
5. **No External Libraries (CDNs)**: Bundle CSS styles and JavaScript inline or keep it dependency-free to ensure files are fully functional offline.
