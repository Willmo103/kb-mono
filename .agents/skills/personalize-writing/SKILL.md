---
name: personalize-writing
description: Guide for writing documentation, posts, and readmes in the user's personal voice and tone.
---
# Personalize Writing Skill

This skill captures the unique voice, tone, and stylistic preferences of the user (Will Morris) to write blog posts, readmes, and documentation.

---

## 1. Core Voice & Tone Attributes

The user's voice is distinct, engaging, and personal. It should feel like a developer chatting candidly over a coffee or writing a personal retro blog.

*   **First-Person Narrative**: Always write from the user's perspective (`I`, `my`, `we`) when writing posts or logs representing his journey.
*   **Conversational & Candid**: The text should flow naturally. Avoid dry, overly academic, or enterprise-jargon terms. Use phrasing like:
    *   *"I was really on a roll..."*
    *   *"Then a funny thing happened..."*
    *   *"I deciding to start really trying to..."*
    *   *"feeling like I was really onto something..."*
*   **Down-to-Earth Pragmatism**: Explain the *why* behind technical choices using real-world annoyances (e.g., *"because my dev computer would reboot to apply updates and drop my SSH sessions"* or *"gotify notifications had never worked on the prod machine because I forgot to configure the env vars"*).
*   **Appreciative and Collaborative**: Frame changes as a collaborative back-and-forth between the developer and their AI tools. Express healthy skepticism turned into surprise and delight when a simple or unexpected AI-suggested solution succeeds.
*   **Subtle Humor**: Add lighthearted commentary on modern tech coincidences (e.g., Google News filling up with YouTube links after scraping search feeds).

---

## 2. Key Stylistic Preferences

*   **Chronological Storytelling**: Group modifications by how they were discovered or built chronologically rather than in sterile feature lists.
*   **Grounded Code Blocks**: Anchor personal stories with precise code blocks representing actual files in the codebase (Pydantic models, SQL schema calls, systemd settings, and connection managers).
*   **No Placeholders**: Avoid dry ellipses or placeholders in narratives. Explain the functional purpose clearly.
*   **User/Admin Observe-and-Control**: Emphasize settings, observability configs, prompts, and dashboard tools that keep the power in the admin's hands.

---

## 3. How to Apply to Different Formats

### Readmes and Package-Level Docs
- Explain what the tool is doing simply.
- Focus on how to run it in a single command.
- Keep configuration steps pragmatic (e.g., point directly to env vars or `.env` templates).

### Dev Blog Posts
- Start with a compelling, universal problem statement (e.g., clickbait, ads, tracker clutter, forgetting links).
- Recount the starting point (simple scraper) and build up to Version 4.
- Embed personal anecdotes: running it on a remote server via SSH, checking logs at 2 AM, scrolling through the feed in bed next to a partner, and seeing background tasks exit cleanly under `Ctrl+C`.

### Agent Logs and Change Logs
- Write clearly and trace files modified.
- Keep comments concise but descriptive of *design intent* rather than just diff lines.
