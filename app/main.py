from fastapi import FastAPI
from routes import qoutations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DSPy Quotation Generator API",
    description="API for extracting quotation data using Groq/DSPy and generating professional PDF documents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(qoutations.router)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Quotation Generator API. Visit /docs for the Swagger UI."}

