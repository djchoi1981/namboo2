with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'r') as f:
    html = f.read()

# 1. Update filter-vehicle
filter_veh_old = """                            <select id="filter-vehicle" class="filter-select">
                                <option value="all">모든 차량 보기</option>
                                <option value="스타렉스 1호">스타렉스 1호</option>
                                <option value="스타렉스 2호">스타렉스 2호</option>
                                <option value="스타렉스 3호">스타렉스 3호</option>
                                <option value="스타리아">스타리아</option>
                                <option value="25인승 버스">25인승 버스</option>
                                <option value="45인승 버스">45인승 버스</option>
                            </select>"""
filter_veh_new = """                            <select id="filter-vehicle" class="filter-select">
                                <option value="all">모든 차량 보기</option>
                                <!-- populated by JS -->
                            </select>"""
html = html.replace(filter_veh_old, filter_veh_new)

# 2. Update form vehicle select
form_veh_old = """                                    <select id="vehicle" required>
                                        <option value="" disabled selected>선택하세요</option>
                                        <option value="스타렉스 1호">스타렉스 1호</option>
                                        <option value="스타렉스 2호">스타렉스 2호</option>
                                        <option value="스타렉스 3호">스타렉스 3호</option>
                                        <option value="스타리아">스타리아</option>
                                        <option value="25인승 버스">25인승 버스</option>
                                        <option value="45인승 버스">45인승 버스</option>
                                    </select>"""
form_veh_new = """                                    <select id="vehicle" required>
                                        <option value="" disabled selected>선택하세요</option>
                                        <!-- populated by JS -->
                                    </select>"""
html = html.replace(form_veh_old, form_veh_new)

# 3. Add Admin panel for vehicles
admin_pw_str = """                        <div class="admin-panel">
                            <h4><i class="ph ph-lock-key"></i> 관리자 비밀번호 변경</h4>"""
veh_admin_panel = """                        <div class="admin-panel">
                            <h4><i class="ph ph-car"></i> 차량 관리</h4>
                            <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1rem;">예약할 수 있는 교회 차량 목록입니다.</p>
                            <div class="add-dept-form">
                                <input type="text" id="new-vehicle-name" placeholder="새 차량 이름 (예: 카니발 1호)">
                                <button type="button" id="add-vehicle-btn" class="btn btn-primary">차량 추가</button>
                            </div>
                            <div class="org-manage-container" style="margin-top: 1rem;">
                                <div class="org-committee-card" style="margin-bottom: 0;">
                                    <ul class="org-dept-list" id="admin-vehicles-list" style="margin: 0; padding-top: 0;">
                                        <!-- populated by JS -->
                                    </ul>
                                </div>
                            </div>
                        </div>
                        
"""
html = html.replace(admin_pw_str, veh_admin_panel + admin_pw_str)

with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'w') as f:
    f.write(html)
