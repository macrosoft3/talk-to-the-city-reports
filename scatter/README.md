# Talk to the City (TttC) - Scatter Reports

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](../LICENSE.txt)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg)](https://openai.com/)

<img width="400" alt="Interactive scatter plot visualization" src="https://github.com/AIObjectives/talk-to-the-city-reports/assets/3934784/57cc6367-0808-40f0-980a-540530ff0866">
<img width="400" alt="Cluster analysis report" src="https://github.com/AIObjectives/talk-to-the-city-reports/assets/3934784/aaf45844-5a19-41c8-8943-78866db9f666">

## What is Talk to the City?

Talk to the City (TttC) is an AI-powered pipeline that transforms CSV files containing public comments into interactive, multilingual HTML reports. The system uses state-of-the-art natural language processing to:

✅ **Extract** key arguments from thousands of comments  
✅ **Cluster** similar viewpoints using semantic analysis  
✅ **Label** and summarize each cluster automatically  
✅ **Visualize** data as an interactive scatter plot map  
✅ **Translate** reports into multiple languages

**Live Examples:**

- [Recursive Public](https://tttc.dev/recursive) - Pol.is data with voting consensus filters
- [GenAI Taiwan](https://tttc.dev/genai) - Bilingual report (English/Mandarin) from Taiwan's public consultation
- [Heal Michigan](https://tttc.dev/heal-michigan) - Community dialogue analysis

Developed by the [AI Objectives Institute](http://aiobjectives.org), a non-profit research organization focused on AI alignment. Read more in our [blog post](https://ai.objectives.institute/blog/talk-to-the-city-an-open-source-ai-tool-to-scale-deliberation).

## ⚠️ AI Safety Disclaimer

TttC is a research project exploring generative AI for public deliberation. **Large Language Models (LLMs) have known biases and can produce unreliable results.** We actively work to mitigate these issues but provide no guarantees at this stage.

**Do not rely solely on this pipeline's results for impactful decisions without independent verification.**

## 🚀 Quick Start

### Prerequisites

Before starting, ensure you have:

- **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
- **Node.js & npm** for report visualization ([Download](https://nodejs.org/))
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))
- **Git LFS** for large example files ([Install guide](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage))
- Your data in **CSV format** with required columns (see [CSV Format](#csv-format))

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AIObjectives/talk-to-the-city-reports.git
   cd talk-to-the-city-reports/scatter
   ```

2. **Set up Python environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -c "import nltk; nltk.download('stopwords')"
   ```

3. **Install Node.js dependencies:**

   ```bash
   cd next-app
   npm install
   cd ..
   ```

4. **Configure OpenAI API key:**

   ```bash
   cd pipeline
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

   > 💡 **Security Note:** Never commit your `.env` file to version control. It's already listed in `.gitignore`.

## 📊 Usage

### Run with Example Data

Test the pipeline with included example datasets:

```bash
cd pipeline
python main.py configs/example-polis.json
```

This processes `inputs/example-polis.csv` (4 comments) and generates a report in `outputs/example-polis/report/`.

**Other examples:**

- `example-videos.json` - Includes video timestamp features

### Generate Your Own Report

#### Step 1: Prepare Your Data

Create a CSV file with these required columns:

| Column         | Type   | Description                        |
| -------------- | ------ | ---------------------------------- |
| `comment-id`   | string | Unique identifier for each comment |
| `comment-body` | string | The actual comment text            |

**Optional columns:** `agree`, `disagree`, `video`, `interview`, `timestamp` (see [CSV Format](#csv-format))

Copy your CSV to the inputs folder:

```bash
cp /path/to/your/data.csv pipeline/inputs/my-project.csv
```

#### Step 2: Create Configuration File

Copy and customize the example config:

```bash
cp pipeline/configs/example-polis.json pipeline/configs/my-project.json
```

Edit `my-project.json`:

```json
{
  "name": "My Project Name",
  "question": "What is the main discussion topic?",
  "input": "my-project",
  "model": "gpt-3.5-turbo",
  "extraction": {
    "limit": 1000,
    "workers": 3
  },
  "clustering": {
    "clusters": 8
  },
  "translation": {
    "languages": ["Spanish", "French"],
    "flags": ["ES", "FR"]
  }
}
```

#### Step 3: Run the Pipeline

```bash
cd pipeline
python main.py configs/my-project.json
```

**Pipeline Options:**

- `-f` - Force re-run all steps (ignore cache)
- `-o <step>` - Run only a specific step
- `-skip-interaction` - Skip confirmation prompt

**Example:**

```bash
python main.py configs/my-project.json -f
```

## 📱 View & Deploy Your Report

### Local Preview

Your generated report is in `pipeline/outputs/my-project/report/`. Serve it locally:

```bash
# From project root directory
npm install -g http-server
http-server -p 8080
open http://localhost:8080/pipeline/outputs/my-project/report/
```

### Deploy to Production

The report is a static website—deploy anywhere:

**Recommended platforms:**

- [Vercel](https://vercel.com/) - `vercel deploy pipeline/outputs/my-project/report`
- [Netlify](https://www.netlify.com/) - Drag & drop the `report` folder
- [GitHub Pages](https://pages.github.com/) - Commit and push to `gh-pages` branch
- Any static host (AWS S3, Azure Storage, etc.)

> ⚠️ **Important:** The HTML uses relative paths. Include trailing slashes in URLs (e.g., `https://example.com/report/`) for proper asset loading.

## 🔧 Pipeline Architecture

The pipeline consists of 9 sequential steps:

| Step                 | Input           | Output              | Description                               |
| -------------------- | --------------- | ------------------- | ----------------------------------------- |
| 1. **Extraction**    | CSV comments    | `args.csv`          | Extract key arguments using LLM           |
| 2. **Embedding**     | Arguments       | `embeddings.pkl`    | Convert text to vectors                   |
| 3. **Clustering**    | Embeddings      | `clusters.csv`      | Group similar arguments (UMAP + BERTopic) |
| 4. **Labelling**     | Clusters        | `labels.csv`        | Generate descriptive labels               |
| 5. **Takeaways**     | Clusters        | `takeaways.csv`     | Extract key insights                      |
| 6. **Overview**      | All data        | `overview.txt`      | Generate executive summary                |
| 7. **Translation**   | Text content    | `translations.json` | Translate to target languages             |
| 8. **Aggregation**   | All outputs     | `result.json`       | Combine all data                          |
| 9. **Visualization** | Aggregated data | `report/`           | Build interactive HTML report             |

Each step caches results—only re-runs when dependencies or parameters change.

---

## 📝 CSV Format

### Required Columns

| Column         | Type   | Description       | Example                         |
| -------------- | ------ | ----------------- | ------------------------------- |
| `comment-id`   | string | Unique identifier | `"C001"`, `"12345"`             |
| `comment-body` | string | Comment text      | `"AI should prioritize safety"` |

### Optional Columns

| Column      | Type   | Description      | Example                             |
| ----------- | ------ | ---------------- | ----------------------------------- |
| `agree`     | number | Upvote count     | `42`                                |
| `disagree`  | number | Downvote count   | `7`                                 |
| `video`     | string | Video URL        | `"https://youtube.com/watch?v=..."` |
| `interview` | string | Interviewee name | `"Jane Doe"`                        |
| `timestamp` | string | Video timestamp  | `"00:15:30"`                        |

**Example CSV:**

```csv
comment-id,comment-body,agree,disagree
C001,"AI development needs ethical guidelines",128,12
C002,"Focus on AI safety is paramount",95,8
C003,"We should pause AI development",45,67
```

## ⚙️ Configuration Reference

### Required Parameters

```json
{
  "input": "my-data", // CSV filename (without .csv)
  "question": "Discussion topic?" // Main question asked to participants
}
```

### Optional Parameters

#### Global Settings

```json
{
  "name": "Project Name", // Display name (optional)
  "intro": "**Markdown** intro", // Project introduction (optional)
  "model": "gpt-3.5-turbo" // Default LLM model
}
```

#### Step-Specific Configuration

**Extraction**

```json
"extraction": {
  "model": "gpt-4",             // Override global model
  "prompt_file": "custom",      // Custom prompt (in prompts/extraction/)
  "prompt": "Extract...",       // Or provide full prompt text
  "limit": 1000,                // Max comments to process
  "workers": 3                  // Parallel workers (1-10)
}
```

**Clustering**

```json
"clustering": {
  "clusters": 8                 // Number of topic clusters (default: 8)
}
```

**Labelling & Takeaways**

```json
"labelling": {
  "model": "gpt-4",
  "sample_size": 30             // Arguments per cluster for labeling
},
"takeaways": {
  "sample_size": 30             // Arguments per cluster for insights
}
```

**Translation**

```json
"translation": {
  "model": "gpt-4",             // Use better model for translations
  "languages": ["Spanish", "Mandarin", "French"],
  "flags": ["ES", "TW", "FR"]   // ISO country codes for flags
}
```

**Visualization**

```json
"visualization": {
  "replacements": [             // Text replacements in UI
    {"replace": "AI", "by": "Artificial Intelligence"}
  ]
}
```

### Custom Prompts

Store custom prompts in `pipeline/prompts/<step>/`:

- `extraction/` - Argument extraction prompts
- `labelling/` - Cluster labeling prompts
- `takeaways/` - Key insights prompts
- `overview/` - Summary generation prompts
- `translation/` - Translation instructions

Reference in config with `"prompt_file": "your-file-name"` (without `.txt`).

## 📂 Output Structure

After successful execution, find outputs in `pipeline/outputs/my-project/`:

```
outputs/my-project/
├── args.csv              # Extracted arguments from comments
├── embeddings.pkl        # Vector embeddings (for caching)
├── clusters.csv          # Cluster assignments for each argument
├── labels.csv            # Generated labels for each cluster
├── takeaways.csv         # Key insights per cluster
├── overview.txt          # Executive summary
├── translations.json     # All translated content
├── result.json           # Aggregated data (used by report)
├── status.json           # Pipeline execution status
└── report/               # 🌐 Interactive HTML report
    ├── index.html
    ├── _next/            # Next.js assets
    └── [cluster-pages].html
```

**Key Files:**

- **`result.json`** - Complete aggregated data used by visualization
- **`status.json`** - Tracks completed steps, parameters, and timing
- **`report/`** - Deploy this folder to your hosting service

> 💡 Intermediate files (CSV/PKL) are cached. Re-run with different config to skip unchanged steps.

## 🐛 Troubleshooting

### Common Issues

**"Job already running and locked"**

```bash
rm pipeline/outputs/my-project/.lock
```

**Import errors after updating dependencies**

```bash
pip install --upgrade -r requirements.txt
```

**LangChain import errors**

- Update imports: `from langchain_openai import ChatOpenAI, OpenAIEmbeddings`
- Use `.invoke()` instead of calling LLM directly: `llm.invoke(messages)`

**Memory errors with large datasets**

- Reduce `extraction.limit` in config
- Lower `extraction.workers` count
- Process in batches

### API Rate Limits

If hitting OpenAI rate limits:

1. Reduce `extraction.workers` to `1`
2. Use `gpt-3.5-turbo` instead of `gpt-4`
3. Add delays between requests (modify `steps/extraction.py`)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas needing help:**

- 🛡️ Improved error handling and retry logic
- ⚡ Performance optimizations
- 📝 Better documentation
- 🧪 Test coverage
- 🌍 Additional language support

Before starting major work, please [open an issue](https://github.com/AIObjectives/talk-to-the-city-reports/issues) or contact the AI Objectives Institute.

---

## 📚 Resources

- **Documentation:** [Full API docs](https://github.com/AIObjectives/talk-to-the-city-reports)
- **Blog:** [Scaling Deliberation with AI](https://ai.objectives.institute/blog/talk-to-the-city-an-open-source-ai-tool-to-scale-deliberation)
- **Examples:** [Live Reports](https://tttc.dev)
- **Community:** [GitHub Discussions](https://github.com/AIObjectives/talk-to-the-city-reports/discussions)

---

## 👥 Credits & Maintainers

**Developed by:** [AI Objectives Institute](http://aiobjectives.org)

**Contributors:**

- [@Klingefjord](https://github.com/Klingefjord) - Early pipeline development
- [@lightningorb](https://github.com/lightningorb) - Core architecture
- Recursive Public team (Chatham House, vTaiwan, OpenAI) - Example datasets

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see [LICENSE.txt](../LICENSE.txt) for details.

---

## 🔗 Related Projects

- **[tttc-light-js](https://github.com/AIObjectives/tttc-light-js)** - Active development (Next-generation version)
- **[TttC Turbo](../turbo/)** - Graph-based reports application (TypeScript)

> **Note:** This repository (Scatter Reports) is in maintenance mode. Active development continues in tttc-light-js.
