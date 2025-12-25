#!/usr/bin/env node
/**
 * MermaidJS Syntax & Style Validator
 * 
 * Validates MermaidJS diagrams through structural and style analysis.
 * 
 * Dependencies: Node.js (built-in modules only)
 * 
 * Usage:
 *   node validate_mermaid.js <file.mmd>
 *   node validate_mermaid.js --code "flowchart TD; A-->B"
 *   node validate_mermaid.js --json --code "..."
 */

const fs = require('fs');
const path = require('path');

// Diagram type patterns - comprehensive list of MermaidJS diagram types
const DIAGRAM_TYPES = {
    flowchart: { pattern: /^flowchart\s+(TB|BT|LR|RL|TD)/i, requiresDirection: true },
    graph: { pattern: /^graph\s+(TB|BT|LR|RL|TD)/i, requiresDirection: true },
    sequenceDiagram: { pattern: /^sequenceDiagram/i },
    classDiagram: { pattern: /^classDiagram/i },
    'stateDiagram-v2': { pattern: /^stateDiagram-v2/i },
    stateDiagram: { pattern: /^stateDiagram(?!-v2)/i },
    erDiagram: { pattern: /^erDiagram/i },
    journey: { pattern: /^journey/i },
    gantt: { pattern: /^gantt/i },
    pie: { pattern: /^pie/i },
    quadrantChart: { pattern: /^quadrantChart/i },
    requirementDiagram: { pattern: /^requirementDiagram/i },
    gitGraph: { pattern: /^gitGraph/i },
    mindmap: { pattern: /^mindmap/i },
    timeline: { pattern: /^timeline/i },
};

// Style thresholds with justification
const STYLE_CONFIG = {
    // 80 chars is standard readable line length for code
    maxLineLength: 80,
    // More than 2 arrows per line reduces readability significantly
    maxArrowsPerLine: 2,
    // More than 4 single-letter IDs suggests poor naming
    maxGenericIds: 4,
    // Files over 100 lines are harder to maintain
    maxLinesWarning: 100,
};

/**
 * Detect diagram type from code.
 * Returns type name and config, or 'unknown' if not recognized.
 */
function detectDiagramType(code) {
    const firstLine = code.trim().split('\n')[0].trim();
    for (const [type, config] of Object.entries(DIAGRAM_TYPES)) {
        if (config.pattern.test(firstLine)) {
            return { type, config };
        }
    }
    return { type: 'unknown', config: null };
}

/**
 * Validate bracket balance, accounting for diagram-specific syntax.
 * ER diagrams use {} for cardinality notation, so those are excluded.
 */
