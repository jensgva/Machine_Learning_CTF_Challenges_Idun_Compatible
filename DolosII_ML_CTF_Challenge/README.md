# Dolos II ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to think like Greek god DOLOS and trick the LLM to reveal the flag. 

![Alt text](Images/Banner1.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench: 

##### :point_right: Step 1 - Getting API Keys

For hosting this challege, openai API key is required.

1. OpenAI-compatible API: use an OpenAI API key or an Idun API key. For Idun, use `https://llm.hpc.ntnu.no/v1` as the base URL and choose a chat model such as `openai/gpt-oss-120b`.

:hand: :exclamation: :exclamation: ***Step 2 can be either building the docker image of application (Step2a) OR setting up the application in local machine (Step2b).*** :no_entry_sign:

##### :point_right: Step 2a - Building Docker Image of the Application To Host The Challenge

`cd Machine_Learning_CTF_Challenges/DolosII_ML_CTF_Challenge/`

`docker build -t dolosll_ml_ctf .`

To run with Idun: `docker run --rm -p 5000:5000 -e OPENAI_BASE_URL="https://llm.hpc.ntnu.no/v1" -e OPENAI_MODEL="openai/gpt-oss-120b" -ti dolosll_ml_ctf --openaikey="<IDUN_API_KEY>"`

### OR

##### :point_right: Step 2b - Setting Up Python Flask App To Host The Challenge

The challenge works best in `Ubuntu` systems with `Python 3.8.10`

Create virtual enviornment in python using `python -m venv virtualspace`

Activate the virtual enviornemnt `source /virtualspace/bin/activate`

`git clone https://github.com/alexdevassy/Machine_Learning_CTF_Challenges.git`

`cd Machine_Learning_CTF_Challenges/DolosII_ML_CTF_Challenge/`

`pip install -r .\requirements.txt` 

`OPENAI_BASE_URL=https://llm.hpc.ntnu.no/v1 OPENAI_MODEL=openai/gpt-oss-120b python3 app.py --openaikey="<IDUN_API_KEY>"`

Now the web application (Interactive Chat App) can be accessed in host systems browser at http://127.0.0.1:5000/

<kbd>![Alt text](Images/Web_App.PNG?raw=true "Web_app")</kbd>

#### Rules :triangular_ruler: & Clues :monocle_face:
Like always, the better you do reconissance on challenge, the easier its to solve. Otherwise you may run into rabbit holes pretty quickly.

Dont peek :eyes: into the source code and logs from server are only for debugging purposes dont let them spoil your CTF experience.

For solution to CTF challenge visit : [DolosII_CTF_Solution](Solution/)

