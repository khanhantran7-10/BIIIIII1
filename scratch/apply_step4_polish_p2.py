import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace the old top banner in Step 4 with the Executive Header Bar
old_banner = """                <!-- Khung Nổi Bật Xuất Báo Cáo Quản Trị DOCX -->
                <div class="panel-box" style="padding:18px 24px; background: linear-gradient(135deg, #f0f7ff 0%, #f5fbf7 100%); border: 1.5px solid #bfdbfe; margin-bottom: 18px; box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08); border-radius: 12px;">
                    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
                        <div style="display:flex; align-items:center; gap:16px; min-width:280px; flex:1;">
                            <div style="font-size:38px; line-height:1; flex-shrink:0;">📄</div>
                            <div>
                                <div style="font-size:16px; font-weight:800; color:#0f172a; margin-bottom:4px;">
                                    Báo cáo Quản trị BI Hoàn chỉnh đã sẵn sàng
                                </div>
                                <div style="font-size:13.5px; color:#334155; line-height:1.5;">
                                    Đã tổng hợp toàn diện: Hồ sơ bối cảnh, Kiểm định chất lượng thô, Nhật ký làm sạch, Bảng đối chiếu Before/After, KPI & Unit Economics, Ma trận 4 góc và Actionable Playbook.
                                </div>
                            </div>
                        </div>
                        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                            <button type="button" onclick="openMappingModal()" class="btn btn-outline" style="font-size:13px; font-weight:700; padding:10px 18px; border-radius:8px; display:inline-flex; align-items:center; gap:6px; cursor:pointer; background:#ffffff; border:1.5px solid #2563eb; color:#2563eb;">
                                ⚙️ Tùy chỉnh cột dữ liệu
                            </button>
                            <label style="display:inline-flex; align-items:center; gap:6px; font-size:13px; font-weight:600; color:#334155; cursor:pointer; user-select:none;">
                                <input type="checkbox" id="auto-download-docx" style="accent-color:#2563eb; width:16px; height:16px;">
                                <span>Tự động tải về khi kết thúc</span>
                            </label>
                            <button onclick="exportReportDocx()" class="btn-primary" style="background:#2563eb; color:#ffffff; font-size:14px; font-weight:700; padding:12px 24px; border-radius:8px; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3); display:inline-flex; align-items:center; gap:8px; cursor:pointer; border:none;">
                                <span style="font-size:16px;">📥</span> Xuất Báo Cáo Quản Trị (.DOCX)
                            </button>
                        </div>
                    </div>
                </div>"""

new_banner = """                <!-- Executive Dashboard Header Bar (Step 4) -->
                <div class="dash-exec-header">
                    <div class="dash-exec-left">
                        <div class="dash-badge-row">
                            <span class="badge badge-step-num">BƯỚC 4</span>
                            <span class="badge badge-scenario" id="dash-scenario-badge">📊 Đang phân tích...</span>
                            <span class="badge badge-file" id="dash-file-badge" style="display:none;">📁 File dữ liệu</span>
                        </div>
                        <h2 class="dash-exec-title">Dashboard Quản Trị & Playbook Chiến Lược</h2>
                        <p class="dash-exec-sub">Tự thích nghi theo từng tập dữ liệu, phân nhóm ma trận 4 góc, cảnh báo điểm nghẽn & đề xuất hành động tối ưu kinh doanh số.</p>
                    </div>
                    <div class="dash-exec-right">
                        <div class="dash-actions-row">
                            <button type="button" onclick="openMappingModal()" class="dash-btn btn-secondary">
                                <span>⚙️</span> Tùy chỉnh cột
                            </button>
                            <button type="button" onclick="exportCleanData('xlsx')" class="dash-btn btn-secondary" title="Xuất dữ liệu sạch sang Excel">
                                <span>📊</span> Xuất Excel
                            </button>
                            <button type="button" onclick="exportCleanData('csv')" class="dash-btn btn-secondary" title="Xuất dữ liệu sạch sang CSV">
                                <span>📄</span> Xuất CSV
                            </button>
                            <button type="button" onclick="exportReportDocx()" class="dash-btn btn-primary-shine">
                                <span>📥</span> Xuất Báo Cáo Word (.DOCX)
                            </button>
                        </div>
                        <div class="dash-auto-row">
                            <label class="dash-auto-label">
                                <input type="checkbox" id="auto-download-docx">
                                <span>Tự động tải về báo cáo Word khi hoàn tất</span>
                            </label>
                        </div>
                    </div>
                </div>"""

