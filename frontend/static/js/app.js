document.addEventListener('DOMContentLoaded', () => {
    // State Management
    const state = {
        categories: {},
        activeTab: 'insights',
        chatHistory: [],
        charts: {}
    };

    // DOM Elements
    // Tab Buttons
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    const currentTabTitle = document.getElementById('current-tab-title');

    // Insights Tab Inputs
    const insightsCategorySelect = document.getElementById('insights-category');
    const insightsRoleSelect = document.getElementById('insights-role');

    // Market Tab Inputs
    const marketRoleInput = document.getElementById('market-role-input');

    // College Tab Inputs
    const collegeRoleInput = document.getElementById('college-role-input');

    // Jobs Tab Inputs
    const jobsCategorySelect = document.getElementById('jobs-category');
    const jobsRoleSelect = document.getElementById('jobs-role');

    // Chat Elements
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    // Initialize App
    const init = async () => {
        try {
            await fetchCategories();
            setupEventListeners();
            // Select first category by default for Insights
            if (Object.keys(state.categories).length > 0) {
                const firstCat = Object.keys(state.categories)[0];
                if (insightsCategorySelect) insightsCategorySelect.value = firstCat;
                updateInsightsRoleOptions(firstCat);
            }
        } catch (error) {
            console.error('Initialization error:', error);
            showNotification('Failed to initialize application', 'error');
        }
    };

    // API Calls
    const fetchCategories = async () => {
        const response = await fetch('/api/careers');
        state.categories = await response.json();

        if (insightsCategorySelect) {
            insightsCategorySelect.innerHTML = Object.keys(state.categories).map(cat =>
                `<option value="${cat}">${cat}</option>`
            ).join('');
        }

        if (jobsCategorySelect) {
            jobsCategorySelect.innerHTML = Object.keys(state.categories).map(cat =>
                `<option value="${cat}">${cat}</option>`
            ).join('');
            // Trigger initial population for Jobs tab too
            if (Object.keys(state.categories).length > 0) {
                updateJobsRoleOptions(Object.keys(state.categories)[0]);
            }
        }
    };

    const generateInsight = async (type) => {
        let payload = {};
        let endpoint = '';
        let btnId = '';

        if (type === 'insights') {
            const category = insightsCategorySelect.value;
            const subcareer = insightsRoleSelect.value;
            if (!subcareer) {
                showNotification('Please select a role', 'warning');
                return;
            }
            payload = { category, subcareer };
            endpoint = '/api/career-insights';
            btnId = 'btn-insights';
        } else if (type === 'market') {
            const subcareer = marketRoleInput.value.trim();
            if (!subcareer) {
                showNotification('Please enter a target role', 'warning');
                return;
            }
            payload = { subcareer };
            endpoint = '/api/market-analysis';
            btnId = 'btn-market';
        } else if (type === 'college') {
            const subcareer = collegeRoleInput.value.trim();
            if (!subcareer) {
                showNotification('Please enter a field of study', 'warning');
                return;
            }
            payload = { subcareer };
            endpoint = '/api/college-recommendations';
            btnId = 'btn-college';
        }

        setLoading(btnId, true);
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            console.log(`Response from ${endpoint}:`, data);

            if (data.error) throw new Error(data.error);
            if (!data.result) throw new Error("No data returned from AI service");

            const outputDiv = document.getElementById(`${type}-output`);
            if (!outputDiv) {
                console.error(`Output div not found: ${type}-output`);
                return;
            }

            // Extract and Render Chart Data
            const chartMatch = data.result.match(/<!-- CHART_DATA\s*([\s\S]*?)\s*-->/);
            if (chartMatch && chartMatch[1]) {
                try {
                    const chartData = JSON.parse(chartMatch[1].trim());
                    renderChart(type, chartData);
                } catch (e) {
                    console.error('Failed to parse chart data:', e);
                }
            }

            // Robust Markdown Parsing
            const content = data.result.replace(/<!-- CHART_DATA[\s\S]*?-->/g, '');
            try {
                if (typeof marked.parse === 'function') {
                    outputDiv.innerHTML = marked.parse(content);
                } else if (typeof marked === 'function') {
                    outputDiv.innerHTML = marked(content);
                } else {
                    console.error("Marked library not found or incomplete");
                    outputDiv.innerText = content;
                }
            } catch (pError) {
                console.error("Markdown parsing error:", pError);
                outputDiv.innerText = content;
            }

            showNotification(`${currentTabTitle.innerText} generated!`, 'success');
        } catch (error) {
            console.error(`Error generating ${type}:`, error);
            showNotification(`Error: ${error.message}`, 'error');
            const outputDiv = document.getElementById(`${type}-output`);
            if (outputDiv) {
                outputDiv.innerHTML = `<div class="p-4 text-red-500 bg-red-50 border border-red-200 rounded-lg">
                    <p class="font-bold">Generation Failed</p>
                    <p class="text-xs mt-1">${error.message}</p>
                </div>`;
            }
        } finally {
            setLoading(btnId, false);
        }
    };

    const analyzeResume = async () => {
        const resumeText = document.getElementById('resume-text-input').value;
        const targetRole = document.getElementById('target-role').value;
        const fileInput = document.getElementById('resume-upload');

        if (!resumeText && (!fileInput.files || fileInput.files.length === 0)) {
            showNotification('Please provide resume text or upload a file', 'warning');
            return;
        }

        setLoading('btn-resume', true);
        const formData = new FormData();
        formData.append('target_role', targetRole || 'General');
        if (resumeText) formData.append('resume_text', resumeText);
        if (fileInput.files.length > 0) formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/api/resume-analysis', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            console.log("Resume analysis response:", data);

            if (data.error) throw new Error(data.error);
            if (!data.result) throw new Error("No feedback received");

            const outputDiv = document.getElementById('resume-output');
            if (outputDiv) {
                const content = data.result;
                try {
                    if (typeof marked.parse === 'function') {
                        outputDiv.innerHTML = marked.parse(content);
                    } else if (typeof marked === 'function') {
                        outputDiv.innerHTML = marked(content);
                    } else {
                        outputDiv.innerText = content;
                    }
                } catch (e) {
                    outputDiv.innerText = content;
                }
            }
            showNotification('Resume analysis complete!', 'success');
        } catch (error) {
            console.error('Error analyzing resume:', error);
            showNotification(`Error: ${error.message}`, 'error');
            const outputDiv = document.getElementById('resume-output');
            if (outputDiv) {
                outputDiv.innerHTML = `<div class="p-4 text-red-500 bg-red-50 border border-red-200 rounded-lg">
                    <p class="font-bold">Analysis Failed</p>
                    <p class="text-xs mt-1">${error.message}</p>
                </div>`;
            }
        } finally {
            setLoading('btn-resume', false);
        }
    };

    const renderChart = (type, chartData) => {
        const canvasId = `${type}Chart`;
        const containerId = `${type}-chart-container`;

        const ctx = document.getElementById(canvasId).getContext('2d');
        const container = document.getElementById(containerId);
        container.classList.remove('hidden');

        if (state.charts[type]) {
            state.charts[type].destroy();
        }

        const chartType = chartData.type || 'bar';
        const isRadar = chartType === 'radar';

        state.charts[type] = new Chart(ctx, {
            type: chartType,
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: chartData.label || 'Data',
                    data: chartData.data,
                    backgroundColor: isRadar ? 'rgba(79, 70, 229, 0.2)' : 'rgba(0, 0, 0, 0.7)',
                    borderColor: isRadar ? '#4f46e5' : '#000000',
                    borderWidth: 1,
                    borderRadius: isRadar ? 0 : 6,
                    barThickness: isRadar ? undefined : 40,
                    pointBackgroundColor: '#fff',
                    pointBorderColor: '#4f46e5',
                    pointHoverBackgroundColor: '#4f46e5',
                    pointHoverBorderColor: '#fff',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: isRadar
                    },
                    tooltip: {
                        backgroundColor: '#ffffff',
                        titleColor: '#000',
                        bodyColor: '#333',
                        borderColor: '#e2e8f0',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                return `${context.dataset.label}: ${context.parsed.r || context.parsed.y} ${chartData.unit || ''}`;
                            }
                        }
                    }
                },
                scales: isRadar ? {
                    r: {
                        angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                        grid: { color: 'rgba(0, 0, 0, 0.1)' },
                        pointLabels: {
                            font: { size: 11, family: 'Inter', weight: '600' },
                            color: '#1e293b'
                        },
                        ticks: { display: false, backdropColor: 'transparent' }
                    }
                } : {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(0, 0, 0, 0.05)', drawBorder: false },
                        ticks: { color: '#64748b', font: { size: 11, family: 'Inter' } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#1e293b', font: { size: 11, weight: 'bold', family: 'Inter' } }
                    }
                }
            }
        });
    };

    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message to UI
        addMessageToChat('user', message);
        chatInput.value = '';

        // Typing indicator
        const typingId = addMessageToChat('ai', '<div class="spinner-small"></div>', true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, history: state.chatHistory })
            });
            const data = await response.json();

            if (data.error) throw new Error(data.error);
            if (!data.answer) throw new Error("No response from advisor");

            // Replace typing indicator with response
            let finalHtml = '';
            try {
                if (typeof marked.parse === 'function') {
                    finalHtml = marked.parse(data.answer);
                } else if (typeof marked === 'function') {
                    finalHtml = marked(data.answer);
                } else {
                    finalHtml = data.answer;
                }
            } catch (e) {
                finalHtml = data.answer;
            }

            updateMessageInChat(typingId, finalHtml);
            state.chatHistory.push({ role: 'user', content: message });
            state.chatHistory.push({ role: 'ai', content: data.answer });
        } catch (error) {
            console.error('Chat error:', error);
            updateMessageInChat(typingId, `<span class="text-red-500">Error: ${error.message}</span>`);
        }
    };

    const findJobs = async () => {
        const role = jobsRoleSelect.value;
        const btnId = 'btn-jobs';

        if (!role) {
            showNotification('Please select a role first', 'warning');
            return;
        }

        setLoading(btnId, true);
        const outputDiv = document.getElementById('jobs-output');
        outputDiv.innerHTML = '<div class="col-span-1 md:col-span-2 flex justify-center p-10"><div class="spinner-small"></div></div>';

        try {
            const response = await fetch('/api/jobs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ role: role })
            });
            const jobs = await response.json();

            if (jobs.error) throw new Error(jobs.error);

            if (jobs.length === 0) {
                outputDiv.innerHTML = `
                    <div class="col-span-1 md:col-span-2 flex flex-col items-center justify-center h-40 text-slate-400 italic">
                        <i class="fas fa-search-minus text-4xl mb-3 opacity-50"></i>
                        <p>No jobs found for this role at the moment.</p>
                    </div>`;
            } else {
                outputDiv.innerHTML = jobs.map(job => `
                    <div class="glass-card p-5 rounded-xl border border-slate-200 hover:shadow-md transition-all bg-white relative group">
                        <div class="flex justify-between items-start mb-2">
                             <h4 class="font-bold text-lg text-black pr-8 leading-tight line-clamp-2">${job.title}</h4>
                             ${job.thumbnail ? `<img src="${job.thumbnail}" class="w-10 h-10 object-contain rounded-md" alt="logo">` : '<i class="fas fa-building text-slate-300 text-xl"></i>'}
                        </div>
                        <p class="text-sm text-slate-600 font-medium mb-2"><i class="fas fa-building mr-1 text-slate-400"></i> ${job.company}</p>
                        <p class="text-xs text-slate-500 mb-4"><i class="fas fa-map-marker-alt mr-1 text-slate-400"></i> ${job.location}</p>
                        
                        <div class="text-xs text-slate-600 mb-4 line-clamp-3 leading-relaxed">
                            ${job.description}
                        </div>
                        
                        <a href="${job.link}" target="_blank" class="block w-full text-center py-2 bg-slate-100 hover:bg-black hover:text-white text-slate-700 font-bold rounded-lg transition-colors text-xs uppercase tracking-wider">
                            Apply Now <i class="fas fa-external-link-alt ml-1"></i>
                        </a>
                    </div>
                `).join('');
                showNotification(`Found ${jobs.length} jobs!`, 'success');
            }

        } catch (error) {
            console.error('Error fetching jobs:', error);
            outputDiv.innerHTML = `
                <div class="col-span-1 md:col-span-2 text-center text-red-500 p-4">
                    <i class="fas fa-exclamation-circle text-2xl mb-2"></i>
                    <p>Failed to fetch jobs: ${error.message}</p>
                    <p class="text-xs mt-2 text-slate-500">Check your SerpAPI key and network connection.</p>
                </div>
            `;
            showNotification(`Error: ${error.message}`, 'error');
        } finally {
            setLoading(btnId, false);
        }
    };

    // UI Helpers
    const updateInsightsRoleOptions = (category) => {
        const careers = state.categories[category] || [];
        if (insightsRoleSelect) {
            insightsRoleSelect.innerHTML = careers.map(career =>
                `<option value="${career}">${career}</option>`
            ).join('');
            // Trigger sync on initial load/change
            syncRoleState(insightsRoleSelect.value);
        }
    };

    const updateJobsRoleOptions = (category) => {
        const careers = state.categories[category] || [];
        if (jobsRoleSelect) {
            jobsRoleSelect.innerHTML = careers.map(career =>
                `<option value="${career}">${career}</option>`
            ).join('');
        }
    };

    const syncRoleState = (role) => {
        if (!role) return;
        if (marketRoleInput) marketRoleInput.value = role;
        if (collegeRoleInput) collegeRoleInput.value = role;
    };

    const setLoading = (btnId, isLoading) => {
        const btn = document.getElementById(btnId);
        if (btn) {
            if (isLoading) {
                btn.classList.add('btn-loading');
                btn.disabled = true;
            } else {
                btn.classList.remove('btn-loading');
                btn.disabled = false;
            }
        }
    };

    const addMessageToChat = (role, content, isHtml = false) => {
        const id = Date.now();
        const div = document.createElement('div');
        div.className = `flex items-start gap-4 chat-bubble ${role === 'user' ? 'flex-row-reverse' : ''}`;
        div.id = `msg-${id}`;

        div.innerHTML = `
            <div class="w-10 h-10 rounded-full ${role === 'user' ? 'bg-black text-white' : 'bg-white border border-slate-200 text-black'} flex-shrink-0 flex items-center justify-center text-[10px] font-bold shadow-sm">
                ${role === 'user' ? 'ME' : 'AI'}
            </div>
            <div class="${role === 'user' ? 'bg-slate-100 text-slate-800' : 'bg-white border border-slate-200 text-slate-700'} p-5 rounded-2xl ${role === 'user' ? 'rounded-tr-none' : 'rounded-tl-none'} text-sm max-w-[75%] shadow-sm leading-relaxed">
                ${content}
            </div>
        `;
        if (chatMessages) {
            chatMessages.appendChild(div);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        return id;
    };

    const updateMessageInChat = (id, content) => {
        const msgDiv = document.getElementById(`msg-${id}`);
        if (msgDiv) {
            const contentContainer = msgDiv.querySelector('div:last-child');
            contentContainer.innerHTML = content;
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
    };

    const showNotification = (message, type = 'info') => {
        console.log(`[${type.toUpperCase()}] ${message}`);
        const badge = document.getElementById('status-badge');
        if (badge) {
            const badgeText = badge.querySelector('span:last-child');
            if (badgeText) {
                badgeText.innerText = message;
                setTimeout(() => {
                    badgeText.innerText = 'System Ready';
                }, 3000);
            }
        }
    };

    const setupEventListeners = () => {
        // Insights Tab: Category change
        if (insightsCategorySelect) {
            insightsCategorySelect.addEventListener('change', (e) => {
                updateInsightsRoleOptions(e.target.value);
            });
        }

        // Insights Tab: Role change (Sync)
        if (insightsRoleSelect) {
            insightsRoleSelect.addEventListener('change', (e) => {
                syncRoleState(e.target.value);
            });
        }

        // Jobs Tab: Category change
        if (jobsCategorySelect) {
            jobsCategorySelect.addEventListener('change', (e) => {
                updateJobsRoleOptions(e.target.value);
            });
        }

        // Tab Switching
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const tab = btn.dataset.tab;

                // Update buttons
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Update panels
                tabPanels.forEach(p => {
                    p.classList.add('hidden');
                    p.classList.remove('active');
                });
                const targetPanel = document.getElementById(`tab-${tab}`);
                if (targetPanel) {
                    targetPanel.classList.remove('hidden');
                    // Force reflow
                    void targetPanel.offsetWidth;
                    targetPanel.classList.add('active');
                }

                // Update title
                if (currentTabTitle) {
                    currentTabTitle.innerText = btn.innerText;
                }
                state.activeTab = tab;

                // Close sidebar on mobile (if applicable)
                if (window.innerWidth < 768) {
                    const sidebar = document.getElementById('sidebar');
                    if (sidebar) sidebar.classList.add('-translate-x-full');
                }
            });
        });

        // Chat
        if (sendBtn) {
            sendBtn.addEventListener('click', sendMessage);
        }
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });
        }

        // Drag & Drop
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('resume-upload');
        const filePreview = document.getElementById('resume-preview');
        const filenameSpan = document.getElementById('resume-filename');

        const handleFileSelect = (files) => {
            if (files.length > 0) {
                fileInput.files = files;
                if (filePreview && filenameSpan) {
                    filenameSpan.innerText = files[0].name;
                    filePreview.classList.remove('hidden');
                }
                showNotification(`File added: ${files[0].name}`, 'success');
            }
        };

        if (dropZone && fileInput) {
            dropZone.addEventListener('click', () => fileInput.click());
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('border-black', 'bg-slate-100');
            });
            dropZone.addEventListener('dragleave', () => {
                dropZone.classList.remove('border-black', 'bg-slate-100');
            });
            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('border-black', 'bg-slate-100');
                handleFileSelect(e.dataTransfer.files);
            });
            fileInput.addEventListener('change', () => {
                handleFileSelect(fileInput.files);
            });
        }
    };

    // Global actions for onclick
    window.generateInsight = generateInsight;
    window.analyzeResume = analyzeResume;
    window.findJobs = findJobs;

    init();
});
