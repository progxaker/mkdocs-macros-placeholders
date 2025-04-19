# Output

{{ create_input_block([
  {"id": "database", "label": "Database Name", "required": True, "default": "my_db"},
  {"id": "env", "label": "Environment", "required": False, "default": ["dev", "staging", "prod"]},
  {"id": "logs_enabled", "label": "Enable Logs", "required": False, "default": "yes"}
]) }}

```bash
<div style="color: green;">const database = "{{ placeholder("database") }}";</div>
<div style="color: blue;">const env = "{{ placeholder("env") }}";</div>
<div style="color: orange;">const logs_enabled = "{{ placeholder("logs_enabled") }}";</div>
```

The database name is {{ placeholder("database") }} and the environment is `{{ placeholder("env") }}`.

```
<div style="color: green;">const database = "{{ placeholder("database") }}";</div>
<div style="color: blue;">const env = "{{ placeholder("env") }}";</div>
<div style="color: orange;">const logs_enabled = "{{ placeholder("logs_enabled") }}";</div>
```
