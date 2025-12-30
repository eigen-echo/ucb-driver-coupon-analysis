#!/usr/bin/env python3
"""
Export Jupyter notebook to HTML with proper Plotly support.
This script converts the notebook to HTML and embeds Plotly charts as interactive HTML.
"""

import json
import base64
from pathlib import Path
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import Preprocessor


class PlotlyPreprocessor(Preprocessor):
    """Preprocessor that converts Plotly JSON outputs to embedded HTML."""

    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type == 'code' and 'outputs' in cell:
            new_outputs = []
            for output in cell.outputs:
                if output.get('output_type') == 'display_data':
                    data = output.get('data', {})
                    if 'application/vnd.plotly.v1+json' in data:
                        # Convert Plotly JSON to embedded HTML
                        plotly_json = data['application/vnd.plotly.v1+json']
                        plotly_html = self._create_plotly_html(plotly_json, index)
                        # Replace with HTML output
                        output['data'] = {'text/html': plotly_html}
                new_outputs.append(output)
            cell.outputs = new_outputs
        return cell, resources

    def _create_plotly_html(self, plotly_data, cell_index):
        """Create standalone HTML for a Plotly chart."""
        import json
        chart_id = f"plotly-chart-{cell_index}-{id(plotly_data)}"
        json_str = json.dumps(plotly_data)

        html = f'''
<div id="{chart_id}" style="width:100%; height:500px;"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
(function() {{
    var data = {json_str};
    Plotly.newPlot("{chart_id}", data.data || data, data.layout || {{}}, {{responsive: true}});
}})();
</script>
'''
        return html


def export_notebook_to_html(notebook_path: str, output_path: str = None):
    """
    Export a Jupyter notebook to HTML with proper Plotly support.

    Args:
        notebook_path: Path to the .ipynb file
        output_path: Path for output HTML (defaults to same name with .html extension)
    """
    notebook_path = Path(notebook_path)
    if output_path is None:
        output_path = notebook_path.with_suffix('.html')
    else:
        output_path = Path(output_path)

    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Create HTML exporter with custom preprocessor
    html_exporter = HTMLExporter()
    html_exporter.register_preprocessor(PlotlyPreprocessor, enabled=True)

    # Export to HTML
    (body, resources) = html_exporter.from_notebook_node(nb)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(body)

    print(f"Exported: {output_path}")
    print(f"Size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        # Default to prompt.ipynb in parent directory
        notebook_path = Path(__file__).parent.parent / 'prompt.ipynb'
    else:
        notebook_path = sys.argv[1]

    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    export_notebook_to_html(notebook_path, output_path)
