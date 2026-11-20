import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update renderStep5 to populate executive header badges and pass scenario
old_renderStep5_start = """        function renderStep5(step5) {
            if (!step5 || !step5.has_dashboard) return;

            const kpis = step5.kpis || {};
            renderAdaptiveKPIs(step5);"""

new_renderStep5_start = """        function renderStep5(step5) {
            if (!step5 || !step5.has_dashboard) return;

            // Cập nhật Executive Badges
            const fileInfo = pipelineData?.step2?.file_info;
            const fileBadge = document.getElementById('dash-file-badge');
            if (fileBadge) {
                if (fileInfo && fileInfo.filename) {
                    fileBadge.innerText = `📁 ${fileInfo.filename} (${fileInfo.row_count || 0} dòng)`;
                    fileBadge.style.display = 'inline-flex';
                } else {
                    fileBadge.style.display = 'none';
                }
            }

            const scBadge = document.getElementById('dash-scenario-badge');
            if (scBadge) {
                const sc = step5.scenario || 'A';
                if (sc === 'A') {
                    scBadge.innerText = '🛒 Kịch bản A: E-Commerce & Ads';
                    scBadge.className = 'badge badge-scenario scenario-a';
                } else if (sc === 'B') {
                    scBadge.innerText = '🏪 Kịch bản B: Bán Hàng & Phân Phối';
                    scBadge.className = 'badge badge-scenario scenario-b';
                } else {
                    scBadge.innerText = '📊 Kịch bản C: Dữ Liệu Tổng Quát';
                    scBadge.className = 'badge badge-scenario scenario-c';
                }
            }

            const kpis = step5.kpis || {};
            renderAdaptiveKPIs(step5);"""

content = content.replace(old_renderStep5_start, new_renderStep5_start)

# In renderStep5, update call to renderScorecardTable
content = content.replace(
    "renderScorecardTable(step5.scorecard || []);",
    "renderScorecardTable(step5.scorecard || [], step5.scenario || 'A');"
)

# In applyDashboardFilters, replace renderStep5Charts() with scheduleChartRender()
content = content.replace(
    """                pipelineData = result.data;
                renderStep5(pipelineData.step5);
                renderStep5Charts();""",
    """                pipelineData = result.data;
                renderStep5(pipelineData.step5);
                scheduleChartRender();"""
)

# In switchScorecardDimension and filterScorecard, pass scenario
content = content.replace(
    "renderScorecardTable(list);",
    "renderScorecardTable(list, pipelineData?.step5?.scenario || 'A');"
)
content = content.replace(
    "renderScorecardTable(filtered);",
    "renderScorecardTable(filtered, pipelineData?.step5?.scenario || 'A');"
)

# 2. Replace renderScorecardTable with adaptive table renderer
scorecard_regex = re.compile(r'function renderScorecardTable\(items\)\s*\{.*?function filterScorecard\(\)', re.DOTALL)

