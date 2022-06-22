# Entail

**Entail** project collects a set of tools which support writing, validating
and managing of
[first-order logic](https://en.wikipedia.org/wiki/First-order_logic)
deductions. The purpose of these tools is mainly educational. They can be used
to support both studying and teaching of formal logic at the elementary level.

The central part of the project is the specification of **Entail Language**. It
is a formal language for writing deductions in first-order logic. It is
designed to be both easily readable and writeable. Detailed specification of
its syntax is provided later in this document. The main benefit of writing
deductions in this language is that it is supported by other tools in this
project which can automatically check for errors, generate nice presentations
and do other useful things.

## Overview of the repository

Here is an overview of all subprojects in this repository. To learn more about
each one of them, see their README.md files.

- **entail-core** is a python library containing general code related to
  first-order logic. It includes data structures like formulas, deductions
  and related algorithms like predicate substitution. In short, all
  domain-specific knowledge about first-order logic is here. It also includes
  functionalities related to Entail Language like parsing and writing.

- **entail-language-server** is a language server written in python. It
  implements [LSP](https://microsoft.github.io/language-server-protocol).
  Its purpose is to work as a backend for text editor extensions to offer
  real-time support for writing deductions in Entail Language.

- **entail-vscode-extension** is an extension for
  [Visual Studio Code](https://code.visualstudio.com) text editor. It is
  written in typescript and uses aforementioned language server as its
  backend.

- **entail-antlr-java** is a helper project where Entail Language parser is
  developed. It is a java project because Entail Language parser is created
  using ANTLR which is a java program. ANTLR is a tool for generating parsers
  by providing language grammars. It can output code in various languages,
  so here it is used to generate python code for **entail-core** library. Maven
  build is configured to output files directly into **entail-core** project.
  Of course, this is only necessary when some changes to Entail Language syntax
  are made, and this doesn't happen too often.

## Entail Language

Here is an informal description of Entail Language syntax. The following
content assumes some familiarity with first-order logic.

### Formula

**Propositional variables** and **Predicate variables** are written single
uppercase latters optionally followed by a sequence of digits. For example:

    A
    A1
    F123

There is no syntactical difference between **propositional variables** and
**predicate variables**. This conforms to the idea that
**propositional variables** can be seen as nullary **predicate variables**. We
can always know whether a symbol is a propositional or a predicate variables
based on its usage. Nevertheless, it is a good practice to follow the
traditional practice of choosing letters from the beginning of the alphabet for
propositional variables, and letters starting from `F` for predicate variables.
This is in no way mandated by Entail Language syntax.

**Individual variables** are written as single lowercase latters optionally
followed by a sequence of digits. For example:

`a`, `x`, `x122`

Some authors prefer the usage of the letters from the beginning of the alphabet
for free individual variables, and letters from the end of the alphabet (`x`,
`y`, `z`, `w`, `u`) for bound individual variables. This practice is adopted
here, but as with propositional and predicate variables, it is not mandated by
the Entail Language grammar.

**Atomic formula** can be either a single propositional variable, or a
predicate variable followed by a sequence of individual variables.

    A
    Fx
    Fx2y
    Gx1y12z

Some people might consider `Gx1y12z` not easily readable. Syntax also allows
enclosing individual variables in parentheses and separating them with a comma:

    F(x)
    F(x2, y)
    G(x1, y12, z)

You are free to use and mix these styles as you see fit.

Formula can be either truth-functionally complex or truth-functionally simple.
All of the mentioned formulas so far were truth-functionally simple.
Truth-functionally complex formula is a formula which contains at least one
truth-functional connective.

**Truth-functional connectives**

|               | Symbol | Placement |
|---------------|--------|-----------|
| Negation      | `~`    | Prefix    |
| Conjunction   | `&`    | Infix     |
| Disjunction   | `\|`   | Infix     |
| Conditional   | `->`   | Infix     |
| Biconditional | `<->`  | Infix     |

Here are some exmaples of truth-functionally complex formulas:

    A -> B
    ~Fxy <-> (Ga | B)

All connectives except `~` are binary. Expressions like the following are not
allowed:

    A & B & C

There is no defined precedence between connectives. Whenever expressions are
nested, parentheses are required:

    A -> (B & G)

Root formula doesn't need to be enclosed in parentheses.

**Quantifiers**

**Universal quantifier** is written as an individual variable enclosed in
parentheses, and **existential quantifier** is written as an individual
variable enclosed in brackets. Quantifiers must be prefixed to a formula.
Here are some formulas with quantifiers:

    (x) Fx
    [x] (x) (Fxy -> ~Gyx)
    (x) A

### Deduction

**Deduction** is a sequence of **steps**. Steps are sometimes called
"lines" because each step is usually written as a single line of text but
it doesn't have to be necessarily so because Entail Language doesn't treat
whitespace characters as significant parts of syntax.

**Step** contains four parts: line number, formula, rule of inference and a
sequence of dependencies. Here are some examples of deduction steps:

    1) A                      : P;
    2) B                      : P;
    3) A & B                  : +AND 1, 2;