if old_banner in content:
    content = content.replace(old_banner, new_banner)
    print("Replaced old top banner with Executive Header Bar.")
else:
    print("WARNING: Old banner not found by exact string, checking regex...")

# 2. Update Table Header & ID in Activity Scorecard
old_scorecard_table = """                    <div class="table-responsive" style="width: 100%; max-width: 100%; overflow-x: auto;">
                        <table class="bi-table">
                            <thead>
                                <tr>
                                    <th>Nhóm Hoạt Động</th>
                                    <th>Phân Nhóm Ma Trận</th>
                                    <th>Mức Cảnh Báo</th>
                                    <th>Doanh Thu</th>
                                    <th>Doanh Thu Thực Thu</th>
                                    <th>Số Đơn / Sản Lượng</th>
                                    <th>Đơn Hoàn</th>
                                    <th>Tỷ Lệ Hoàn (%)</th>
                                    <th>Lượt Truy Cập</th>
                                    <th>Tỷ Lệ Chuyển Đổi (%)</th>
                                    <th>Giá Trị TB Đơn (AOV)</th>
                                    <th>Chi Phí Ads</th>
                                    <th>Giá Vốn (COGS)</th>
                                    <th>Chi Phí/Đơn (CAC)</th>
                                    <th>Tỷ Lệ Chi Phí Ads (CIR %)</th>
                                    <th>Lợi Nhuận Ròng</th>
                                    <th>Biên Lợi Nhuận (%)</th>
                                    <th>Hiệu Quả Ads (ROAS)</th>
                                </tr>
                            </thead>
                            <tbody id="step5-scorecard-tbody"></tbody>
                        </table>
                    </div>"""

new_scorecard_table = """                    <div class="table-responsive" style="width: 100%; max-width: 100%; overflow-x: auto; border: 1px solid var(--border-card); border-radius: 8px;">
                        <table class="bi-table" id="step5-scorecard-table">
                            <thead id="step5-scorecard-thead">
                                <!-- Dynamic Scenario Header -->
                            </thead>
                            <tbody id="step5-scorecard-tbody"></tbody>
                        </table>
                    </div>"""

if old_scorecard_table in content:
    content = content.replace(old_scorecard_table, new_scorecard_table)
    print("Replaced Activity Scorecard Table markup.")
else:
    print("WARNING: Old scorecard table not found by exact string.")

# 3. Add global formatMoney, escapeHtml, and scheduleChartRender
old_format_line = """        const formatNum = (v) => (v === null || v === undefined || isNaN(v)) ? '--' : new Intl.NumberFormat('vi-VN', { maximumFractionDigits: 2 }).format(v);"""
new_format_block = """        const formatNum = (v) => (v === null || v === undefined || isNaN(v)) ? '--' : new Intl.NumberFormat('vi-VN', { maximumFractionDigits: 2 }).format(v);
        const formatMoney = (v) => (v === null || v === undefined || isNaN(v)) ? '--' : new Intl.NumberFormat('vi-VN', { maximumFractionDigits: 0 }).format(v) + ' đ';
        const escapeHtml = (str) => {
            if (str == null) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        };

        let _chartRenderTimeout = null;
        function scheduleChartRender() {
            if (_chartRenderTimeout) clearTimeout(_chartRenderTimeout);
            _chartRenderTimeout = setTimeout(() => {
                renderStep5Charts();
            }, 80);
        }"""

if old_format_line in content:
    content = content.replace(old_format_line, new_format_block)
    print("Added formatMoney, escapeHtml, and scheduleChartRender.")

# 4. Update goToStep(4) to use scheduleChartRender
content = content.replace("setTimeout(renderStep5Charts, 100);", "scheduleChartRender();")
content = content.replace("setTimeout(renderStep5Charts, 120);", "scheduleChartRender();")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("P2 completed successfully.")
