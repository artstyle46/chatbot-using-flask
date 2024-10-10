from flask import Blueprint, render_template
from flask import request
from openai import OpenAI
from dataclasses import dataclass

routes = Blueprint('routes', __name__)
api_key = "openai_api_key"
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key,
)

@dataclass
class Result:
    time: str
    messagetype: str
    message: str


def ask(question, chat_log=None):
    prompt = f'{chat_log}Human: {question}\nAI:'

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    answer = response.choices[0].message.content
    return answer


historyData = []
@routes.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        query = request.args.get('query')
        if query == "" or query is None:
            return render_template('response_view.html')
        response = ask(query)
        dataList = []
        queryMessage = Result(time="This Time", messagetype="other-message float-right", message=query)
        responseMessage = Result(time="This Time", messagetype="my-message", message=response)
        dataList.append(queryMessage)
        dataList.append(responseMessage)
        historyData.append(queryMessage)
        historyData.append(responseMessage)
        return render_template('response_view.html', results=dataList)
    else:
        return render_template('history.html', results=historyData)
