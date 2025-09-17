/**
 * Typography Agent - Illustrator Host Script (ExtendScript)
 * Provides the bridge between CEP panel and Illustrator application
 */

// Typography Agent namespace
if (typeof TypographyAgent === 'undefined') {
    TypographyAgent = {};
}

/**
 * Get information about currently selected elements
 */
TypographyAgent.getSelectedElements = function() {
    if (app.documents.length === 0) {
        return JSON.stringify({
            success: false,
            error: "No document is open"
        });
    }
    
    var doc = app.activeDocument;
    var selection = doc.selection;
    var elements = [];
    
    try {
        for (var i = 0; i < selection.length; i++) {
            var item = selection[i];
            
            if (item.typename === "TextFrame") {
                var textFrame = item;
                var textRange = textFrame.textRange;
                
                // Extract text properties
                var element = {
                    type: "text",
                    family: textRange.characterAttributes.textFont ? textRange.characterAttributes.textFont.name : "Unknown",
                    fontSize: textRange.characterAttributes.size,
                    fontWeight: getFontWeight(textRange.characterAttributes.textFont),
                    lineHeight: textRange.paragraphAttributes.leading,
                    characterSpacing: textRange.characterAttributes.tracking,
                    color: getColorHex(textRange.characterAttributes.fillColor),
                    text: textRange.contents,
                    lineLength: estimateLineLength(textRange.contents, textFrame.width),
                    bounds: {
                        left: textFrame.left,
                        top: textFrame.top,
                        width: textFrame.width,
                        height: textFrame.height
                    },
                    overflowed: textFrame.overflowed
                };
                
                elements.push(element);
            }
        }
        
        return JSON.stringify({
            success: true,
            elements: elements,
            count: elements.length
        });
        
    } catch (error) {
        return JSON.stringify({
            success: false,
            error: error.toString()
        });
    }
};

/**
 * Get current document context
 */
TypographyAgent.getCurrentContext = function() {
    if (app.documents.length === 0) {
        return JSON.stringify({
            success: false,
            error: "No document is open"
        });
    }
    
    var doc = app.activeDocument;
    
    try {
        var context = {
            document: {
                name: doc.name,
                width: doc.width,
                height: doc.height,
                colorSpace: doc.documentColorSpace.toString(),
                artboards: doc.artboards.length
            },
            selection: {
                count: doc.selection.length,
                types: getSelectionTypes(doc.selection)
            },
            fonts: getUsedFonts(doc),
            colors: getUsedColors(doc)
        };
        
        return JSON.stringify({
            success: true,
            context: context
        });
        
    } catch (error) {
        return JSON.stringify({
            success: false,
            error: error.toString()
        });
    }
};

/**
 * Apply typography fixes to selected elements
 */
TypographyAgent.applyTypographyFix = function(fixType, parameters) {
    if (app.documents.length === 0) {
        return JSON.stringify({
            success: false,
            error: "No document is open"
        });
    }
    
    var doc = app.activeDocument;
    var selection = doc.selection;
    
    try {
        var results = [];
        
        switch (fixType) {
            case "kerning":
                results = applyKerningFix(selection, parameters);
                break;
                
            case "hierarchy":
                results = applyHierarchyFix(selection, parameters);
                break;
                
            case "readability":
                results = applyReadabilityFix(selection, parameters);
                break;
                
            case "alignment":
                results = applyAlignmentFix(selection, parameters);
                break;
                
            default:
                throw new Error("Unknown fix type: " + fixType);
        }
        
        return JSON.stringify({
            success: true,
            fixType: fixType,
            results: results
        });
        
    } catch (error) {
        return JSON.stringify({
            success: false,
            error: error.toString()
        });
    }
};

/**
 * Batch format text elements
 */
TypographyAgent.batchFormatText = function(formatRules) {
    if (app.documents.length === 0) {
        return JSON.stringify({
            success: false,
            error: "No document is open"
        });
    }
    
    var doc = app.activeDocument;
    var textFrames = doc.textFrames;
    var rules = JSON.parse(formatRules);
    var results = [];
    
    try {
        for (var i = 0; i < textFrames.length; i++) {
            var textFrame = textFrames[i];
            var textRange = textFrame.textRange;
            var appliedRules = [];
            
            // Apply each formatting rule
            for (var j = 0; j < rules.length; j++) {
                var rule = rules[j];
                
                if (shouldApplyRule(textFrame, rule)) {
                    applyFormattingRule(textRange, rule);
                    appliedRules.push(rule.name || "rule_" + j);
                }
            }
            
            results.push({
                index: i,
                appliedRules: appliedRules
            });
        }
        
        return JSON.stringify({
            success: true,
            processed: results.length,
            results: results
        });
        
    } catch (error) {
        return JSON.stringify({
            success: false,
            error: error.toString()
        });
    }
};

/**
 * Auto-adjust text boxes for optimal layout
 */
