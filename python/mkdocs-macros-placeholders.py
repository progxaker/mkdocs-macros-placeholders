import json
import html

def define_env(env):
    css_content = """
    .form-group {
      margin-bottom: 10px;
    }
    label {
      display: inline-block;
      width: 160px;
    }
    """

    js_template = """
    function getUrlParams() {
      const params = {};
      const search = window.location.search.substring(1);
      if (!search) return params;

      search.split("&").forEach(pair => {
        const [key, val] = pair.split("=");
        if (!key) return;

        try {
          const decodedKey = decodeURIComponent(key);
          const decodedVal = decodeURIComponent(val.replace(/\+/g, " "));
          params[decodedKey] = decodedVal;
        } catch (e) {
          console.warn("Could not decode URI component:", val, e);
          params[key] = val; // fallback to raw
        }
      });

      return params;
    }

    function applyInputs(auto = false) {
      const inputs = document.querySelectorAll('[data-param-id]');
      const rawValues = {};
      const resolvedValues = {};

      // Gather raw input values
      inputs.forEach(input => {
        const id = input.dataset.paramId;
        rawValues['%%' + id + '%%'] = input.value || '';
      });

      // Recursively resolve placeholders inside values
      const resolve = (value, depth = 0) => {
        if (depth > 10) return value; // safeguard against circular refs
        return value.replace(/%%(.*?)%%/g, (match, key) => {
          const token = '%%' + key + '%%';
          const resolved = rawValues[token] || '';
          return resolve(resolved, depth + 1);
        });
      };

      for (const [key, val] of Object.entries(rawValues)) {
        resolvedValues[key] = resolve(val);
      }

      // Replace placeholders across the entire page (text nodes only)
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
        false
      );

      let node;
      while ((node = walker.nextNode())) {
        for (const [key, val] of Object.entries(resolvedValues)) {
          if (node.nodeValue.includes(key)) {
            node.nodeValue = node.nodeValue.replaceAll(key, val);
          }
        }
      }

      if (auto) {
        console.log("Auto-applied from GET params with resolved values:", resolvedValues);
      }
    }

    document.addEventListener("DOMContentLoaded", () => {
      const urlParams = getUrlParams();
      let shouldAutoApply = false;

      const inputs = document.querySelectorAll('[data-param-id]');
      inputs.forEach(input => {
        const id = input.dataset.paramId;

        // Fill from URL if available
        if (urlParams[id]) {
          const value = urlParams[id];
          // If it's a select and the value is not in the options, add it
          if (input.tagName === "SELECT" && input.dataset.allowCustom === "true") {
            const exists = Array.from(input.options).some(opt => opt.value === value);
            if (!exists) {
              const option = document.createElement("option");
              option.value = value;
              option.textContent = value + " (custom)";
              input.appendChild(option);
            }
          }
          input.value = value;
          shouldAutoApply = true;
        }

        // Apply on "Enter" key
        input.addEventListener("keydown", (e) => {
          if (e.key === "Enter") {
            applyInputs();
          }
        });
      });

      if (shouldAutoApply) {
        applyInputs(true);
      }
    });
    """

    @env.macro
    def placeholder(field_id):
        return f'%%{field_id}%%'

    @env.macro
    def create_input_block(params=None):
        if not params:
            return "<p><em>No parameters defined</em></p>"

        required_fields = []
        optional_fields = []

        for param in params:
            field_html = '<div class="form-group">'
            label = param.get("label", param["id"])
            required = param.get("required", False)
            default = param.get("default", "")
            input_id = param["id"]

            field_html += f'<label for="{input_id}">{label}{" (required)" if required else " (optional)"}:</label>'

            if isinstance(default, list):
                # Add a marker to allow JS to patch in missing values if needed
                field_html += f'<select id="{input_id}" data-param-id="{input_id}" data-allow-custom="true">'
                for val in default:
                    field_html += f'<option value="{val}">{val}</option>'
                field_html += '</select>'
            else:
                default_attr = f'value="{html.escape(str(default))}"' if default else ''
                field_html += f'<input type="text" id="{input_id}" data-param-id="{input_id}" {default_attr}>'

            field_html += '</div>'

            if required:
                required_fields.append(field_html)
            else:
                optional_fields.append(field_html)

        html_output = """
<div>
  <style>{css}</style>
""".format(css=css_content)

        # Required
        html_output += "\n".join(required_fields)

        # Optional (inside <details>)
        if optional_fields:
            html_output += '<details><summary>Show Optional Fields</summary>'
            html_output += "\n".join(optional_fields)
            html_output += '</details>'

        html_output += """
<button onclick="applyInputs()">Apply</button>
<script>{js}</script>
</div>
""".format(js=js_template)

        return html_output
