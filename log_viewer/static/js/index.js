// script.js

document.addEventListener('DOMContentLoaded', function () {
    // DOM elements
    const searchInput = document.getElementById('searchInput');
    const levelFilter = document.getElementById('levelFilter');
    const logsContainer = document.getElementById('logsContainer');

    // Function to fetch logs based on filters and update UI
    function fetchAndRenderLogs() {
        const searchQuery = searchInput.value;
        const selectedLevel = levelFilter.value;

        // Build API URL with filters
        const apiUrl = `/logs/?search=${searchQuery}&level=${selectedLevel}`;

        // Fetch logs from the API
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Clear existing logs
                logsContainer.innerHTML = '';

                // Render each log entry
                data.logs.forEach(log => {
                    const logEntry = document.createElement('div');
                    logEntry.classList.add('log-entry');
                    logEntry.innerHTML = `
                        <span>Level:</span> ${log.level}<br>
                        <span>Message:</span> ${log.message}<br>
                        <span>Resource ID:</span> ${log.resourceId}<br>
                        <span>Timestamp:</span> ${log.timestamp}<br>
                        <span>Trace ID:</span> ${log.traceId}<br>
                        <span>Span ID:</span> ${log.spanId}<br>
                        <span>Commit:</span> ${log.commit}<br>
                        <span>Parent Resource ID:</span> ${log.parentResourceId || 'N/A'}<br>
                    `;
                    logsContainer.appendChild(logEntry);
                });
            })
            .catch(error => {
                console.error('Error fetching logs:', error);
            });
    }

    // Attach event listeners
    searchInput.addEventListener('input', fetchAndRenderLogs);
    levelFilter.addEventListener('change', fetchAndRenderLogs);

    // Initial fetch and render
    fetchAndRenderLogs();
});
