# YouTube Tooling and Warning Fixes

**Date**: June 5, 2026  
**Status**: Completed  

This document logs the robust resolution of YouTube video ingestion failures and extraction warnings on production servers lacking proper binary dependencies (such as `ffmpeg` or JS runtimes).

---

## 1. Problem Description

The production deployment of `kb-web` encountered failures and verbose logs when users attempted to import YouTube videos:
1. **Missing JS Runtime / ffmpeg Warnings**: `yt-dlp` printed multiple warning lines to `stdout`/`stderr` regarding the absence of `deno`/`js-runtimes` and `ffmpeg`.
2. **`youtube-transcript-api` Failure**: The transcript extraction crashed with `type object 'YouTubeTranscriptApi' has no attribute 'get_transcript'`. This was caused by version discrepancies between the local environment and the production environment (which requires instance-based `.fetch()` instead of static `.get_transcript()`).

---

## 2. Solutions Implemented

### Robust Subtitle Retrieval
- In [server.py](../remotes/kb-web/src/kb_web/server.py), the `youtube-transcript-api` integration was updated to support both:
  - Legacy/static method: `YouTubeTranscriptApi.get_transcript(video_id)`
  - Modern/instance method: `YouTubeTranscriptApi().fetch(video_id)`
- Handled different return formats gracefully:
  - List of raw dictionaries (legacy: dictionary subscripting for keys `start` and `text`).
  - List of `FetchedTranscriptSnippet` objects (modern: attribute access for fields `start` and `text`).

### Quietened `yt-dlp` Output
- Added a custom `QuietLogger` class mock to discard all debug, warning, and error logs originating from `yt-dlp`.
- Specified `no_warnings: True` in `YoutubeDL` options to fully suppress warnings regarding missing `ffmpeg` and JavaScript runtimes on the production server.

---

## 3. Testing and Verification

- Expanded [test_server.py](../remotes/kb-web/tests/test_server.py) to add a test case checking the instance-method fallback path (`DummyTranscriptApiInstance` and `DummySnippet` mocks).
- Verified that both the static and instance fallback paths work correctly, formatting timestamps and text properly.
- All unit tests pass cleanly, and the `build.py` script successfully synched, tested, and packaged the build artifacts.
