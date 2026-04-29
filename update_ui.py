import re

with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'r') as f:
    html = f.read()

# 1. Update Logo Link
logo_old = """            <div class="logo">
                <img src="logo.jpg" alt="남부전원교회" class="church-logo" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMzAiPjx0ZXh0IHg9IjAiIHk9IjIwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiPuyCrOynhOydhCDsspjtg4A8L3RleHQ+PC9zdmc+'">
            </div>"""
logo_new = """            <div class="logo">
                <a href="https://www.nambooch.or.kr/" target="_blank" title="남부전원교회 홈페이지로 이동">
                    <img src="logo.jpg" alt="남부전원교회" class="church-logo" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMzAiPjx0ZXh0IHg9IjAiIHk9IjIwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiPuyCrOynhOydhCDsspjtg4A8L3RleHQ+PC9zdmc+'">
                </a>
            </div>"""
html = html.replace(logo_old, logo_new)

# 2. Remove nav-admin from <nav>
html = re.sub(r'<a href="#" id="nav-admin".*?</a>', '', html)

# 3. Make upcoming-summary flexible so footer stays at bottom, and add footer
upcoming_old = """            <div class="upcoming-summary">"""
upcoming_new = """            <div class="upcoming-summary" style="flex: 1; overflow-y: auto;">"""
html = html.replace(upcoming_old, upcoming_new)

sidebar_close_old = """        </aside>"""
sidebar_close_new = """            <div class="sidebar-footer" style="padding-top: 1rem; border-top: 1px solid var(--border); margin-top: auto;">
                <a href="#" id="sidebar-admin-btn" class="nav-item"><i class="ph ph-gear"></i> 관리자 모드</a>
                <a href="#" id="sidebar-logout-btn" class="nav-item" style="color: var(--danger); display: none; margin-top: 0.5rem;"><i class="ph ph-sign-out"></i> 로그아웃</a>
            </div>
        </aside>"""
html = html.replace(sidebar_close_old, sidebar_close_new)

# 4. Remove page-title and user-profile
top_header_old = """            <header class="top-header">
                <div class="header-left">
                    <h2 id="page-title">통합 캘린더</h2>
                    <div class="month-navigation">
                        <button id="prev-month" class="icon-btn"><i class="ph ph-caret-left"></i></button>
                        <span id="current-month-display">2026년 4월</span>
                        <button id="next-month" class="icon-btn"><i class="ph ph-caret-right"></i></button>
                        <button id="today-btn" class="btn btn-outline btn-sm" style="margin-left: 1rem;">오늘</button>
                        
                        <select id="calendar-filter" class="filter-select" style="margin-left: 1rem;">
                            <option value="all">모든 예약 보기</option>
                            <option value="committee" id="opt-cal-committee">위원회/부서 일정만</option>
                            <option value="cell" id="opt-cal-cell">셀/모임 장소예약만</option>
                            <option value="vehicle" id="opt-cal-vehicle">차량 운영예약만</option>
                        </select>
                    </div>
                </div>
                <div class="user-profile">
                    <button id="login-btn" class="btn btn-outline" style="padding: 0.5rem 1rem;">관리자 로그인</button>
                    <div id="admin-profile" style="display: none; align-items: center; gap: 0.75rem;">
                        <div class="avatar">
                            <i class="ph ph-user"></i>
                        </div>
                        <span>관리자</span>
                        <button id="logout-btn" class="icon-btn" title="로그아웃"><i class="ph ph-sign-out"></i></button>
                    </div>
                </div>
            </header>"""

top_header_new = """            <header class="top-header">
                <div class="header-left" style="width: 100%;">
                    <div class="month-navigation" style="width: 100%; display: flex; align-items: center;">
                        <button id="prev-month" class="icon-btn"><i class="ph ph-caret-left"></i></button>
                        <span id="current-month-display">2026년 4월</span>
                        <button id="next-month" class="icon-btn"><i class="ph ph-caret-right"></i></button>
                        <button id="today-btn" class="btn btn-outline btn-sm" style="margin-left: 1rem;">오늘</button>
                        
                        <select id="calendar-filter" class="filter-select" style="margin-left: auto;">
                            <option value="all">모든 예약 보기</option>
                            <option value="committee" id="opt-cal-committee">위원회/부서 일정만</option>
                            <option value="cell" id="opt-cal-cell">셀/모임 장소예약만</option>
                            <option value="vehicle" id="opt-cal-vehicle">차량 운영예약만</option>
                        </select>
                    </div>
                </div>
            </header>"""
html = html.replace(top_header_old, top_header_new)

# 5. Remove 0191 text from login modal
login_modal_old = """<p style="margin-bottom: 1rem; font-size: 0.875rem; color: var(--text-muted);">조직도 관리 및 시스템 설정을 위해 로그인하세요. (초기 비밀번호: 0191)</p>"""
login_modal_new = """<p style="margin-bottom: 1rem; font-size: 0.875rem; color: var(--text-muted);">조직도 관리 및 시스템 설정을 위해 로그인하세요.</p>"""
html = html.replace(login_modal_old, login_modal_new)

with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'w') as f:
    f.write(html)
