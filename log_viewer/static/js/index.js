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
                        <strong>Level:</strong> ${log.level}
                        <strong>Message:</strong> ${log.message}
                        <strong>Resource ID:</strong> ${log.resourceId}
                        <strong>Timestamp:</strong> ${log.timestamp}
                        <strong>Trace ID:</strong> ${log.traceId}
                        <strong>Span ID:</strong> ${log.spanId}
                        <strong>Commit:</strong> ${log.commit}
                        <strong>Parent Resource ID:</strong> ${log.parentResourceId || 'N/A'}
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
