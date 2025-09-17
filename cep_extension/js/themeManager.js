/**
 * Theme Manager for Typography Agent CEP Extension
 * Handles Adobe application theme changes and UI adaptation
 */

class ThemeManager {
    constructor() {
        this.csInterface = new CSInterface();
        this.currentTheme = null;
    }
    
    init() {
        // Get initial theme
        this.updateTheme();
        
        // Listen for theme changes
        this.csInterface.addEventListener('com.adobe.csxs.events.ThemeColorChanged', () => {
            this.updateTheme();
        });
    }
    
    updateTheme() {
        try {
            // Get current theme from Adobe host application
            const skinInfo = this.csInterface.getHostEnvironment().appSkinInfo;
            
            if (skinInfo) {
                this.currentTheme = {
                    panelBackgroundColor: skinInfo.panelBackgroundColor,
                    appBarBackgroundColor: skinInfo.appBarBackgroundColor,
                    baseFontFamily: skinInfo.baseFontFamily,
                    baseFontSize: skinInfo.baseFontSize
                };
                
                this.applyTheme(this.currentTheme);
            }
        } catch (error) {
            console.warn('Failed to get theme from host application:', error);
            // Use default theme
            this.applyDefaultTheme();
        }
    }
    
    applyTheme(theme) {
        const root = document.documentElement;
        
        // Convert Adobe color format to CSS
        const bgColor = this.toHex(theme.panelBackgroundColor);
        const appBarColor = this.toHex(theme.appBarBackgroundColor);
        
        // Determine if dark theme
        const isDark = this.isColorDark(theme.panelBackgroundColor);
        
        // Apply CSS custom properties
        root.style.setProperty('--bg-color', bgColor);
        root.style.setProperty('--primary-color', isDark ? '#4a90e2' : '#2c5aa0');
        root.style.setProperty('--text-color', isDark ? '#ffffff' : '#333333');
        root.style.setProperty('--border-color', isDark ? '#555555' : '#dddddd');
        root.style.setProperty('--secondary-color', isDark ? '#404040' : '#f0f0f0');
        
        // Apply font settings
        if (theme.baseFontFamily) {
            root.style.setProperty('--font-family', theme.baseFontFamily);
        }
        
        if (theme.baseFontSize) {
            root.style.setProperty('--font-size', theme.baseFontSize + 'px');
        }
        
        // Add theme class to body
        document.body.className = `typography-agent-panel ${isDark ? 'dark-theme' : 'light-theme'}`;
        
        console.log('Theme applied:', { isDark, bgColor, appBarColor });
    }
    
    applyDefaultTheme() {
        // Apply default light theme
        const root = document.documentElement;
        root.style.setProperty('--bg-color', '#fafafa');
        root.style.setProperty('--primary-color', '#2c5aa0');
        root.style.setProperty('--text-color', '#333333');
        root.style.setProperty('--border-color', '#dddddd');
        root.style.setProperty('--secondary-color', '#f0f0f0');
        
        document.body.className = 'typography-agent-panel light-theme';
    }
    
    toHex(colorObj) {
        if (!colorObj) return '#ffffff';
        
        try {
            // Adobe color object has r, g, b properties (0-255)
            const r = Math.round(colorObj.color.red).toString(16).padStart(2, '0');
            const g = Math.round(colorObj.color.green).toString(16).padStart(2, '0');
            const b = Math.round(colorObj.color.blue).toString(16).padStart(2, '0');
            
            return `#${r}${g}${b}`;
        } catch (error) {
            console.warn('Failed to convert color to hex:', error);
            return '#ffffff';
        }
    }
    
    isColorDark(colorObj) {
        if (!colorObj) return false;
        
        try {
            const { red, green, blue } = colorObj.color;
            
            // Calculate luminance
            const luminance = (0.299 * red + 0.587 * green + 0.114 * blue) / 255;
            
            return luminance < 0.5;
        } catch (error) {
            return false;
        }
    }
    
    getCurrentTheme() {
        return this.currentTheme;
    }
}
