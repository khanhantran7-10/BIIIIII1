import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Title and Headers
content = content.replace(
    "<title>Hệ Thống BI & Quản Trị Kinh Doanh Số 5 Bước (Zero-Data & Schema-Agnostic)</title>",
    "<title>Smart BI Studio - Hệ Thống Quản Trị Kinh Doanh Số 4 Bước</title>"
)
content = content.replace(
    '<span class="pipeline-tag">Pipeline 5 Bước • Zero-Data & Schema-Agnostic 100%</span>',
    '<span class="pipeline-tag">Pipeline 4 Bước Chuẩn Quản Trị • Zero-Data & Schema-Agnostic 100%</span>'
)
content = content.replace(
    '<span id="nav-unlocked-status">Trắng hoàn toàn (Clean Slate • Bước 1/5)</span>',
    '<span id="nav-unlocked-status">Trắng hoàn toàn (Clean Slate • Bước 1/4)</span>'
)
content = content.replace(
    '<div class="sidebar-section-title">PIPELINE 5 BƯỚC TUẦN TỰ</div>',
    '<div class="sidebar-section-title">PIPELINE 4 BƯỚC TUẦN TỰ</div>'
)

# 2. Add New Styles right before </style>
new_styles = """
        /* Executive Dashboard Header Bar (Step 4) */
        .dash-exec-header {
            background: #ffffff;
            border: 1px solid var(--border-card);
            border-radius: 14px;
            padding: 20px 24px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        }
        .dash-exec-left {
            flex: 1;
            min-width: 280px;
        }
        .dash-badge-row {
            display: flex;
            gap: 8px;
            align-items: center;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }
        .badge-step-num {
            background: #2563eb;
            color: #ffffff;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 6px;
            letter-spacing: 0.5px;
        }
        .badge-scenario {
            background: #eff6ff;
            color: #1e40af;
            border: 1px solid #bfdbfe;
            font-size: 12px;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 6px;
        }
        .badge-scenario.scenario-a { background: #eff6ff; color: #1e40af; border-color: #bfdbfe; }
        .badge-scenario.scenario-b { background: #f0fdf4; color: #166534; border-color: #bbf7d0; }
        .badge-scenario.scenario-c { background: #faf5ff; color: #6b21a8; border-color: #e9d5ff; }
        .badge-file {
            background: #f8fafc;
            color: #475569;
            border: 1px solid #e2e8f0;
            font-size: 12px;
            font-weight: 500;
            padding: 3px 10px;
            border-radius: 6px;
        }
        .dash-exec-title {
            font-size: 21px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.3px;
            margin-bottom: 4px;
        }
        .dash-exec-sub {
            font-size: 13.5px;
            color: #475569;
            line-height: 1.5;
        }
        .dash-exec-right {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 10px;
        }
        .dash-actions-row {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }
        .dash-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 9px 16px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s ease;
            border: 1px solid transparent;
            text-decoration: none;
        }
        .dash-btn.btn-secondary {
            background: #ffffff;
            color: #334155;
            border-color: #cbd5e1;
        }
        .dash-btn.btn-secondary:hover {
            background: #f8fafc;
            border-color: #94a3b8;
            color: #0f172a;
        }
        .dash-btn.btn-primary-shine {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
            border: none;
        }
        .dash-btn.btn-primary-shine:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
            transform: translateY(-1px);
        }
        .dash-auto-row {
            display: flex;
            align-items: center;
        }
        .dash-auto-label {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: #64748b;
            cursor: pointer;
            user-select: none;
        }
        .dash-auto-label input {
            accent-color: #2563eb;
        }
        .num-col {
            text-align: right !important;
            font-variant-numeric: tabular-nums !important;
            white-space: nowrap;
        }
"""
if ".dash-exec-header" not in content:
    content = content.replace("    </style>", new_styles + "\n    </style>")

# 3. Enhance .quad-card styles
old_quad = """.quad-card.star { border-left: 4px solid #10b981; }
        .quad-card.cow { border-left: 4px solid #0284c7; }
        .quad-card.trap { border-left: 4px solid #f59e0b; }
        .quad-card.burner { border-left: 4px solid #ef4444; }"""
new_quad = """.quad-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .quad-card.star { border-left: 4px solid #10b981; background: linear-gradient(135deg, #ffffff 60%, #f0fdf4 100%); }
        .quad-card.cow { border-left: 4px solid #0284c7; background: linear-gradient(135deg, #ffffff 60%, #f0f9ff 100%); }
        .quad-card.trap { border-left: 4px solid #f59e0b; background: linear-gradient(135deg, #ffffff 60%, #fffbeb 100%); }
        .quad-card.burner { border-left: 4px solid #ef4444; background: linear-gradient(135deg, #ffffff 60%, #fef2f2 100%); }"""
content = content.replace(old_quad, new_quad)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Step 1 & 2 applied.")
