document.addEventListener('DOMContentLoaded', function() {
    const calendarContainer = document.getElementById('calendarss');

    function generateCalendar(monthOffset = 0) {
        const date = new Date();
        date.setMonth(date.getMonth() + monthOffset);
        const currentMonth = date.getMonth();
        const currentYear = date.getFullYear();
        const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
        const lastDayOfMonth = new Date(currentYear, currentMonth + 1, 0);
        const daysInMonth = lastDayOfMonth.getDate();
        const firstDay = firstDayOfMonth.getDay();
        
        let calendarHTML = `
            <div class="calendarss-header">
                ${date.toLocaleString('default', { month: 'long' })} ${currentYear}
            </div>
            <div class="calendarss-days">
                <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
        `;

        // Create empty cells for the previous month's days
        for (let i = 0; i < firstDay; i++) {
            calendarHTML += '<div class="calendarss-day"></div>';
        }

        // Add the actual days of the current month
        for (let day = 1; day <= daysInMonth; day++) {
            const isToday = new Date().getDate() === day && new Date().getMonth() === currentMonth;
            const dayClass = isToday ? 'calendarss-day today' : 'calendarss-day';
            calendarHTML += `<div class="${dayClass}">${day}</div>`;
        }

        calendarHTML += `</div>`;
        calendarContainer.innerHTML = calendarHTML;
    }

    generateCalendar();

});