/**
 * Illustrator Interface for Typography Agent CEP Extension
 * Handles communication with Adobe Illustrator via ExtendScript
 */

class IllustratorInterface {
    constructor() {
        this.csInterface = new CSInterface();
    }
    
    async getCurrentContext() {
        try {
            const result = await this.evalScript('TypographyAgent.getCurrentContext()');
            const parsed = JSON.parse(result);
            
            if (parsed.success) {
                return parsed.context;
            } else {
                throw new Error(parsed.error || 'Failed to get context');
            }
        } catch (error) {
            console.error('Error getting current context:', error);
            return {
                document: { name: 'Unknown', width: 0, height: 0 },
                selection: { count: 0, types: [] },
                fonts: [],
                colors: []
            };
        }
    }
    
    async getSelectedElements() {
        try {
            const result = await this.evalScript('TypographyAgent.getSelectedElements()');
            const parsed = JSON.parse(result);
            
            if (parsed.success) {
                return parsed.elements;
            } else {
                throw new Error(parsed.error || 'Failed to get selected elements');
            }
        } catch (error) {
            console.error('Error getting selected elements:', error);
            return [];
        }
    }
    
    async applyTypographyFix(fixType, parameters = {}) {
        try {
            const paramString = JSON.stringify(parameters);
            const script = `TypographyAgent.applyTypographyFix("${fixType}", '${paramString}')`;
            
            const result = await this.evalScript(script);
            const parsed = JSON.parse(result);
            
            return parsed;
        } catch (error) {
            console.error('Error applying typography fix:', error);
            return { success: false, error: error.message };
        }
    }
    
    async batchFormatText(formatRules) {
        try {
            const rulesString = JSON.stringify(formatRules);
            const script = `TypographyAgent.batchFormatText('${rulesString}')`;
            
            const result = await this.evalScript(script);
            const parsed = JSON.parse(result);
            
            return parsed;
        } catch (error) {
            console.error('Error in batch format:', error);
            return { success: false, error: error.message };
        }
    }
    
    async autoAdjustTextBoxes(adjustmentParams = {}) {
        try {
            const paramsString = JSON.stringify(adjustmentParams);
            const script = `TypographyAgent.autoAdjustTextBoxes('${paramsString}')`;
            
            const result = await this.evalScript(script);
            const parsed = JSON.parse(result);
            
            return parsed;
        } catch (error) {
            console.error('Error adjusting text boxes:', error);
            return { success: false, error: error.message };
        }
    }
    
    async createTextStyle(styleName, styleProperties) {
        try {
            const styles = [{
                name: styleName,
                ...styleProperties
            }];
            
            const stylesString = JSON.stringify({ styles });
            const script = `TypographyAgent.createAndApplyTextStyles('${stylesString}')`;
            
            const result = await this.evalScript(script);
            const parsed = JSON.parse(result);
            
            return parsed;
        } catch (error) {
            console.error('Error creating text style:', error);
            return { success: false, error: error.message };
        }
    }
    
    async getDocumentInfo() {
        try {
            const script = `
                if (app.documents.length > 0) {
                    var doc = app.activeDocument;
                    JSON.stringify({
                        success: true,
                        name: doc.name,
                        width: doc.width,
                        height: doc.height,
                        artboards: doc.artboards.length,
                        textFrames: doc.textFrames.length,
                        colorSpace: doc.documentColorSpace.toString()
                    });
                } else {
                    JSON.stringify({
                        success: false,
                        error: "No document is open"
                    });
                }
            `;
            
            const result = await this.evalScript(script);
            return JSON.parse(result);
        } catch (error) {
            console.error('Error getting document info:', error);
            return { success: false, error: error.message };
        }
    }
    
    async selectTextFrames(criteria = {}) {
        try {
            const criteriaString = JSON.stringify(criteria);
            const script = `
                if (app.documents.length === 0) {
                    JSON.stringify({ success: false, error: "No document is open" });
                } else {
                    var doc = app.activeDocument;
                    var criteria = ${criteriaString};
                    var selectedFrames = [];
                    
                    try {
                        doc.selection = null;
                        var selection = [];
                        
                        for (var i = 0; i < doc.textFrames.length; i++) {
                            var frame = doc.textFrames[i];
                            var shouldSelect = true;
                            
                            if (criteria.minFontSize && frame.textRange.characterAttributes.size < criteria.minFontSize) {
                                shouldSelect = false;
                            }
                            if (criteria.maxFontSize && frame.textRange.characterAttributes.size > criteria.maxFontSize) {
                                shouldSelect = false;
                            }
                            if (criteria.fontFamily && frame.textRange.characterAttributes.textFont.name.indexOf(criteria.fontFamily) === -1) {
                                shouldSelect = false;
                            }
                            
                            if (shouldSelect) {
                                selection.push(frame);
                                selectedFrames.push({
                                    index: i,
                                    fontSize: frame.textRange.characterAttributes.size,
                                    fontFamily: frame.textRange.characterAttributes.textFont.name
                                });
                            }
                        }
                        
                        doc.selection = selection;
                        
                        JSON.stringify({
                            success: true,
                            selected: selectedFrames.length,
                            frames: selectedFrames
                        });
                    } catch (error) {
                        JSON.stringify({
                            success: false,
                            error: error.toString()
                        });
                    }
                }
            `;
            
            const result = await this.evalScript(script);
            return JSON.parse(result);
        } catch (error) {
            console.error('Error selecting text frames:', error);
            return { success: false, error: error.message };
        }
    }
    
    async exportDocument(format = 'pdf', options = {}) {
        try {
            const optionsString = JSON.stringify(options);
            const script = `
                if (app.documents.length === 0) {
                    JSON.stringify({ success: false, error: "No document is open" });
                } else {
                    try {
                        var doc = app.activeDocument;
                        var options = ${optionsString};
                        var format = "${format}";
                        
                        // This is a simplified export - in practice, you'd implement
                        // specific export options for different formats
                        
                        JSON.stringify({
                            success: true,
                            message: "Export functionality ready (implementation depends on specific format requirements)",
                            format: format,
                            document: doc.name
                        });
                    } catch (error) {
                        JSON.stringify({
                            success: false,
                            error: error.toString()
                        });
                    }
                }
            `;
            
            const result = await this.evalScript(script);
            return JSON.parse(result);
        } catch (error) {
            console.error('Error exporting document:', error);
            return { success: false, error: error.message };
        }
    }
    
    // Helper method to execute ExtendScript
    evalScript(script) {
        return new Promise((resolve, reject) => {
            this.csInterface.evalScript(script, (result) => {
                if (result === 'EvalScript error.') {
                    reject(new Error('ExtendScript execution failed'));
                } else {
                    resolve(result);
                }
            });
        });
    }
    
    // Utility methods for common operations
    async isDocumentOpen() {
        try {
            const result = await this.evalScript('app.documents.length > 0');
            return result === 'true';
        } catch (error) {
            return false;
        }
    }
    
    async getSelectionCount() {
        try {
            const result = await this.evalScript('app.activeDocument ? app.activeDocument.selection.length : 0');
            return parseInt(result) || 0;
        } catch (error) {
            return 0;
        }
    }
    
    async showAlert(message) {
        try {
            await this.evalScript(`alert("${message.replace(/"/g, '\\"')}")`);
            return true;
        } catch (error) {
            console.error('Error showing alert:', error);
            return false;
        }
    }
}