new_scorecard_func = """function renderScorecardTable(items, scenario) {
            const sc = scenario || (pipelineData?.step5?.scenario) || 'A';
            const thead = document.getElementById('step5-scorecard-thead');
            const tbody = document.getElementById('step5-scorecard-tbody');
            if (!tbody) return;

            if (thead) {
                if (sc === 'A') {
                    thead.innerHTML = `
                        <tr>
                            <th style="min-width:140px;">Nhóm / Đối Tượng</th>
                            <th style="min-width:140px;">Phân Nhóm Ma Trận</th>
                            <th style="min-width:100px;">Mức Cảnh Báo</th>
                            <th class="num-col">Doanh Thu (GMV)</th>
                            <th class="num-col">Thực Thu</th>
                            <th class="num-col">Đơn Hàng</th>
                            <th class="num-col">Đơn Hoàn</th>
                            <th class="num-col">Tỷ Lệ Hoàn</th>
                            <th class="num-col">Lượt Xem</th>
                            <th class="num-col">CR (%)</th>
                            <th class="num-col">AOV</th>
                            <th class="num-col">Chi Phí Ads</th>
                            <th class="num-col">Giá Vốn (COGS)</th>
                            <th class="num-col">CPA</th>
                            <th class="num-col">CIR (%)</th>
                            <th class="num-col">Lợi Nhuận Ròng</th>
                            <th class="num-col">Biên Lãi (%)</th>
                            <th class="num-col">ROAS</th>
                        </tr>
                    `;
                } else if (sc === 'B') {
                    thead.innerHTML = `
                        <tr>
                            <th style="min-width:160px;">Nhóm / Đối Tượng</th>
                            <th style="min-width:140px;">Phân Nhóm Ma Trận</th>
                            <th style="min-width:100px;">Mức Cảnh Báo</th>
                            <th class="num-col">Tổng Doanh Thu</th>
                            <th class="num-col">Doanh Thu Thực Thu</th>
                            <th class="num-col">Số Đơn / Lượng Bán</th>
                            <th class="num-col">Giá Trị TB Đơn (AOV)</th>
                            <th class="num-col">Chi Phí / Giá Vốn</th>
                            <th class="num-col">Lợi Nhuận Ròng</th>
                            <th class="num-col">Biên Lợi Nhuận (%)</th>
                        </tr>
                    `;
                } else {
                    thead.innerHTML = `
                        <tr>
                            <th style="min-width:180px;">Nhóm / Đối Tượng</th>
                            <th style="min-width:140px;">Phân Nhóm Ma Trận</th>
                            <th style="min-width:100px;">Mức Cảnh Báo</th>
                            <th class="num-col">Tổng Giá Trị / Doanh Thu</th>
                            <th class="num-col">Số Lượng / Bản Ghi</th>
                            <th class="num-col">Giá Trị Trung Bình</th>
                            <th class="num-col">Lợi Nhuận / Giá Trị Thuần</th>
                        </tr>
                    `;
                }
            }

            if (!items || items.length === 0) {
                const colsCount = sc === 'A' ? 18 : (sc === 'B' ? 10 : 7);
                tbody.innerHTML = `<tr><td colspan="${colsCount}" style="text-align:center; padding:30px; color:#64748b;">Không có dữ liệu phù hợp với bộ lọc hiện tại.</td></tr>`;
                return;
            }

            tbody.innerHTML = items.map(s => {
                const q = String(s.quadrant || '');
                const qClass = (q.includes('Ngôi sao') || q === 'Star') ? 'star' :
                    ((q.includes('Bò sữa') || q === 'Cash Cow') ? 'cow' :
                    ((q.includes('Bẫy') || q === 'Volume Trap') ? 'trap' : 'burner'));
                const a = String(s.alert || '');
                const aClass = (a.includes('Nguy hiểm') || a === 'RED') ? 'red-alert' :
                    ((a.includes('Cảnh báo') || a === 'YELLOW') ? 'yellow-alert' : 'green-alert');

                if (sc === 'A') {
                    return `
                        <tr>
                            <td><strong>${escapeHtml(s.name)}</strong></td>
                            <td><span class="badge ${qClass}">${s.quadrant}</span></td>
                            <td><span class="badge ${aClass}">${s.alert}</span></td>
                            <td class="num-col">${formatMoney(s.revenue)}</td>
                            <td class="num-col" style="color:#059669; font-weight:700;">${formatMoney(s.net_realized_revenue)}</td>
                            <td class="num-col">${formatNum(s.orders)}</td>
                            <td class="num-col" style="${s.returned_orders > 0 ? 'color:#dc2626;' : ''}">${formatNum(s.returned_orders)}</td>
                            <td class="num-col" style="${s.return_rate > 15 ? 'color:#dc2626; font-weight:700;' : ''}">${s.return_rate}%</td>
                            <td class="num-col">${formatNum(s.traffic)}</td>
                            <td class="num-col">${s.cr_percent}%</td>
                            <td class="num-col">${formatMoney(s.aov)}</td>
                            <td class="num-col">${formatMoney(s.ad_spend)}</td>
                            <td class="num-col">${formatMoney(s.cogs)}</td>
                            <td class="num-col">${formatMoney(s.cpa)}</td>
                            <td class="num-col">${s.cir_percent}%</td>
                            <td class="num-col" style="${s.net_profit < 0 ? 'color:#dc2626; font-weight:700;' : 'color:#059669; font-weight:700;'}">${formatMoney(s.net_profit)}</td>
                            <td class="num-col">${s.net_margin_percent}%</td>
                            <td class="num-col"><strong style="color:#0284c7;">${s.roas}x</strong></td>
                        </tr>
                    `;
                } else if (sc === 'B') {
                    return `
                        <tr>
                            <td><strong>${escapeHtml(s.name)}</strong></td>
                            <td><span class="badge ${qClass}">${s.quadrant}</span></td>
                            <td><span class="badge ${aClass}">${s.alert}</span></td>
                            <td class="num-col">${formatMoney(s.revenue)}</td>
                            <td class="num-col" style="color:#059669; font-weight:700;">${formatMoney(s.net_realized_revenue || s.revenue)}</td>
                            <td class="num-col">${formatNum(s.orders)}</td>
                            <td class="num-col">${formatMoney(s.aov)}</td>
                            <td class="num-col">${formatMoney(s.cogs || s.ad_spend)}</td>
                            <td class="num-col" style="${s.net_profit < 0 ? 'color:#dc2626; font-weight:700;' : 'color:#059669; font-weight:700;'}">${formatMoney(s.net_profit)}</td>
                            <td class="num-col">${s.net_margin_percent}%</td>
                        </tr>
                    `;
                } else {
                    const avgVal = s.orders > 0 ? Math.round(s.revenue / s.orders) : 0;
                    return `
                        <tr>
                            <td><strong>${escapeHtml(s.name)}</strong></td>
                            <td><span class="badge ${qClass}">${s.quadrant}</span></td>
                            <td><span class="badge ${aClass}">${s.alert}</span></td>
                            <td class="num-col">${formatMoney(s.revenue)}</td>
                            <td class="num-col">${formatNum(s.orders)}</td>
                            <td class="num-col">${formatMoney(avgVal || s.aov)}</td>
                            <td class="num-col" style="color:#059669; font-weight:700;">${formatMoney(s.net_profit || s.revenue)}</td>
                        </tr>
                    `;
                }
            }).join('');
        }

        function filterScorecard()"""

