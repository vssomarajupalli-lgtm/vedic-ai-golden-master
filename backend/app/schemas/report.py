from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.chart import ChartProcessRequest

class ReportGenerationRequest(ChartProcessRequest):
    question_ids: Optional[List[str]] = Field(
        None, 
        description="A list of question IDs to include in the report. If not provided, a default set will be used."
    )