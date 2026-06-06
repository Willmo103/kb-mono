# Agent Log - Stateless Authentication & Concurrency Testing Refactor
**Date**: June 5, 2026  
**Agent**: Antigravity  

---

## 1. Problem Statement
When deploying `kb-web` to production using a Gunicorn server running multiple concurrent worker processes, attempting to log in or navigate the portal throws `sqlite3.OperationalError: database is locked`.

### Root Cause
1. **Write-on-Read Anti-pattern**: In version `0.1.13`, sessions were stored in a SQLite database table (`active_sessions`). To clean up expired sessions, the `clear_expired_tokens()` function executed a `DELETE` query on **every GET request** (e.g., `/`, `/pages`, `/view/page`, `/tags`).
2. **SQLite Lock Contention**: SQLite supports concurrent readers but only **one writer** at a time. When Gunicorn workers concurrently hit `/pages` or `/view/page`, they simultaneously attempted `DELETE` write operations.
3. **Timeout Hangs**: The configured connection `timeout=30.0` caused blocked workers to sit idle, waiting for the write lock to release, resulting in hangs before eventually failing with a locked database error.

---

## 2. Refactored Solution

### Stateless Signed Session Cookies
We transitioned the authentication system from stateful, database-backed sessions to **stateless, cryptographically signed cookies**:
1. **HMAC-SHA256 Signatures**: When logging in, the server derives a SHA-256 secret key from `config.admin_password` and signs the expiration timestamp.
2. **Instant Verification**: On subsequent requests, the server reads the cookie, splits the timestamp and signature, checks expiration, and recalculates the signature using `hmac.compare_digest`.
3. **Zero-Database Queries**: Verification is purely CPU/in-memory, requiring no database reads or write-on-read operations. GET requests are completely lock-free.
4. **Submodule Database Cleanup**: Added a schema migration step to `db.py` to drop the legacy `active_sessions` table automatically.

### Database Connection Thread-Safety
1. **Thread-Local Storage**: Cached connection objects in `_get_db()` using `threading.local()` so each thread owns its database connection, eliminating cursor/connection state collision.
2. **Schema Lock**: Synchronized connection initialization and `init_db()` calls with a threading Lock (`_init_lock`) to prevent concurrent table creation race conditions.

---

## 3. Concurrency Integration Testing
We added two integration tests to `tests/test_server.py` to prevent regressions:
1. `test_get_requests_are_write_free`: Patches `sqlite_utils.Database.execute` during GET requests to assert that zero write statements (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `CREATE`, `REPLACE`) are executed on the database.
2. `test_concurrent_reads_no_lock`: Uses `ThreadPoolExecutor` to send concurrent GET requests across multiple threads to pages, detail views, and tags, validating lock-free concurrent execution.

---

## 4. Verification Results
- All 15 unit and integration tests passed successfully under `uv run pytest`.
- The packaging pipeline built `kb-web` version `0.1.15` successfully.
