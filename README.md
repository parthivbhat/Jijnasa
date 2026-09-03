#  Jijnasa

> **A personal technology intelligence and learning agent.**

Jijnasa is a personal AI-powered technology intelligence and learning agent built to help me **discover, understand, learn, remember, and share technology knowledge**.

It combines technology news, AI analysis, personal learning, Obsidian knowledge management, X content generation, and automated workflows into one personal system.

The goal is simple:

> **Turn information into knowledge.**

---

## ✨ What Jijnasa Does

Jijnasa has two primary workflows:

```text
                         JIJNASA
                              │
                ┌─────────────┴─────────────┐
                │                           │
           📰 NEWS PIPELINE            🧠 LEARNING
                │                           │
          RSS Sources                   User Input
                │                           │
        Collect Articles            "I learnt Docker"
                │                           │
         Deduplication                    Groq
                │                           │
             Ranking                Structured Learning
                │                           │
              Groq                          │
                │                           │
       Importance Filter                    │
                │                           │
             Gemini                         │
                │                           │
        Deep Analysis                       │
                │                           │
                └─────────────┬─────────────┘
                              │
                              ▼
                       🗂️ Obsidian
                              │
                              ▼
                         ✍️ X Content
```

---

## 📰 Current News Sources

Jijnasa currently supports:

- TechCrunch
- Ars Technica
- MIT News
- Hacker News
- IEEE Spectrum

The sources are configurable through:

```
config/sources.json
```

Example:

```json
{
  "news": {
    "TechCrunch": "https://techcrunch.com/feed/",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "MIT News": "https://news.mit.edu/rss/feed",
    "Hacker News": "https://news.ycombinator.com/rss",
    "IEEE Spectrum": "https://spectrum.ieee.org/feeds/feed.rss"
  }
}
```

This makes adding or removing RSS sources easy without modifying the Python code.

---

## 🔄 News Processing Pipeline

The complete news workflow is:

```
RSS Sources
     ↓
Collect Articles
     ↓
Deduplicate
     ↓
Process Articles
     ↓
Rank Candidates
     ↓
Groq Analysis
     ↓
Importance Filtering
     ↓
Gemini Deep Analysis
     ↓
Groq Fallback if Gemini Fails
     ↓
Save Important Stories
     ↓
Obsidian Knowledge Base
```

### 1. News Collection

Jijnasa collects articles from all configured RSS sources.

```
Collecting news...

Collecting from TechCrunch...
Collecting from Ars Technica...
Collecting from MIT News...
Collecting from Hacker News...
Collecting from IEEE Spectrum...

Collected: 150
```

The number of articles depends on the current RSS feeds.

### 2. Article Deduplication

Multiple sources may report the same technology story.

Jijnasa removes duplicate or highly similar articles before continuing through the pipeline.

```
150 Articles
      ↓
Deduplication
      ↓
Unique Articles
```

This reduces unnecessary processing and API usage.

### 3. Article Processing

Collected articles are normalized and prepared for analysis.

Information can include:

- Article title
- Source
- URL
- Publication date
- Description
- Category
- Content

This gives the later stages a consistent article structure.

### 4. Candidate Ranking

Jijnasa does not need to deeply analyze every collected article.

Instead, articles are ranked and a smaller number of promising candidates are selected.

```
Collected: 150
     ↓
Candidates: 5
```

This makes the system more efficient.

### 5. Groq News Analysis

Groq performs the first AI analysis of candidate articles.

It evaluates the articles and helps determine which stories are important.

```
Collected: 150
Candidates: 5
Groq analyzed: 5
Important: 3
```

Only important stories continue to deep analysis.

### 6. Importance Filtering

The importance filter reduces the number of stories that require deeper analysis.

```
150 collected
      ↓
5 candidates
      ↓
Groq analysis
      ↓
3 important stories
```

This saves API requests and focuses the system on useful technology developments.

### 7. Gemini Deep Analysis

Important stories are sent to Google Gemini for deeper analysis.

```
Starting Gemini deep analysis...

Deep analyzing 1/3
Deep analyzing 2/3
Deep analyzing 3/3

Deep analyzed: 3
```

Gemini is used as the deeper reasoning/analysis layer for important stories.

### 8. Groq Fallback

If Gemini fails because of:

