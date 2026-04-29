import json

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    lines = f.readlines()

new_app = """document.addEventListener('DOMContentLoaded', () => {
    // State
    let events = JSON.parse(localStorage.getItem('churchEvents')) || [];
    let currentDate = new Date(); // Represents the currently viewed month
    
    const defaultOrganization = [
        { id: 'c1', name: '예배위원회', departments: ['예배부', '찬양대', '방송실'] },
        { id: 'c2', name: '교육위원회', departments: ['영아부', '유치부', '아동부', '학생부', '청년부'] },
        { id: 'c3', name: '선교위원회', departments: ['국내선교부', '해외선교부'] }
    ];
    let organization = JSON.parse(localStorage.getItem('churchOrganization')) || defaultOrganization;
    let adminPassword = localStorage.getItem('churchAdminPassword') || '0191';
    let isLoggedIn = false;

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
    const navCalendar = document.getElementById('nav-calendar');
    const navDepartment = document.getElementById('nav-department');
    const calendarSection = document.querySelector('.calendar-section');
    const departmentSection = document.getElementById('department-view');
    const pageTitle = document.getElementById('page-title');
    
    const filterCommittee = document.getElementById('filter-committee');
    const filterDepartment = document.getElementById('filter-department');
    const departmentListContainer = document.getElementById('department-list-container');
    
    const navLocation = document.getElementById('nav-location');
    const locationSection = document.getElementById('location-view');
    const filterLocation = document.getElementById('filter-location');
    const locationListContainer = document.getElementById('location-list-container');
    const monthNavigation = document.querySelector('.month-navigation');
    
    // Auth & Admin DOM Elements
    const navAdmin = document.getElementById('nav-admin');
    const adminSection = document.getElementById('admin-view');
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

    // Department Selects
    const committeeSelect = document.getElementById('committee');
    const departmentSelect = document.getElementById('department');

    // Initialize
    populateOrganizationOptions();
    renderCalendar();
    renderUpcomingEvents();
    renderDepartmentList();
    renderLocationList();
    
    // Default form date to today
    const todayStr = new Date().toISOString().split('T')[0];
    dateInput.value = todayStr;

    // Event Listeners
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
        pageTitle.textContent = '장소 현황';
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

    // Real-time conflict detection
    const checkInputs = [dateInput, startTimeInput, endTimeInput, locationInput];
    checkInputs.forEach(input => {
        input.addEventListener('change', checkForConflicts);
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        if (checkForConflicts()) {
            const proceed = confirm("일정이 겹칩니다! 그래도 등록하시겠습니까?");
            if (!proceed) return;
        }

        const newEvent = {
            id: Date.now().toString(),
            committee: committeeSelect.value,
            department: departmentSelect.value,
            title: document.getElementById('title').value,
            date: dateInput.value,
            startTime: startTimeInput.value,
            endTime: endTimeInput.value,
            location: locationInput.value,
            description: document.getElementById('description').value
        };

        events.push(newEvent);
        saveEvents();
        
        renderCalendar();
        renderUpcomingEvents();
        renderDepartmentList();
        renderLocationList();
        
        form.reset();
        departmentSelect.innerHTML = '<option value="" disabled selected>위원회를 먼저 선택하세요</option>';
        dateInput.value = todayStr;
        conflictAlert.style.display = 'none';
        
        showToast("일정이 성공적으로 등록되었습니다.");
    });

    function saveEvents() {
        localStorage.setItem('churchEvents', JSON.stringify(events));
    }
    
    function saveOrganization() {
        localStorage.setItem('churchOrganization', JSON.stringify(organization));
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
        eventsContainer.style.gap = '2px';
        eventsContainer.style.marginTop = '4px';

        dayEvents.forEach(e => {
            const tag = document.createElement('div');
            const cName = getCommitteeName(e.committee);
            tag.className = `event-tag`;
            tag.style.backgroundColor = getCommitteeColor(e.committee);
            tag.style.color = '#fff';
            tag.title = `${e.title} (${e.startTime} - ${e.endTime} @ ${e.location})`;
            tag.innerHTML = `<span>${e.startTime}</span> [${cName}] ${e.department} - ${e.title}`;
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
            
            item.innerHTML = `
                <h4>${e.title}</h4>
                <p><i class="ph ph-calendar"></i> ${formattedDate} ${e.startTime} | [${getCommitteeName(e.committee)}] ${e.department}</p>
                <p><i class="ph ph-map-pin"></i> ${e.location}</p>
            `;
            upcomingList.appendChild(item);
        });
    }

    function checkForConflicts() {
        const date = dateInput.value;
        const start = startTimeInput.value;
        const end = endTimeInput.value;
        const loc = locationInput.value;

        if (!date || !start || !end || !loc) {
            conflictAlert.style.display = 'none';
            return false;
        }

        const conflictingEvents = events.filter(e => {
            if (e.date !== date) return false;
            if (e.location !== loc) return false;
            return (start < e.endTime) && (end > e.startTime);
        });

        if (conflictingEvents.length > 0) {
            conflictAlert.style.display = 'flex';
            const firstConflict = conflictingEvents[0];
            conflictMessage.innerHTML = `해당 시간/장소에 이미 <strong>[${getCommitteeName(firstConflict.committee)}] ${firstConflict.department}</strong>의 <strong>[${firstConflict.title}]</strong> 일정이 있습니다.<br>(${firstConflict.startTime} ~ ${firstConflict.endTime})`;
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
        let filteredEvents = events;
        
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
                    등록된 일정이 없습니다.
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
                    <h4>${e.title}</h4>
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
        let filteredEvents = events;
        
        if (filterVal !== 'all') {
            filteredEvents = events.filter(e => e.location === filterVal);
        }

        filteredEvents.sort((a, b) => {
            if (a.date !== b.date) return a.date.localeCompare(b.date);
            return a.startTime.localeCompare(b.startTime);
        });

        locationListContainer.innerHTML = '';

        if (filteredEvents.length === 0) {
            locationListContainer.innerHTML = `
                <div class="empty-state" style="padding: 2rem; text-align: center; color: var(--text-muted);">
                    해당 장소에 등록된 일정이 없습니다.
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
                    <h4>${e.title}</h4>
                </div>
                <div class="dept-item-meta">
                    <span><i class="ph ph-calendar"></i> ${e.date}</span>
                    <span><i class="ph ph-clock"></i> ${e.startTime} ~ ${e.endTime}</span>
                    <span style="color: var(--primary); font-weight: 500;"><i class="ph ph-map-pin"></i> ${e.location}</span>
                    <span style="margin-left: auto;">[${getCommitteeName(e.committee)}] ${e.department}</span>
                </div>
            `;
            locationListContainer.appendChild(item);
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
                const btnEl = e.currentTarget; // use currentTarget for icon clicks
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

