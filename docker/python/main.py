import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
import os

# main app object
app = FastAPI()

class Mail(BaseModel):
    sender: str
    dest: str
    subject: str
    message: str


@app.get("/mail")
def process_get():
  return {'status': 'mail server online'}

@app.post("/mail")
def process_post(mail: Mail):
  if not mail.sender or not mail.dest or not mail.subject or not mail.message:
    raise HTTPException(status_code=400, detail="Invalid data structure")

  mail_body = "Subject: %s\n\n%s" % (
     mail.subject,
     mail.message
  )

  # connecting to mail server
  try:
    smtpObj = smtplib.SMTP(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT'))
    smtpObj.sendmail(mail.sender, [mail.dest], mail_body)
  except  Exception as err:
    raise HTTPException(status_code=422, detail=err)
     

  return {'status': 'mail sent'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")