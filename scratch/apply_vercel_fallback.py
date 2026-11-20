with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update confirmStep3AndOpenDashboard
old_confirm = """        async function confirmStep3AndOpenDashboard() {
            try {
                const res = await fetch('/api/step3-confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
                const result = await res.json();
                if (result.status === 'success') {
                    pipelineData = result.data;
                    unlockedStep = Math.max(unlockedStep, 4);
                    renderAllSteps(pipelineData);
                    goToStep(4);
                    scheduleChartRender();
                } else {
                    alert(result.message || "Lỗi xác nhận Bước 3.");
                }
            } catch (e) {
                console.error("Lỗi xác nhận Bước 3:", e);
            }
        }"""

new_confirm = """        async function confirmStep3AndOpenDashboard() {
            try {
                const res = await fetch('/api/step3-confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
                const result = await res.json();
                if (result.status === 'success') {
                    pipelineData = result.data;
                    // Tương thích ngược: Nếu backend chưa tự động sinh step5 ở step3-confirm (bản Vercel cũ), tự động gọi step4-confirm
                    if (!pipelineData.step5 || !pipelineData.step5.has_dashboard) {
                        try {
                            const res4 = await fetch('/api/step4-confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
                            const r4 = await res4.json();
                            if (r4.status === 'success' && r4.data) {
                                pipelineData = r4.data;
                            }
                        } catch (e4) {
                            console.warn("Fallback step4-confirm error:", e4);
                        }
                    }
                    unlockedStep = Math.max(unlockedStep, 4);
                    renderAllSteps(pipelineData);
                    goToStep(4);
                    scheduleChartRender();
                } else {
                    alert(result.message || "Lỗi xác nhận Bước 3.");
                }
            } catch (e) {
                console.error("Lỗi xác nhận Bước 3:", e);
            }
        }"""

if old_confirm in content:
    content = content.replace(old_confirm, new_confirm)
    print("1. Updated confirmStep3AndOpenDashboard.")
else:
    print("WARNING: old_confirm not found by exact string!")

# 2. Update goToStep(4)
old_goToStep_step4 = """            if (step === 4) {
                if (pipelineData && pipelineData.step5 && pipelineData.step5.has_dashboard) {
                    scheduleChartRender();
                } else {
                    // Nếu chưa khởi tạo dashboard Bước 4, gọi xác nhận ngầm
                    fetch('/api/step3-confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
                        .then(r => r.json())
                        .then(res => {
                            if (res.status === 'success') {
                                pipelineData = res.data;
                                renderAllSteps(pipelineData);
                                scheduleChartRender();
                            }
                        }).catch(e => console.warn(e));
                }
            }"""

new_goToStep_step4 = """            if (step === 4) {
                if (pipelineData && pipelineData.step5 && pipelineData.step5.has_dashboard) {
                    scheduleChartRender();
                } else {
                    // Nếu chưa khởi tạo dashboard Bước 4, gọi xác nhận ngầm kèm auto-fallback
                    fetch('/api/step3-confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
                        .then(r => r.json())
                        .then(async res => {
                            if (res.status === 'success') {
                                pipelineData = res.data;
                                if (!pipelineData.step5 || !pipelineData.step5.has_dashboard) {
                                    try {
                                        const res4 = await fetch('/api/step4-confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
                                        const r4 = await res4.json();
                                        if (r4.status === 'success' && r4.data) {
                                            pipelineData = r4.data;
                                        }
                                    } catch (e4) {}
                                }
                                renderAllSteps(pipelineData);
                                scheduleChartRender();
                            }
                        }).catch(e => console.warn(e));
                }
            }"""

if old_goToStep_step4 in content:
    content = content.replace(old_goToStep_step4, new_goToStep_step4)
    print("2. Updated goToStep(4).")
else:
    print("WARNING: old_goToStep_step4 not found by exact string!")

# 3. Add auto-healing in renderStep5
old_renderStep5 = """        function renderStep5(step5) {
            if (!step5 || !step5.has_dashboard) return;"""

new_renderStep5 = """        function renderStep5(step5) {
            if (!step5 || !step5.has_dashboard) {
                // Tự động kích hoạt dashboard nếu chưa có dữ liệu (Auto-Heal fallback cho bản Vercel cũ)
                if (!window._isHealingDashboard) {
                    window._isHealingDashboard = true;
                    fetch('/api/step4-confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
                        .then(r => r.json())
                        .then(res => {
                            if (res.status === 'success' && res.data && res.data.step5 && res.data.step5.has_dashboard) {
                                pipelineData = res.data;
                                renderAllSteps(pipelineData);
                                scheduleChartRender();
                            }
                        }).catch(e => console.warn("Auto-heal error:", e))
                        .finally(() => { setTimeout(() => { window._isHealingDashboard = false; }, 2000); });
                }
                return;
            }"""

if old_renderStep5 in content:
    content = content.replace(old_renderStep5, new_renderStep5)
    print("3. Updated renderStep5 auto-healing.")
else:
    print("WARNING: old_renderStep5 not found by exact string!")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Saved index.html with fallbacks.")
