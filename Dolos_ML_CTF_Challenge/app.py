from flask import Flask, render_template, redirect, url_for, request, jsonify
import subprocess
import re
import argparse
import sys

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.disabled = True

__header__ = """
Running...

╔╦╗╔═╗╦  ╔═╗┌─┐  ╔╦╗╦    ╔═╗╔╦╗╔═╗  ╔═╗┬ ┬┌─┐┬  ┬  ┌─┐┌┐┌┌─┐┌─┐
 ║║║ ║║  ║ ║└─┐  ║║║║    ║   ║ ╠╣   ║  ├─┤├─┤│  │  ├┤ ││││ ┬├┤ 
═╩╝╚═╝╩═╝╚═╝└─┘  ╩ ╩╩═╝  ╚═╝ ╩ ╚    ╚═╝┴ ┴┴ ┴┴─┘┴─┘└─┘┘└┘└─┘└─┘

Author: Alex Devassy
Access http://127.0.0.1:5000/
Category: Prompt Injection Attack
Description: Flag is at same directory as of flask app, [FLAG].txt.
Press Ctrl+C to quit
"""

print(__header__)

user_input = None

class _InjectionDetectionResult:
    def __init__(self, injection_detected):
        self.injectionDetected = injection_detected

class LocalRebuff:
    """Built-in stand-in for the hosted Rebuff prompt-injection detector
    (playground.rebuff.ai has been discontinued, so no Rebuff API key is
    needed). Flags obvious injection attempts with simple heuristics so the
    challenge flow stays the same as with the original service."""

    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior|above)",
        r"disregard",
        r"system\s+prompt",
        r"jailbreak",
        r"you\s+are\s+now",
        r"__import__",
        r"\bsubprocess\b|\bos\.(system|popen)\b",
        r"\b(eval|exec|execfile|import)\b",
        r"open\s*\(",
        r"flag",
        r"\.txt\b",
        r"\bfile\b",
        r"\b(ls|cat|rm|sudo)\b",
    ]

    def detect_injection(self, user_input):
        detected = any(
            re.search(pattern, user_input, re.IGNORECASE)
            for pattern in self.INJECTION_PATTERNS
        )
        return _InjectionDetectionResult(detected)

def remove_ansi_escape_codes(input_text):
    # Pattern to match ANSI escape codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    # Replace ANSI escape codes except newline characters
    cleaned_result = ansi_escape.sub('', input_text)
    return cleaned_result

def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global user_input
    if request.form.get('message'):
        user_input = request.form.get('message')
        result = rb.detect_injection(user_input)
        if result.injectionDetected:
            response_data = {'result': "Possible injection detected."}
        else:
            redirect_url = '/chat'
            response_data = {'response_result': "Verified", 'redirect_url': redirect_url}
        return jsonify({'response': response_data})
    elif request.form.get('value'):
        value = request.form.get('value')
        try:
            command = f'"{sys.executable}" aiexecuter.py --user_input="{user_input}" --api_key="{openaiapikey}"'
            # Run the subprocess
            rawresult = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            cleaned_result = remove_ansi_escape_codes(rawresult.stdout)
            result = cleaned_result
            if not rawresult.stdout:
                result = rawresult.stderr
        except Exception as e:
            result = "I’m good at solving about the math related problems. Other stuff, not so good."
            print(e)
        return render_template('index.html', response_data=result)
    else:
        print("Final Else")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask application")
    parser.add_argument('--openaikey', type=str, help='OpenAI/Idun API Key')
    args = parser.parse_args()
    openaiapikey = args.openaikey
    if openaiapikey is not None:
        rb = LocalRebuff()
        app.run(host="0.0.0.0", port=5000)
        app.run(debug=True)
    else:
        print("Please provide API Key to proceed")
