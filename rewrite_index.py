import json

with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'r') as f:
    lines = f.readlines()

new_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>교회 위원회 부서별 일정 조율 프로그램</title>
    
    <!-- Google Fonts: Inter & Noto Sans KR -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
    
    <!-- Phosphor Icons -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <!-- Sidebar / Navigation -->
        <aside class="sidebar">
            <div class="logo">
                <img src="logo.jpg" alt="남부전원교회" class="church-logo" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMzAiPjx0ZXh0IHg9IjAiIHk9IjIwIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiPuyCrOynhOydhCDsspjtg4A8L3RleHQ+PC9zdmc+'">
            </div>
            <nav>
                <a href="#" id="nav-calendar" class="nav-item active"><i class="ph ph-calendar-blank"></i> 통합 캘린더</a>
                <a href="#" id="nav-department" class="nav-item"><i class="ph ph-list-dashes"></i> 부서별 일정</a>
                <a href="#" id="nav-location" class="nav-item"><i class="ph ph-map-pin"></i> 장소 현황</a>
                <a href="#" id="nav-admin" class="nav-item" style="display: none;"><i class="ph ph-gear"></i> 관리자 설정</a>
            </nav>
            <div class="upcoming-summary">
                <h3>다가오는 일정</h3>
                <div class="upcoming-list" id="upcoming-list-mini">
                    <!-- Javascript will populate upcoming events here -->
                </div>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="main-content">
            <header class="top-header">
                <div class="header-left">
                    <h2 id="page-title">통합 캘린더</h2>
                    <div class="month-navigation">
                        <button id="prev-month" class="icon-btn"><i class="ph ph-caret-left"></i></button>
                        <span id="current-month-display">2026년 4월</span>
                        <button id="next-month" class="icon-btn"><i class="ph ph-caret-right"></i></button>
                        <button id="today-btn" class="btn btn-outline btn-sm" style="margin-left: 1rem;">오늘</button>
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
            </header>

            <div class="content-grid">
                <!-- Calendar View -->
                <section class="calendar-section card">
                    <div class="calendar-header">
                        <div class="weekday">일</div>
                        <div class="weekday">월</div>
                        <div class="weekday">화</div>
                        <div class="weekday">수</div>
                        <div class="weekday">목</div>
                        <div class="weekday">금</div>
                        <div class="weekday">토</div>
                    </div>
                    <div class="calendar-body" id="calendar-grid">
                        <!-- Javascript will populate days here -->
                    </div>
                </section>

                <!-- Department View (Hidden by default) -->
                <section class="department-section card" id="department-view" style="display: none;">
                    <div class="card-header">
                        <h3><i class="ph ph-list-dashes"></i> 부서별 일정 조회</h3>
                        <div class="filter-group" style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                            <select id="filter-committee" class="filter-select">
                                <option value="all">모든 위원회 보기</option>
                            </select>
                            <select id="filter-department" class="filter-select">
                                <option value="all">모든 부서 보기</option>
                            </select>
                        </div>
                    </div>
                    <div class="department-list-body" id="department-list-container">
                        <!-- Javascript will populate events here -->
                        <div class="empty-state" style="padding: 2rem; text-align: center; color: var(--text-muted);">
                            등록된 일정이 없습니다.
                        </div>
                    </div>
                </section>

                <!-- Location View (Hidden by default) -->
                <section class="location-section card" id="location-view" style="display: none;">
                    <div class="card-header">
                        <h3><i class="ph ph-map-pin"></i> 장소 현황 조회</h3>
                        <div class="filter-group" style="margin-top: 1rem;">
                            <select id="filter-location" class="filter-select">
                                <option value="all">모든 장소 보기</option>
                                <option value="본당">본당</option>
                                <option value="소예배실">소예배실</option>
                                <option value="식당">식당</option>
                                <option value="교육관 1층">교육관 1층</option>
                                <option value="교육관 2층">교육관 2층</option>
                                <option value="청년부실">청년부실</option>
                                <option value="야외 주차장">야외 주차장</option>
                            </select>
                        </div>
                    </div>
                    <div class="department-list-body" id="location-list-container">
                        <!-- Javascript will populate events here -->
                        <div class="empty-state" style="padding: 2rem; text-align: center; color: var(--text-muted);">
                            등록된 일정이 없습니다.
                        </div>
                    </div>
                </section>

                <!-- Admin View (Hidden by default) -->
                <section class="admin-section card" id="admin-view" style="display: none;">
                    <div class="card-header">
                        <h3><i class="ph ph-gear"></i> 시스템 관리자 설정</h3>
                        <p>부서 목록을 편집하고 관리자 비밀번호를 변경할 수 있습니다.</p>
                    </div>
                    <div class="admin-body">
                        <div class="admin-panel">
                            <h4><i class="ph ph-tree-structure"></i> 조직도 (위원회 및 부서) 관리</h4>
                            <div class="add-dept-form">
                                <input type="text" id="new-committee-name" placeholder="새 위원회 이름 (예: 예배위원회)">
                                <button type="button" id="add-committee-btn" class="btn btn-primary">위원회 추가</button>
                            </div>
                            <div class="org-manage-container" id="org-manage-container">
                                <!-- Javascript will populate org chart here -->
                            </div>
                        </div>
                        <div class="admin-panel">
                            <h4><i class="ph ph-lock-key"></i> 관리자 비밀번호 변경</h4>
                            <div class="password-form">
                                <input type="password" id="current-password" placeholder="현재 비밀번호">
                                <input type="password" id="new-password" placeholder="새 비밀번호">
                                <button type="button" id="change-pw-btn" class="btn btn-outline">비밀번호 변경</button>
                            </div>
                            <p id="pw-change-msg" style="margin-top: 0.5rem; font-size: 0.875rem; display: none;"></p>
                        </div>
                    </div>
                </section>

                <!-- Registration Form -->
                <section class="registration-section card">
                    <div class="card-header">
                        <h3><i class="ph ph-calendar-plus"></i> 새 예약 / 일정 등록</h3>
                        <p>일정 유형을 선택하고 예약 정보를 입력해 주세요.</p>
                    </div>
                    <form id="event-form">
                        
                        <!-- Event Type Selector -->
                        <div class="form-group event-type-selector" style="margin-bottom: 1.5rem;">
                            <label style="margin-bottom: 0.5rem; display: block; font-weight: 500;">예약 유형 <span class="required" style="color: var(--danger);">*</span></label>
                            <div class="radio-group" style="display: flex; gap: 1.5rem;">
                                <label style="display: flex; align-items: center; gap: 0.25rem;"><input type="radio" name="eventType" value="committee" checked> 위원회/부서 일정</label>
                                <label style="display: flex; align-items: center; gap: 0.25rem;"><input type="radio" name="eventType" value="cell"> 셀/모임 장소예약</label>
                                <label style="display: flex; align-items: center; gap: 0.25rem;"><input type="radio" name="eventType" value="vehicle"> 차량 운영예약</label>
                            </div>
                        </div>

                        <div id="conflict-alert" class="conflict-alert" style="display: none;">
                            <i class="ph-fill ph-warning"></i>
                            <div id="conflict-message">해당 시간/장소에 이미 겹치는 일정이 있습니다!</div>
                        </div>

                        <!-- Type A: Committee -->
                        <div id="fields-committee" class="type-fields">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="committee">위원회 <span class="required" style="color: var(--danger);">*</span></label>
                                    <select id="committee">
                                        <option value="" disabled selected>선택하세요</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="department">하위 부서 <span class="required" style="color: var(--danger);">*</span></label>
                                    <select id="department">
                                        <option value="" disabled selected>위원회를 먼저 선택하세요</option>
                                    </select>
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="title-committee">행사 제목 <span class="required" style="color: var(--danger);">*</span></label>
                                <input type="text" id="title-committee" placeholder="예: 여름 성경학교">
                            </div>
                        </div>

                        <!-- Type B: Cell / Group -->
                        <div id="fields-cell" class="type-fields" style="display: none;">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="cellName">셀/모임명 <span class="required" style="color: var(--danger);">*</span></label>
                                    <input type="text" id="cellName" placeholder="예: 바나바 1셀, 청년부 임원진">
                                </div>
                                <div class="form-group">
                                    <label for="reserver-cell">예약자 성명 <span class="required" style="color: var(--danger);">*</span></label>
                                    <input type="text" id="reserver-cell" placeholder="예: 홍길동">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="title-cell">모임 목적 <span class="required" style="color: var(--danger);">*</span></label>
                                <input type="text" id="title-cell" placeholder="예: 임원진 회의, 셀 모임">
                            </div>
                        </div>

                        <!-- Type C: Vehicle -->
                        <div id="fields-vehicle" class="type-fields" style="display: none;">
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="vehicle">차량 선택 <span class="required" style="color: var(--danger);">*</span></label>
                                    <select id="vehicle">
                                        <option value="" disabled selected>선택하세요</option>
                                        <option value="스타렉스 1호">스타렉스 1호</option>
                                        <option value="스타렉스 2호">스타렉스 2호</option>
                                        <option value="스타렉스 3호">스타렉스 3호</option>
                                        <option value="스타리아">스타리아</option>
                                        <option value="25인승 버스">25인승 버스</option>
                                        <option value="45인승 버스">45인승 버스</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label for="reserver-vehicle">예약자 성명 <span class="required" style="color: var(--danger);">*</span></label>
                                    <input type="text" id="reserver-vehicle" placeholder="예: 이순신">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="title-vehicle">운행 목적 (제목) <span class="required" style="color: var(--danger);">*</span></label>
                                <input type="text" id="title-vehicle" placeholder="예: 학생부 수련회 운행">
                            </div>
                        </div>

                        <!-- Common Fields -->
                        <div class="form-row">
                            <div class="form-group">
                                <label for="date">날짜 <span class="required" style="color: var(--danger);">*</span></label>
                                <input type="date" id="date" required>
                            </div>
                            <div class="form-group">
                                <label for="start-time">시작 시간 <span class="required" style="color: var(--danger);">*</span></label>
                                <input type="time" id="start-time" required>
                            </div>
                            <div class="form-group">
                                <label for="end-time">종료 시간 <span class="required" style="color: var(--danger);">*</span></label>
                                <input type="time" id="end-time" required>
                            </div>
                        </div>
                        
                        <div class="form-group" id="location-container">
                            <label for="location" id="location-label">장소 (또는 목적지) <span class="required" style="color: var(--danger);">*</span></label>
                            <input type="text" id="location" placeholder="예: 본당, 소예배실, 양평수양관" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="description">상세 내용 (선택)</label>
                            <textarea id="description" rows="3" placeholder="기타 필요한 내용을 입력하세요"></textarea>
                        </div>

                        <!-- Password for Edit/Delete -->
                        <div class="form-group" style="border-top: 1px solid var(--border); padding-top: 1rem; margin-top: 1rem;">
                            <label for="event-password">비밀번호 (수정/삭제용) <span class="required" style="color: var(--danger);">*</span></label>
                            <input type="password" id="event-password" placeholder="4자리 이상 숫자/문자" required>
                            <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">이 비밀번호는 나중에 일정을 수정하거나 삭제할 때 필요합니다.</p>
                        </div>

                        <input type="hidden" id="edit-event-id">

                        <button type="submit" class="btn btn-primary btn-block" id="submit-event-btn">일정 등록하기</button>
                        <button type="button" class="btn btn-outline btn-block" id="cancel-edit-btn" style="display: none; margin-top: 0.5rem;">수정 취소</button>
                    </form>
                </section>
            </div>
        </main>
    </div>

    <!-- Notification Toast -->
    <div id="toast" class="toast">
        <i class="ph ph-check-circle"></i>
        <span id="toast-message">일정이 성공적으로 등록되었습니다.</span>
    </div>

    <!-- Login Modal -->
    <div id="login-modal" class="modal-overlay" style="display: none;">
        <div class="modal-content">
            <div class="modal-header">
                <h3>관리자 로그인</h3>
                <button class="close-modal" id="close-login-btn"><i class="ph ph-x"></i></button>
            </div>
            <div class="modal-body">
                <p style="margin-bottom: 1rem; font-size: 0.875rem; color: var(--text-muted);">부서 관리 및 시스템 설정을 위해 로그인하세요. (초기 비밀번호: 0191)</p>
                <div class="form-group">
                    <input type="password" id="login-password" placeholder="비밀번호를 입력하세요">
                </div>
                <p id="login-error" style="color: var(--danger); font-size: 0.875rem; margin-top: 0.5rem; display: none;">비밀번호가 일치하지 않습니다.</p>
                <button type="button" id="submit-login-btn" class="btn btn-primary btn-block" style="margin-top: 1rem;">로그인</button>
            </div>
        </div>
    </div>
    
    <!-- Event Details & Actions Modal -->
    <div id="event-modal" class="modal-overlay" style="display: none;">
        <div class="modal-content" style="max-width: 500px;">
            <div class="modal-header">
                <h3>일정 상세 정보</h3>
                <button class="close-modal" id="close-event-btn"><i class="ph ph-x"></i></button>
            </div>
            <div class="modal-body">
                <div id="event-detail-content">
                    <!-- Javascript populates this -->
                </div>
                
                <div id="event-action-auth" style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border);">
                    <p style="font-size: 0.875rem; margin-bottom: 0.5rem;">수정/삭제를 위해 등록 시 입력한 비밀번호를 입력하세요.<br>(관리자로 로그인 시 생략 가능)</p>
                    <div style="display: flex; gap: 0.5rem;">
                        <input type="password" id="event-action-password" placeholder="비밀번호" style="flex: 1;">
                        <button type="button" id="btn-edit-event" class="btn btn-primary btn-sm">수정</button>
                        <button type="button" id="btn-delete-event" class="btn btn-danger btn-sm">삭제</button>
                    </div>
                    <p id="event-action-error" style="color: var(--danger); font-size: 0.875rem; margin-top: 0.5rem; display: none;">비밀번호가 일치하지 않습니다.</p>
                </div>
            </div>
        </div>
    </div>

    <script src="app.js"></script>
</body>
</html>
"""

with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'w') as f:
    f.write(new_html)

