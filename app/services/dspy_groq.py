from dotenv import load_dotenv
import dspy
from models import QuotationOutput

# from config import model, provider, cache_setting -> This shit is not working for some reason

provider = "groq"
model = "llama-3.3-70b-versatile"
cache_setting = False
load_dotenv()

lm = dspy.LM(f"{provider}/{model}", cache=cache_setting)
dspy.configure(lm=lm)

class StructuredQuotationSignature(dspy.Signature):
    """Your job is to take in unstructured info and provide structured output as defined."""
    raw_text: str = dspy.InputField()
    quotation_output: QuotationOutput = dspy.OutputField(
        desc="A JSON object containing the client and quotation details."
    )

class QuotationExtractor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict(StructuredQuotationSignature)

    def forward(self, raw_text: str) -> dspy.Prediction:
        return self.predictor(raw_text=raw_text)

def extract_quotation_data(text_to_process: str) -> any:
    extractor = QuotationExtractor()
    prediction = extractor(raw_text=text_to_process)
    return prediction.quotation_output