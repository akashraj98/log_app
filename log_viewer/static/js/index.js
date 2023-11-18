// script.js

document.addEventListener('DOMContentLoaded', function () {
    // DOM elements
    const searchInput = document.getElementById('searchInput');
    const levelFilter = document.getElementById('levelFilter');
    const logsContainer = document.getElementById('logsContainer');
    const searchField = document.getElementById('searchField');
    const applyFiltersBtn = document.getElementById('applyFiltersBtn');
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    const current_page = document.getElementById('currentPage');
    const total_pages = document.getElementById('totalPages');
    const nextPageBtn = document.getElementById('nextPageBtn');
    const prevPageBtn = document.getElementById('prevPageBtn');


    flatpickr('#startDate', {
        enableTime: true,
        allowInput: true,
        dateFormat: "Y-m-d h:iK",
        "plugins": [new rangePlugin({ input: "#endDate"})]
      });

    // debounce
    function debounce(func, delay) {
        let timeoutId;
        return function () {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                func.apply(this, arguments);
            }, delay);
        };
    }

    // Function to fetch logs based on filters and update UI
    function fetchAndRenderLogs(pageNumber = 1) {
        const searchQuery = searchInput.value;
        const selectedLevel = levelFilter.value;
        const selectedField = searchField.value;
        const selectedStartDate = startDate.value;
        const selectedEndDate = endDate.value;
        


        // Build API URL with filters
        let apiUrl = `/logs/?level=${selectedLevel}`;
        if (selectedField !== '') {
            apiUrl += `&${selectedField}=${searchQuery}`
        } else {
            apiUrl += `&q=${searchQuery}`
        }
        if (selectedStartDate !== '') {
            apiUrl += `&start_timestamp=${selectedStartDate}`
        }
        if (selectedEndDate !== '') {
            apiUrl += `&end_timestamp=${selectedEndDate}`
        }
        apiUrl += `&page=${pageNumber}`

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
                current_page.textContent = data.current_page;
                total_pages.textContent = data.total_pages;

            })
            .catch(error => {
                console.error('Error fetching logs:', error);
            });
    }

    // Attach event listeners
    const debouncedFetchAndRenderLogs = debounce(function() {
        fetchAndRenderLogs()
    }, 500);
    searchInput.addEventListener('input', debouncedFetchAndRenderLogs);
    levelFilter.addEventListener('change', function() {
        fetchAndRenderLogs(); 
    });
    applyFiltersBtn.addEventListener('click', function() {
        fetchAndRenderLogs(); 
    });

    
    nextPageBtn.addEventListener('click', function () {
        const currentPageNumber = parseInt(current_page.textContent, 10);
        const nextPageNumber = currentPageNumber + 1;

        // Update the current_page span
        current_page.textContent = nextPageNumber;

        // Fetch and render logs for the next page
        fetchAndRenderLogs(nextPageNumber);
    });

    prevPageBtn.addEventListener('click', function () {
        const currentPageNumber = parseInt(current_page.textContent, 10);
        
        // Ensure the page number doesn't go below 1
        const prevPageNumber = Math.max(currentPageNumber - 1, 1);

        // Update the current_page span
        current_page.textContent = prevPageNumber;

        // Fetch and render logs for the previous page
        fetchAndRenderLogs(prevPageNumber);
    });

    // Initial fetch and render
    fetchAndRenderLogs();
});
