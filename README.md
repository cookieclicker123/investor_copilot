# Investor Copilot

## Vision

This repository showcases an example of using AI agents, LLM's, and finance API's to create an AI Agent for an investor.
Equipped with capabiltiies such as drawing from internal pdf knowledge bases that are self building, utilising Serper API for 
relavent and timely market news + events, and imbueing the LLm with access to alpha vantage for real time prices , and other metrics
regarding specific sotcks and sectors. With specialised intent recognition for each agent, the need for to rely on massive models such as 
claude for quality answers using the right agent/s goes away, and we instead utilise discrete spacy named entity recognition models (NER's)
to take care of the complex job of decyphering intent. Smaller models using the groq API becomes viabale as we remove the need for it to
understand user intent, and even using small local llama models becomes a possibility, democratising access to quality AI agent automation software
without sacrifcing money, time , data privacy and third party external api dependcencies that come along with closed source models.
The report agent allows users to upload financial documents and have them analysed, using tools such as pdf indexers, calculators, and more.
we then automate the job of sending reports of to important people by using the embodied agent which has mouse and click functionalities, 
making this thing truly agentic and end to end in nature. Not only will this tool be amazing for education and advisory that is non judemental,
indefatiguable and 24/7 available, but you can actively generate reports, and have them sent to your boss for example, and be required only for 
the natural langiage prompt, and send off confirmation. This means no interfaces are required between you and informaiton, and you can accomplish 
in hours what would take days in a standard finance firm, making you fundmanetlaly more efficient. We will also extend functionality to API's such as 
Trading 212 and interactive brokers, allowing people to interact through natural language with these trading platforms, and recieve real time analsysis
and advice on what to do in the markets, whether long term or this very minute, you have a copilot automating every step of the way.

## Plan of action

- Build the data model which will define the API signatures for the whole code base.
- Make mock LLM and a Mock front end( make sure you see ability to attach files) , testing every step of the way.
- Once this works, hooke chainlit up with a fast api server for the backend, making communciaiton for the front end and back end simple.
- begin to implement real moving parts, beginning with agent selection logic, and a real system prompt.
- Add in the three intial agents , along with their tools, and create the code for the pdf knowledge base, and hook up the external API's.
- Add in conversation memory as well as the prompts for each agent and the meta agent which coorindates them.
- Add in the logic for the workpad which the meta agent scribbles down its plans to.
- make sure follow ups, if they dont match selection logic for any agent type, are treated as follow ups to the last 1000 tokens, or last question for
example, so that conversations flow naturally.
- Add in functionality to use different types of LLM's.
- Add in pdf report functionality, allowing users to attach pdfs, and have them analysed by the report agent.
- Add the embodied agent, which is triggered when the user requests the doing of a task requiring mouse and click funcitonality, whether it be sending or reports to
bosses or coworkers, or having websties scraped and reviewed in real time, even trading platforms.
- Create a simple database which stores the reports and info created or retrieved by the report + embodied agents, as well as adding in memory peristence, with the dual aim of learning about the user and tailoring future answers to them.

## Inital setup

```bash
git clone
cd investor_copilot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir tmp
```

## index the PDF's into the knowledge base

```bash
python knowledge_base/pdf_to_json.py

python knowledge_base/json_to_index.py
```

## Run in terminal

```bash
python main.py
```
