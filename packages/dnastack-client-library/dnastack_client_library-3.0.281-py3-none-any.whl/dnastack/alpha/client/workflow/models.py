from typing import Dict, Optional, Any

from pydantic import BaseModel


class WorkflowDescriptor(BaseModel):
    workflow_name: str
    input_schema: Dict
    output_schema: Dict
    wdl_version: str
    errors: Optional[Any]
