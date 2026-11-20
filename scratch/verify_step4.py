import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Check key DOM elements
required_ids = [
    "view-step-1", "view-step-2", "view-step-3", "view-step-4",
    "step-tab-1", "step-tab-2", "step-tab-3", "step-tab-4",
    "dash-scenario-badge", "dash-file-badge", "auto-download-docx",
    "adaptive-kpi-container", "system-alert-badge",
    "kpi-count-star", "kpi-count-cow", "kpi-count-trap", "kpi-count-burner",
    "timeTrendChart", "channelBarChart", "categoryDonutChart", "matrixScatterChart",
    "scorecard-dim-switcher", "scorecard-search", "scorecard-quad-filter", "scorecard-alert-filter",
    "step5-scorecard-table", "step5-scorecard-thead", "step5-scorecard-tbody",
    "pivot-row-select", "pivot-col-select",
    "p-btn-1", "p-btn-2", "p-btn-3", "p-content-1", "p-content-2", "p-content-3",
    "p-tbody-1", "p-tbody-2", "p-tbody-3",
    "playbook-highlights-list", "playbook-bottlenecks-list", "playbook-actions-list",
    "ai-messages-container", "ai-prompt-input"
]

missing = [i for i in required_ids if f'id="{i}"' not in content]
if missing:
    print("MISSING IDs:", missing)
else:
    print("ALL REQUIRED DOM IDs FOUND!")

# Check if Chart.getChart is used
if "Chart.getChart" in content:
    print("Chart.getChart verified.")
else:
    print("WARNING: Chart.getChart not found!")

# Check if formatMoney is defined globally
if "const formatMoney =" in content:
    print("formatMoney verified.")
else:
    print("WARNING: formatMoney not found!")

print("File size:", len(content), "bytes")
