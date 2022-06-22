grammar Entail;

start: theoremImports+=theoremImport* substitutions+=substitution* deduction;

// Import
theoremImport: 'import' theorem=rootFormula 'from' filepath=STRING ';';

// Substitution
substitution: 'in' theorem=rootFormula 'substitute' specs+=spec (',' specs+=spec)* 'result' result=rootFormula ';';
spec: substituted=atomicFormula 'with' substitute=rootFormula;

// Deduction
deduction: lines+=line+;
line: lineNumber=NUMBER ')' rootFormula ':' ruleOfInference ';';
ruleOfInference: ruleName=(
    RULE_PREMISE | RULE_THEOREM | RULE_A_IN | RULE_A_OUT | RULE_E_IN | RULE_E_OUT | RULE_IF_IN | RULE_IF_OUT |
    RULE_IFF_IN | RULE_IFF_OUT | RULE_AND_IN | RULE_AND_OUT | RULE_OR_IN | RULE_OR_OUT | RULE_NOT_IN | RULE_NOT_OUT |
    RULE_EXPLOSION | RULE_REPETITION)
    ruleDependencies?;

ruleDependencies: lineNumbers+=NUMBER (',' lineNumbers+=NUMBER)*;

// Formula
rootFormula: compRootFormula | quantFormula | atomicFormula;
formula: compFormula | quantFormula | atomicFormula;

compRootFormula: compRootBinaryFormula | compUnaryFormula;
compFormula: compBinaryFormula | compUnaryFormula;

compRootBinaryFormula: lFormula=formula binaryOperator rFormula=formula;
compBinaryFormula: lParen='(' lFormula=formula binaryOperator rFormula=formula rParen=')';
compUnaryFormula: operator=NEGATION formula;

binaryOperator: operator=(CONDITIONAL | DISJUNCTION | CONJUNCTION | BICONDITIONAL);

quantFormula: uniFormula | exiFormula;
uniFormula: lParen='(' indVar=IND_VAR rParen=')' formula;
exiFormula: lBracket='[' indVar=IND_VAR rBracket=']' formula;

atomicFormula: predVar=(RULE_PREMISE | RULE_THEOREM | RULE_EXPLOSION | PRED_VAR) terms?;
terms: indVars+=IND_VAR+ | lParen='(' indVars+=IND_VAR (',' indVars+=IND_VAR)* rParen=')';

STRING: '"' (ESC|.)*? '"' ;
fragment
ESC : '\\"' | '\\\\' ;

RULE_PREMISE: 'PR';
RULE_THEOREM: 'TH';
RULE_A_IN: '+A';
RULE_A_OUT: '-A';
RULE_E_IN: '+E';
RULE_E_OUT: '-E';
RULE_IF_IN: '+IF';
RULE_IF_OUT: '-IF';
RULE_IFF_IN: '+IFF';
RULE_IFF_OUT: '-IFF';
RULE_AND_IN: '+AND';
RULE_AND_OUT: '-AND';
RULE_OR_IN: '+OR';
RULE_OR_OUT: '-OR';
RULE_NOT_IN: '+NOT';
RULE_NOT_OUT: '-NOT';
RULE_EXPLOSION: 'XP';
RULE_REPETITION: 'RP';

PRED_VAR: [A-Z][0-9]*; // Predicate variable
IND_VAR: [a-z][0-9]*; // Individual variable

NUMBER: [1-9][0-9]*;

NEWLINE: '\r'? '\n' -> skip;
WS: [ \t]+ -> skip;

NEGATION: '~';
CONJUNCTION: '&';
DISJUNCTION: '|';
CONDITIONAL: '->';
BICONDITIONAL: '<->';

UNKNOWN: .;
