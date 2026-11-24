# 🧪 AI-Powered Test Log Analyzer

A Python-based application that analyzes automated software test logs, identifies failures, calculates test execution statistics, and uses AI to generate troubleshooting recommendations.

Built with **Python, Pandas, Streamlit, and GroqCloud**, this project demonstrates automated log analysis, AI integration, interactive dashboard development, and software testing.

## Features

- **Upload Test Logs:** Analyze `.log` and `.txt` files through the Streamlit dashboard.
- **Paste Logs:** Paste log lines directly for quick analysis.
- **Automated Parsing:** Extract timestamps, test statuses, and messages from structured logs.
- **Test Statistics:** Calculate total tests, passed tests, failed tests, and pass rates.
- **Failure Detection:** Associate failed tests with their error messages.
- **AI-Powered Troubleshooting:** Generate explanations, two possible root causes, and three troubleshooting steps using GroqCloud.
- **Interactive Dashboard:** View metrics, charts, and expandable failure details.
- **JSON Export:** Download analysis reports, including AI recommendations when available.
- **Automated Testing:** Verify application behavior using pytest and mocked API responses.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Pandas | Data processing and analysis |
| Streamlit | Interactive web dashboard |
| GroqCloud API | AI-powered failure analysis |
| GPT-OSS 20B | Language model used for troubleshooting |
| python-dotenv | Environment variable management |
| pytest | Automated unit testing |
| unittest.mock | Testing API integration without real requests |

## How It Works

1. The user uploads a test log file or pastes log text.
2. The application parses the log entries using regular expressions.
3. Pandas processes the entries and calculates test statistics.
4. Failed tests are associated with relevant error messages.
5. The user can optionally request AI-powered troubleshooting.
6. The application displays the results and provides a downloadable JSON report.

## Example Input

```text
2026-11-23 11:00:01 PASS LoginTest
2026-11-23 11:00:02 FAIL CheckoutTest
2026-11-23 11:00:03 ERROR Payment gateway timeout
2026-11-23 11:00:04 PASS LogoutTest
```

## Example Analysis Results

| Metric | Result |
|---|---:|
| Total Tests | 3 |
| Passed | 2 |
| Failed | 1 |
| Pass Rate | 66.67% |

**Detected failure:** `CheckoutTest`

**Error message:** `Payment gateway timeout`

The optional AI analysis provides a short explanation, two possible causes, and three troubleshooting steps. AI-generated suggestions are diagnostic guidance, not confirmed root causes.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/AlSult/ai-powered-test-log-analyzer.git
cd ai-powered-test-log-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your Groq API key:

```dotenv
GROQ_API_KEY=your_actual_api_key
```

Never commit your `.env` file or share your API key publicly.

### 5. Generate the sample analysis report

```bash
python report_generator.py
```

This creates `reports/analysis.json` using the included sample log and requests AI analysis for detected failures.

A configured Groq API key and network access are required for AI analysis.

### 6. Start the Streamlit dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, typically `http://localhost:8501`.

## Running Automated Tests

Run the complete test suite:

```bash
python -m pytest tests/ -v
```

The project currently includes **15 automated tests** covering:

- Log parsing and invalid input handling
- Test statistics and empty datasets
- Failure-to-error association
- AI response validation
- Mocked Groq API responses
- Empty and malformed AI responses

The mocked API tests do not require real Groq API requests.

## Project Structure

```text
ai-powered-test-log-analyzer/
├── app.py
├── ai_analyzer.py
├── data_analyzer.py
├── log_parser.py
├── report_generator.py
├── requirements.txt
├── .env.example
├── .gitignore
├── logs/
│   └── sample.log
├── reports/
│   └── analysis.json
└── tests/
    ├── test_log_parser.py
    ├── test_data_analyzer.py
    └── test_ai_analyzer.py
```

## Current Limitations

- The parser currently supports structured log lines using the format `YYYY-MM-DD HH:MM:SS STATUS Message`.
- Supported statuses are `INFO`, `PASS`, `FAIL`, and `ERROR`.
- Error association relies on the order of log entries.
- AI recommendations may be inaccurate and should be verified against actual system evidence.
- The application requires a Groq API key for AI troubleshooting.

## Future Improvements

- Support additional log formats and testing frameworks.
- Add filtering and searching within log results.
- Export reports in PDF format.
- Add automated GitHub Actions testing.
- Support larger log files and batch analysis.

## Security and Privacy

Only use sample or sanitized logs for AI troubleshooting. When AI analysis is requested, test names and error messages are sent to GroqCloud. Avoid submitting passwords, access tokens, personal data, or confidential production logs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.