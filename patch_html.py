with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'r') as f:
    html = f.read()

# 1. Update location field in registration section
location_old = """                        <div class="form-group" id="location-container">
                            <label for="location" id="location-label">장소 <span class="required" id="location-required" style="color: var(--danger);">*</span></label>
                            <input type="text" id="location" placeholder="예: 본당, 소예배실, 양평수양관" required>
                        </div>"""
location_new = """                        <div class="form-group" id="location-container">
                            <label for="location" id="location-label">장소 <span class="required" id="location-required" style="color: var(--danger);">*</span></label>
                            <select id="location-select" required>
                                <option value="" disabled selected>장소를 선택하세요</option>
                                <!-- options populated by JS -->
                            </select>
                            <input type="text" id="location-input" placeholder="직접 입력 (예: 본당, 소예배실)" style="display: none; margin-top: 0.5rem;" required>
                        </div>"""
html = html.replace(location_old, location_new)

# 2. Add Room Management to Admin Section
admin_pw_panel_str = """                        <div class="admin-panel">
                            <h4><i class="ph ph-lock-key"></i> 관리자 비밀번호 변경</h4>"""
room_admin_panel = """                        <div class="admin-panel">
                            <h4><i class="ph ph-map-pin"></i> 장소(룸) 관리</h4>
                            <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 1rem;">셀/모임 및 위원회 예약 시 선택할 수 있는 장소 목록입니다.</p>
                            <div class="add-dept-form">
                                <input type="text" id="new-room-name" placeholder="새 장소 이름 (예: 비전센터 1층 식당)">
                                <button type="button" id="add-room-btn" class="btn btn-primary">장소 추가</button>
                            </div>
                            <div class="org-manage-container" style="margin-top: 1rem;">
                                <div class="org-committee-card" style="margin-bottom: 0;">
                                    <ul class="org-dept-list" id="admin-rooms-list" style="margin: 0; padding-top: 0;">
                                        <!-- populated by JS -->
                                    </ul>
                                </div>
                            </div>
                        </div>
                        
"""
html = html.replace(admin_pw_panel_str, room_admin_panel + admin_pw_panel_str)

with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'w') as f:
    f.write(html)