TypographyAgent.autoAdjustTextBoxes = function(adjustmentParams) {
    if (app.documents.length === 0) {
        return JSON.stringify({
            success: false,
            error: "No document is open"
        });
    }
    
    var doc = app.activeDocument;
    var selection = doc.selection.length > 0 ? doc.selection : doc.textFrames;
    var params = JSON.parse(adjustmentParams);
    var results = [];
    
    try {
        for (var i = 0; i < selection.length; i++) {
            var item = selection[i];
            
            if (item.typename === "TextFrame") {
                var textFrame = item;
                var original = {
                    width: textFrame.width,
                    height: textFrame.height,
                    left: textFrame.left,
                    top: textFrame.top
                };
                
                // Apply auto-fit if requested
                if (params.autoFit) {
                    autoFitText(textFrame, params);
                }
                
                // Apply specific adjustments
                if (params.adjustments && params.adjustments[i]) {
                    var adj = params.adjustments[i];
                    if (adj.width) textFrame.width = adj.width;
                    if (adj.height) textFrame.height = adj.height;
                    if (adj.left !== undefined) textFrame.left = adj.left;
                    if (adj.top !== undefined) textFrame.top = adj.top;
                }
                
                results.push({
                    index: i,
                    success: true,
                    original: original,
                    final: {
                        width: textFrame.width,
                        height: textFrame.height,
                        left: textFrame.left,
                        top: textFrame.top
                    }
                });
            }
        }
        
        return JSON.stringify({
            success: true,
            processed: results.length,
            results: results
        });
        
    } catch (error) {
        return JSON.stringify({
            success: false,
            error: error.toString()
        });
    }
};

// Helper Functions

function getFontWeight(textFont) {
    if (!textFont) return "regular";
    
    var fontName = textFont.name.toLowerCase();
    if (fontName.indexOf("bold") !== -1) return "bold";
    if (fontName.indexOf("light") !== -1) return "light";
    if (fontName.indexOf("medium") !== -1) return "medium";
    if (fontName.indexOf("semibold") !== -1) return "semibold";
    if (fontName.indexOf("black") !== -1) return "black";
    
    return "regular";
}

function getColorHex(color) {
    try {
        if (color.typename === "RGBColor") {
            var r = Math.round(color.red).toString(16).padStart(2, '0');
            var g = Math.round(color.green).toString(16).padStart(2, '0');
            var b = Math.round(color.blue).toString(16).padStart(2, '0');
            return "#" + r + g + b;
        }
        return "#000000"; // Default to black
    } catch (e) {
        return "#000000";
    }
}

function estimateLineLength(text, frameWidth) {
    // Rough estimation: average character width is about 0.6em
    // This is a simplified calculation
    var avgCharWidth = 7; // pixels, rough estimate
    var maxCharsPerLine = Math.floor(frameWidth / avgCharWidth);
    
    var lines = text.split('\n');
    var maxLineLength = 0;
    
    for (var i = 0; i < lines.length; i++) {
        if (lines[i].length > maxLineLength) {
            maxLineLength = lines[i].length;
        }
    }
    
    return Math.min(maxLineLength, maxCharsPerLine);
}

function getSelectionTypes(selection) {
    var types = [];
    for (var i = 0; i < selection.length; i++) {
        var type = selection[i].typename;
        if (types.indexOf(type) === -1) {
            types.push(type);
        }
    }
    return types;
}

function getUsedFonts(doc) {
    var fonts = [];
    var textFrames = doc.textFrames;
    
    for (var i = 0; i < textFrames.length; i++) {
        var fontName = textFrames[i].textRange.characterAttributes.textFont.name;
        if (fonts.indexOf(fontName) === -1) {
            fonts.push(fontName);
        }
    }
    
    return fonts;
}

function getUsedColors(doc) {
    var colors = [];
    var textFrames = doc.textFrames;
    
    for (var i = 0; i < textFrames.length; i++) {
        var color = getColorHex(textFrames[i].textRange.characterAttributes.fillColor);
        if (colors.indexOf(color) === -1) {
            colors.push(color);
        }
    }
    
    return colors;
}

function applyKerningFix(selection, parameters) {
    var results = [];
    
    for (var i = 0; i < selection.length; i++) {
        if (selection[i].typename === "TextFrame") {
            var textRange = selection[i].textRange;
            
            // Apply optical kerning
            if (parameters.opticalKerning) {
                textRange.characterAttributes.autoKernType = AutoKernType.OPTICAL;
            }
            
            // Apply custom kerning pairs
            if (parameters.kerningPairs) {
                // This would need more complex implementation for specific character pairs
                textRange.characterAttributes.tracking = parameters.tracking || 0;
            }
            
            results.push({
                index: i,
                kerningApplied: true
            });
        }
    }
    
    return results;
}

