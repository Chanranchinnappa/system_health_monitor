document.addEventListener('DOMContentLoaded', () => {
    const machinesList = document.getElementById('machines-list');
    const osFilter = document.getElementById('os-filter');
    const statusFilter = document.getElementById('status-filter');
    let allMachinesData = [];

    const API_URL = "http://127.0.0.1:5000/api/v1/machines";

    async function fetchMachines() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            allMachinesData = await response.json();
            renderMachines();
        } catch (error) {
            console.error("Could not fetch machines:", error);
            machinesList.innerHTML = `<p class="error">Failed to load data. Is the backend server running?</p>`;
        }
    }

    function renderMachines() {
        const selectedOS = osFilter.value;
        const selectedStatus = statusFilter.value;

        const filteredMachines = allMachinesData.filter(machine => {
            const hasIssue = hasConfigurationIssues(machine);
            const osMatch = selectedOS === 'all' || machine.os === selectedOS;
            const statusMatch = selectedStatus === 'all' || (selectedStatus === 'ok' && !hasIssue) || (selectedStatus === 'issue' && hasIssue);
            return osMatch && statusMatch;
        });

        machinesList.innerHTML = '';
        if (filteredMachines.length === 0) {
            machinesList.innerHTML = `<p class="no-results">No machines found matching your criteria.</p>`;
            return;
        }

        filteredMachines.forEach(machine => {
            const hasIssue = hasConfigurationIssues(machine);
            const cardClass = hasIssue ? 'issue' : 'ok';
            const statusIcon = hasIssue ? '🔴' : '🟢';

           const machineCard = document.createElement('div');
        machineCard.className = `machine-card ${cardClass}`;
        machineCard.innerHTML = `
            <h3>${statusIcon} ${machine.os} <small>(ID: ${machine.machine_id.slice(0, 8)})</small></h3>
            <small>Last check-in: ${new Date(machine.last_check_in * 1000).toLocaleString()}</small>
            <ul class="check-list">
                ${Object.entries(machine.checks).map(([key, value]) => `
                    <li class="check-item">
                        <span>${key.replace(/_/g, ' ').toUpperCase()}:</span>
                        <span class="check-status ${value === 'Encrypted' || value === 'Up to Date' || value === 'Present' || (value.includes('%') ? 'ok' : 'issue')}">
                            ${value}
                        </span>
                    </li>
                `).join('')}
            </ul>
            `;
            machinesList.appendChild(machineCard);
        });
    }

    function hasConfigurationIssues(machine) {
        return Object.values(machine.checks).some(value => {
            return value === 'Not Encrypted' || value === 'Updates Available' || value === 'Not Present';
        });
    }

    osFilter.addEventListener('change', renderMachines);
    statusFilter.addEventListener('change', renderMachines);

    // Initial fetch
    fetchMachines();
    // Refresh data every 30 seconds
    setInterval(fetchMachines, 30000);
});