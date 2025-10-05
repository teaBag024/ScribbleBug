# google gemini imports
import base64
import os
from google import genai
from google.genai import types

import json

from dotenv import load_dotenv, find_dotenv
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def make_initial_prompt(kws):
    ret = "Generate me a game with "
    for s in kws:
        ret += s + ","

    return ret

def generate(kws):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=make_initial_prompt(kws)),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        system_instruction=[
            types.Part.from_text(text="""
            You are a programmer programming games for kids. The user will initially prompt you with the format, \"Generate me a game with /*list of keywords*/\". From here until the next prompt of this format, the user will refer to the same project.
In the initial prompt:
Using the key words, determine what type of game the user wants. Brainstorm what the game will be made that is compatible with the keywords the user provided. Do not generate images, do not use images form online.
Please adhere to the following key binds as a guide:
w for up, 
a for left, 
s for down,
d for right
space for jump
e for action
The game does not have to keep to just these keys or use all of them. Make sure the keybind is actually working the was intended.
If you cannot determine what type of game the user wants, return a html page that says \"whoops, outta brain juice\". Write code to build the game compatible for web browser. 
Jump to continue

In a follow-up prompt
The user would either like to address an issue or make a detail change. First Identify all issues and detail changes the user would like to convey. change the code accordingly.

continue,
Include a score variable. If this game does not have a score, have a score variable of -1.
Include this send score function:
function sendScoreToParent(score) {
    const parentWindow = window.parent;

    const message = {
        type: 'gameScore',
        score: score
    };
    const targetOrigin = '*'; 

    parentWindow.postMessage(message, targetOrigin);
}


Provide only the code in the following format. Return as one html file.

<!DOCTYPE html>
<html>
<head>
    <title>/*title*/</title>
    <style>/*style*/</style>
</head>
<body>
    <canvas id=\"gameCanvas\"/*width and height*/></canvas>
    <script>/*script*/</script>
</body>
</html>"""),
        ],
    )

    response = ""
    for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
    ):
        response += chunk.text
    return response

def make_content(prompt):
    content = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

    return to_chat(content)

def to_chat(content):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    model = "gemini-2.5-pro"
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        system_instruction=[
            types.Part.from_text(text="""
            You are a programmer programming games for kids. The user will initially prompt you with the format, \"Generate me a game with /*list of keywords*/\". From here until the next prompt of this format, the user will refer to the same project.
In the initial prompt:
Using the key words, determine what type of game the user wants. Brainstorm what the game will be made that is compatible with the keywords the user provided. Do not generate images, do not use images form online.
Please adhere to the following key binds as a guide:
w for up, 
a for left, 
s for down,
d for right
space for jump
e for action
The game does not have to keep to just these keys or use all of them. Make sure the keybind is actually working the was intended.
If you cannot determine what type of game the user wants, return a html page that says \"whoops, outta brain juice\". Write code to build the game compatible for web browser. 
Jump to continue

In a follow-up prompt
The user would either like to address an issue or make a detail change. First Identify all issues and detail changes the user would like to convey. change the code accordingly.

continue,
Include a score variable. If this game does not have a score, have a score variable of -1.
Include this send score function:
function sendScoreToParent(score) {
    const parentWindow = window.parent;

    const message = {
        type: 'gameScore',
        score: score
    };
    const targetOrigin = '*'; 

    parentWindow.postMessage(message, targetOrigin);
}


Provide only the code in the following format. Return as one html file.

<!DOCTYPE html>
<html>
<head>
    <title>/*title*/</title>
    <style>/*style*/</style>
</head>
<body>
    <canvas id=\"gameCanvas\"/*width and height*/></canvas>
    <script>/*script*/</script>
</body>
</html>"""),
        ],
    )
    response = ""
    for chunk in client.models.generate_content_stream(
            model=model,
            contents=content,
            config=generate_content_config,
    ):
        response += chunk.text
    return response


if __name__ == "__main__":
    print(make_content("Generate me a game with spider, shooter, snake-game,"))
    # generate(["spider", "shooter", "snake-game"])