function applyHierarchyFix(selection, parameters) {
    var results = [];
    
    // Sort by font size to establish hierarchy
    var textFrames = [];
    for (var i = 0; i < selection.length; i++) {
        if (selection[i].typename === "TextFrame") {
            textFrames.push({
                frame: selection[i],
                size: selection[i].textRange.characterAttributes.size,
                index: i
            });
        }
    }
    
    textFrames.sort(function(a, b) { return b.size - a.size; });
    
    // Apply hierarchy scaling
    var baseRatio = parameters.scaleRatio || 1.25;
    
    for (var j = 0; j < textFrames.length; j++) {
        var item = textFrames[j];
        var newSize = parameters.baseSize ? parameters.baseSize * Math.pow(baseRatio, textFrames.length - j - 1) : item.size;
        
        item.frame.textRange.characterAttributes.size = newSize;
        
        results.push({
            index: item.index,
            oldSize: item.size,
            newSize: newSize
        });
    }
    
    return results;
}

function applyReadabilityFix(selection, parameters) {
    var results = [];
    
    for (var i = 0; i < selection.length; i++) {
        if (selection[i].typename === "TextFrame") {
            var textRange = selection[i].textRange;
            
            // Adjust line height for readability
            if (parameters.lineHeight) {
                textRange.paragraphAttributes.leading = textRange.characterAttributes.size * parameters.lineHeight;
            }
            
            // Adjust character spacing
            if (parameters.characterSpacing) {
                textRange.characterAttributes.tracking = parameters.characterSpacing;
            }
            
            results.push({
                index: i,
                readabilityImproved: true
            });
        }
    }
    
    return results;
}

function applyAlignmentFix(selection, parameters) {
    var results = [];
    
    for (var i = 0; i < selection.length; i++) {
        if (selection[i].typename === "TextFrame") {
            var textRange = selection[i].textRange;
            
            // Apply paragraph alignment
            if (parameters.alignment) {
                switch (parameters.alignment) {
                    case "left":
                        textRange.paragraphAttributes.justification = Justification.LEFT;
                        break;
                    case "center":
                        textRange.paragraphAttributes.justification = Justification.CENTER;
                        break;
                    case "right":
                        textRange.paragraphAttributes.justification = Justification.RIGHT;
                        break;
                    case "justify":
                        textRange.paragraphAttributes.justification = Justification.FULLJUSTIFY;
                        break;
                }
            }
            
            results.push({
                index: i,
                alignmentApplied: parameters.alignment
            });
        }
    }
    
    return results;
}

function shouldApplyRule(textFrame, rule) {
    var textRange = textFrame.textRange;
    
    switch (rule.selector) {
        case "all":
            return true;
        case "heading":
            return textRange.characterAttributes.size > (rule.headingThreshold || 18);
        case "body":
            return textRange.characterAttributes.size <= (rule.headingThreshold || 18);
        case "contains":
            return textRange.contents.indexOf(rule.text) !== -1;
        default:
            return false;
    }
}

function applyFormattingRule(textRange, rule) {
    // Apply font family
    if (rule.fontFamily) {
        try {
            textRange.characterAttributes.textFont = app.textFonts.getByName(rule.fontFamily);
        } catch (e) {
            // Font not found, continue with other properties
        }
    }
    
    // Apply font size
    if (rule.fontSize) {
        textRange.characterAttributes.size = rule.fontSize;
    }
    
    // Apply line height
    if (rule.lineHeight) {
        textRange.paragraphAttributes.leading = rule.fontSize * rule.lineHeight;
    }
    
    // Apply character spacing
    if (rule.characterSpacing) {
        textRange.characterAttributes.tracking = rule.characterSpacing;
    }
    
    // Apply color
    if (rule.color) {
        var color = new RGBColor();
        color.red = parseInt(rule.color.substring(1, 3), 16);
        color.green = parseInt(rule.color.substring(3, 5), 16);
        color.blue = parseInt(rule.color.substring(5, 7), 16);
        textRange.characterAttributes.fillColor = color;
    }
}

function autoFitText(textFrame, params) {
    var textRange = textFrame.textRange;
    var maxIterations = 20;
    var iteration = 0;
    var baseFontSize = params.baseFontSize || 12;
    var maxFontSize = params.maxFontSize || 72;
    
    // Start with base font size
    textRange.characterAttributes.size = baseFontSize;
    
    // Reduce size if overflowing
    while (textFrame.overflowed && iteration < maxIterations) {
        textRange.characterAttributes.size *= 0.95;
        iteration++;
    }
    
    // Increase size if there's room
    iteration = 0;
    while (!textFrame.overflowed && 
           textRange.characterAttributes.size < maxFontSize && 
           iteration < maxIterations) {
        textRange.characterAttributes.size *= 1.05;
        iteration++;
        
        if (textFrame.overflowed) {
            textRange.characterAttributes.size *= 0.95;
            break;
        }
    }
}
