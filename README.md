# MkDocs Macros - Placeholders

This macros allows defining input parameters on a page, and automatically replace placeholders throughout the page.

## How it works

1. Placeholders like `%%database%%` are used in Markdown wherever you want dynamic substitution.
2. The macro `{{ placeholder("database") }}` auto-generates that format.
3. The macro `{{ create_input_block([...]) }}` renders:
   - An input form for required/optional fields.
   - A JavaScript function that walks the entire rendered page and replaces all instances of `%%<placeholder-id>%%`.
4. When the user clicks "Apply" or presses Enter inside a field:
   - The entire page is scanned.
   - All matching placeholders (e.g. `%%database%%`) are replaced live.
   - Placeholders in other field values (like `%%env%%` inside `%%database%%`) are also resolved.

### Using GET parameters for defaults

- If values are present in the URL, fields are pre-filled and automatically applied.
  ```
  http://localhost:8000/?database=mkdocsDb&env=test
  ```

## Usage example

```md
# Output Demo

{{ create_input_block([
  {"id": "env", "label": "Environment", "required": True, "default": ["dev", "prod", "test"]},
  {"id": "database", "label": "Database", "required": False, "default": "%%env%%_db"},
]) }}

\```html
<div style="color: green;">const database = "{{ placeholder("database") }}";</div>
<div style="color: green;">const env = "{{ placeholder("env") }}";</div>
\```
```

## Run the demo

### Build the container

```bash
docker build -t mkdocs-macros-placeholders .
```

### Run the MkDocs server

```bash
docker run -p 127.0.0.1:8000:8000 --rm -v "${PWD}:/app" mkdocs-macros-placeholders
```
