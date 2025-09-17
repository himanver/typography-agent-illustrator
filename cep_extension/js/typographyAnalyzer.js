/**
 * Typography Analyzer for CEP Extension
 * Client-side typography analysis and validation
 */

class TypographyAnalyzer {
    constructor() {
        this.readabilityRules = {
            minFontSize: 9,
            maxFontSize: 72,
            optimalLineHeight: 1.4,
            minLineHeight: 1.2,
            maxLineHeight: 1.8,
            optimalLineLength: 60,
            minLineLength: 45,
            maxLineLength: 75
        };
        
        this.fontCategories = {
            serif: ['Times', 'Georgia', 'Minion', 'Garamond', 'Baskerville'],
            sansSerif: ['Helvetica', 'Arial', 'Futura', 'Avenir', 'Proxima'],
            script: ['Script', 'Brush', 'Handwriting', 'Calligraphy'],
            monospace: ['Courier', 'Monaco', 'Consolas', 'Menlo']
        };
    }
    
    analyzeElements(elements) {
        const results = [];
        
        if (!elements || elements.length === 0) {
            return [{
                type: 'warning',
                message: 'No text elements found to analyze',
                suggestions: ['Select some text elements in Illustrator and try again']
            }];
        }
        
        // Font pairing analysis
        const fontPairingResult = this.analyzeFontPairing(elements);
        if (fontPairingResult) {
            results.push(fontPairingResult);
        }
        
        // Readability analysis
        const readabilityResults = this.analyzeReadability(elements);
        results.push(...readabilityResults);
        
        // Hierarchy analysis
        const hierarchyResult = this.analyzeHierarchy(elements);
        if (hierarchyResult) {
            results.push(hierarchyResult);
        }
        
        return results;
    }
    
    analyzeFontPairing(elements) {
        const fonts = [...new Set(elements.map(el => el.family))];
        
        if (fonts.length < 2) {
            return null; // Single font, no pairing to analyze
        }
        
        const categories = fonts.map(font => this.categorizeFontFamily(font));
        const uniqueCategories = [...new Set(categories)];
        
        if (uniqueCategories.length === 1) {
            return {
                type: 'warning',
                category: 'font-pairing',
                message: `All fonts are from the same category (${uniqueCategories[0]}). Consider adding contrast with a different font category.`,
                suggestions: [
                    'Try pairing serif with sans-serif fonts',
                    'Use different weights within the same font family',
                    'Consider a script or display font for headings'
                ]
            };
        }
        
        // Check for problematic combinations
        if (categories.includes('script') && categories.filter(c => c === 'script').length > 1) {
            return {
                type: 'error',
                category: 'font-pairing',
                message: 'Multiple script fonts detected. This can create visual chaos and poor readability.',
                suggestions: [
                    'Use only one script font per design',
                    'Pair script fonts with simple sans-serif or serif fonts',
                    'Reserve script fonts for headings or accents only'
                ]
            };
        }
        
        return {
            type: 'success',
            category: 'font-pairing',
            message: `Good font variety detected: ${uniqueCategories.join(', ')}. This creates nice typographic contrast.`,
            suggestions: [
                'Ensure sufficient size difference between font pairs',
                'Test readability at final output size'
            ]
        };
    }
    
    analyzeReadability(elements) {
        const results = [];
        
        elements.forEach((element, index) => {
            const issues = [];
            const suggestions = [];
            
            // Font size check
            if (element.fontSize < this.readabilityRules.minFontSize) {
                issues.push(`Font size ${element.fontSize}pt is too small`);
                suggestions.push(`Increase font size to at least ${this.readabilityRules.minFontSize}pt`);
            } else if (element.fontSize > this.readabilityRules.maxFontSize) {
                issues.push(`Font size ${element.fontSize}pt may be too large for body text`);
                suggestions.push('Consider reducing font size for better readability');
            }
            
            // Line height check
            if (element.lineHeight < this.readabilityRules.minLineHeight) {
                issues.push(`Line height ${element.lineHeight} is too tight`);
                suggestions.push(`Increase line height to at least ${this.readabilityRules.minLineHeight}`);
            } else if (element.lineHeight > this.readabilityRules.maxLineHeight) {
                issues.push(`Line height ${element.lineHeight} is too loose`);
                suggestions.push(`Reduce line height to around ${this.readabilityRules.optimalLineHeight}`);
            }
            
            // Line length check (if available)
            if (element.lineLength) {
                if (element.lineLength < this.readabilityRules.minLineLength) {
                    issues.push(`Line length ${element.lineLength} characters is too short`);
                    suggestions.push('Increase column width or font size');
                } else if (element.lineLength > this.readabilityRules.maxLineLength) {
                    issues.push(`Line length ${element.lineLength} characters is too long`);
                    suggestions.push('Reduce column width or use multi-column layout');
                }
            }
            
            // Character spacing check
            if (element.characterSpacing && Math.abs(element.characterSpacing) > 0.1) {
                issues.push('Extreme character spacing detected');
                suggestions.push('Reduce character spacing for better readability');
            }
            
            if (issues.length > 0) {
                results.push({
                    type: 'warning',
                    category: 'readability',
                    message: `Element ${index + 1}: ${issues.join(', ')}`,
                    suggestions: suggestions
                });
            }
        });
        
        return results;
    }
    
