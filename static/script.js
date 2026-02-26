document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('scrape-form');
    const startBtn = document.getElementById('startBtn');
    const loader = document.querySelector('.loader');
    const btnText = document.querySelector('.btn-text');
    const logsContainer = document.getElementById('logs');
    
    // Tab containers
    const tabsHeader = document.getElementById('tabsHeader');
    const tabsContent = document.getElementById('tabsContent');
    const emptyState = document.getElementById('emptyState');

    // Restore saved settings
    ['keyword', 'maxPrice', 'maxPages', 'currency', 'tgToken', 'tgChatId'].forEach(id => {
        const saved = localStorage.getItem(id);
        if (saved) document.getElementById(id).value = saved;
    });

    let eventSource = null;

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Save settings
        ['keyword', 'maxPrice', 'maxPages', 'currency', 'tgToken', 'tgChatId'].forEach(id => {
            localStorage.setItem(id, document.getElementById(id).value);
        });

        const keyword = document.getElementById('keyword').value;
        const maxPrice = document.getElementById('maxPrice').value;
        const maxPages = document.getElementById('maxPages').value;
        const crc = document.getElementById('currency').value;
        const tgToken = document.getElementById('tgToken').value;
        const tgChatId = document.getElementById('tgChatId').value;

        // UI Reset
        logsContainer.innerHTML = '';
        tabsHeader.innerHTML = '';
        tabsContent.innerHTML = '<div class="empty-state" id="emptyState" style="display:none;">Results will appear here...</div>';
        addLog('Connecting to server...', 'log');
        setLoading(true);

        // Build URL
        const params = new URLSearchParams({
            keyword: keyword, 
            max_price: maxPrice, 
            max_pages: maxPages, 
            crc: crc,
            tg_token: tgToken, 
            tg_chat_id: tgChatId
        });

        // Close existing SSE connection if any
        if (eventSource) {
            eventSource.close();
        }

        eventSource = new EventSource(`/api/start?${params.toString()}`);

        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                
                if (data.type === 'log') {
                    addLog(data.message, 'log');
                } else if (data.type === 'error') {
                    addLog(data.message, 'error');
                } else if (data.type === 'item') {
                    addItemToTable(data);
                } else if (data.type === 'finish') {
                    addLog(data.message, 'log');
                    addLog('✅ Done!', 'log');
                    setLoading(false);
                    eventSource.close();
                }
            } catch (err) {
                console.error("Error parsing SSE data", err);
            }
        };

        eventSource.onerror = (err) => {
            console.error("EventSource failed:", err);
            addLog('[Error] Connection to server lost.', 'error');
            setLoading(false);
            eventSource.close();
        };
    });

    function addLog(message, type) {
        const div = document.createElement('div');
        div.className = `log-entry ${type === 'error' ? 'log-error' : ''}`;
        div.textContent = message;
        logsContainer.appendChild(div);
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }

    function createTab(keyword) {
        const tabId = 'tab-' + btoa(unescape(encodeURIComponent(keyword))).replace(/[^a-zA-Z0-9]/g, '');
        
        // Check if tab already exists
        if (document.getElementById(`btn-${tabId}`)) return tabId;
        
        const isFirstTab = tabsHeader.children.length === 0;

        if (isFirstTab && emptyState) {
            emptyState.style.display = 'none';
        }

        // Create Tab Button
        const btn = document.createElement('button');
        btn.id = `btn-${tabId}`;
        btn.className = `tab-btn ${isFirstTab ? 'active' : ''}`;
        btn.textContent = keyword;
        btn.onclick = (e) => {
            e.preventDefault();
            // Remove active class from all tabs and panes
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            // Add active class to clicked tab and corresponding pane
            btn.classList.add('active');
            document.getElementById(`pane-${tabId}`).classList.add('active');
        };
        tabsHeader.appendChild(btn);

        // Create Tab Pane
        const pane = document.createElement('div');
        pane.id = `pane-${tabId}`;
        pane.className = `tab-pane ${isFirstTab ? 'active' : ''}`;
        pane.innerHTML = `
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Price</th>
                            <th>Link</th>
                        </tr>
                    </thead>
                    <tbody id="body-${tabId}">
                    </tbody>
                </table>
            </div>
        `;
        tabsContent.appendChild(pane);

        return tabId;
    }

    function addItemToTable(item) {
        const keyword = item.keyword || 'Unknown';
        const tabId = createTab(keyword);
        const tbody = document.getElementById(`body-${tabId}`);

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${item.title}</strong></td>
            <td style="color: #28a745; font-weight: bold;">${item.price.toLocaleString('en-US')} ${item.currency || ''}</td>
            <td><a href="${item.link}" target="_blank" rel="noopener noreferrer">Open ↗</a></td>
        `;
        
        // Add smooth fade-in animation
        tr.style.opacity = '0';
        tr.style.transition = 'opacity 0.5s ease-in';
        tbody.appendChild(tr);
        
        // Trigger reflow to ensure transition runs
        void tr.offsetWidth;
        tr.style.opacity = '1';
    }

    function setLoading(isLoading) {
        if (isLoading) {
            startBtn.disabled = true;
            btnText.textContent = 'Running...';
            loader.classList.remove('hidden');
        } else {
            startBtn.disabled = false;
            btnText.textContent = '🚀 Start Scraper';
            loader.classList.add('hidden');
        }
    }
});
