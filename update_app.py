import re

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    js = f.read()

# Remove old references
js = re.sub(r'const navAdmin = document.getElementById\(\'nav-admin\'\);', '', js)
js = re.sub(r'const pageTitle = document.getElementById\(\'page-title\'\);', '', js)
js = re.sub(r'const loginBtn = document.getElementById\(\'login-btn\'\);', '', js)
js = re.sub(r'const logoutBtn = document.getElementById\(\'logout-btn\'\);', '', js)
js = re.sub(r'const adminProfile = document.getElementById\(\'admin-profile\'\);', '', js)

# Add new references near the top
new_refs = """    const sidebarAdminBtn = document.getElementById('sidebar-admin-btn');
    const sidebarLogoutBtn = document.getElementById('sidebar-logout-btn');"""
js = js.replace('    const navVehicle = document.getElementById(\'nav-vehicle\');', '    const navVehicle = document.getElementById(\'nav-vehicle\');\n' + new_refs)

# Replace pageTitle updates with empty strings or comments
js = re.sub(r'if\(navCommittee\.classList\.contains\(\'active\'\)\) pageTitle\.textContent = `\$\{menuNames\.committee\} 등록 및 현황`;', '', js)
js = re.sub(r'if\(navCell\.classList\.contains\(\'active\'\)\) pageTitle\.textContent = `\$\{menuNames\.cell\} 및 현황`;', '', js)
js = re.sub(r'if\(navVehicle\.classList\.contains\(\'active\'\)\) pageTitle\.textContent = `\$\{menuNames\.vehicle\} 및 현황`;', '', js)

js = re.sub(r'pageTitle\.textContent = .*?;', '', js)

# Update hideAllSections
hide_all_old = """        navCalendar.classList.remove('active');
        navCommittee.classList.remove('active');
        navCell.classList.remove('active');
        navVehicle.classList.remove('active');
        navAdmin.classList.remove('active');"""
hide_all_new = """        navCalendar.classList.remove('active');
        navCommittee.classList.remove('active');
        navCell.classList.remove('active');
        navVehicle.classList.remove('active');
        sidebarAdminBtn.classList.remove('active');"""
js = js.replace(hide_all_old, hide_all_new)

# Update navAdmin.addEventListener to sidebarAdminBtn click handling logic
nav_admin_event_old = """    navAdmin.addEventListener('click', (e) => {
        e.preventDefault();
        hideAllSections();
        navAdmin.classList.add('active');
        adminSection.style.display = 'block';
        registrationSection.style.display = 'none';
        
        monthNavigation.style.display = 'none';
        renderAdminOrgList();
        renderAdminEventsList();
    });"""

nav_admin_event_new = """    sidebarAdminBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (!isLoggedIn) {
            loginModal.style.display = 'flex';
            loginPassword.value = '';
            loginError.style.display = 'none';
            loginPassword.focus();
        } else {
            hideAllSections();
            sidebarAdminBtn.classList.add('active');
            adminSection.style.display = 'block';
            registrationSection.style.display = 'none';
            monthNavigation.style.display = 'none';
            renderAdminOrgList();
            renderAdminEventsList();
        }
    });
    
    sidebarLogoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        isLoggedIn = false;
        sidebarLogoutBtn.style.display = 'none';
        sidebarAdminBtn.innerHTML = '<i class="ph ph-gear"></i> 관리자 모드';
        
        if (adminSection.style.display === 'block') {
            navCalendar.click();
        }
        showToast("로그아웃 되었습니다.");
    });"""
js = js.replace(nav_admin_event_old, nav_admin_event_new)

# Remove old login logic
js = re.sub(r'loginBtn\.addEventListener\(\'click\', \(\) => \{[\s\S]*?loginPassword\.focus\(\);\n    \}\);', '', js)
js = re.sub(r'logoutBtn\.addEventListener\(\'click\', \(\) => \{[\s\S]*?showToast\("로그아웃 되었습니다\."\);\n    \}\);', '', js)

# Update submitLoginBtn success logic
submit_login_old = """        if(loginPassword.value === adminPassword) {
            isLoggedIn = true;
            loginModal.style.display = 'none';
            loginBtn.style.display = 'none';
            adminProfile.style.display = 'flex';
            navAdmin.style.display = 'flex';
            showToast("관리자로 로그인되었습니다.");"""
submit_login_new = """        if(loginPassword.value === adminPassword) {
            isLoggedIn = true;
            loginModal.style.display = 'none';
            
            sidebarAdminBtn.innerHTML = '<i class="ph ph-gear"></i> 관리자 설정 (마스터)';
            sidebarLogoutBtn.style.display = 'block';
            
            showToast("관리자로 로그인되었습니다.");
            
            // automatically click admin btn to open it
            sidebarAdminBtn.click();"""
js = js.replace(submit_login_old, submit_login_new)

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(js)
