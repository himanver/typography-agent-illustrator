/**
 * Typography Agent - Main CEP Extension Script
 * Integrates with MCP servers and Illustrator for typography assistance
 */

class TypographyAgentCEP {
    constructor() {
        this.csInterface = new CSInterface();
        this.mcpClient = new MCPClient();
        this.typographyAnalyzer = new TypographyAnalyzer();
        this.illustratorInterface = new IllustratorInterface();
        this.themeManager = new ThemeManager();
        
        this.currentMode = 'guide';
        this.isConnected = false;
        this.autoAnalysis = true;
        
        this.init();
    }
    
    async init() {
        console.log('Initializing Typography Agent CEP Extension...');
        
        // Initialize theme management
        this.themeManager.init();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Initialize MCP connection
        await this.initializeMCPConnection();
        
        // Set up Illustrator event listeners
        this.setupIllustratorEvents();
        
        console.log('Typography Agent initialized successfully');
    }
    
    setupEventListeners() {
        // Mode selection buttons
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setMode(e.target.dataset.mode);
            });
        });
        
        // Chat functionality
        const chatInput = document.getElementById('chat-input');
        const sendButton = document.getElementById('send-message');
        
        sendButton.addEventListener('click', () => this.sendChatMessage());
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendChatMessage();
            }
        });
        
        // Quick actions
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.dataset.action;
                this.executeQuickAction(action);
            });
        });
        
        // Footer buttons
        document.getElementById('settings-btn').addEventListener('click', () => {
            this.toggleSettings();
        });
        
        document.getElementById('help-btn').addEventListener('click', () => {
            this.showHelp();
        });
        
        // Settings
        document.getElementById('auto-analysis').addEventListener('change', (e) => {
            this.autoAnalysis = e.target.checked;
        });
    }
    
    async initializeMCPConnection() {
        try {
            this.updateConnectionStatus('connecting', 'Connecting to MCP servers...');
            
            const serverUrl = document.getElementById('mcp-server-url').value || 'http://localhost:3000';
            await this.mcpClient.connect(serverUrl);
            
            this.isConnected = true;
            this.updateConnectionStatus('connected', 'Connected to MCP servers');
            
            // Initialize MCP servers
            await this.mcpClient.initializeServers([
                'typography-analysis',
                'illustrator-integration',
                'typesetting-engine',
                'workflow-automation'
            ]);
            
        } catch (error) {
            console.error('Failed to connect to MCP servers:', error);
            this.updateConnectionStatus('error', 'Connection failed');
            this.addChatMessage('system', 'Unable to connect to MCP servers. Some features may be limited.', 'error');
        }
    }
    
    setupIllustratorEvents() {
        // Listen for selection changes
        this.csInterface.addEventListener('com.adobe.csxs.events.SelectionChanged', (event) => {
            if (this.autoAnalysis) {
                this.analyzeCurrentSelection();
            }
        });
        
        // Listen for document changes
        this.csInterface.addEventListener('com.adobe.csxs.events.DocumentChanged', (event) => {
            this.onDocumentChanged(event);
        });
    }
    
    setMode(mode) {
        this.currentMode = mode;
        
        // Update UI
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-mode="${mode}"]`).classList.add('active');
        
        // Update chat context
        const modeMessages = {
            'critic': 'Switched to Critic mode. I\'ll provide professional, constructive feedback on your typography choices.',
            'guide': 'Switched to Guide mode. I\'ll help you learn typography principles and best practices.',
            'helper': 'Switched to Helper mode. I\'ll focus on automating tasks and providing practical solutions.'
        };
        
        this.addChatMessage('system', modeMessages[mode], 'info');
    }
    
    async sendChatMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addChatMessage('user', message);
        input.value = '';
        
        // Show loading
        this.showLoading('Processing your request...');
        
        try {
            // Get current context from Illustrator
            const context = await this.illustratorInterface.getCurrentContext();
            
            // Send to MCP for processing
            const response = await this.mcpClient.processQuery({
                message: message,
                mode: this.currentMode,
                context: context
            });
            
            // Add agent response
            this.addChatMessage('agent', response.message, response.type || 'info');
            
            // Execute any suggested actions
            if (response.actions && response.actions.length > 0) {
                await this.executeSuggestedActions(response.actions);
            }
            
        } catch (error) {
            console.error('Error processing chat message:', error);
            this.addChatMessage('system', 'Sorry, I encountered an error processing your request. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async executeQuickAction(action) {
        this.showLoading(`Executing ${action}...`);
        
        try {
            switch (action) {
                case 'analyze-selection':
                    await this.analyzeCurrentSelection();
                    break;
                    
                case 'fix-kerning':
                    await this.fixKerning();
                    break;
                    
                case 'adjust-hierarchy':
                    await this.adjustHierarchy();
                    break;
                    
                case 'batch-format':
                    await this.batchFormat();
                    break;
                    
                case 'readability-check':
                    await this.checkReadability();
                    break;
                    
                case 'optical-margins':
                    await this.applyOpticalMargins();
                    break;
                    
                default:
                    console.warn('Unknown action:', action);
            }
        } catch (error) {
            console.error('Error executing action:', error);
            this.addChatMessage('system', `Error executing ${action}: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async analyzeCurrentSelection() {
        try {
            // Get selected elements from Illustrator
            const selection = await this.illustratorInterface.getSelectedElements();
            
            if (!selection || selection.length === 0) {
                this.addChatMessage('system', 'Please select some text elements to analyze.', 'warning');
                return;
            }
            
            // Analyze with MCP server
            const analysis = await this.mcpClient.callTool('typography-analysis', 'analyze_elements', {
                elements: selection,
                context: await this.illustratorInterface.getCurrentContext(),
                mode: this.currentMode
            });
            
            // Display results
            this.displayAnalysisResults(analysis);
            
        } catch (error) {
            console.error('Analysis error:', error);
            this.addChatMessage('system', 'Analysis failed. Please ensure text is selected and try again.', 'error');
        }
    }
    
    async fixKerning() {
        const selection = await this.illustratorInterface.getSelectedElements();
        
        if (!selection || selection.length === 0) {
            this.addChatMessage('system', 'Please select text elements to apply kerning fixes.', 'warning');
            return;
        }
        
        const result = await this.mcpClient.callTool('illustrator-integration', 'apply_advanced_kerning', {
            kerning_pairs: [
                {"characters": "AV", "adjustment": -50},
                {"characters": "To", "adjustment": -30},
                {"characters": "We", "adjustment": -20}
            ],
            optical_kerning: true
        });
        
        if (result.success) {
            this.addChatMessage('system', 'Kerning improvements applied successfully!', 'success');
        } else {
            this.addChatMessage('system', `Kerning failed: ${result.error}`, 'error');
        }
    }
    
    async adjustHierarchy() {
        const selection = await this.illustratorInterface.getSelectedElements();
        
        if (!selection || selection.length < 2) {
            this.addChatMessage('system', 'Please select multiple text elements to adjust hierarchy.', 'warning');
            return;
        }
        
        // Apply hierarchical formatting
        const formatRules = [
            {
                "selector": "heading",
                "fontSize": 24,
                "fontWeight": "bold",
                "lineHeight": 1.2
            },
            {
                "selector": "subheading", 
                "fontSize": 18,
                "fontWeight": "medium",
                "lineHeight": 1.3
            },
            {
                "selector": "body",
                "fontSize": 12,
                "fontWeight": "regular",
                "lineHeight": 1.4
            }
        ];
        
        const result = await this.mcpClient.callTool('illustrator-integration', 'batch_format_text', {
            format_rules: formatRules
        });
        
        if (result.success) {
            this.addChatMessage('system', 'Hierarchy adjustments applied successfully!', 'success');
        }
    }
    
    async batchFormat() {
        // Show format options dialog
        const formatOptions = await this.showFormatDialog();
        
        if (formatOptions) {
            const result = await this.mcpClient.callTool('illustrator-integration', 'batch_format_text', {
                format_rules: formatOptions
            });
            
            if (result.success) {
                this.addChatMessage('system', `Batch formatting applied to ${result.processed} elements.`, 'success');
            }
        }
    }
    
    async checkReadability() {
        const selection = await this.illustratorInterface.getSelectedElements();
        
        const readabilityResult = await this.mcpClient.callTool('typography-analysis', 'readability_assessment', {
            text_elements: selection
        });
        
        this.displayReadabilityResults(readabilityResult);
    }
    
    async applyOpticalMargins() {
        const result = await this.mcpClient.callTool('illustrator-integration', 'optical_margin_alignment', {
            margin_adjustment: 0.05
        });
        
        if (result.success) {
            this.addChatMessage('system', 'Optical margin alignment applied!', 'success');
        }
    }
    
    displayAnalysisResults(analysis) {
        const resultsPanel = document.getElementById('analysis-results');
        const resultsContent = document.getElementById('results-content');
        
        resultsContent.innerHTML = '';
        
        if (analysis && analysis.length > 0) {
            analysis.forEach(result => {
                const resultElement = document.createElement('div');
                resultElement.className = `result-item ${result.severity}`;
                resultElement.innerHTML = `
                    <div class="result-header">
                        <span class="result-type">${result.task_type}</span>
                        <span class="result-severity ${result.severity}">${result.severity}</span>
                    </div>
                    <div class="result-message">${result.message}</div>
                    ${result.suggestions && result.suggestions.length > 0 ? `
                        <div class="result-suggestions">
                            <strong>Suggestions:</strong>
                            <ul>
                                ${result.suggestions.map(s => `<li>${s}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    ${result.auto_fix_available ? `
                        <button class="auto-fix-btn" data-task="${result.task_type}">
                            Apply Auto-fix
                        </button>
                    ` : ''}
                `;
                
                resultsContent.appendChild(resultElement);
            });
            
            // Add event listeners for auto-fix buttons
            resultsContent.querySelectorAll('.auto-fix-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    this.applyAutoFix(e.target.dataset.task);
                });
            });
            
            resultsPanel.style.display = 'block';
            
            // Add to chat
            const summary = `Analysis complete: Found ${analysis.length} items to review.`;
            this.addChatMessage('system', summary, 'info');
        } else {
            this.addChatMessage('system', 'Analysis complete: No issues found!', 'success');
        }
    }
    
    addChatMessage(sender, message, type = 'info') {
        const chatMessages = document.getElementById('chat-messages');
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message ${type}`;
        
        const timestamp = new Date().toLocaleTimeString();
        const senderLabel = sender === 'user' ? 'You' : 
                           sender === 'agent' ? 'Typography Agent' : 'System';
        
        messageElement.innerHTML = `
            <div class="message-content">
                <strong>${senderLabel}:</strong> ${message}
            </div>
            <div class="message-timestamp">${timestamp}</div>
        `;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    updateConnectionStatus(status, message) {
        const indicator = document.getElementById('status-indicator');
        const text = document.getElementById('status-text');
        
        indicator.className = `status-indicator ${status}`;
        text.textContent = message;
    }
    
    showLoading(message = 'Processing...') {
        const overlay = document.getElementById('loading-overlay');
        const text = overlay.querySelector('.loading-text');
        text.textContent = message;
        overlay.style.display = 'flex';
    }
    
    hideLoading() {
        document.getElementById('loading-overlay').style.display = 'none';
    }
    
    toggleSettings() {
        const panel = document.getElementById('settings-panel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    }
    
    showHelp() {
        const helpMessage = `
            <strong>Typography Agent Help</strong><br><br>
            <strong>Modes:</strong><br>
            • <strong>Critic:</strong> Provides professional feedback and identifies issues<br>
            • <strong>Guide:</strong> Teaches typography principles and best practices<br>
            • <strong>Helper:</strong> Focuses on automation and quick fixes<br><br>
            <strong>Quick Actions:</strong><br>
            • <strong>Analyze Selection:</strong> Analyze selected text for typography issues<br>
            • <strong>Fix Kerning:</strong> Apply professional kerning adjustments<br>
            • <strong>Adjust Hierarchy:</strong> Improve visual hierarchy<br>
            • <strong>Batch Format:</strong> Apply consistent formatting to multiple elements<br>
            • <strong>Check Readability:</strong> Assess text readability<br>
            • <strong>Optical Margins:</strong> Apply optical margin alignment<br><br>
            <strong>Chat:</strong> Ask questions, request analysis, or describe what you need help with.
        `;
        
        this.addChatMessage('system', helpMessage, 'info');
    }
}

// Initialize the extension when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.typographyAgent = new TypographyAgentCEP();
});

// Handle extension lifecycle
window.addEventListener('beforeunload', () => {
    if (window.typographyAgent && window.typographyAgent.mcpClient) {
        window.typographyAgent.mcpClient.disconnect();
    }
});
