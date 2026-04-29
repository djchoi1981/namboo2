with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'r') as f:
    html = f.read()

import re

loc_container = re.search(r'(\s*<div class="form-group" id="location-container">.*?</select>\s*<input type="text" id="location-input".*?</div>)', html, re.DOTALL)
if loc_container:
    loc_text = loc_container.group(1)
    # Remove it from the original place
    html = html.replace(loc_text, '')
    
    # Insert it after conflict-alert
    conflict_alert = '                            <div id="conflict-message">해당 시간/장소에 이미 겹치는 일정이 있습니다!</div>\n                        </div>\n'
    
    html = html.replace(conflict_alert, conflict_alert + '\n' + loc_text + '\n')
    
    with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'w') as f:
        f.write(html)
        print("Moved successfully")
else:
    print("Could not find loc container")