**Line numbers** need to be consecutive. Their purpose is to make possible
referencing to previous formulas when applying a rule of inference. After the
line number comes a **formula** which represents a proposition established at
this step of deduction. Then comes a colon separator followed by an
abbreviation of the **rule of inference** used in this step and, if necessary,
a sequence of line numbers which are references to previous steps - steps
containing formulas which serve as **dependencies** to the used rule of
inference.

**Rules of inference**

Here is a list of available rules of inference along with their alternative
names and symbols used in Entail Language.

| Name                                   | Alternative name                  | Symbol |
|----------------------------------------|-----------------------------------|--------|
| Premise                                |                                   | `PR`   |
| Theorem                                |                                   | `TH`   |
| Introduction of Universal Quantifier   | Universal Generalization          | `+A`   |
| Elimination of Universal Quantifier    | Universal Instantiation           | `-A`   |
| Introduction of Existential Quantifier | Existential Generalization        | `+E`   |
| Elimination of Existential Quantifier  | Existential Instantiation         | `-E`   |
| Introduction of Conditional            | Deduction                         | `+IF`  |
| Elimination of Conditional             | Modus Ponens                      | `-IF`  |
| Introduction of Biconditional          |                                   | `+IFF` |
| Elimination of Biconditional           | Converse Conditionals             | `-IFF` |
| Introduction of Conjunction            | Conjunction                       | `+AND` |
| Elimination of Conjunction             | Simplification                    | `-AND` |
| Introduction on Disjunction            | Addition                          | `+OR`  |
| Elimination of Disjunction             | Dilemma                           | `-OR`  |
| Introduction of Negation               | Reductio Ad Absurdum              | `+NOT` |
| Elimination of Negation                |                                   | `-NOT` |
| Explosion                              | Introduction of Arbitrary Formula | `XP`   |
| Repetition                             |                                   | `RP`   |

Informal illustration of how each rule can is applied in a deduction.

**The Rule of Premise**

    ----
    A

where `A` is an arbitrary formula.

**The Rule of Theorem**

    ----
    A

where `A` is a substitution instance of a theorem.

**The Rule of Universal Generalization**
*(Introduction of Universal Quantifier)*

    Fa
    -----
    (x) Fx

**The Rule of Universal Instantiation**
*(Elimination of Universal Quantifier)*

    (x) Fx
    -----
    Fa

**The Rule of Existential Generalization**
*(Introduction of Existential Quantifier)*

    Fa
    -----
    [x] Fx

**The Rule of Existential Instantiation**
*(Elimination of Existential Quantifier)*

    Ex Fx
    -----
    Fa

**The Rule of Deduction**
*(Introduction of Conditional)*

    A
    B
    ------
    A -> B

where `A` is a premise.

**The Rule of Modus Ponens**
*(Elimination of Conditional)*

    A -> B
    A
    ------
    B

**The Rule of Biconditional**
*(Introduction of Biconditional)*

    A -> B
    B -> A
    -------
    A <-> B

**The Rule of Converse Conditionals**
*(Elimination of Biconditional)*

    A <-> B
    -------
    A -> B

or

    A <-> B
    -------
    B -> A

**The Rule of Conjunction**
*(Introduction of Conjunction)*

    A
    B
    -----
    A & B

**The Rule of Simplification**
*(Elimination of Conjunction)*

    A & B
    -----
    A

or

    A & B
    -----
    B

**The Rule of Addition**
*(Introduction of Disjunction)*

    A
    -----
    A | B

or

    A
    -----
    B | A

**The Rule of Dilemma**
*(Elimination of Disjunction)*

    A | B
    A -> C
    B -> C
    ------
    C

**The Rule of Reductio Ad Absurdum**
*(Introduction of Negation)*

    A -> B
    A -> ~B
    -------
    ~A

**The Rule of Double Negation**
*(Elimination of Negation)*

    ~~A
    ---
    A

**The Rule of Explosion**
*(Introduction of Arbitrary Formula)*

    A & ~A
    ------
    B

This is an example of a full deduction which establishes
[modus tollens](https://en.wikipedia.org/wiki/Modus_tollens):

    1) (A -> B) & ~B         : PR;
    2) A -> B                : -AND 1;
    3) A                     : PR;
    4) ~B                    : -AND 1;
    5) A -> ~B               : +IF; 
    6) ~A                    : +NOT 2, 5;
    7) ((A -> B) & ~B) -> ~A : +IF;
