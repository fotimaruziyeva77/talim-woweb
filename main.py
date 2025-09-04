from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from loader import db
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Referral API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- MODELLAR ---
class UserProfile(BaseModel):
    full_name: Optional[str]
    telegram_id: int
    phone: Optional[str]
    referrals: int
    invited_by: Optional[int]

class Result(BaseModel):
    user_id: int
    question_id: int
    chosen_option_id: int
    correct: bool
    spent_time: float

class QuestionOption(BaseModel):
    id: Optional[int]  # DB da autoincrement bo'lishi mumkin
    text: str
    is_correct: bool

class Question(BaseModel):
    id: Optional[int]
    text: str
    options: List[QuestionOption]

# --- ENDPOINTLAR ---
@app.get("/profile/{telegram_id}", response_model=UserProfile)
def get_profile(telegram_id: int):
    user = db.get_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    full_name, telegram_id, phone, referrals, invited_by = user
    return UserProfile(
        full_name=full_name,
        telegram_id=telegram_id,
        phone=phone,
        referrals=referrals,
        invited_by=invited_by
    )


@app.post("/add-question", response_model=Question)
def add_question(question: Question):
    # Savolni DB ga qo‘shish
    question_id = db.add_question(question.text)
    options = []
    for option in question.options:
        option_id = db.add_option(question_id, option.text, option.is_correct)
        options.append(QuestionOption(id=option_id, text=option.text, is_correct=option.is_correct))
    return Question(id=question_id, text=question.text, options=options)


@app.post("/add-result", response_model=Result)
def add_result(result: Result):
    db.add_result(
        user_id=result.user_id,
        question_id=result.question_id,
        chosen_option_id=result.chosen_option_id,
        correct=result.correct,
        spent_time=result.spent_time
    )
    return result


@app.get("/get-question/{question_id}", response_model=Question)
def get_question(question_id: int):
    question = db.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    q_id, text = question
    options = db.get_options(q_id)
    return Question(
        id=q_id,
        text=text,
        options=[QuestionOption(id=o[0], text=o[1], is_correct=o[2]) for o in options]
    )
