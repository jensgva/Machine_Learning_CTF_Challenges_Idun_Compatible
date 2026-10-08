# Dolos ML CTF Challenges

In this web application challenge, the :detective: security researcher needs to think like Greek god DOLOS and trick the LLM to reveal the flag. 

![Alt text](Images/Banner1.PNG?raw=true "Banner")

#### Setup :hammer_and_wrench: 

##### :point_right: Step 1 - Getting an API Key

Only **one** API key is required: an OpenAI-compatible **chat** API key.

1. **Idun (NTNU LLM HPC service)**: connect to the NTNU VPN, get your Idun API key (`sk-...`) and use `https://llm.hpc.ntnu.no/v1` as the base URL with one of the available chat models, e.g. `Inferact/GLM-5.3-NVFP4` (others: `Qwen/Qwen3.8-27B-FP8`, `moonshotai/Kimi-K2.6` — which models your key may use can vary; `Inferact/GLM-5.3-NVFP4` was verified working end to end).
2. **OpenAI**: a regular OpenAI API key also works (no extra configuration needed).

> :information_source: The original challenge also required a Rebuff API key. The hosted Rebuff service (playground.rebuff.ai) has been discontinued, so the app now ships with a small built-in local injection detector instead — no second key needed.

> :information_source: The original challenge ran on an unaligned OpenAI completion model. The modern chat models available today (GLM, Qwen, ...) are safety-aligned and do not follow every instruction in a prompt every single time — if a reply seems to skip part of your message, just send it again (in testing the models followed such instructions roughly every second to fourth attempt).

:hand: :exclamation: :exclamation: ***Step 2 can be either building the docker image of application (Step2a) OR setting up the application in local machine (Step2b).*** :no_entry_sign:

##### :point_right: Step 2a - Building Docker Image of the Application To Host The Challenge

Docker Desktop must be running. The commands below are for Windows PowerShell (on Linux/macOS, put the flags on one line without the backticks):

```powershell
cd path\to\Machine_Learning_CTF_Challenges_Idun_Compatible\Dolos_ML_CTF_Challenge\
docker build -t dolos_ml_ctf .
```

To run with Idun:

```powershell
docker run --rm -p 5000:5000 `
  -e OPENAI_BASE_URL="https://llm.hpc.ntnu.no/v1" `
  -e OPENAI_MODEL="Inferact/GLM-5.3-NVFP4" `
  -ti dolos_ml_ctf --openaikey="<IDUN_API_KEY>"
```

### OR

##### :point_right: Step 2b - Setting Up Python Flask App To Host The Challenge

The challenge relies on a legacy ML stack (`langchain` 0.0.x / `openai` 0.28 / `langchain-experimental` 0.0.14), which needs **Python 3.10–3.12**. Python 3.13+ will fail to install the dependencies. (On Windows, install a compatible Python first if needed: `winget install -e --id Python.Python.3.12`)

From a fresh PC, clone and set up the app:

```powershell
git clone https://github.com/jensgva/Machine_Learning_CTF_Challenges_Idun_Compatible.git
cd Machine_Learning_CTF_Challenges_Idun_Compatible\Dolos_ML_CTF_Challenge
python -m venv virtualspace
.\virtualspace\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

Run with Idun (PowerShell):

```powershell
$env:OPENAI_BASE_URL = "https://llm.hpc.ntnu.no/v1"
$env:OPENAI_MODEL = "Inferact/GLM-5.3-NVFP4"
python app.py --openaikey="<IDUN_API_KEY>"
```

or on Linux/macOS:

```bash
source virtualspace/bin/activate
OPENAI_BASE_URL=https://llm.hpc.ntnu.no/v1 OPENAI_MODEL=Inferact/GLM-5.3-NVFP4 python3 app.py --openaikey="<IDUN_API_KEY>"
```

Now the web application (Interactive Chat App) can be accessed in host systems browser at http://127.0.0.1:5000/

<kbd>![Alt text](Images/Web_App.PNG?raw=true "Web_app")</kbd>

#### Rules :triangular_ruler: & Clues :monocle_face:
Like always, the better you do reconissance on challenge, the easier its to solve. Otherwise you may run into rabbit holes pretty quickly.

For solution to CTF challenge visit : [Dolos_CTF_Solution](Solution/)

:no_entry_sign: A quick heads-up: The video below is contains CTF solution spoilers :sweat_smile:. So, if you're still up for the challenge and enjoy a bit of mystery, it might be best to steer clear of this one.  


https://github.com/alexdevassy/Machine_Learning_CTF_Challenges/assets/31893005/0b264da9-2259-4ed4-af47-61341134059b
