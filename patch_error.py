import re

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    js = f.read()

old_block = """        if (isLoggedIn) {
            renderAdminOrgList();
            renderAdminEventsList();
        }
    });"""

new_block = """        if (isLoggedIn) {
            renderAdminOrgList();
            renderAdminEventsList();
        }
    }, (error) => {
        alert("파이어베이스 오류가 발생했습니다! (보안 규칙 또는 네트워크 문제)\\n" + error.message);
    });"""

js = js.replace(old_block, new_block)

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(js)

