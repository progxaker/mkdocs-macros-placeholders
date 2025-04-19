# MkDocs Macros - Placeholders

This macros allows defining input parameters on a page, and automatically replace placeholders throughout the page.

## How it works

1. Placeholders like `%%database%%` are used in Markdown wherever you want dynamic substitution.
2. The macro `{{ placeholder("database") }}` auto-generates that format.
3. The macro `{{ create_input_block([...]) }}` renders:
   - An input form for required/optional fields.
   - A JavaScript function that walks the entire rendered page and replaces all instances of `%%<placeholder-id>%%`.
4. Once the "Apply" button is clicked or "Enter" is pressed, all content is updated in place.

### Using GET parameters for defaults

- If values are present in the URL, fields are pre-filled and automatically applied.
  ```
  http://localhost:8000/?database=mkdocsDb&env=test
  ```

## Usage example

```md
# Output Demo

{{ create_input_block([
  {"id": "database", "label": "Database", "required": True, "default": "my_db"},
  {"id": "env", "label": "Environment", "required": False, "default": ["dev", "prod", "test"]}
]) }}

\`\`\`html
<div style="color: green;">const database = "{{ placeholder("database") }}";</div>
<div style="color: green;">const env = "{{ placeholder("env") }}";</div>
\`\`\`
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
