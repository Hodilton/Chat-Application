# log-manager

---
## Usages
```python
from log_manager import LoggerConfig, LogManager

# Example configuration dict
config_dict = {
    "console": {
        "type": "console",
        "level": "DEBUG",
        "use_color": True
    },
    "file": {
        "type": "file",
        "path": "app.log",
        "level": "INFO"
    },
    "rotate_s": {
        "type": "rotate_size",
        "path": "logs/rotate.log",
        "level": "WARNING",
        "max_bytes": 10240,
        "backup_count": 5
    },
    "rotate_t": {
        "type": "rotate_time",
        "path": "logs/daily.log",
        "level": "ERROR",
        "when": "midnight",
        "interval": 1,
        "backup_count": 7
    }
}

# Initialize LoggerConfig from dict or from JSON file path
config = LoggerConfig(config=config_dict,log_dir="logs")

# Create LogManager with config
manager = LogManager(config)

# Log messages to specific loggers
manager.log("console", "Test DEBUG message to console only", level="DEBUG")
manager.log("file", "Test WARNING message to file only", level="WARNING")
manager.log(["console", "file"], "Test INFO message to list loggers", level="INFO")

# Log message to all configured loggers
manager.log_all("System shutting down!!!", level="CRITICAL")
```
## Output
```json
# console
[2025-05-18 22:54:36] DEBUG: Test DEBUG message to console only
[2025-05-18 22:54:36] INFO: Test INFO message to list loggers
[2025-05-18 22:54:36] CRITICAL: System shutting down!!!
```
```json
# file
[2025-05-18 22:54:36] WARNING: Test WARNING message to file only
[2025-05-18 22:54:36] INFO: Test INFO message to list loggers
[2025-05-18 22:54:36] CRITICAL: System shutting down!!!
```
---
## Configuration format
The configuration can be provided as a Python dict or loaded from a JSON file.

| Key            | Description                                                             | Required?                        | Default                |
|----------------|-------------------------------------------------------------------------|----------------------------------|------------------------|
| `type`         | `"console"`, `"file"`, `"rotate_size"`, `"rotate_time"`                 | **Yes**                          | —                      |
| `path`         | File path for file-based loggers (relative to `log_dir`)                | Required for all but `"console"` | —                      |
| `level`        | `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`               | No                               | `"DEBUG"`              |
| `use_color`    | For `"console"` only                                                    | No                               | `True`                 |
| `max_bytes`    | For `"rotate_size"`: max file size in bytes before rotation             | No                               | `10240` (10 KB)        |
| `backup_count` | For `"rotate_size"` and `"rotate_time"`: number of backup files to keep | No                               | `3` (size), `7` (time) |
| `when`         | For `"rotate_time"`: time interval unit (e.g. `"midnight"`)             | No                               | `"midnight"`           |
| `interval`     | For `"rotate_time"`: number of intervals between rotations              | No                               | `1`                    |
