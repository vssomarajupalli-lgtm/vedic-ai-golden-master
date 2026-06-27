from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from app.reports.schemas import FinalReportSchema

class HTMLGenerator:
    """
    Consumes the Pydantic FinalReportSchema and renders it into a standalone
    HTML document using Jinja2 templates.
    """
    def __init__(self):
        # Locate the templates directory relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_dir, "templates")
        
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(self, report_data: FinalReportSchema) -> str:
        """
        Renders the base template with the full report dictionary.
        Returns the raw HTML string.
        """
        template = self.env.get_template("base.html")
        return template.render(report=report_data.dict())