function validateBrackets(code, diagramType) {
    const errors = [];
    
    // ER diagrams use {} for cardinality (e.g., ||--o{), skip curly brackets
    const brackets = diagramType === 'erDiagram' 
        ? { '(': ')', '[': ']' }
        : { '(': ')', '[': ']', '{': '}' };
    
    const stack = [];
    let inString = false;
    let stringChar = null;
    
    for (let i = 0; i < code.length; i++) {
        const char = code[i];
        const prevChar = i > 0 ? code[i - 1] : '';
        
        // Track string boundaries (ignore escaped quotes)
        if ((char === '"' || char === "'") && prevChar !== '\\') {
            if (!inString) {
                inString = true;
                stringChar = char;
            } else if (char === stringChar) {
                inString = false;
                stringChar = null;
            }
            continue;
        }
        
        // Skip bracket checking inside strings
        if (inString) continue;
        
        if (brackets[char]) {
            stack.push({ char, pos: i, line: code.substring(0, i).split('\n').length });
        } else if (Object.values(brackets).includes(char)) {
            if (stack.length === 0) {
                const line = code.substring(0, i).split('\n').length;
                errors.push(`Line ${line}: Unmatched closing '${char}'`);
            } else {
                const last = stack.pop();
                if (brackets[last.char] !== char) {
                    errors.push(`Line ${last.line}: '${last.char}' closed with '${char}' on line ${code.substring(0, i).split('\n').length}`);
                }
            }
        }
    }
    
    for (const { char, line } of stack) {
        errors.push(`Line ${line}: Unclosed '${char}'`);
    }
    
    // Check quote balance
    const doubleQuotes = (code.match(/(?<!\\)"/g) || []).length;
    if (doubleQuotes % 2 !== 0) {
        errors.push('Unbalanced double quotes detected');
    }
    
    return errors;
}

/**
 * Validate flowchart/graph specific syntax and style.
 */
function validateFlowchart(code, lines) {
    const errors = [];
    const warnings = [];
    
    // Check direction declaration
    const firstLine = lines[0].trim();
    if (!/(flowchart|graph)\s+(tb|bt|lr|rl|td)/i.test(firstLine)) {
        errors.push('Flowchart must specify direction: TD, TB, LR, RL, or BT');
    }
    
    // Check for long arrow chains (readability issue)
    lines.forEach((line, i) => {
        const arrowCount = (line.match(/-->/g) || []).length;
        if (arrowCount > STYLE_CONFIG.maxArrowsPerLine) {
            warnings.push(`Line ${i + 1}: Chain has ${arrowCount} arrows - break into separate lines`);
        }
        
        if (line.length > STYLE_CONFIG.maxLineLength) {
            warnings.push(`Line ${i + 1}: ${line.length} chars - consider breaking up`);
        }
    });
    
    // Check for generic single-letter IDs (poor naming)
    const singleLetterNodes = code.match(/\b([A-Z])\s*[\[\(\{]/g) || [];
    if (singleLetterNodes.length > STYLE_CONFIG.maxGenericIds) {
        warnings.push(`Found ${singleLetterNodes.length} single-letter node IDs - use descriptive names`);
    }
    
    // Check for unlabeled decision branches
    const decisions = (code.match(/\{[^}]+\}/g) || []).length;
    const labeledArrows = (code.match(/-->\|[^|]+\|/g) || []).length;
    if (decisions > 0 && labeledArrows < decisions) {
        warnings.push('Some decision branches lack labels - add -->|Yes| or -->|No|');
    }
    
    // Check subgraph balance (only match 'end' on its own line)
    const subgraphStarts = (code.match(/^\s*subgraph\s+/gmi) || []).length;
    const subgraphEnds = (code.match(/^\s*end\s*$/gmi) || []).length;
    if (subgraphStarts !== subgraphEnds) {
        errors.push(`Subgraph mismatch: ${subgraphStarts} 'subgraph' vs ${subgraphEnds} 'end'`);
    }
    
    return { errors, warnings };
}

/**
 * Validate sequence diagram syntax and style.
 */
function validateSequence(code, lines) {
    const errors = [];
    const warnings = [];
    
    const hasParticipant = /participant\s+\w+/i.test(code);
    const hasActor = /actor\s+\w+/i.test(code);
    
    if (!hasParticipant && !hasActor) {
        warnings.push('Declare participants at the top for better ordering control');
    }
    
    // Check for messages without labels
    const unlabeledMessages = code.match(/[A-Za-z0-9_]+\s*->>?\s*[A-Za-z0-9_]+\s*$/gm) || [];
    if (unlabeledMessages.length > 0) {
        warnings.push(`${unlabeledMessages.length} message(s) lack labels - add description after ':'`);
    }
    
    // Check activation balance
    const activates = (code.match(/\bactivate\b/gi) || []).length;
    const deactivates = (code.match(/\bdeactivate\b/gi) || []).length;
    const plusActivates = (code.match(/->>?\+/g) || []).length;
    const minusDeactivates = (code.match(/-->>?-/g) || []).length;
    
    const totalActivates = activates + plusActivates;
    const totalDeactivates = deactivates + minusDeactivates;
    
    if (totalActivates !== totalDeactivates) {
        warnings.push(`Activation imbalance: ${totalActivates} activate vs ${totalDeactivates} deactivate`);
    }
    
    // Check block balance (only match 'end' on its own line)
    const blockKeywords = ['alt', 'opt', 'loop', 'par', 'critical', 'break', 'rect'];
    const blockPattern = new RegExp(`^\\s*(${blockKeywords.join('|')})\\b`, 'gmi');
    const blockStarts = (code.match(blockPattern) || []).length;
    const blockEnds = (code.match(/^\s*end\s*$/gmi) || []).length;
    
    if (blockStarts !== blockEnds) {
        errors.push(`Block mismatch: ${blockStarts} block starts vs ${blockEnds} 'end'`);
    }
    
    return { errors, warnings };
}

/**
 * Validate Gantt chart syntax and style.
 */
function validateGantt(code, lines) {
    const errors = [];
    const warnings = [];
    
    if (!/title\s+.+/i.test(code)) {
        warnings.push('Add a title for better readability');
    }
    
    if (!/dateFormat\s+.+/i.test(code)) {
        warnings.push('Specify dateFormat for consistent date parsing');
    }
    
    // Check for sections in larger charts
    const sections = (code.match(/section\s+.+/gi) || []).length;
    const tasks = (code.match(/^\s*\w.*:\s*(\w+,)?\s*\d/gm) || []).length;
    
    if (tasks > 5 && sections === 0) {
        warnings.push('Consider organizing tasks into sections');
    }
    
    return { errors, warnings };
}

/**
 * Validate state diagram syntax.
 */
function validateState(code, lines) {
    const errors = [];
    const warnings = [];
    
    if (!/\[\*\]/.test(code)) {
        warnings.push('Consider adding initial state [*] for clarity');
    }
    
    return { errors, warnings };
}

/**
 * Validate ER diagram syntax.
 */
function validateER(code, lines) {
    const errors = [];
    const warnings = [];
    
    // Check for relationships without labels
    const relationships = (code.match(/\w+\s*[\|\}o].*[\|\{o]\s*\w+/g) || []).length;
    const labeledRelationships = (code.match(/\w+\s*[\|\}o].*[\|\{o]\s*\w+\s*:/g) || []).length;
    
    if (relationships > labeledRelationships) {
        warnings.push('Some relationships lack labels - add description after ":"');
    }
    
    return { errors, warnings };
}

/**
 * Check general style issues applicable to all diagram types.
 */
function checkGeneralStyle(code, lines) {
    const warnings = [];
    
    // Check for mixed tabs and spaces
    const hasSpaceIndent = lines.some(l => /^ +\S/.test(l));
    const hasTabIndent = lines.some(l => /^\t+\S/.test(l));
    if (hasSpaceIndent && hasTabIndent) {
        warnings.push('Mixed tabs and spaces - use 4 spaces consistently');
    }
    
    // Check for markdown fences (common mistake)
    if (code.includes('```')) {
        warnings.push('Remove markdown code fences (```) from diagram code');
    }
    
    // Large file warning
    if (lines.length > STYLE_CONFIG.maxLinesWarning) {
        warnings.push(`Large diagram (${lines.length} lines) - consider splitting`);
    }
    
    return warnings;
}

/**
 * Main validation function.
 * Returns structured result with validity status, errors, and warnings.
 */
function validate(code) {
    const result = {
        valid: false,
        diagramType: null,
        errors: [],
        warnings: []
    };
    
    // Handle empty input gracefully
    if (!code || !code.trim()) {
        result.errors.push('Empty diagram code');
        return result;
    }
    
    code = code.trim();
    const lines = code.split('\n');
    const { type, config } = detectDiagramType(code);
    result.diagramType = type;
    
    if (type === 'unknown') {
        result.errors.push('Unknown diagram type - check first line declaration');
    }
    
    // Bracket validation
    result.errors.push(...validateBrackets(code, type));
    
    // Type-specific validation
    const validators = {
        flowchart: validateFlowchart,
        graph: validateFlowchart,
        sequenceDiagram: validateSequence,
        gantt: validateGantt,
        stateDiagram: validateState,
        'stateDiagram-v2': validateState,
        erDiagram: validateER,
    };
    
    if (validators[type]) {
        const { errors, warnings } = validators[type](code, lines);
        result.errors.push(...errors);
        result.warnings.push(...warnings);
    }
    
    // General style checks
    result.warnings.push(...checkGeneralStyle(code, lines));
    
    result.valid = result.errors.length === 0;
    return result;
}

/**
 * Format validation result for human-readable output.
 */
function formatResult(result) {
    const status = result.valid ? '✅ Valid' : '❌ Invalid';
    const lines = [status];
    
    if (result.diagramType) {
        lines.push(`   Type: ${result.diagramType}`);
    }
    
    result.errors.forEach(err => {
        lines.push(`   ❌ ${err}`);
    });
    
    result.warnings.forEach(warn => {
        lines.push(`   ⚠️  ${warn}`);
    });
    
    if (result.valid && result.warnings.length === 0) {
        lines.push('   No issues found');
    }
    
    return lines.join('\n');
}

/**
 * Read file with error handling.
 * Returns file contents or exits with helpful error message.
 */
function readFile(filePath) {
    const resolved = path.resolve(filePath);
    
    if (!fs.existsSync(resolved)) {
        console.error(`❌ File not found: ${resolved}`);
        console.error('   Check the file path and try again.');
        process.exit(1);
    }
    
    try {
        return fs.readFileSync(resolved, 'utf-8');
    } catch (err) {
        if (err.code === 'EACCES') {
            console.error(`❌ Permission denied: ${resolved}`);
        } else if (err.code === 'EISDIR') {
            console.error(`❌ Path is a directory: ${resolved}`);
        } else {
            console.error(`❌ Error reading file: ${err.message}`);
        }
        process.exit(1);
    }
}

function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
        console.log(`
MermaidJS Validator

Validates syntax and style of MermaidJS diagrams.

Usage:
  node validate_mermaid.js <file.mmd>
  node validate_mermaid.js --code "flowchart TD; A-->B"

Options:
  --code, -c    Validate inline code string
  --json        Output results as JSON
  --help, -h    Show this help

Examples:
  node validate_mermaid.js diagram.mmd
  node validate_mermaid.js -c "sequenceDiagram; A->>B: Hello"
  node validate_mermaid.js --json -c "flowchart LR; A-->B"
        `);
        process.exit(0);
    }
    
    let code = '';
    const jsonOutput = args.includes('--json');
    
    // Parse --code argument
    const codeIndex = args.findIndex(a => a === '--code' || a === '-c');
    if (codeIndex !== -1 && args[codeIndex + 1]) {
        code = args[codeIndex + 1];
    } else {
        // Find file argument (first non-flag argument)
        const fileArg = args.find(a => !a.startsWith('-'));
        if (fileArg) {
            code = readFile(fileArg);
        }
    }
    
    if (!code) {
        console.error('❌ No code provided. Use --code or specify a file.');
        console.error('   Run with --help for usage information.');
        process.exit(1);
    }
    
    const result = validate(code);
    
    if (jsonOutput) {
        console.log(JSON.stringify(result, null, 2));
    } else {
        console.log(formatResult(result));
    }
    
    process.exit(result.valid ? 0 : 1);
}

// Export for programmatic use
module.exports = { validate, detectDiagramType };

if (require.main === module) {
    main();
}
