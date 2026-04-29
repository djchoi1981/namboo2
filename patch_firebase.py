import re

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    js = f.read()

# 1. Remove DOMContentLoaded wrapper because it's a module
js = js.replace("document.addEventListener('DOMContentLoaded', () => {", "")
js = js.rstrip()
if js.endswith("});"):
    js = js[:-3]

# 2. Add Firebase imports and initialization at the top
firebase_header = """import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getDatabase, ref, onValue, set, remove, get } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";

const firebaseConfig = {
  apiKey: "AIzaSyDSyk8SUIMDGM9OHh6EciapPp3I7tyOH6o",
  authDomain: "nambooch-c4a73.firebaseapp.com",
  projectId: "nambooch-c4a73",
  storageBucket: "nambooch-c4a73.firebasestorage.app",
  messagingSenderId: "168237220696",
  appId: "1:168237220696:web:c13440fbecd443dc20db2d",
  measurementId: "G-HG0Z1PV29Z"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// Data states
let events = [];
let organization = [];
let menuNames = { committee: '위원회/부서 일정', cell: '셀/모임 장소예약', vehicle: '차량 운영예약' };
let adminPassword = '0191';
let isDataLoaded = false;
let currentDate = new Date();
"""

# Replace the state definitions in original file
state_def_pattern = re.compile(r'// State.*?let currentDate = new Date\(\);\n', re.DOTALL)
js = state_def_pattern.sub("", js)

org_def_pattern = re.compile(r'const defaultOrganization = \[.*?\];\n.*?let adminPassword = localStorage\.getItem\(\'churchAdminPassword\'\) \|\| \'0191\';\n.*?let menuNames = JSON\.parse\(localStorage\.getItem\(\'churchMenuNames\'\)\) \|\| \{.*?\};\n', re.DOTALL)
js = org_def_pattern.sub("", js)

# We need to add the default organization definition back so we can use it for seeding
default_org = """
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
"""

js = firebase_header + default_org + js

# Replace Initialization Logic
init_old = """    // Initialize
    applyMenuNames();
    populateOrganizationOptions();
    renderCalendar();
    renderUpcomingEvents();
    renderCommitteeList();
    renderCellList();
    renderVehicleList();
    
    const todayStr = new Date().toISOString().split('T')[0];
    dateInput.value = todayStr;"""

init_new = """    const todayStr = new Date().toISOString().split('T')[0];
    if(dateInput) dateInput.value = todayStr;

    // Listen to Firebase Data Changes
    const appDataRef = ref(db, 'churchApp');
    onValue(appDataRef, (snapshot) => {
        const data = snapshot.val() || {};
        
        // 1. Load Organization
        if(data.organization) {
            organization = data.organization;
        } else {
            organization = defaultOrganization;
            // Seed DB
            set(ref(db, 'churchApp/organization'), defaultOrganization);
        }
        
        // 2. Load Events
        if(data.events) {
            events = Object.values(data.events); // convert object back to array
        } else {
            events = [];
        }
        
        // 3. Load Menu Names
        if(data.menuNames) {
            menuNames = data.menuNames;
        } else {
            set(ref(db, 'churchApp/menuNames'), menuNames);
        }
        
        // 4. Load Admin Password
        if(data.adminPassword) {
            adminPassword = data.adminPassword;
        } else {
            set(ref(db, 'churchApp/adminPassword'), adminPassword);
        }

        isDataLoaded = true;
        
        // Re-render UI
        applyMenuNames();
        populateOrganizationOptions();
        renderCalendar();
        renderUpcomingEvents();
        renderCommitteeList();
        renderCellList();
        renderVehicleList();
        if (isLoggedIn) {
            renderAdminOrgList();
            renderAdminEventsList();
        }
    });"""
js = js.replace(init_old, init_new)

# Replace localstorage sets
js = re.sub(r'localStorage\.setItem\(\'churchMenuNames\', JSON\.stringify\(menuNames\)\);', r'set(ref(db, \'churchApp/menuNames\'), menuNames);', js)
js = re.sub(r'localStorage\.setItem\(\'churchAdminPassword\', adminPassword\);', r'set(ref(db, \'churchApp/adminPassword\'), adminPassword);', js)

# Change saveEvents and saveOrganization implementations
save_events_old = """    function saveEvents() {
        localStorage.setItem('churchEvents_v2', JSON.stringify(events));
    }
    
    function saveOrganization() {
        localStorage.setItem('nambuOrganization_v1', JSON.stringify(organization));
    }"""
    
save_events_new = """    function saveEvents() {
        // Firebase works best with objects instead of arrays. Let's convert array to object using id as key
        const eventsObj = {};
        events.forEach(e => { eventsObj[e.id] = e; });
        set(ref(db, 'churchApp/events'), eventsObj);
    }
    
    function saveOrganization() {
        set(ref(db, 'churchApp/organization'), organization);
    }"""
js = js.replace(save_events_old, save_events_new)

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(js)

