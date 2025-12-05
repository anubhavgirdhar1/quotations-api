from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from services.dspy_groq import extract_quotation_data
from utils.pdf_maker import generate_quotation_pdf
import io

router = APIRouter(
    prefix="/quotation",
    tags=["Quotation Generation"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/generate", 
    summary="Generate a PDF Quotation from Unstructured Text",
    description="Uses DSPy to extract structured data from raw input text and generates a professional PDF quotation, returned as a downloadable file.",
    response_description="A binary stream of the generated PDF file.",
)
async def generate_quotation_endpoint(
    raw_text: str = Query(
        ...,
        min_length=10,
        example="client Company name is Involead, items are 5 tables, 6 chairs, price is 20K per day, client is Anubhav, Date 10/12/2025",
        description="The unstructured text containing all quotation details."
    )
):
    try:
        structured_data = extract_quotation_data(raw_text)
        
        if not structured_data.items and not structured_data.client_name:
             raise HTTPException(status_code=400, detail="Could not extract sufficient data from the provided text.")

        pdf_bytes = generate_quotation_pdf(structured_data)
        
        
        client_name_clean = structured_data.client_name.replace(' ', '_').replace('.', '') or "Quotation"
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=Quotation_{client_name_clean}.pdf",
                "Content-Length": str(len(pdf_bytes)),
            }
        )
    except Exception as e:
        print(f"Error during quotation generation: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")