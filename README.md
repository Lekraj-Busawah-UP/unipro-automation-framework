[![Unipro Automation Suite](https://github.com/Lekraj-Busawah-UP/unipro-automation-framework/actions/workflows/automation.yml/badge.svg)](https://github.com/Lekraj-Busawah-UP/unipro-automation-framework/actions/workflows/automation.yml)

[**View Live Allure Report**](https://lekraj-busawah-up.github.io/unipro-automation-framework/)

# Unipro BDD Automation Framework

A scalable automated testing framework built with **Python**, **Behave (BDD)**, and **Selenium**.

## Architecture
- **Page Object Model (POM):** Separation of test logic and page locators.
- **Reporting:** Integrated with Allure for rich HTML reports.
- **CI/CD:** GitHub Actions pipeline configured for Headless Chrome.

## Setup & Usage

### 1. Prerequisites
- Python 3.10+
- Chrome Browser
- Allure Commandline (only needed to generate/serve HTML reports locally). This is a separate Java-based CLI, distinct from the `allure-behave`/`allure-python-commons` pip packages, which only produce the raw `allure-results` data.
  - Requires a Java Runtime (JRE 8+) on your `PATH`.
  - Without admin rights: install via [Scoop](https://scoop.sh/) (no elevation needed):
    ```powershell
    irm get.scoop.sh | iex
    scoop bucket add java
    scoop install temurin21-jre allure
    ```
  - With admin rights: `winget install --id EclipseAdoptium.Temurin.21.JRE -e` then `npm install -g allure-commandline`, or see the official Allure install docs.
  - After installing, restart your terminal (or VS Code) so the updated `PATH` is picked up, then verify with `allure --version`.

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Running Tests

**Option A: Using the Helper Script (Recommended)**
This script runs the tests, automatically configures the Allure report output, and lets you view the results immediately. Any arguments you pass are forwarded directly to `behave`, so all native Behave options (feature files, tags, scenario names, etc.) work here too.

```bash
# Run all tests
python run.py

# Run a specific feature file
python run.py features/homepage.feature

# Run multiple feature files
python run.py features/homepage.feature features/footer.feature

# Run a single scenario by name (matches the Scenario title)
python run.py features/who_we_are.feature --name="Hero section renders on desktop"

# Run scenarios with a specific tag
python run.py --tags=@mobile

# Run scenarios matching ANY of the tags (OR)
python run.py --tags=@mobile,@desktop

# Run scenarios matching ALL of the tags (AND)
python run.py --tags=@smoke --tags=@whatwedo

# Exclude a tag (NOT)
python run.py --tags=~@wip

# Combine a feature file with a tag filter
python run.py features/what_we_do.feature --tags=@smoke

# Dry run - validates that every step has a matching step definition
# without actually launching a browser or executing any steps
python run.py --dry-run
```

**Cross-browser runs**
If [configurations/config.ini](configurations/config.ini)'s `browser` value lists more than one browser (e.g. `browser = chrome, firefox`), `run.py` automatically repeats the same command once per browser, sequentially, with no extra flags needed:

```bash
# With browser = chrome, firefox in config.ini, this runs on Chrome, then Firefox
python run.py --tags=@homepage
```

Each browser gets its own Allure results folder (`allure-results-chrome`, `allure-results-firefox`, ...) so reports never mix between browsers. With only one browser configured, results still go to the single `allure-results` folder as before. See [Configuration](#4-configuration) and [Manually Generating/Serving Reports](#manually-generatingserving-reports) below.

> Note: this only applies to local runs via `run.py`. The CI pipeline always runs against the first browser listed in `config.ini`, regardless of how many are configured (see [CI/CD & Reporting](#cicd--reporting)).

**Option B: Using Native Behave Commands**
If you prefer running raw commands without the helper script:

```bash
# Run tests (Console output only, no report file saved)
behave

# Run a specific feature file
behave features/homepage.feature

# Run tests filtered by tag
behave --tags=@smoke

# Run tests filtered by tag, hiding scenarios/steps that were skipped
# (by default, behave still lists every non-matching scenario as "skipped")
behave --tags=@smoke --no-skipped

# Run a single Scenario Outline Examples row by its line number
behave features/what_we_do.feature:34

# Run multiple specific rows
behave features/what_we_do.feature:34 features/what_we_do.feature:35

# Dry run - validates step definitions without executing anything
behave --dry-run

# Run tests and generate Allure report data
behave -f allure_behave.formatter:AllureFormatter -o allure-results

# View the generated HTML report
allure serve allure-results
```

### Available Tags
Scenarios are tagged by feature area, page section, test type (e.g. `@smoke`, `@content`), and viewport (e.g. `@desktop`, `@mobile`). 

### 4. Configuration
Test settings live in [configurations/config.ini](configurations/config.ini):

```ini
[common info]
baseURL = https://www.unipro.io/
browser = chrome      # chrome | firefox, or a comma-separated list for cross-browser runs (e.g. chrome, firefox)
headless = false      # true | false
```

### Manually Generating/Serving Reports
`python run.py` prompts you to serve each generated report at the end of a run. To do it manually instead (e.g. after a run you didn't serve immediately), target the relevant results folder:

```bash
# Quick view (temporary local server, opens in your browser)
allure serve allure-results
allure serve allure-results-chrome
allure serve allure-results-firefox

# Persistent static report (e.g. for sharing)
allure generate allure-results-chrome --clean -o allure-report-chrome
allure open allure-report-chrome
```

## CI/CD & Reporting
This repository includes a GitHub Actions workflow that:
1. Runs tests on every Push/PR.
2. Generates an Allure Report.
3. Deploys the report to GitHub Pages.