- API quota
- Rate limits
- Temporary API errors
- Service availability

Jijnasa automatically falls back to Groq.

```
                    Gemini
                       │
              ┌────────┴────────┐
              │                 │
           Success            Failure
              │                 │
              ▼                 ▼
        Deep Analysis      Groq Fallback
                                │
                                ▼
                          Deep Analysis
```

This keeps the news pipeline running even when Gemini is unavailable.

```
Trying Gemini...
Gemini failed: 429 quota exceeded

Trying Groq fallback...
Groq fallback succeeded.

Finished [Groq Fallback]
```

### 9. Save to Obsidian

After deep analysis, important stories are saved as Markdown files.

```
obsidian/Jijnasa/News/
├── AI/
├── Business/
├── Cybersecurity/
├── Regulation/
└── Research/
```

---

## 🧠 Personal Learning Assistant

Jijnasa is also a personal learning assistant.

Instead of manually creating a learning note, I can simply tell Jijnasa what I learned.

```
Jijnasa > I learnt Docker
```

Jijnasa extracts the topic:

```
Docker
```

and sends it through the learning pipeline.

### 🧠 Structured Learning Notes

The learning pipeline uses Groq to generate structured technical knowledge.

Each learning note contains:

- 🧠 Concept
- 📖 Explanation
- 🔑 Key Points
- 💻 Example
- ⚠️ Common Mistakes
- 🎯 Interview Questions
- 🔗 Related Topics

Example:

```
Jijnasa > I learnt Docker

🧠 Learning: Docker

Calling Groq for learning...
Groq responded.
Learning JSON parsed successfully.

Saved learning:
obsidian/Jijnasa/Learning/Docker.md
```

The generated knowledge is then saved as Markdown.

### 📝 Learning JSON Structure

The learning model generates structured JSON similar to:

```json
{
  "concept": "",
  "explanation": "",
  "key_points": [],
  "example": "",
  "common_mistakes": [],
  "interview_questions": [
    {
      "question": "",
      "answer": ""
    }
  ],
  "related_topics": []
}
```

This structured approach makes the learning output predictable and easy to convert into Markdown.

### ✍️ Today I Learned — X Content

After generating structured learning content, Jijnasa can generate X-ready content.

Example:

```
Jijnasa > I learnt Docker
```

Output:

```
=== 𝕏 TODAY I LEARNED — POST ===

Today I learned that Docker is a platform for automating
application deployment using lightweight containers.

Containers package applications and their dependencies
so they can run consistently across environments.
```

Jijnasa can also generate a short thread:

```
=== 𝕏 TODAY I LEARNED — THREAD ===

1. Docker images are immutable snapshots, while containers
   are running instances of those images.

2. A Dockerfile is a recipe for building a Docker image.

3. Containers use OS-level isolation while sharing the
   host kernel, making them lighter than traditional VMs.
```

The workflow is:

```
Learning Topic
      ↓
Groq
      ↓
Structured Knowledge
      ↓
Markdown Note
      ↓
Obsidian
      ↓
X Post
      ↓
X Thread
```

---

## 🐦 X Content from Technology News

Jijnasa can also generate X-ready content from important technology news.

The workflow is:

```
Technology News
      ↓
Article Processing
      ↓
AI Analysis
      ↓
Importance Detection
      ↓
Deep Analysis
      ↓
X Content
```

This allows Jijnasa to transform technology information into content that can be shared.

---

## 🤖 AI Architecture

Jijnasa uses multiple AI components for different tasks.

```
                         JIJNASA
                              │
                 ┌────────────┴────────────┐
                 │                         │
              📰 NEWS                   🧠 LEARNING
                 │                         │
                Groq                      Groq
                 │                         │
        Importance Filter          Structured Learning
                 │                         │
              Gemini                       │
                 │                         │
          Deep Analysis                    │
                 │                         │
          Groq Fallback                    │
                 │                         │
                 └────────────┬────────────┘
                              │
                              ▼
                         🗂️ Obsidian
                              │
                              ▼
                         ✍️ X Content
```

### ⚡ Groq

Groq is the fast AI processing layer in Jijnasa.

It is used for:

- News analysis
- Learning generation
- Structured JSON generation
- X content generation
- Fallback deep analysis

The learning workflow is:

```
Topic
  ↓
Groq
  ↓
Structured JSON
  ↓
Markdown
```

