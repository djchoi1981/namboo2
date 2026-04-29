import re

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    js = f.read()

# Default Rooms
default_rooms = """
const defaultRooms = [
    '본당 1층 새벽기도실 1',
    '본당 1층 새벽기도실 2',
    '본당 3층 자모실',
    '교육관 3층 중보기도실',
    '교육관 3층 소그룹실',
    '비전센터 2층 당회실',
    '비전센터 3층 소망실',
    '비전센터 3층 사랑실'
];
let rooms = [];
"""
js = js.replace('let isDataLoaded = false;', default_rooms + 'let isDataLoaded = false;')

# DOM Elements
new_doms = """    const locationSelect = document.getElementById('location-select');
    const locationInput = document.getElementById('location-input');
    const newRoomName = document.getElementById('new-room-name');
    const addRoomBtn = document.getElementById('add-room-btn');
    const adminRoomsList = document.getElementById('admin-rooms-list');"""
js = js.replace('const locationInput = document.getElementById(\'location\');', new_doms)

# Firebase Load
fb_rooms = """        // 5. Load Rooms
        if(data.rooms) {
            rooms = data.rooms;
        } else {
            rooms = defaultRooms;
            set(ref(db, 'churchApp/rooms'), defaultRooms);
        }"""
js = js.replace('        isDataLoaded = true;', fb_rooms + '\n\n        isDataLoaded = true;')

# populateRooms call in onValue
js = js.replace('populateOrganizationOptions();', 'populateOrganizationOptions();\n        populateRooms();')

# populateRooms definition
populate_fn = """    function populateRooms() {
        if(!locationSelect) return;
        locationSelect.innerHTML = '<option value="" disabled selected>장소를 선택하세요</option>';
        rooms.forEach(room => {
            locationSelect.innerHTML += `<option value="${room}">${room}</option>`;
        });
        locationSelect.innerHTML += `<option value="custom">기타 (직접 입력)</option>`;
    }"""
js = js.replace('function populateOrganizationOptions() {', populate_fn + '\n\n    function populateOrganizationOptions() {')

# switchFormType updates
switch_old = """        if (type === 'vehicle') {
            locationLabel.innerHTML = '목적지 (선택)';
            locationInput.removeAttribute('required');
            formTitle.innerHTML = `<i class="ph ph-calendar-plus"></i> ${menuNames.vehicle} 등록`;
        } else if (type === 'cell') {
            locationLabel.innerHTML = '예약 장소 <span class="required" style="color: var(--danger);">*</span>';
            locationInput.setAttribute('required', 'true');
            formTitle.innerHTML = `<i class="ph ph-calendar-plus"></i> ${menuNames.cell} 등록`;
        } else {
            locationLabel.innerHTML = '장소 <span class="required" style="color: var(--danger);">*</span>';
            locationInput.setAttribute('required', 'true');
            formTitle.innerHTML = `<i class="ph ph-calendar-plus"></i> ${menuNames.committee} 등록`;
        }"""
switch_new = """        if (type === 'vehicle') {
            locationLabel.innerHTML = '목적지 (선택)';
            locationSelect.style.display = 'none';
            locationSelect.removeAttribute('required');
            locationInput.style.display = 'block';
            locationInput.removeAttribute('required');
            locationInput.placeholder = "예: 양평수양관, 시청역";
            formTitle.innerHTML = `<i class="ph ph-calendar-plus"></i> ${menuNames.vehicle} 등록`;
        } else if (type === 'cell') {
            locationLabel.innerHTML = '예약 장소 <span class="required" style="color: var(--danger);">*</span>';
            locationSelect.style.display = 'block';
            locationSelect.setAttribute('required', 'true');
            if (locationSelect.value !== 'custom') locationInput.style.display = 'none';
            locationInput.setAttribute('required', 'true');
            locationInput.placeholder = "직접 입력 (예: 본당, 소예배실)";
            formTitle.innerHTML = `<i class="ph ph-calendar-plus"></i> ${menuNames.cell} 등록`;
        } else {
            locationLabel.innerHTML = '장소 <span class="required" style="color: var(--danger);">*</span>';
            locationSelect.style.display = 'block';
            locationSelect.setAttribute('required', 'true');
            if (locationSelect.value !== 'custom') locationInput.style.display = 'none';
            locationInput.setAttribute('required', 'true');
            locationInput.placeholder = "직접 입력 (예: 본당, 소예배실)";
            formTitle.innerHTML = `<i class="ph ph-calendar-plus"></i> ${menuNames.committee} 등록`;
        }"""
