from openai import OpenAI
import os

ocr_text = "test"
prompt_text = f"Without giving excess information take a speculative guess at what this ocr text is meant to say. Output as markdown so I can easily copy and paste it: {ocr_text}"

client = OpenAI(

)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{prompt_text}",
        }
    ],
    model="gpt-3.5-turbo",
)

# Printing the response
answer = chat_completion.choices[0].message.content
print(answer)