Groq is useful for the fast stages of the system.

### ✨ Google Gemini

Google Gemini is used primarily for deeper analysis of important technology news.

The architecture intentionally does not send every collected article directly to Gemini.

Instead:

```
Many Articles
      ↓
Candidate Selection
      ↓
Groq Analysis
      ↓
Important Articles
      ↓
Gemini Deep Analysis
```

This helps reduce unnecessary API usage.

### 🔀 LLM Router

Jijnasa includes an LLM routing layer.

The router provides an abstraction between the application and individual LLM providers.

Conceptually:

```
                 Application
                      │
                      ▼
                 LLM Router
                      │
             ┌────────┴────────┐
             │                 │
            Groq             Gemini
             │                 │
        Fast Tasks        Deep Analysis
```

This architecture makes it easier to add additional model providers later.

### 🛡️ LLM Fallback Architecture

The system is designed so that failure of one provider does not necessarily stop the workflow.

```
                    Task
                     │
                     ▼
                  Gemini
                     │
              ┌──────┴──────┐
              │             │
           Success         Failure
              │             │
              ▼             ▼
          Continue          Groq
                              │
                              ▼
                           Continue
```

This is especially useful for free-tier API limits.

---

## 🗂️ Knowledge Management

Jijnasa uses Obsidian as its personal knowledge base.

Generated learning notes and analyzed news are stored as Markdown.

```
obsidian/
└── Jijnasa/
    ├── Learning/
    │   ├── Docker.md
    │   ├── Neural Networks.md
    │   └── Beam Search.md
    │
    └── News/
        ├── AI/
        ├── Business/
        ├── Cybersecurity/
        ├── Regulation/
        └── Research/
```

The personal Obsidian knowledge base is kept locally and is **not** included in the public GitHub repository.

Only the application code and configuration required to generate the knowledge are included in the repository.

---

## 📰 Configurable News Sources

RSS sources are stored separately from the application logic.

File:

```
config/sources.json
```

Example:

```json
{
  "news": {
    "TechCrunch": "https://techcrunch.com/feed/",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "MIT News": "https://news.mit.edu/rss/feed",
    "Hacker News": "https://news.ycombinator.com/rss",
    "IEEE Spectrum": "https://spectrum.ieee.org/feeds/feed.rss"
  }
}
```

This makes source management simple.

To add a source, add another entry:

```json
"Example Source": "https://example.com/rss"
```

To remove a source, remove its entry from the JSON file.

No Python code changes are required.

---

## 📡 News Collection

The RSS collector uses `feedparser` to read configured RSS feeds.

Conceptually:

```
sources.json
     ↓
RSS Collector
     ↓
feedparser
     ↓
Articles
```

The collector loops through all active sources.

```
Collecting from TechCrunch...
Collecting from Ars Technica...
Collecting from MIT News...
Collecting from Hacker News...
Collecting from IEEE Spectrum...
```

---

## 🧹 Article Processing

The news system contains separate components for:

- RSS collection
- Article processing
- Deduplication
- Ranking
- AI analysis
- Deep analysis
- Storage

This separation keeps the pipeline modular.

---

## 🧠 AI News Analysis

The AI analysis stage determines which stories are worth deeper processing.

```
Collected: 150
Candidates: 5
Analyzed: 5
Important: 3
```

This approach allows Jijnasa to process a large number of articles while deeply analyzing only the most relevant ones.

---

## ⏰ Daily News Automation

Jijnasa can run automatically using Linux cron.

Example cron schedule:

```
30 14 * * *
```

The automation runs:

```
run_daily_news.sh
        ↓
Jijnasa News Pipeline
        ↓
Collect
        ↓
Analyze
        ↓
Deep Analyze
        ↓
Save
```

Output can be redirected to a log file:

```
daily_news.log
```

Example cron configuration:

```
30 14 * * * /home/parthiv_setu/jijnasa/run_daily_news.sh >> /home/parthiv_setu/jijnasa/daily_news.log 2>&1
```

The exact schedule can be changed depending on the server's timezone and requirements.

---

## ▶️ Running Jijnasa

### Start Interactive Mode

Run:

```bash
python jijnasa.py
```

You will see:

