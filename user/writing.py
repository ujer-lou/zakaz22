from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
import openai
import traceback

app = FastAPI()
openai.api_key = "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"


@app.post("/submit-response/")
async def submit_response_from_django(task_id: int = Form(...), response: str = Form(...)):
    try:
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user",
                 "content": f"Review this IELTS response and find mistakes and and give like IELTS answer like  {response}"}
            ]
        )
        print(chat_response.choices[0].message['content'])
        return JSONResponse(status_code=200, content={
            "task_id": task_id,
            "response": response,
            "evaluation": chat_response.choices[0].message['content']
        })


    except Exception as e:
        traceback.print_exc()
        if hasattr(e, 'response') and e.response:
            print(e.response.text)
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/generate-task/")
async def generate_task(type: str):
    try:
        prompt = {
            "task1": "Generate an IELTS Writing Task 1 prompt.",
            "task2": "Generate an IELTS Writing Task 2 prompt.",
            "fulltest": "Generate both an IELTS Writing Task 1 and Task 2 prompts."
        }.get(type, None)

        if prompt is None:
            return {"error": "Invalid task type."}

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an IELTS writing task generator."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"task": response.choices[0].message['content']}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
