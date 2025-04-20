# Output

{{ create_input_block([
  {"id": "env", "label": "Environment", "required": True, "default": ["dev", "staging", "prod"]},
  {"id": "database", "label": "Database Name", "required": False, "default": "%%env%%_db"},
  {"id": "logs_enabled", "label": "Enable Logs", "required": False, "default": "yes"}
]) }}


**Regular text:**  
The database name is {{ placeholder("database") }}.

**Inline code:**  
The environment is `{{ placeholder("env") }}`.

**Preformated:**
```noformat
<div style="color: green;">const database = "{{ placeholder("database") }}";</div>
<div style="color: blue;">const env = "{{ placeholder("env") }}";</div>
<div style="color: orange;">const logs_enabled = "{{ placeholder("logs_enabled") }}";</div>
```

**Code block:**
```html
<div style="color: green;">const database = "{{ placeholder("database") }}";</div>
<div style="color: blue;">const env = "{{ placeholder("env") }}";</div>
<div style="color: orange;">const logs_enabled = "{{ placeholder("logs_enabled") }}";</div>
```
