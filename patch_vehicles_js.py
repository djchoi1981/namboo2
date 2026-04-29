import re

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    js = f.read()

# 1. Add Default Vehicles
default_veh = """
const defaultVehicles = [
    '스타렉스 1호',
    '스타렉스 2호',
    '스타렉스 3호',
    '스타리아',
    '25인승 버스',
    '45인승 버스'
];
let vehicles = [];
"""
js = js.replace('let rooms = [];', 'let rooms = [];\n' + default_veh)

# 2. Add DOM Elements
new_doms = """    const newVehicleName = document.getElementById('new-vehicle-name');
    const addVehicleBtn = document.getElementById('add-vehicle-btn');
    const adminVehiclesList = document.getElementById('admin-vehicles-list');
    const vehicleSelect = document.getElementById('vehicle');"""
js = js.replace('const filterVehicle = document.getElementById(\'filter-vehicle\');', 'const filterVehicle = document.getElementById(\'filter-vehicle\');\n' + new_doms)

# 3. Load Vehicles in onValue
fb_veh = """        // 6. Load Vehicles
        if(data.vehicles) {
            vehicles = data.vehicles;
        } else {
            vehicles = defaultVehicles;
            set(ref(db, 'churchApp/vehicles'), defaultVehicles);
        }"""
js = js.replace('        isDataLoaded = true;', fb_veh + '\n\n        isDataLoaded = true;')

# 4. Add populateVehicles logic
populate_veh = """    function populateVehicles() {
        if(!filterVehicle || !vehicleSelect) return;
        filterVehicle.innerHTML = '<option value="all">모든 차량 보기</option>';
        vehicleSelect.innerHTML = '<option value="" disabled selected>선택하세요</option>';
        vehicles.forEach(veh => {
            filterVehicle.innerHTML += `<option value="${veh}">${veh}</option>`;
            vehicleSelect.innerHTML += `<option value="${veh}">${veh}</option>`;
        });
    }"""
js = js.replace('function populateRooms() {', populate_veh + '\n\n    function populateRooms() {')
js = js.replace('populateRooms();', 'populateRooms();\n        populateVehicles();')

# 5. Admin vehicle logic
admin_veh_code = """    function renderAdminVehiclesList() {
        if(!adminVehiclesList) return;
        adminVehiclesList.innerHTML = '';
        vehicles.forEach((veh, idx) => {
            const li = document.createElement('li');
            li.className = 'org-dept-item';
            li.innerHTML = `
                ${veh}
                <button type="button" class="delete-vehicle-btn" data-index="${idx}" title="삭제"><i class="ph ph-x"></i></button>
            `;
            adminVehiclesList.appendChild(li);
        });
        
        document.querySelectorAll('.delete-vehicle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idx = e.currentTarget.getAttribute('data-index');
                showConfirm("차량 삭제", `'${vehicles[idx]}' 항목을 삭제하시겠습니까?`, () => {
                    vehicles.splice(idx, 1);
                    set(ref(db, 'churchApp/vehicles'), vehicles);
                    showToast("차량이 삭제되었습니다.");
                });
            });
        });
    }

    if(addVehicleBtn) {
        addVehicleBtn.addEventListener('click', () => {
            const name = newVehicleName.value.trim();
            if(name) {
                if(!vehicles.includes(name)) {
                    vehicles.push(name);
                    set(ref(db, 'churchApp/vehicles'), vehicles);
                    newVehicleName.value = '';
                    showToast("차량이 추가되었습니다.");
                } else {
                    alert('이미 존재하는 차량입니다.');
                }
            }
        });
    }"""
js = js.replace('function renderAdminRoomsList() {', admin_veh_code + '\n\n    function renderAdminRoomsList() {')
js = js.replace('renderAdminRoomsList();', 'renderAdminRoomsList();\n        renderAdminVehiclesList();')

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(js)