```
 JIJNASA

Type something like: I learnt Docker
Type 'news' for today's news.
Type 'exit' to quit.

Jijnasa >
```

### 🧠 Learn Something

You can tell Jijnasa what you learned.

```
Jijnasa > I learnt Docker
```

It will:

```
Extract Topic
     ↓
Generate Learning
     ↓
Save Markdown
     ↓
Generate X Content
```

Other examples:

```
I learnt Kubernetes
I learned Docker networking
Today I learnt neural networks
```

### 📰 Run News

Inside interactive mode:

```
Jijnasa > news
```

Jijnasa will run the complete news pipeline.

```
=== JIJNASA NEWS ===

Collecting news...

Collected: 150
Candidates: 5
Analyzed: 5
Important: 3
Deep analyzed: 3
Saved: 3
```

### 💻 Direct Learning Command

Learning can also be executed directly from the terminal.

```bash
python jijnasa.py learn "Docker"
```

Another example:

```bash
python jijnasa.py learn "Neural Networks"
```

### 💻 Direct News Command

The news pipeline can also be executed directly:

```bash
python jijnasa.py news
```

### 🚪 Exit Interactive Mode

Inside Jijnasa:

```
Jijnasa > exit
```

or:

```
Jijnasa > quit
```

---

## 📁 Project Structure

```
Jijnasa/
│
├── app/
│   ├── __init__.py
│   │
│   ├── agent/
│   │   └── __init__.py
│   │
│   ├── content/
│   │   ├── __init__.py
│   │   ├── learning_x.py
│   │   └── x_generator.py
│   │
│   ├── learning/
│   │   ├── __init__.py
│   │   └── learner.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── gemini.py
│   │   ├── groq.py
│   │   └── router.py
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   └── obsidian.py
│   │
│   └── news/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── deduplicator.py
│       ├── deep_analyzer.py
│       ├── gemini_news.py
│       ├── pipeline.py
│       ├── processor.py
│       ├── ranker.py
│       └── rss_collector.py
│
├── config/
│   └── sources.json
│
├── jijnasa.py
│
├── requirements.txt
│
├── run_daily_news.sh
│
├── .env.example
│
├── .gitignore
│
└── README.md
```

---

## 🛠️ Tech Stack

**Programming Language**
- Python

**AI / LLM**
- Groq
- Google Gemini

**News Collection**
- RSS
- Feedparser

**Data Processing**
- JSON
- Regular Expressions
- Python data structures

**Knowledge Management**
- Obsidian
- Markdown

**Automation**
- Linux
- Cron
- Bash

**Development**
- Git
- GitHub
- Ubuntu Server
- Python Virtual Environment

---

## ⚙️ Installation

### 1. Clone the Repository

Using SSH:

```bash
git clone git@github.com:parthivbhat/Jijnasa.git
```

Then:

```bash
cd Jijnasa
```

HTTPS can also be used:

```bash
git clone https://github.com/parthivbhat/Jijnasa.git
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create your environment file:

```bash
cp .env.example .env
```

Add the required API keys to `.env`.

Example:

```
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Use the exact variable names expected by the application.

---

## 🔒 Security

API keys must never be committed to GitHub.

The project uses:

```
.env
```

for local secrets.

The repository includes:

```
.env.example
```

as a template.

The `.gitignore` file excludes:

```
.env
.venv/
```

and the personal Obsidian knowledge base.

> **Important**
> Never commit real API keys.
> If an API key is accidentally pushed to GitHub, revoke it and generate a new one.

---

## 🧪 Testing

The project contains tests for major components.

Current test files include:

```
app/test_gemini.py
app/test_groq.py
app/test_news.py
app/test_router.py
app/test_rss.py
```

Run the test suite with:

```bash
python -m pytest
```

---

## 🧩 Modular Architecture

Jijnasa is intentionally divided into modules.

```
News
 ├── Collector
 ├── Processor
 ├── Deduplicator
 ├── Ranker
 ├── Analyzer
 └── Deep Analyzer

Learning
 └── Learner

LLM
 ├── Groq
 ├── Gemini
 └── Router

Content
 ├── News/X Generator
 └── Learning/X Generator

Memory
 └── Obsidian
```

This makes individual components easier to improve or replace.

---

## 🔌 Extensibility

The architecture is designed to support future additions.

Potential additions include:

- More RSS sources
- More LLM providers
- Local AI models
- Better ranking algorithms
- Better duplicate detection
- Voice interaction
- More content platforms
- Smarter memory
- Learning history
- Personalized recommendations

---

## 📊 Example News Run

A typical Jijnasa news run looks like:

```
=== JIJNASA NEWS ===

Collecting news...
Collecting from TechCrunch...
Collecting from Ars Technica...
Collecting from MIT News...
Collecting from Hacker News...
Collecting from IEEE Spectrum...

Collected: 150
Candidates: 5
Groq analyzed: 5
Important: 3

Starting Gemini deep analysis...

Deep analyzing 1/3...
Trying Gemini...

Deep analyzing 2/3...
Trying Gemini...
Gemini failed...
Trying Groq fallback...
Groq fallback succeeded.

Deep analyzing 3/3...
Trying Gemini...
Gemini failed...
Trying Groq fallback...
Groq fallback succeeded.

Deep analyzed: 3

Saving to Obsidian...

Saved to Obsidian: 3

=== SUMMARY ===

Collected: 150
Candidates: 5
Analyzed: 5
Important: 3
Deep analyzed: 3
Saved: 3
```

---

## 📚 Example Learning Run

Example:

```
Jijnasa > I learnt Docker
```

Output:

```
🧠 Learning: Docker

Calling Groq for learning...
Groq responded.
Learning JSON parsed successfully.

Saved learning:
obsidian/Jijnasa/Learning/Docker.md

Generating learning X content...
Learning X content generated.

=== 𝕏 TODAY I LEARNED — POST ===

Today I learned that Docker is a platform for automating
application deployment using lightweight containers...

=== 𝕏 TODAY I LEARNED — THREAD ===

1. Docker images are immutable snapshots...
2. A Dockerfile is a recipe for building an image...
3. Containers provide isolation while sharing the host kernel...
```

---

## 🎯 Project Goal

Jijnasa is more than a news scraper.

The long-term goal is to build a personal technology intelligence system that continuously helps me:

```
        Discover
           ↓
        Understand
           ↓
          Learn
           ↓
        Remember
           ↓
          Share
```

The larger idea is:

```
Technology News
       +
Personal Learning
       +
Knowledge Management
       +
AI Analysis
       +
Content Generation
       ↓
Personal Technology Intelligence
```

---

## 🔮 Future Improvements

Planned or possible improvements include:

- [ ] Better news ranking
- [ ] Improved duplicate detection
- [ ] More RSS sources
- [ ] Smarter learning history
- [ ] Learning progress tracking
- [ ] Automatic daily learning summaries
- [ ] Better X threads
- [ ] More LLM providers
- [ ] Local AI models
- [ ] Voice interaction
- [ ] Agent-based workflows
- [ ] Richer Obsidian linking
- [ ] Personalized technology recommendations
- [ ] Improved news categorization
- [ ] Better source reliability scoring
- [ ] Search across personal knowledge
- [ ] Cross-linking between news and learning notes

---

## 🧭 Development Philosophy

Jijnasa is built around a simple principle:

> Don't just consume information. Build knowledge from it.

Instead of:

```
News
 ↓
Read
 ↓
Forget
```

Jijnasa aims for:

```
News
 ↓
Collect
 ↓
Analyze
 ↓
Understand
 ↓
Store
 ↓
Remember
 ↓
Share
```

The same idea applies to learning:

```
Learn
 ↓
Structure
 ↓
Store
 ↓
Review
 ↓
Share
```

---

## Why "Jijnasa"?

**Jijnasa (जिज्ञासा)** means curiosity or the desire to know and learn.

That idea is at the heart of the project.

**Stay Curious. Keep Learning. Build Knowledge.**

---

## 👨‍💻 Author

**Parthiv Bhat V S**

GitHub: [@parthivbhat](https://github.com/parthivbhat)

Repository: [https://github.com/parthivbhat/Jijnasa](https://github.com/parthivbhat/Jijnasa)

---

## ⭐ Final Note

Jijnasa is a personal project built to explore how AI can be combined with:

- Technology intelligence
- Personal learning
- Knowledge management
- Automation
- LLM routing
- Content generation

The project will continue evolving as new ideas and capabilities are added.

---

###  Jijnasa

*Stay curious. Keep learning. Build knowledge.*