content = scorecard_regex.sub(new_scorecard_func, content)

# 3. Replace renderStep5Charts with safe chart destruction and scenario adaptation
charts_regex = re.compile(r'function renderStep5Charts\(\)\s*\{.*?function exportCleanData\(fmt\)', re.DOTALL)

new_charts_func = """function renderStep5Charts() {
            if (!pipelineData || !pipelineData.step5 || !pipelineData.step5.has_dashboard) return;
            const s5 = pipelineData.step5;

            // Safe destruction of any existing charts on canvases
            ['timeTrendChart', 'channelBarChart', 'categoryDonutChart', 'matrixScatterChart'].forEach(id => {
                const el = document.getElementById(id);
                if (el) {
                    const existing = Chart.getChart(el);
                    if (existing) {
                        try { existing.destroy(); } catch (e) { console.warn("Destroy error", id, e); }
                    }
                }
            });

            const lightScales = {
                x: { grid: { color: 'rgba(0, 0, 0, 0.05)' }, ticks: { color: '#64748b' } },
                y: { grid: { color: 'rgba(0, 0, 0, 0.05)' }, ticks: { color: '#64748b' } }
            };

            // 1. Chart 1: Time Trend / Top 10
            const ctxTrend = document.getElementById('timeTrendChart');
            const hasDate = s5.has_date || (s5.time_trend && s5.time_trend.is_date);
            const chart1Title = document.getElementById('chart-title-1');
            const tt = s5.time_trend || {};
            const ttLabels = tt.labels || [];
            const ttRev = tt.revenue || [];
            const ttSpend = tt.ad_spend || [];
            const ttProfit = tt.net_profit || [];

            if (ctxTrend) {
                if (hasDate) {
                    if (chart1Title) chart1Title.innerText = "📈 Xu Hướng Doanh Thu, Chi Phí & Lợi Nhuận Theo Thời Gian";
                    const datasets = [
                        { label: 'Doanh Thu', data: ttRev, borderColor: '#10b981', backgroundColor: 'rgba(16, 185, 129, 0.08)', fill: true, tension: 0.3 }
                    ];
                    if (s5.scenario === 'A') {
                        datasets.push({ label: 'Chi Phí Ads', data: ttSpend, borderColor: '#f59e0b', tension: 0.3 });
                    }
                    datasets.push({ label: 'Lợi Nhuận Ròng', data: ttProfit, borderColor: '#2563eb', tension: 0.3 });

                    chartInstances.trend = new Chart(ctxTrend, {
                        type: 'line',
                        data: { labels: ttLabels, datasets },
                        options: { responsive: true, maintainAspectRatio: false, scales: lightScales }
                    });
                } else {
                    if (chart1Title) chart1Title.innerText = "🏆 Top 10 Nhóm Hoạt Động Có Doanh Thu / Giá Trị Cao Nhất";
                    chartInstances.trend = new Chart(ctxTrend, {
                        type: 'bar',
                        data: {
                            labels: ttLabels,
                            datasets: [
                                { label: 'Doanh Thu / Giá Trị', data: ttRev, backgroundColor: '#10b981', borderRadius: 4 },
                                { label: 'Lợi Nhuận / Giá Trị Ròng', data: ttProfit, backgroundColor: '#2563eb', borderRadius: 4 }
                            ]
                        },
                        options: {
                            indexAxis: 'y',
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: lightScales
                        }
                    });
                }
            }

            // 2. Chart 2: Grouped Bar Chart
            const ctxBar = document.getElementById('channelBarChart');
            if (ctxBar) {
                const gb = s5.grouped_bar || {};
                const gbDatasets = [
                    { label: 'Doanh Thu', data: gb.revenue || [], backgroundColor: '#10b981', borderRadius: 4 }
                ];
                if (s5.scenario === 'A') {
                    gbDatasets.push({ label: 'Chi Phí Ads', data: gb.ad_spend || [], backgroundColor: '#f59e0b', borderRadius: 4 });
                }
                gbDatasets.push({ label: 'Lợi Nhuận Ròng', data: gb.net_profit || [], backgroundColor: '#2563eb', borderRadius: 4 });

                chartInstances.bar = new Chart(ctxBar, {
                    type: 'bar',
                    data: {
                        labels: gb.labels || [],
                        datasets: gbDatasets
                    },
                    options: { responsive: true, maintainAspectRatio: false, scales: lightScales }
                });
            }

            // 3. Chart 3: Donut Chart
            const ctxDonut = document.getElementById('categoryDonutChart');
            if (ctxDonut) {
                const cd = s5.cat_donut || {};
                chartInstances.donut = new Chart(ctxDonut, {
                    type: 'doughnut',
                    data: {
                        labels: cd.labels || [],
                        datasets: [{
                            data: cd.revenue || [],
                            backgroundColor: ['#10b981', '#38bdf8', '#8b5cf6', '#f59e0b', '#ec4899', '#64748b', '#14b8a6']
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false }
                });
            }

            // 4. Chart 4: Scatter Matrix Chart
            const ctxScatter = document.getElementById('matrixScatterChart');
            if (ctxScatter) {
                const pts = (s5.matrix_scatter || []).map(p => ({
                    x: Number(p.x) || 0,
                    y: Number(p.y) || 0,
                    name: p.name || '',
                    quadrant: p.quadrant || '',
                    rev: Number(p.revenue) || 0
                }));

                chartInstances.scatter = new Chart(ctxScatter, {
                    type: 'scatter',
                    data: {
                        datasets: [{
                            label: 'Nhóm Hoạt Động',
                            data: pts,
                            backgroundColor: (ctx) => {
                                const pt = ctx.raw;
                                if (!pt) return '#10b981';
                                const q = String(pt.quadrant || '');
                                if (q.includes('Ngôi sao') || q === 'Star') return '#10b981';
                                if (q.includes('Bò sữa') || q === 'Cash Cow') return '#0284c7';
                                if (q.includes('Bẫy') || q === 'Volume Trap') return '#f59e0b';
                                return '#ef4444';
                            },
                            pointRadius: (ctx) => {
                                const pt = ctx.raw;
                                if (!pt) return 6;
                                const maxR = Math.max(...pts.map(p => p.rev), 1);
                                return Math.min(18, Math.max(7, Math.round((pt.rev / maxR) * 16) + 4));
                            }
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: lightScales,
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: (ctx) => {
                                        const pt = ctx.raw;
                                        if (!pt) return '';
                                        const xLabel = s5.scenario === 'A' ? `ROAS: ${pt.x}x` : `AOV: ${formatMoney(pt.x)}`;
                                        return `${pt.name || ''} [${pt.quadrant || ''}]: ${xLabel}, Biên Lãi: ${pt.y}%, Doanh thu: ${formatMoney(pt.rev)}`;
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }

        function exportCleanData(fmt)"""

content = charts_regex.sub(new_charts_func, content)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("JS Polish completed.")
