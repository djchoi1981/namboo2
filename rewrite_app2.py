import json

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    lines = f.readlines()

new_app = """document.addEventListener('DOMContentLoaded', () => {
    // State
    let events = JSON.parse(localStorage.getItem('churchEvents_v2')) || [];
    let currentDate = new Date(); // Represents the currently viewed month
    
    const defaultOrganization = [
        { id: 'c1', name: '예배드림위원회', departments: ['기획준비부', '예배운영·안내부', '예배미디어부', '성례성찬부'] },
        { id: 'c2', name: '찬양울림위원회', departments: ['성가대', '찬양단', '음악찬양단', '워십팀', '청년·청소년 찬양팀'] },
        { id: 'c3', name: '기도숨결·영성위원회', departments: ['중보기도부', '기도훈련부', '기도네트워크부'] },
        { id: 'c4', name: '교제·복지위원회', departments: ['행사역무부', '교제부', '샬롬케어·경조부', '세대소통·나눔부', '교인관리부'] },
        { id: 'c5', name: '교육위원회', departments: ['영아부', '유치부', '유·초등부', '중등부', '고등부', '청년1부', '청년2부', '여호수아부', '기독교교육부', '차세대교육혁신센터'] },
        { id: 'c6', name: '양육·훈련사역위원회', departments: ['제자훈련·리더십개발부', '성경·교리교육부', '시니어교육부', '입교·세례부'] },
        { id: 'c7', name: '만남·동행위원회', departments: ['남부전도단', '새가족환영부', '초기양육·정착부'] },
        { id: 'c8', name: '봉사·섬김위원회', departments: ['주방부', '워킹카페부', '성전돌봄부', '자원봉사자관리부'] },
        { id: 'c9', name: '문화·커뮤니케이션위원회', departments: ['문화·디자인부', '미디어홍보부', '사진부', '시니어부', 'Hope Touch부'] },
        { id: 'c10', name: '글로컬선교위원회', departments: ['국내·특수선교부', '지역사회·연대부', '이주·다문화선교부', '해외선교·후원부', '이단사이비대응·정보센터'] },
        { id: 'c11', name: '움직이는 교회사역 위원회', departments: ['프라이빗예배부', '멘토링부', '콘텐츠부', '위기개입부', '간증·리커버리부'] },
        { id: 'c12', name: '기획·행정위원회', departments: ['행정사무팀', '홍보부', '대외협력부', '기록예산부(겸)'] },
        { id: 'c13', name: '재정위원회', departments: ['재정수입부', '재정지출부', '감사부'] },
        { id: 'c14', name: '미래발전위원회', departments: ['비전·지역연구부', '차세대리더부', '기록아카이브부'] },
        { id: 'c15', name: '시설·안전·건축위원회', departments: ['시설관리부', '차량운행·배차', '주차부', '차량관리부', '안전부', '건축·자산관리부'] }
    ];
    let organization = JSON.parse(localStorage.getItem('nambuOrganization_v1')) || defaultOrganization;
    let adminPassword = localStorage.getItem('churchAdminPassword') || '0191';
    let isLoggedIn = false;
    let currentEventIdForAction = null;

    // DOM Elements
    const form = document.getElementById('event-form');
    const calendarGrid = document.getElementById('calendar-grid');
    const currentMonthDisplay = document.getElementById('current-month-display');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const todayBtn = document.getElementById('today-btn');
    const upcomingList = document.getElementById('upcoming-list-mini');
    const conflictAlert = document.getElementById('conflict-alert');
    const conflictMessage = document.getElementById('conflict-message');
    const toast = document.getElementById('toast');
    
    // Navigation
    const navCalendar = document.getElementById('nav-calendar');
    const navDepartment = document.getElementById('nav-department');
    const navLocation = document.getElementById('nav-location');
    const navAdmin = document.getElementById('nav-admin');
    
    // Sections
    const calendarSection = document.querySelector('.calendar-section');
    const departmentSection = document.getElementById('department-view');
    const locationSection = document.getElementById('location-view');
    const adminSection = document.getElementById('admin-view');
    const pageTitle = document.getElementById('page-title');
    const monthNavigation = document.querySelector('.month-navigation');
    
    // Modals
    const eventModal = document.getElementById('event-modal');
    const closeEventBtn = document.getElementById('close-event-btn');
    const eventDetailContent = document.getElementById('event-detail-content');
    const eventActionPassword = document.getElementById('event-action-password');
    const btnEditEvent = document.getElementById('btn-edit-event');
    const btnDeleteEvent = document.getElementById('btn-delete-event');
    const eventActionError = document.getElementById('event-action-error');
    
    // Auth & Admin DOM
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const adminProfile = document.getElementById('admin-profile');
    const loginModal = document.getElementById('login-modal');
    const closeLoginBtn = document.getElementById('close-login-btn');
    const loginPassword = document.getElementById('login-password');
    const submitLoginBtn = document.getElementById('submit-login-btn');
    const loginError = document.getElementById('login-error');
    const newCommitteeName = document.getElementById('new-committee-name');
    const addCommitteeBtn = document.getElementById('add-committee-btn');
    const orgManageContainer = document.getElementById('org-manage-container');
    const currentPassword = document.getElementById('current-password');
    const newPassword = document.getElementById('new-password');
    const changePwBtn = document.getElementById('change-pw-btn');
    const pwChangeMsg = document.getElementById('pw-change-msg');
    
    // Form Inputs
    const dateInput = document.getElementById('date');
    const startTimeInput = document.getElementById('start-time');
    const endTimeInput = document.getElementById('end-time');
    const locationInput = document.getElementById('location');
    const descriptionInput = document.getElementById('description');
    const eventPasswordInput = document.getElementById('event-password');
    const editEventIdInput = document.getElementById('edit-event-id');
    const submitEventBtn = document.getElementById('submit-event-btn');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const eventTypeRadios = document.querySelectorAll('input[name="eventType"]');
    const locationLabel = document.getElementById('location-label');
    
    // Committee / Department Fields
    const committeeSelect = document.getElementById('committee');
    const departmentSelect = document.getElementById('department');
    const filterCommittee = document.getElementById('filter-committee');
    const filterDepartment = document.getElementById('filter-department');
    const departmentListContainer = document.getElementById('department-list-container');
    const filterLocation = document.getElementById('filter-location');
    const locationListContainer = document.getElementById('location-list-container');

    // Initialize
    populateOrganizationOptions();
    renderCalendar();
    renderUpcomingEvents();
    renderDepartmentList();
    renderLocationList();
    
    const todayStr = new Date().toISOString().split('T')[0];
    dateInput.value = todayStr;

    // Type Change Listener
    eventTypeRadios.forEach(r => {
        r.addEventListener('change', (e) => {
            const val = e.target.value;
            document.getElementById('fields-committee').style.display = 'none';
            document.getElementById('fields-cell').style.display = 'none';
            document.getElementById('fields-vehicle').style.display = 'none';
            
            // disable requires
            document.querySelectorAll('.type-fields input, .type-fields select').forEach(el => el.removeAttribute('required'));
            
            document.getElementById(`fields-${val}`).style.display = 'block';
            document.querySelectorAll(`#fields-${val} input, #fields-${val} select`).forEach(el => el.setAttribute('required', 'true'));
            
            if (val === 'vehicle') {
                locationLabel.innerHTML = '목적지 <span class="required" style="color: var(--danger);">*</span>';
            } else {
                locationLabel.innerHTML = '장소 <span class="required" style="color: var(--danger);">*</span>';
            }
        });
    });
    
    // Navigation toggles
    navCalendar.addEventListener('click', (e) => {
        e.preventDefault();
        navCalendar.classList.add('active');
        navDepartment.classList.remove('active');
        navLocation.classList.remove('active');
        navAdmin.classList.remove('active');
        calendarSection.style.display = 'block';
        departmentSection.style.display = 'none';
        locationSection.style.display = 'none';
        adminSection.style.display = 'none';
        pageTitle.textContent = '통합 캘린더';
        monthNavigation.style.display = 'flex';
        renderCalendar();
    });

    navDepartment.addEventListener('click', (e) => {
        e.preventDefault();
        navDepartment.classList.add('active');
        navCalendar.classList.remove('active');
        navLocation.classList.remove('active');
        navAdmin.classList.remove('active');
        calendarSection.style.display = 'none';
        departmentSection.style.display = 'flex';
        locationSection.style.display = 'none';
        adminSection.style.display = 'none';
        pageTitle.textContent = '부서별 일정';
        monthNavigation.style.display = 'none';
        renderDepartmentList();
    });

    navLocation.addEventListener('click', (e) => {
        e.preventDefault();
        navLocation.classList.add('active');
        navCalendar.classList.remove('active');
        navDepartment.classList.remove('active');
        navAdmin.classList.remove('active');
        calendarSection.style.display = 'none';
        departmentSection.style.display = 'none';
        locationSection.style.display = 'flex';
        adminSection.style.display = 'none';
        pageTitle.textContent = '장소/차량 현황';
        monthNavigation.style.display = 'none';
        renderLocationList();
    });

    navAdmin.addEventListener('click', (e) => {
        e.preventDefault();
        navAdmin.classList.add('active');
        navCalendar.classList.remove('active');
        navDepartment.classList.remove('active');
        navLocation.classList.remove('active');
        calendarSection.style.display = 'none';
        departmentSection.style.display = 'none';
        locationSection.style.display = 'none';
        adminSection.style.display = 'block';
        pageTitle.textContent = '시스템 관리자 설정';
        monthNavigation.style.display = 'none';
        renderAdminOrgList();
    });

    // Calendar Navigation
    prevMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    nextMonthBtn.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    todayBtn.addEventListener('click', () => {
        currentDate = new Date();
        renderCalendar();
    });

    // Form Interactions
    committeeSelect.addEventListener('change', () => {
        const commId = committeeSelect.value;
        const org = organization.find(o => o.id === commId);
        departmentSelect.innerHTML = '<option value="" disabled selected>선택하세요</option>';
        if (org) {
            org.departments.forEach(dept => {
                departmentSelect.innerHTML += `<option value="${dept}">${dept}</option>`;
            });
        }
    });

    filterCommittee.addEventListener('change', () => {
        const commId = filterCommittee.value;
        filterDepartment.innerHTML = '<option value="all">모든 부서 보기</option>';
        if (commId !== 'all') {
            const org = organization.find(o => o.id === commId);
            if (org) {
                org.departments.forEach(dept => {
                    filterDepartment.innerHTML += `<option value="${dept}">${dept}</option>`;
                });
            }
        }
        renderDepartmentList();
    });

    filterDepartment.addEventListener('change', renderDepartmentList);
    filterLocation.addEventListener('change', renderLocationList);

    // Form Submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const isEditMode = editEventIdInput.value !== '';
        
        if (checkForConflicts(isEditMode ? editEventIdInput.value : null)) {
            const proceed = confirm("일정이 겹칩니다! 그래도 등록/수정하시겠습니까?");
            if (!proceed) return;
        }

        const selectedType = document.querySelector('input[name="eventType"]:checked').value;
        
        const newEvent = {
            id: isEditMode ? editEventIdInput.value : Date.now().toString(),
            eventType: selectedType,
            date: dateInput.value,
            startTime: startTimeInput.value,
            endTime: endTimeInput.value,
            location: locationInput.value,
            description: descriptionInput.value,
            password: eventPasswordInput.value
        };

        if (selectedType === 'committee') {
            newEvent.committee = committeeSelect.value;
            newEvent.department = departmentSelect.value;
            newEvent.title = document.getElementById('title-committee').value;
        } else if (selectedType === 'cell') {
            newEvent.cellName = document.getElementById('cellName').value;
            newEvent.reserver = document.getElementById('reserver-cell').value;
            newEvent.title = document.getElementById('title-cell').value;
        } else if (selectedType === 'vehicle') {
            newEvent.vehicle = document.getElementById('vehicle').value;
            newEvent.reserver = document.getElementById('reserver-vehicle').value;
            newEvent.title = document.getElementById('title-vehicle').value;
        }

        if (isEditMode) {
            events = events.map(ev => ev.id === newEvent.id ? newEvent : ev);
            showToast("일정이 수정되었습니다.");
            exitEditMode();
        } else {
            events.push(newEvent);
            showToast("일정이 성공적으로 등록되었습니다.");
        }
        
        saveEvents();
        renderCalendar();
        renderUpcomingEvents();
        renderDepartmentList();
        renderLocationList();
        
        form.reset();
        departmentSelect.innerHTML = '<option value="" disabled selected>위원회를 먼저 선택하세요</option>';
        dateInput.value = todayStr;
        conflictAlert.style.display = 'none';
        document.getElementById('fields-committee').style.display = 'block';
        document.getElementById('fields-cell').style.display = 'none';
        document.getElementById('fields-vehicle').style.display = 'none';
    });
    
    cancelEditBtn.addEventListener('click', exitEditMode);

    function exitEditMode() {
        editEventIdInput.value = '';
        submitEventBtn.textContent = '일정 등록하기';
        cancelEditBtn.style.display = 'none';
        form.reset();
        dateInput.value = new Date().toISOString().split('T')[0];
    }

    function saveEvents() {
        localStorage.setItem('churchEvents_v2', JSON.stringify(events));
    }
    
    function saveOrganization() {
        localStorage.setItem('nambuOrganization_v1', JSON.stringify(organization));
    }

    function populateOrganizationOptions() {
        committeeSelect.innerHTML = '<option value="" disabled selected>선택하세요</option>';
        filterCommittee.innerHTML = '<option value="all">모든 위원회 보기</option>';
        
        organization.forEach(org => {
            committeeSelect.innerHTML += `<option value="${org.id}">${org.name}</option>`;
            filterCommittee.innerHTML += `<option value="${org.id}">${org.name}</option>`;
        });
        
        departmentSelect.innerHTML = '<option value="" disabled selected>위원회를 먼저 선택하세요</option>';
        filterDepartment.innerHTML = '<option value="all">모든 부서 보기</option>';
    }

    function getCommitteeName(id) {
        const org = organization.find(o => o.id === id);
        return org ? org.name : (id || '알 수 없음');
    }

    // Modal Actions
    closeEventBtn.addEventListener('click', () => {
        eventModal.style.display = 'none';
    });
    
    btnDeleteEvent.addEventListener('click', () => {
        const ev = events.find(e => e.id === currentEventIdForAction);
        if(!ev) return;
        
        if (!isLoggedIn && eventActionPassword.value !== ev.password) {
            eventActionError.style.display = 'block';
            return;
        }
        
        if(confirm("정말로 이 일정을 삭제하시겠습니까?")) {
            events = events.filter(e => e.id !== ev.id);
            saveEvents();
            renderCalendar();
            renderUpcomingEvents();
            renderDepartmentList();
            renderLocationList();
            eventModal.style.display = 'none';
            showToast("일정이 삭제되었습니다.");
        }
    });

    btnEditEvent.addEventListener('click', () => {
        const ev = events.find(e => e.id === currentEventIdForAction);
        if(!ev) return;
        
        if (!isLoggedIn && eventActionPassword.value !== ev.password) {
            eventActionError.style.display = 'block';
            return;
        }
        
        // Enter edit mode
        eventModal.style.display = 'none';
        
        // Select radio
        document.querySelector(`input[name="eventType"][value="${ev.eventType}"]`).click();
        
        editEventIdInput.value = ev.id;
        dateInput.value = ev.date;
        startTimeInput.value = ev.startTime;
        endTimeInput.value = ev.endTime;
        locationInput.value = ev.location;
        descriptionInput.value = ev.description;
        eventPasswordInput.value = ev.password;
        
        if (ev.eventType === 'committee') {
            committeeSelect.value = ev.committee;
            // trigger change to load departments
            committeeSelect.dispatchEvent(new Event('change'));
            departmentSelect.value = ev.department;
            document.getElementById('title-committee').value = ev.title;
        } else if (ev.eventType === 'cell') {
            document.getElementById('cellName').value = ev.cellName;
            document.getElementById('reserver-cell').value = ev.reserver;
            document.getElementById('title-cell').value = ev.title;
        } else if (ev.eventType === 'vehicle') {
            document.getElementById('vehicle').value = ev.vehicle;
            document.getElementById('reserver-vehicle').value = ev.reserver;
            document.getElementById('title-vehicle').value = ev.title;
        }
        
        submitEventBtn.textContent = '수정된 내용 저장';
        cancelEditBtn.style.display = 'block';
        
        // Scroll to form
        form.scrollIntoView({ behavior: 'smooth' });
    });

    function showEventDetails(ev) {
        currentEventIdForAction = ev.id;
        eventActionPassword.value = '';
        eventActionError.style.display = 'none';
        
        let typeStr = '';
        let titleStr = ev.title;
        let specificInfo = '';
        
        if(ev.eventType === 'committee') {
            typeStr = '<span style="background:var(--primary);color:#fff;padding:2px 6px;border-radius:4px;font-size:12px;">위원회/부서</span>';
            specificInfo = `
                <p><strong>위원회:</strong> ${getCommitteeName(ev.committee)}</p>
                <p><strong>부서:</strong> ${ev.department}</p>
            `;
        } else if(ev.eventType === 'cell') {
            typeStr = '<span style="background:#10b981;color:#fff;padding:2px 6px;border-radius:4px;font-size:12px;">셀/모임</span>';
            specificInfo = `
                <p><strong>모임명:</strong> ${ev.cellName}</p>
                <p><strong>예약자:</strong> ${ev.reserver}</p>
            `;
        } else if(ev.eventType === 'vehicle') {
            typeStr = '<span style="background:#f59e0b;color:#fff;padding:2px 6px;border-radius:4px;font-size:12px;">차량예약</span>';
            specificInfo = `
                <p><strong>배차차량:</strong> ${ev.vehicle}</p>
                <p><strong>예약자:</strong> ${ev.reserver}</p>
            `;
        }
        
        const locLabel = ev.eventType === 'vehicle' ? '목적지' : '장소';
        
        eventDetailContent.innerHTML = `
            <div style="margin-bottom:1rem;">${typeStr}</div>
            <h4 style="margin-bottom:1rem; font-size:1.25rem;">${titleStr}</h4>
            <div style="background:var(--background); padding:1rem; border-radius:var(--radius-md); font-size:0.9rem; line-height:1.6;">
                ${specificInfo}
                <p><strong>일시:</strong> ${ev.date} ${ev.startTime} ~ ${ev.endTime}</p>
                <p><strong>${locLabel}:</strong> ${ev.location}</p>
                ${ev.description ? `<p><strong>상세내용:</strong> ${ev.description}</p>` : ''}
            </div>
        `;
        
        // Show/hide auth instruction based on admin status
        if(isLoggedIn) {
            document.getElementById('event-action-auth').querySelector('p').style.display = 'none';
            eventActionPassword.style.display = 'none';
        } else {
            document.getElementById('event-action-auth').querySelector('p').style.display = 'block';
            eventActionPassword.style.display = 'block';
        }
        
        eventModal.style.display = 'flex';
    }

    function renderCalendar() {
        calendarGrid.innerHTML = '';
        
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        
        currentMonthDisplay.textContent = `${year}년 ${month + 1}월`;

        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        
        const startingDayOfWeek = firstDay.getDay();
        const totalDays = lastDay.getDate();

        const prevMonthLastDay = new Date(year, month, 0).getDate();
        for (let i = startingDayOfWeek - 1; i >= 0; i--) {
            createDayCell(prevMonthLastDay - i, true, new Date(year, month - 1, prevMonthLastDay - i));
        }

        const today = new Date();
        for (let i = 1; i <= totalDays; i++) {
            const isToday = today.getDate() === i && today.getMonth() === month && today.getFullYear() === year;
            createDayCell(i, false, new Date(year, month, i), isToday);
        }

        const totalCellsCreated = startingDayOfWeek + totalDays;
        const remainingCells = (Math.ceil(totalCellsCreated / 7) * 7) - totalCellsCreated;
        for (let i = 1; i <= remainingCells; i++) {
            createDayCell(i, true, new Date(year, month + 1, i));
        }
    }

    function createDayCell(day, isOtherMonth, dateObj, isToday = false) {
        const cell = document.createElement('div');
        cell.className = `calendar-day ${isOtherMonth ? 'other-month' : ''} ${isToday ? 'today' : ''}`;
        
        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;
        cell.appendChild(dayNumber);

        const dateString = formatLocalISODate(dateObj);
        const dayEvents = events.filter(e => e.date === dateString);
        
        dayEvents.sort((a, b) => a.startTime.localeCompare(b.startTime));

        const eventsContainer = document.createElement('div');
        eventsContainer.style.display = 'flex';
        eventsContainer.style.flexDirection = 'column';
        eventsContainer.style.gap = '3px';
        eventsContainer.style.marginTop = '4px';

        dayEvents.forEach(e => {
            const tag = document.createElement('div');
            tag.className = `event-tag`;
            
            let icon = '';
            let label = '';
            
            if(e.eventType === 'committee') {
                tag.style.backgroundColor = getCommitteeColor(e.committee);
                icon = '<i class="ph ph-users-three"></i>';
                label = `${e.department}`;
            } else if(e.eventType === 'cell') {
                tag.style.backgroundColor = '#10b981';
                icon = '<i class="ph ph-users"></i>';
                label = `${e.cellName}`;
            } else if(e.eventType === 'vehicle') {
                tag.style.backgroundColor = '#f59e0b';
                icon = '<i class="ph ph-car"></i>';
                label = `${e.vehicle}`;
            }
            
            tag.style.color = '#fff';
            tag.title = `${e.title} (${e.startTime} ~ ${e.endTime})`;
            tag.innerHTML = `<span>${e.startTime}</span> ${icon} ${label}`;
            
            // Add click listener for Modal
            tag.style.cursor = 'pointer';
            tag.addEventListener('click', () => showEventDetails(e));
            
            eventsContainer.appendChild(tag);
        });

        cell.appendChild(eventsContainer);
        calendarGrid.appendChild(cell);
    }

    function formatLocalISODate(date) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
    }

    function renderUpcomingEvents() {
        upcomingList.innerHTML = '';
        
        const todayStr = formatLocalISODate(new Date());
        
        const upcoming = events
            .filter(e => e.date >= todayStr)
            .sort((a, b) => {
                if(a.date !== b.date) return a.date.localeCompare(b.date);
                return a.startTime.localeCompare(b.startTime);
            })
            .slice(0, 5);

        if (upcoming.length === 0) {
            upcomingList.innerHTML = '<p style="color: var(--text-muted); font-size: 0.875rem;">예정된 일정이 없습니다.</p>';
            return;
        }

        upcoming.forEach(e => {
            const item = document.createElement('div');
            item.className = 'mini-event';
            
            const [, mm, dd] = e.date.split('-');
            const formattedDate = `${parseInt(mm)}/${parseInt(dd)}`;
            
            let label = '';
            if(e.eventType === 'committee') label = `[${getCommitteeName(e.committee)}] ${e.department}`;
            else if(e.eventType === 'cell') label = `[셀/모임] ${e.cellName}`;
            else if(e.eventType === 'vehicle') label = `[차량] ${e.vehicle}`;
            
            item.innerHTML = `
                <h4 style="cursor:pointer;" class="clickable-title" data-id="${e.id}">${e.title}</h4>
                <p><i class="ph ph-calendar"></i> ${formattedDate} ${e.startTime} | ${label}</p>
            `;
            
            upcomingList.appendChild(item);
        });
        
        document.querySelectorAll('.clickable-title').forEach(el => {
            el.addEventListener('click', (ev) => {
                const id = ev.target.getAttribute('data-id');
                const eventObj = events.find(x => x.id === id);
                if(eventObj) showEventDetails(eventObj);
            });
        });
    }

    function checkForConflicts(excludeId = null) {
        const date = dateInput.value;
        const start = startTimeInput.value;
        const end = endTimeInput.value;
        const loc = locationInput.value; // For vehicle, this is destination. For others, location.
        const type = document.querySelector('input[name="eventType"]:checked').value;
        
        // For vehicle, the conflict is about the vehicle itself, not the destination location
        const targetResource = type === 'vehicle' ? document.getElementById('vehicle').value : loc;

        if (!date || !start || !end || !targetResource) {
            conflictAlert.style.display = 'none';
            return false;
        }

        const conflictingEvents = events.filter(e => {
            if (e.id === excludeId) return false;
            if (e.date !== date) return false;
            
            if (type === 'vehicle') {
                if (e.eventType !== 'vehicle') return false; // Vehicles don't conflict with locations
                if (e.vehicle !== targetResource) return false; // Different vehicles
            } else {
                if (e.eventType === 'vehicle') return false; // Locations don't conflict with vehicles
                if (e.location !== targetResource) return false; // Different locations
            }
            
            return (start < e.endTime) && (end > e.startTime);
        });

        if (conflictingEvents.length > 0) {
            conflictAlert.style.display = 'flex';
            const conflict = conflictingEvents[0];
            let label = conflict.eventType === 'vehicle' ? `차량(${conflict.vehicle})` : `해당 장소`;
            let owner = conflict.eventType === 'committee' ? `[${getCommitteeName(conflict.committee)}] ${conflict.department}` :
                        conflict.eventType === 'cell' ? `[셀/모임] ${conflict.cellName}` :
                        `${conflict.reserver}님`;
            
            conflictMessage.innerHTML = `${label}에 이미 <strong>${owner}</strong>의 <strong>[${conflict.title}]</strong> 일정이 있습니다.<br>(${conflict.startTime} ~ ${conflict.endTime})`;
            return true;
        } else {
            conflictAlert.style.display = 'none';
            return false;
        }
    }

    function showToast(message) {
        document.getElementById('toast-message').textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    function renderDepartmentList() {
        if (!departmentListContainer) return;
        
        const filterC = filterCommittee.value;
        const filterD = filterDepartment.value;
        let filteredEvents = events.filter(e => e.eventType === 'committee');
        
        if (filterC !== 'all') {
            filteredEvents = filteredEvents.filter(e => e.committee === filterC);
        }
        if (filterD !== 'all') {
            filteredEvents = filteredEvents.filter(e => e.department === filterD);
        }

        filteredEvents.sort((a, b) => {
            if (a.date !== b.date) return a.date.localeCompare(b.date);
            return a.startTime.localeCompare(b.startTime);
        });

        departmentListContainer.innerHTML = '';

        if (filteredEvents.length === 0) {
            departmentListContainer.innerHTML = `
                <div class="empty-state" style="padding: 2rem; text-align: center; color: var(--text-muted);">
                    등록된 부서 일정이 없습니다.
                </div>
            `;
            return;
        }

        filteredEvents.forEach(e => {
            const item = document.createElement('div');
            item.className = 'department-item';
            item.style.borderLeftColor = getCommitteeColor(e.committee);
            
            item.innerHTML = `
                <div class="dept-item-info">
                    <h4 style="cursor:pointer;" class="list-title" data-id="${e.id}">${e.title}</h4>
                </div>
                <div class="dept-item-meta">
                    <span><i class="ph ph-calendar"></i> ${e.date}</span>
                    <span><i class="ph ph-clock"></i> ${e.startTime} ~ ${e.endTime}</span>
                    <span><i class="ph ph-map-pin"></i> ${e.location}</span>
                    <span style="color: var(--primary); font-weight: 500; margin-left: auto;">[${getCommitteeName(e.committee)}] ${e.department}</span>
                </div>
            `;
            departmentListContainer.appendChild(item);
        });
        
        document.querySelectorAll('.list-title').forEach(el => {
            el.addEventListener('click', (ev) => {
                const id = ev.target.getAttribute('data-id');
                const eventObj = events.find(x => x.id === id);
                if(eventObj) showEventDetails(eventObj);
            });
        });
    }

    function getCommitteeColor(commId) {
        if(!commId) return 'var(--border)';
        const palette = ['#4338ca', '#15803d', '#a16207', '#be123c', '#7e22ce', '#0369a1', '#c2410c', '#be185d', '#e11d48', '#d97706', '#65a30d', '#0891b2', '#4f46e5', '#9333ea', '#c026d3'];
        let hash = 0;
        for (let i = 0; i < commId.length; i++) {
            hash = commId.charCodeAt(i) + ((hash << 5) - hash);
        }
        return palette[Math.abs(hash) % palette.length];
    }

    function renderLocationList() {
        if (!locationListContainer) return;
        
        const filterVal = filterLocation.value;
        let filteredEvents = events.filter(e => e.eventType !== 'committee'); // Show Cells and Vehicles here
        
        if (filterVal !== 'all') {
            filteredEvents = filteredEvents.filter(e => e.location === filterVal || e.vehicle === filterVal);
        }

        filteredEvents.sort((a, b) => {
            if (a.date !== b.date) return a.date.localeCompare(b.date);
            return a.startTime.localeCompare(b.startTime);
        });

        locationListContainer.innerHTML = '';

        if (filteredEvents.length === 0) {
            locationListContainer.innerHTML = `
                <div class="empty-state" style="padding: 2rem; text-align: center; color: var(--text-muted);">
                    등록된 장소/차량 예약이 없습니다.
                </div>
            `;
            return;
        }

        filteredEvents.forEach(e => {
            const item = document.createElement('div');
            item.className = 'department-item';
            
            let color = '';
            let owner = '';
            let locInfo = '';
            
            if(e.eventType === 'cell') {
                color = '#10b981';
                owner = `[셀/모임] ${e.cellName} (${e.reserver})`;
                locInfo = `<i class="ph ph-map-pin"></i> 장소: ${e.location}`;
            } else if(e.eventType === 'vehicle') {
                color = '#f59e0b';
                owner = `[차량예약] ${e.vehicle} (${e.reserver})`;
                locInfo = `<i class="ph ph-map-pin"></i> 목적지: ${e.location}`;
            }
            
            item.style.borderLeftColor = color;
            
            item.innerHTML = `
                <div class="dept-item-info">
                    <h4 style="cursor:pointer;" class="list-title" data-id="${e.id}">${e.title}</h4>
                </div>
                <div class="dept-item-meta">
                    <span><i class="ph ph-calendar"></i> ${e.date}</span>
                    <span><i class="ph ph-clock"></i> ${e.startTime} ~ ${e.endTime}</span>
                    <span style="color: ${color}; font-weight: 500;">${locInfo}</span>
                    <span style="margin-left: auto;">${owner}</span>
                </div>
            `;
            locationListContainer.appendChild(item);
        });
        
        document.querySelectorAll('.list-title').forEach(el => {
            el.addEventListener('click', (ev) => {
                const id = ev.target.getAttribute('data-id');
                const eventObj = events.find(x => x.id === id);
                if(eventObj) showEventDetails(eventObj);
            });
        });
    }

    // Auth & Admin Logic
    loginBtn.addEventListener('click', () => {
        loginModal.style.display = 'flex';
        loginPassword.value = '';
        loginError.style.display = 'none';
        loginPassword.focus();
    });
    
    closeLoginBtn.addEventListener('click', () => {
        loginModal.style.display = 'none';
    });
    
    submitLoginBtn.addEventListener('click', () => {
        if(loginPassword.value === adminPassword) {
            isLoggedIn = true;
            loginModal.style.display = 'none';
            loginBtn.style.display = 'none';
            adminProfile.style.display = 'flex';
            navAdmin.style.display = 'flex';
            showToast("관리자로 로그인되었습니다.");
            
            // If viewing a modal, hide password auth prompt
            const pElem = document.getElementById('event-action-auth').querySelector('p');
            if(pElem) pElem.style.display = 'none';
            eventActionPassword.style.display = 'none';
            
        } else {
            loginError.style.display = 'block';
        }
    });
    
    logoutBtn.addEventListener('click', () => {
        isLoggedIn = false;
        loginBtn.style.display = 'inline-block';
        adminProfile.style.display = 'none';
        navAdmin.style.display = 'none';
        if (adminSection.style.display === 'block') {
            navCalendar.click();
        }
        showToast("로그아웃 되었습니다.");
    });
    
    changePwBtn.addEventListener('click', () => {
        const curr = currentPassword.value;
        const nw = newPassword.value;
        
        if(curr !== adminPassword) {
            pwChangeMsg.textContent = "현재 비밀번호가 일치하지 않습니다.";
            pwChangeMsg.style.color = "var(--danger)";
            pwChangeMsg.style.display = "block";
            return;
        }
        
        if(nw.length < 4) {
            pwChangeMsg.textContent = "새 비밀번호는 4자리 이상이어야 합니다.";
            pwChangeMsg.style.color = "var(--danger)";
            pwChangeMsg.style.display = "block";
            return;
        }
        
        adminPassword = nw;
        localStorage.setItem('churchAdminPassword', adminPassword);
        pwChangeMsg.textContent = "비밀번호가 성공적으로 변경되었습니다.";
        pwChangeMsg.style.color = "var(--success)";
        pwChangeMsg.style.display = "block";
        currentPassword.value = '';
        newPassword.value = '';
        
        setTimeout(() => { pwChangeMsg.style.display = 'none'; }, 3000);
    });

    addCommitteeBtn.addEventListener('click', () => {
        const name = newCommitteeName.value.trim();
        if(name) {
            const exists = organization.find(o => o.name === name);
            if(!exists) {
                organization.push({
                    id: 'c' + Date.now(),
                    name: name,
                    departments: []
                });
                saveOrganization();
                populateOrganizationOptions();
                renderAdminOrgList();
                newCommitteeName.value = '';
                showToast("위원회가 추가되었습니다.");
            } else {
                alert('이미 존재하는 위원회입니다.');
            }
        }
    });

    function renderAdminOrgList() {
        orgManageContainer.innerHTML = '';
        organization.forEach((org, orgIndex) => {
            const card = document.createElement('div');
            card.className = 'org-committee-card';
            
            // Header
            const header = document.createElement('div');
            header.className = 'org-committee-header';
            header.innerHTML = `
                <span class="org-committee-title">${org.name}</span>
                <button type="button" class="btn btn-sm btn-danger delete-comm-btn" data-index="${orgIndex}">위원회 삭제</button>
            `;
            card.appendChild(header);
            
            // Departments List
            const deptList = document.createElement('ul');
            deptList.className = 'org-dept-list';
            org.departments.forEach((dept, deptIndex) => {
                const item = document.createElement('li');
                item.className = 'org-dept-item';
                item.innerHTML = `
                    ${dept}
                    <button type="button" class="delete-subdept-btn" data-org="${orgIndex}" data-dept="${deptIndex}" title="삭제"><i class="ph ph-x"></i></button>
                `;
                deptList.appendChild(item);
            });
            card.appendChild(deptList);
            
            // Add Department Form
            const addForm = document.createElement('div');
            addForm.className = 'add-dept-inline-form';
            addForm.innerHTML = `
                <input type="text" placeholder="새 부서 추가" id="new-dept-input-${orgIndex}">
                <button type="button" class="btn btn-outline add-subdept-btn" data-org="${orgIndex}">추가</button>
            `;
            card.appendChild(addForm);
            
            orgManageContainer.appendChild(card);
        });
        
        // Attach Events for Admin Org List
        document.querySelectorAll('.delete-comm-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const orgIdx = e.target.getAttribute('data-index');
                const orgName = organization[orgIdx].name;
                if(confirm(`'${orgName}'와 그 안의 모든 부서를 정말 삭제하시겠습니까?`)) {
                    organization.splice(orgIdx, 1);
                    saveOrganization();
                    populateOrganizationOptions();
                    renderAdminOrgList();
                    showToast("위원회가 삭제되었습니다.");
                }
            });
        });
        
        document.querySelectorAll('.delete-subdept-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const btnEl = e.currentTarget; 
                const orgIdx = btnEl.getAttribute('data-org');
                const deptIdx = btnEl.getAttribute('data-dept');
                if(confirm(`이 부서를 삭제하시겠습니까?`)) {
                    organization[orgIdx].departments.splice(deptIdx, 1);
                    saveOrganization();
                    populateOrganizationOptions();
                    renderAdminOrgList();
                    showToast("부서가 삭제되었습니다.");
                }
            });
        });
        
        document.querySelectorAll('.add-subdept-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const orgIdx = e.target.getAttribute('data-org');
                const inputEl = document.getElementById(`new-dept-input-${orgIdx}`);
                const deptName = inputEl.value.trim();
                if(deptName) {
                    if(!organization[orgIdx].departments.includes(deptName)) {
                        organization[orgIdx].departments.push(deptName);
                        saveOrganization();
                        populateOrganizationOptions();
                        renderAdminOrgList();
                        showToast("부서가 추가되었습니다.");
                    } else {
                        alert("이미 존재하는 부서입니다.");
                    }
                }
            });
        });
    }
});
"""

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(new_app)