js = js.replace(switch_old, switch_new)

# Location Select Event Listener
select_listener = """    locationSelect.addEventListener('change', () => {
        if (locationSelect.value === 'custom') {
            locationInput.style.display = 'block';
            locationInput.setAttribute('required', 'true');
            locationInput.value = '';
            locationInput.focus();
        } else {
            locationInput.style.display = 'none';
            locationInput.removeAttribute('required');
        }
    });"""
js = js.replace('// Form Interactions', '// Form Interactions\n' + select_listener)

# conflict check loc
conflict_loc_old = """        const loc = locationInput.value;"""
conflict_loc_new = """        let loc = locationInput.value;
        if (type !== 'vehicle' && locationSelect.value !== 'custom') {
            loc = locationSelect.value;
        }"""
js = js.replace(conflict_loc_old, conflict_loc_new)

# Form Submit loc
submit_loc_old = """        const newEvent = {
            id: isEditMode ? editEventIdInput.value : Date.now().toString(),
            eventType: selectedType,
            date: dateInput.value,
            startTime: startTimeInput.value,
            endTime: endTimeInput.value,
            location: locationInput.value,
            description: descriptionInput.value,
            password: eventPasswordInput.value
        };"""
submit_loc_new = """        let finalLocation = locationInput.value;
        if (selectedType !== 'vehicle') {
            if (locationSelect.value !== 'custom') {
                finalLocation = locationSelect.value;
            }
        }
        
        const newEvent = {
            id: isEditMode ? editEventIdInput.value : Date.now().toString(),
            eventType: selectedType,
            date: dateInput.value,
            startTime: startTimeInput.value,
            endTime: endTimeInput.value,
            location: finalLocation,
            description: descriptionInput.value,
            password: eventPasswordInput.value
        };"""
js = js.replace(submit_loc_old, submit_loc_new)

# Edit event population
edit_pop_old = """        locationInput.value = ev.location;"""
edit_pop_new = """        if (ev.eventType === 'vehicle') {
            locationInput.value = ev.location;
        } else {
            if (rooms.includes(ev.location)) {
                locationSelect.value = ev.location;
                locationSelect.dispatchEvent(new Event('change'));
            } else {
                locationSelect.value = 'custom';
                locationSelect.dispatchEvent(new Event('change'));
                locationInput.value = ev.location;
            }
        }"""
js = js.replace(edit_pop_old, edit_pop_new)

# Admin Room Management Rendering and Handlers
admin_rooms_code = """    function renderAdminRoomsList() {
        if(!adminRoomsList) return;
        adminRoomsList.innerHTML = '';
        rooms.forEach((room, idx) => {
            const li = document.createElement('li');
            li.className = 'org-dept-item';
            li.innerHTML = `
                ${room}
                <button type="button" class="delete-room-btn" data-index="${idx}" title="삭제"><i class="ph ph-x"></i></button>
            `;
            adminRoomsList.appendChild(li);
        });
        
        document.querySelectorAll('.delete-room-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idx = e.currentTarget.getAttribute('data-index');
                showConfirm("장소 삭제", `'${rooms[idx]}' 항목을 삭제하시겠습니까?`, () => {
                    rooms.splice(idx, 1);
                    set(ref(db, 'churchApp/rooms'), rooms);
                    showToast("장소가 삭제되었습니다.");
                });
            });
        });
    }

    addRoomBtn.addEventListener('click', () => {
        const name = newRoomName.value.trim();
        if(name) {
            if(!rooms.includes(name)) {
                rooms.push(name);
                set(ref(db, 'churchApp/rooms'), rooms);
                newRoomName.value = '';
                showToast("장소가 추가되었습니다.");
            } else {
                alert('이미 존재하는 장소입니다.');
            }
        }
    });"""

js = js.replace('function renderAdminOrgList() {', admin_rooms_code + '\n\n    function renderAdminOrgList() {')

# Hook renderAdminRoomsList into renderAdminOrgList wrapper or onValue
js = js.replace('renderAdminOrgList();', 'renderAdminOrgList();\n        renderAdminRoomsList();')

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(js)

