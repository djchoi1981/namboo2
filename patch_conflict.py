with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    js = f.read()

conflict_old = """    function checkForConflicts(excludeId = null) {
        const date = dateInput.value;
        const start = startTimeInput.value;
        const end = endTimeInput.value;
        let loc = locationInput.value;
        if (type !== 'vehicle' && locationSelect.value !== 'custom') {
            loc = locationSelect.value;
        } 
        const type = currentEventTypeInput.value;"""

conflict_new = """    function checkForConflicts(excludeId = null) {
        const date = dateInput.value;
        const start = startTimeInput.value;
        const end = endTimeInput.value;
        const type = currentEventTypeInput.value;
        let loc = locationInput.value;
        if (type !== 'vehicle' && locationSelect.value !== 'custom') {
            loc = locationSelect.value;
        } """

js = js.replace(conflict_old, conflict_new)

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'w') as f:
    f.write(js)
