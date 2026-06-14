from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

router = APIRouter()


class AskRequest(BaseModel):
    question: str
    company_id: str | None = None


STUB_CONTEXT = """
Company: Transport Dupont SPRL
Period: June 2026
Revenue: €48,200 | Costs: €31,800 | Margin: 34%
Top route: Brussels → Rotterdam (margin 47%)
Worst route: Ghent → Amsterdam (margin 4.3%)
Top customer: Delhaize Group (margin 40%)
Lowest margin customer: Proximus (margin 19%)
Active vehicles: 8 | Trips this month: 54
"""


@router.post("/ask")
async def ask_ai(body: AskRequest):
    if not body.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty")

    if not settings.openai_api_key:
        return {
            "answer": (
                "AI assistant is not configured yet. "
                "Set OPENAI_API_KEY in your .env file to enable it. "
                f"Your question was: {body.question}"
            ),
            "model": "stub",
        }

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a logistics profitability analyst assistant for a Belgian transport company. "
                        "Answer questions based on the company data provided. "
                        "Respond in the same language as the question (French, Dutch, or English). "
                        "Be concise and factual.\n\n"
                        f"Company data:\n{STUB_CONTEXT}"
                    ),
                },
                {"role": "user", "content": body.question},
            ],
            max_tokens=500,
            temperature=0.3,
        )
        return {
            "answer": response.choices[0].message.content,
            "model": "gpt-4o",
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {e}")
