import re

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    content = f.read()

custom_confirm_fn = """
    function showConfirm(title, message, onOk) {
        document.getElementById('confirm-title').textContent = title;
        document.getElementById('confirm-message').textContent = message;
        const modal = document.getElementById('confirm-modal');
        const okBtn = document.getElementById('confirm-ok-btn');
        const cancelBtn = document.getElementById('confirm-cancel-btn');
        
        modal.style.display = 'flex';
        
        // Remove old event listeners
        const newOkBtn = okBtn.cloneNode(true);
        const newCancelBtn = cancelBtn.cloneNode(true);
        okBtn.parentNode.replaceChild(newOkBtn, okBtn);
        cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);
        
        newCancelBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
        
        newOkBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            onOk();
        });
    }

    // Modal Actions
"""
content = content.replace('    // Modal Actions\n', custom_confirm_fn)

delete_event_code_old = """        if(confirm("정말로 이 일정을 삭제하시겠습니까?")) {
            events = events.filter(e => e.id !== ev.id);
            saveEvents();
            renderCalendar();
            renderUpcomingEvents();
            renderCommitteeList();
            renderCellList();
            renderVehicleList();
            if(isLoggedIn) renderAdminEventsList();
            eventModal.style.display = 'none';
            showToast("삭제되었습니다.");
        }"""
delete_event_code_new = """        showConfirm("일정 삭제", "정말로 이 일정을 삭제하시겠습니까?", () => {
            events = events.filter(e => e.id !== ev.id);
            saveEvents();
            renderCalendar();
            renderUpcomingEvents();
            renderCommitteeList();
            renderCellList();
            renderVehicleList();
            if(isLoggedIn) renderAdminEventsList();
            eventModal.style.display = 'none';
            showToast("삭제되었습니다.");
        });"""
content = content.replace(delete_event_code_old, delete_event_code_new)

admin_delete_event_old = """                if(confirm("정말로 이 예약을 강제 삭제하시겠습니까? (관리자 권한)")) {
                    events = events.filter(e => e.id !== id);
                    saveEvents();
                    renderAdminEventsList();
                    renderCalendar();
                    renderUpcomingEvents();
                    showToast("삭제되었습니다.");
                }"""
admin_delete_event_new = """                showConfirm("예약 강제 삭제", "정말로 이 예약을 강제 삭제하시겠습니까? (관리자 권한)", () => {
                    events = events.filter(e => e.id !== id);
                    saveEvents();
                    renderAdminEventsList();
                    renderCalendar();
                    renderUpcomingEvents();
                    showToast("삭제되었습니다.");
                });"""
content = content.replace(admin_delete_event_old, admin_delete_event_new)

delete_comm_old = """                if(confirm(`'${orgName}'와 그 안의 모든 부서를 정말 삭제하시겠습니까?`)) {
                    organization.splice(orgIdx, 1);
                    saveOrganization();
                    populateOrganizationOptions();
                    renderAdminOrgList();
                    showToast("위원회가 삭제되었습니다.");
                }"""
delete_comm_new = """                showConfirm("위원회 삭제", `'${orgName}'와 그 안의 모든 부서를 정말 삭제하시겠습니까?`, () => {
                    organization.splice(orgIdx, 1);
                    saveOrganization();
                    populateOrganizationOptions();
                    renderAdminOrgList();
                    showToast("위원회가 삭제되었습니다.");
                });"""
content = content.replace(delete_comm_old, delete_comm_new)

delete_dept_old = """                if(confirm(`이 부서를 삭제하시겠습니까?`)) {
                    organization[orgIdx].departments.splice(deptIdx, 1);
                    saveOrganization();
                    populateOrganizationOptions();
                    renderAdminOrgList();
                    showToast("부서가 삭제되었습니다.");
                }"""
delete_dept_new = """                showConfirm("부서 삭제", `이 부서를 삭제하시겠습니까?`, () => {
                    organization[orgIdx].departments.splice(deptIdx, 1);
                    saveOrganization();
                    populateOrganizationOptions();
                    renderAdminOrgList();
                    showToast("부서가 삭제되었습니다.");
                });"""
content = content.replace(delete_dept_old, delete_dept_new)

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(content)