    analyzeHierarchy(elements) {
        if (elements.length < 2) {
            return null; // Need at least 2 elements for hierarchy
        }
        
        const fontSizes = elements.map(el => el.fontSize).sort((a, b) => b - a);
        const ratios = [];
        
        for (let i = 0; i < fontSizes.length - 1; i++) {
            ratios.push(fontSizes[i] / fontSizes[i + 1]);
        }
        
        const poorRatios = ratios.filter(ratio => ratio < 1.15 || ratio > 3.0);
        
        if (poorRatios.length > 0) {
            return {
                type: 'info',
                category: 'hierarchy',
                message: 'Typography hierarchy could be improved with better size relationships.',
                suggestions: [
                    'Use consistent scale ratios (1.25x, 1.5x, 2x)',
                    'Ensure minimum 1.2x difference between hierarchy levels',
                    'Consider using weight and color for additional hierarchy'
                ]
            };
        }
        
        return {
            type: 'success',
            category: 'hierarchy',
            message: 'Good typography hierarchy detected with appropriate size relationships.',
            suggestions: [
                'Maintain consistent hierarchy across all pages',
                'Test hierarchy effectiveness with actual content'
            ]
        };
    }
    
    categorizeFontFamily(fontFamily) {
        const family = fontFamily.toLowerCase();
        
        for (const [category, fonts] of Object.entries(this.fontCategories)) {
            if (fonts.some(font => family.includes(font.toLowerCase()))) {
                return category;
            }
        }
        
        // Default categorization based on common patterns
        if (family.includes('serif')) return 'serif';
        if (family.includes('sans') || family.includes('arial') || family.includes('helvetica')) return 'sansSerif';
        if (family.includes('mono') || family.includes('courier')) return 'monospace';
        if (family.includes('script') || family.includes('italic')) return 'script';
        
        return 'sansSerif'; // Default assumption
    }
    
    validateColorContrast(foreground, background) {
        // Simple contrast ratio calculation
        const fgLuminance = this.calculateLuminance(foreground);
        const bgLuminance = this.calculateLuminance(background);
        
        const contrast = (Math.max(fgLuminance, bgLuminance) + 0.05) / 
                        (Math.min(fgLuminance, bgLuminance) + 0.05);
        
        return {
            ratio: contrast,
            wcagAA: contrast >= 4.5,
            wcagAAA: contrast >= 7.0
        };
    }
    
    calculateLuminance(hexColor) {
        // Convert hex to RGB
        const rgb = hexColor.match(/\w\w/g).map(x => parseInt(x, 16) / 255);
        
        // Calculate relative luminance
        const [r, g, b] = rgb.map(c => {
            return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        });
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }
    
    generateRecommendations(analysisResults) {
        const recommendations = [];
        
        const errors = analysisResults.filter(r => r.type === 'error');
        const warnings = analysisResults.filter(r => r.type === 'warning');
        
        if (errors.length > 0) {
            recommendations.push({
                priority: 'high',
                message: `${errors.length} critical typography issues need immediate attention.`,
                action: 'Fix errors first before proceeding with design.'
            });
        }
        
        if (warnings.length > 0) {
            recommendations.push({
                priority: 'medium',
                message: `${warnings.length} typography improvements recommended.`,
                action: 'Review warnings to enhance design quality.'
            });
        }
        
        if (errors.length === 0 && warnings.length === 0) {
            recommendations.push({
                priority: 'low',
                message: 'Typography looks good! No major issues detected.',
                action: 'Consider fine-tuning details for perfection.'
            });
        }
        
        return recommendations;
    }
}
