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
        if (key && val !== undefined) {
          params[decodeURIComponent(key)] = decodeURIComponent(val.replace(/\+/g, " "));
        }
      });

      return params;
    }

    function applyInputs(auto = false) {
      const inputs = document.querySelectorAll('[data-param-id]');
      const values = {};
      inputs.forEach(input => {
        const id = input.dataset.paramId;
        values['%%' + id + '%%'] = input.value || '';
      });

      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
        false
      );

      let node;
      while ((node = walker.nextNode())) {
        for (const [key, val] of Object.entries(values)) {
          if (node.nodeValue.includes(key)) {
            node.nodeValue = node.nodeValue.replaceAll(key, val);
          }
        }
      }

      if (auto) {
        console.log("Auto-applied parameters from URL:", values);
      }
    }

    document.addEventListener("DOMContentLoaded", () => {
      const urlParams = getUrlParams();
      let shouldAutoApply = false;

      const inputs = document.querySelectorAll('[data-param-id]');
      inputs.forEach(input => {
        // Fill from URL if present
        const key = input.dataset.paramId;
        if (urlParams[key]) {
          input.value = urlParams[key];
          shouldAutoApply = true;
        }

        // Apply on Enter
        input.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') {
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
                field_html += f'<select id="{input_id}" data-param-id="{input_id}">'
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
