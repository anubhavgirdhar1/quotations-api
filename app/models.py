from typing import List, Optional
from pydantic import BaseModel

class QuotationItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total_price: float
    
class QuotationData(BaseModel):
    client_name: str
    client_company: Optional[str] = None
    quotation_date: str # Date ISO String
    itmes: List[QuotationItem]
    notes: Optional[str] = None
    
class GenRequest(BaseModel):
    raw_text: str