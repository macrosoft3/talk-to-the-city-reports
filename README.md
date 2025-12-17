# Talk to the City

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE.txt)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node.js-18+-green.svg)](https://nodejs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](https://openai.com/)

Talk to the City (TttC) is an AI-powered open-source platform that transforms public comments, surveys, and deliberations into interactive, multilingual reports. Built by the [AI Objectives Institute](http://aiobjectives.org), it uses state-of-the-art natural language processing and large language models to extract insights, identify consensus, and visualize perspectives at scale.

## Table of Contents

- [Quick Overview](#quick-overview)
- [What You Can Build](#what-you-can-build)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Support & Resources](#support--resources)
- [Contributing](#contributing)
- [License](#license)

## Quick Overview

Talk to the City consists of two complementary applications:

### 🔄 **Scatter Reports** (Python + Next.js)

CLI-based report generation producing static, interactive scatter-plot visualizations with AI-generated summaries.

**Live examples:**

- [Recursive Public](https://tttc.dev/recursive)
- [GenAI Taiwan](https://tttc.dev/genai)
- [Heal Michigan](https://tttc.dev/heal-michigan)

### 🎯 **Turbo** (TypeScript + Svelte)

Graph-based computational pipeline application for building complex LLM-powered reports with real-time collaboration and customizable workflows.

**Live examples:**

- [Heal Michigan](https://tttc-turbo.web.app/report/heal-michigan-9)
- [Taiwan same-sex marriage](https://tttc-turbo.web.app/report/taiwan-zh)
- [Mina protocol](https://tttc-turbo.web.app/report/mina-protocol)

## What You Can Build

✨ **Extract** key arguments from thousands of comments using AI  
🗂️ **Cluster** similar viewpoints through semantic analysis  
🏷️ **Label** and summarize clusters automatically  
📊 **Visualize** data as interactive scatter plots or custom dashboards  
🌍 **Translate** reports into multiple languages  
🔗 **Build** complex AI pipelines with dependency graphs

### ⚠️ AI Safety Disclaimer

TttC is a research project exploring generative AI for public deliberation. **Large Language Models (LLMs) have known biases and can produce unreliable results.** While we actively work to mitigate these issues, we provide no guarantees at this stage.

**Do not rely solely on this pipeline's results for impactful decisions without independent verification.**

## Project Structure

```
talk-to-the-city-reports/
├── scatter/               # Scatter Reports application (Python + Next.js)
│   ├── pipeline/          # AI processing pipeline
│   ├── next-app/          # Report visualization frontend
│   └── configs/           # Configuration files for projects
├── turbo/                 # Turbo application (TypeScript + Svelte)
│   ├── src/
│   │   ├── lib/           # Compute functions and utilities
│   │   ├── components/    # Svelte UI components
│   │   └── routes/        # SvelteKit routes
│   └── static/            # Static assets
└── LICENSE.txt            # Apache 2.0 License
```

## Getting Started

Choose the application that best fits your needs:

### Option 1: Scatter Reports (Simpler, Recommended for CSV Input)

Perfect for transforming CSV files with public comments into interactive reports.

**Prerequisites:**

- Python 3.10+
- Node.js 18+ with npm
- [OpenAI API key](https://platform.openai.com/api-keys)
- [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)

**Quick Start:**

```bash
# Clone and navigate
git clone https://github.com/AIObjectives/talk-to-the-city-reports.git
cd talk-to-the-city-reports/scatter

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords')"

# Install Node.js dependencies
cd next-app && npm install && cd ..

# Configure OpenAI API
cd pipeline && echo "OPENAI_API_KEY=your-api-key-here" > .env && cd ..

# Run with example data
cd pipeline && python main.py configs/example-polis.json
```

**View your report:**

```bash
npm install -g http-server
http-server -p 8080
# Open http://localhost:8080/pipeline/outputs/example-polis/report/
```

**Generate your own report:**

1. Prepare a CSV file with columns: `comment-id`, `comment-body` (and optional: `agree`, `disagree`, `video`, `interview`, `timestamp`)
2. Copy to `pipeline/inputs/my-project.csv`
3. Create `pipeline/configs/my-project.json` (copy from `example-polis.json`)
4. Run: `python main.py configs/my-project.json`

📖 See [scatter/README.md](scatter/README.md) for detailed documentation.

### Option 2: Turbo (Advanced, Graph-Based Pipelines)

For building complex, customizable LLM-powered applications with real-time collaboration.

**Prerequisites:**

- Node.js 18+
- Firebase account (for deployment; local dev also supported)
- Google Cloud credentials (optional, for cloud features)

**Quick Start:**

```bash
# Clone and navigate
git clone https://github.com/AIObjectives/talk-to-the-city-reports.git
cd talk-to-the-city-reports/turbo

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Fill in your Firebase and configuration details

# Start development server
npm run dev
```

**Available commands:**

```bash
npm run dev          # Start development server (http://localhost:5173)
npm run build        # Build for production
npm run preview      # Preview production build
npm test             # Run tests
npm run lint         # Check code formatting
npm run format       # Format code
```

📖 See [turbo/README.md](turbo/README.md) for advanced setup, Firebase configuration, and deployment instructions.

## Support & Resources

### Documentation

- **Scatter Reports:** [scatter/README.md](scatter/README.md) - Complete setup, usage, and pipeline architecture
- **Turbo:** [turbo/README.md](turbo/README.md) - Advanced configuration, Firebase setup, and development guide
- **Contributing:** [scatter/CONTRIBUTING.md](scatter/CONTRIBUTING.md) and [turbo/CONTRIBUTOR_GUIDE.md](turbo/CONTRIBUTOR_GUIDE.md)

### Getting Help

- **Issues & Bugs:** [GitHub Issues](https://github.com/AIObjectives/talk-to-the-city-reports/issues)
- **Discussions:** [GitHub Discussions](https://github.com/AIObjectives/talk-to-the-city-reports/discussions)
- **Contact:** Reach out to [AI Objectives Institute](http://aiobjectives.org)

### Learning Resources

- **Blog Post:** [Talk to the City: An Open-Source AI Tool to Scale Deliberation](https://ai.objectives.institute/blog/talk-to-the-city-an-open-source-ai-tool-to-scale-deliberation)
- **AI Pipeline Guide:** [AI Pipeline Engineering Guide #1](https://tttc-turbo.web.app/docs/ai-pipe-guide)
- **User Docs:** [tttc-turbo.web.app/docs](https://tttc-turbo.web.app/docs)

## Contributing

We welcome contributions from the open-source community! Before starting work on major features, please:

1. Check [GitHub Issues](https://github.com/AIObjectives/talk-to-the-city-reports/issues) for existing work
2. Review the contribution guidelines:
   - [Scatter CONTRIBUTING.md](scatter/CONTRIBUTING.md)
   - [Turbo CONTRIBUTOR_GUIDE.md](turbo/CONTRIBUTOR_GUIDE.md)
3. Reach out to [AI Objectives Institute](http://aiobjectives.org) before starting substantial work

**Ways to contribute:**

- 🐛 Report bugs and request features
- 📝 Improve documentation
- ✨ Add new pipeline steps or components
- 🌍 Add language translations
- 🧪 Write tests and improve robustness
- 🚀 Optimize performance

## Development

### Code Quality

Both projects enforce code standards:

- **TypeScript/Svelte (Turbo):** ESLint, Prettier, TypeScript strict mode
- **Python (Scatter):** Black formatter recommended

Run formatters before submitting PRs:

```bash
# Turbo
npm run format
npm run lint

# Scatter
# Format Python files with Black
black pipeline/
```

### Running Tests

```bash
# Turbo
npm test                 # Run all tests
npm run test-watch      # Watch mode
npm run test-ui         # UI with coverage

# Scatter
# Tests run as part of the pipeline
```

## Technology Stack

### Scatter Reports

- **Backend:** Python 3.10+, LangChain, OpenAI API, UMAP, BERTopic
- **Frontend:** Next.js, React, Tailwind CSS
- **ML/NLP:** scikit-learn, spaCy, sentence-transformers

### Turbo

- **Frontend:** SvelteKit, Svelte, TypeScript, Tailwind CSS
- **State Management:** Stores, reactive variables
- **UI Components:** Svelte Material UI, SvelteFlow
- **Backend:** Firebase/Firestore, Google Cloud Storage
- **Testing:** Vitest, Svelte Testing Library

## License

This project is licensed under the **Apache License 2.0** - see [LICENSE.txt](LICENSE.txt) for details.

The Turbo application uses components licensed under **GPL v3** - see [turbo/LICENSE.md](turbo/LICENSE.md) for details.

## Maintainers

Maintained by the [AI Objectives Institute](http://aiobjectives.org), a non-profit research organization focused on AI alignment and beneficial AI research.
