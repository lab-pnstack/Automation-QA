# Test Dashboard

Your test results are automatically published to GitHub Pages after each test run.

## 📊 View Dashboard

**Live Dashboard:** https://npv2k1.github.io/Automation-QA/

The dashboard shows:
- ✅ Test execution metrics (pass/fail/error counts)
- 📈 Pass rate trends over time
- 🔍 Detailed test case results
- 📦 Module-based filtering
- 🕐 Test history with run comparisons

## 🔄 Auto-Update

The dashboard automatically updates after:
- CI Automation Tests complete
- Smoke Tests complete
- Regression Tests complete

## 🚀 Manual Deployment

To manually deploy the dashboard:

```bash
# Trigger the workflow
gh workflow run deploy-dashboard.yml
```

Or go to: Actions → Deploy Test Dashboard → Run workflow

## 📁 Local Dashboard

To run the dashboard locally:

```bash
# Install Flask
pip install flask

# Run the dashboard server
cd dashboard
python app.py

# Open browser
open http://localhost:5000
```

The local dashboard reads from `reports/history/` directory.

## 🎨 Features

- **Real-time Metrics** - Latest test run statistics
- **Pass Rate Donut** - Visual pass/fail distribution
- **Status Breakdown** - Detailed status counts
- **Module View** - Filter by test modules
- **Run History** - Compare multiple test runs
- **Trend Chart** - Pass rate over time
- **Test Case Table** - Searchable and filterable
- **Modal Details** - Deep dive into specific runs

## 📝 Report Files

After each test run, the following files are generated:

- `reports/history/index.json` - List of all test runs
- `reports/history/{run_id}.json` - Detailed results for each run
- `reports/report_{browser}.html` - HTML test report
- `screenshots/*.png` - Failure screenshots

## 🔗 Integration

The dashboard is automatically linked in:
- GitHub Actions summary
- Pull request comments (when enabled)
- README badges (optional)

## 🛠️ Customization

To customize the dashboard:

1. Edit `dashboard/templates/dashboard.html`
2. Modify styles in the `<style>` section
3. Update JavaScript logic as needed
4. Commit changes - dashboard auto-deploys

## 📊 API Endpoints (Local)

When running locally with Flask:

- `GET /` - Dashboard UI
- `GET /api/runs` - List all test runs
- `GET /api/run/{run_id}` - Get specific run details

## 🌐 GitHub Pages Setup

The dashboard is deployed to GitHub Pages automatically. To enable:

1. Go to Settings → Pages
2. Source: GitHub Actions
3. The workflow handles the rest

Already configured in `.github/workflows/deploy-dashboard.yml`
