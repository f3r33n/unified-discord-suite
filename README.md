# unified-discord-suite
An intelligent, dual-agent Discord framework built using Python and the Cohere LLM API. This project showcases how a single natural language processing engine can be dynamically altered using Python to deploy completely different interactive user experiences within a server or via private Direct Messages (DMs).

 Moonday(bot alpha) & Oracle(bot beta) 

An intelligent, dual-agent Discord framework built using Python and the Cohere LLM API. This project showcases how a single natural language processing engine can be dynamically altered using Python to deploy completely different interactive user experiences within a server or via private Direct Messages (DMs).

 🤖 The Ecosystem Agents

Our framework deploys two highly specialized conversational agents running simultaneously off the same API keys but executing fundamentally distinct prompt parameters.

1. Moonday (The Playful Companion)
*   Design Role: Community Engagement & Entertainment.
*   Behavior Matrix: Sarcastic, highly humorous, playful, and witty.
*   Execution Profile: Moonday answers user questions up to a moderate complexity level but prioritizes keeping server channels active and entertaining. It injects personality and banter into conversations, making it an excellent fit for general discussion channels.

2. Oracle (The Knowledge Base)
*   Design Role: High-Utility Academic Assistance.
*   Behavior Matrix: Serious, analytical, hyper-focused, and highly intelligent.
*   Execution Profile: Oracle strips away all humor, fluff, and sarcasm. It interacts with deep precision, analyzing user queries comprehensively. It is built to answer complex technical, theoretical, or informational questions with minimal noise, serving as a pristine support tool.


 🛠️ How it Works

Both bots operate using asynchronous runtime event loops managed via `discord.py`. They continuously monitor gateway intents—listening for direct tags within public server channels or incoming private DMs. 

1. Ingestion: Python intercepts incoming strings from the Discord gateway.
2. Payload Restructuring: The text is dynamically packaged alongside deep, custom instructions specific to the persona being triggered (Moonday's humor parameters vs. Oracle's logic constraints).
3. API Routing: Python forwards the asynchronous payload to the Cohere natural language processing model.
4. Dispatch: The parsed response is securely piped back and sent to the corresponding chat channel or private DM.


   Optimization Mechanics

Both bots operate using asynchronous runtime event loops managed via `discord.py` to monitor active server text streams and incoming private DMs. 

# 💡 Core Optimization Features:
* Token Conservation Layer: To prevent unnecessary and costly API token consumption, Monday runs on a hybrid framework. It intercepts input strings locally to process custom commands and formatted static structural replies instantly, bypassing the AI backend whenever possible.
* Autonomous Interjection Control: Rather than requiring explicit user pings every time, both agents utilize ambient context-awareness. They analyze the local text environment asynchronously, evaluating conditions to dynamically determine if they should jump into the discussion or stay passive.
* Secure API Routing: When dynamic generation is necessary, Python restructures the payload text with targeted system personality variables and forwards it securely via environment variables (`.env`) to the "Cohere NLP model".

  
 📂 Repository Layout

```text
astromind-ecosystem/
├── README.md               <- Project presentation & architectural overview
├── requirements.txt         <- Core package dependencies
├── bot_alpha/               <- Monday source directory
│   └── main.py              
└── bot_beta/                <- Oracle source directory
    └── main.py
