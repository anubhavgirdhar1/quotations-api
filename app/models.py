from typing import List, Optional
from pydantic import BaseModel
    
class QuotationItem(BaseModel):
    name: str
    quantity: int
    price: str 
    
class QuotationOutput(BaseModel):
    client_name: str
    client_company: Optional[str]
    quotation_date: str
    items: List[QuotationItem]
    notes: Optional[str]
    
class GenRequest(BaseModel):
    raw_text: str