# 🧑‍⚖️ Legal Advice Chatbot (Streamlit + LLaMA 3 via Ollama)

This is an AI-powered legal assistant chatbot built using **Streamlit** and **Ollama** with the **LLaMA 3** model. The chatbot provides responses to general legal questions in an interactive web interface. It runs entirely **locally** using open-source models—no API key required!

---

## 🔍 Features

- ⚖️ Ask legal questions or describe your case.
- 💡 AI-powered responses via LLaMA 3 using Ollama.
- 📄 Option to upload a document (e.g., legal notice, contract).
- 🌐 Simple and clean Streamlit interface.
- 🧠 Works offline after model is downloaded via Ollama.

---

## 📦 Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) (for running LLaMA 3 locally)
- Streamlit
- Requests

---

## 🛠️ Setup Instructions

### ✅ Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/legal-advice-chatbot.git
cd legal-advice-chatbot
```

---

### ✅ Step 2: Install Python Dependencies

Make sure you're in a virtual environment (recommended), then run:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit requests
```

---

### ✅ Step 3: Install & Run Ollama

> Ollama lets you run open-source large language models like LLaMA 3 **locally**.

1. Download Ollama from [https://ollama.com](https://ollama.com)  
2. Install and start Ollama
3. Open a terminal and pull the model:

```bash
ollama run llama3
```

This command downloads and runs the model. Keep this terminal window running in the background.

---

### ✅ Step 4: Run the Streamlit App

In your project folder, start the chatbot:

```bash
streamlit run app.py
```

The chatbot will open in your default browser at:

```
http://localhost:8501
```

---

## 🧪 Example Prompt

> "What IPC section applies to fraud?"  
> "Can I get bail in a domestic violence case?"

---

## 📂 Project Structure

```
legal-advice-chatbot/
├── app.py               # Streamlit web app
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── .gitignore           # Ignore files (optional)
```

---

## ⚠️ Disclaimer

> This chatbot is built for educational and prototyping purposes only. It does **not** offer professional legal advice. Always consult a qualified attorney for any legal matters.

---

## 🪪 License

This project is licensed under the **MIT License**. Feel free to use and modify it.

---

## 🤝 Contributions

PRs and feedback are welcome! If you find issues or want to add features, feel free to contribute.

---

## 📬 Contact

For any queries, feel free to reach out via GitHub or open an issue.

```
