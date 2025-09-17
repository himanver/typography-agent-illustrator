/**
 * MCP Client for Typography Agent CEP Extension
 * Handles communication with MCP servers for typography analysis and automation
 */

class MCPClient {
    constructor() {
        this.serverUrl = null;
        this.isConnected = false;
        this.servers = new Map();
        this.websocket = null;
    }
    
    async connect(serverUrl) {
        this.serverUrl = serverUrl;
        
        try {
            // For CEP extension, we'll use HTTP requests instead of direct MCP protocol
            // This acts as a bridge to the actual MCP servers
            const response = await fetch(`${serverUrl}/health`);
            if (response.ok) {
                this.isConnected = true;
                console.log('Connected to MCP bridge server');
            } else {
                throw new Error('Server health check failed');
            }
        } catch (error) {
            console.error('Failed to connect to MCP bridge:', error);
            throw error;
        }
    }
    
    async initializeServers(serverNames) {
        for (const serverName of serverNames) {
            try {
                const response = await fetch(`${this.serverUrl}/servers/${serverName}/initialize`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.ok) {
                    const serverInfo = await response.json();
                    this.servers.set(serverName, serverInfo);
                    console.log(`Initialized MCP server: ${serverName}`);
                } else {
                    console.warn(`Failed to initialize server: ${serverName}`);
                }
            } catch (error) {
                console.error(`Error initializing ${serverName}:`, error);
            }
        }
    }
    
    async callTool(serverName, toolName, arguments) {
        if (!this.isConnected) {
            throw new Error('Not connected to MCP servers');
        }
        
        try {
            const response = await fetch(`${this.serverUrl}/servers/${serverName}/tools/${toolName}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    arguments: arguments,
                    timestamp: Date.now()
                })
            });
            
            if (!response.ok) {
                throw new Error(`Tool call failed: ${response.statusText}`);
            }
            
            const result = await response.json();
            return result;
            
        } catch (error) {
            console.error(`Error calling tool ${toolName} on ${serverName}:`, error);
            throw error;
        }
    }
    
    async processQuery(query) {
        try {
            const response = await fetch(`${this.serverUrl}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(query)
            });
            
            if (!response.ok) {
                throw new Error(`Query processing failed: ${response.statusText}`);
            }
            
            const result = await response.json();
            return result;
            
        } catch (error) {
            console.error('Error processing query:', error);
            throw error;
        }
    }
    
    async getServerCapabilities(serverName) {
        try {
            const response = await fetch(`${this.serverUrl}/servers/${serverName}/capabilities`);
            if (response.ok) {
                return await response.json();
            }
            return null;
        } catch (error) {
            console.error(`Error getting capabilities for ${serverName}:`, error);
            return null;
        }
    }
    
    async listAvailableTools(serverName) {
        try {
            const response = await fetch(`${this.serverUrl}/servers/${serverName}/tools`);
            if (response.ok) {
                return await response.json();
            }
            return [];
        } catch (error) {
            console.error(`Error listing tools for ${serverName}:`, error);
            return [];
        }
    }
    
    disconnect() {
        if (this.websocket) {
            this.websocket.close();
        }
        this.isConnected = false;
        this.servers.clear();
        console.log('Disconnected from MCP servers');
    }
    
    // Utility method for batch operations
    async batchCall(calls) {
        const promises = calls.map(call => 
            this.callTool(call.server, call.tool, call.arguments)
                .catch(error => ({ error: error.message, call }))
        );
        
        return await Promise.all(promises);
    }
    
    // Method to check server health
    async checkServerHealth() {
        try {
            const response = await fetch(`${this.serverUrl}/health`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}
