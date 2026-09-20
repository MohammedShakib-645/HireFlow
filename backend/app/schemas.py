from pydantic import BaseModel
from typing import List, Optional
class JobIn(BaseModel):title:str;raw_jd:str
class ReqOut(BaseModel):id:str;label:str;category:str;weight:int
class CandIn(BaseModel):job_id:str;name:str;email:Optional[str]="";resume_text:str
class QOut(BaseModel):id:str;prompt:str;gap_type:str
class RespondIn(BaseModel):transcript:str
class SearchOut(BaseModel):candidate_id:str;name:str;snippet:str;score:float
