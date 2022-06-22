import textwrap

negation = textwrap.dedent("""\
    **Negation**
    
    `~A` is true if and only if `A` is false. 
    `~A` corresponds to the phrase "Not A" or "It is not the case that A".
    """)
conditional = textwrap.dedent("""\
    **Conditional**
    
    `A -> B` is `false` if and only if `A` is false and `B` is true.
    `A -> B` corresponds to the phrase "If A, then B.".
    """)
conjunction = textwrap.dedent("""\
    **Conjunction**
    
    `A & B` is true if and only if both `A` and `B` are true.
    `A & B` corresponds to the phrase "A and B".
    """)
disjunction = textwrap.dedent("""\
    **Disjunction**
    
    `A | B` is false if and only if both `A` and `B` are false.
    `A | B` corresponds to the phrase "A or B (or both)"
    """)
biconditional = textwrap.dedent("""\
    **Biconditional**
    
    `A <-> B` is true if and only if `A` and `B` are both `true` or both 
    `false` (they have the same truth value).
    `A <-> B` corresponds to the phrase "A if and only if B".
    """)

rule_of_premise = textwrap.dedent("""\
    **The Rule of Premise**

    ```

    ----
    A
    ```

    where `A` is an arbitrary formula.

    Short description of the rule of premise.
    """)

rule_of_theorem = textwrap.dedent("""\
    **The Rule of Theorem**

    ```

    ----
    A
    ``` 

    where `A` is a substitution instance of a theorem.

    Short description of the rule of theorem.
    """)

rule_of_universal_generalization = textwrap.dedent("""\
    **The Rule of Universal Generalization**

    *(Introduction of Universal Quantifier)*

    ```
    Fa
    -----
    (x) Fx
    ```

    Short description of the rule of universal generalization.
    """)

rule_of_universal_instantiation = textwrap.dedent("""\
    **The Rule of Universal Instantiation**

    *(Elimination of Universal Quantifier)*

    ```
    (x) Fx
    -----
    Fa
    ```

    Short description of the rule of universal instantiation.
    """)

rule_of_existential_generalization = textwrap.dedent("""\
    **The Rule of Existential Generalization**

    *(Introduction of Existential Quantifier)*

    ```
    Fa
    -----
    [x] Fx
    ```

    Short description of the rule of existential generalization.
    """)

rule_of_existential_instantiation = textwrap.dedent("""\
    **The Rule of Existential Instantiation**

    *(Elimination of Existential Quantifier)*

    ```
    Ex Fx
    -----
    Fa
    ```

    Short description of the rule of existential instantiation.
    """)

rule_of_deduction = textwrap.dedent("""\
    **The Rule of Deduction**

    *(Introduction of Conditional)*

    ```
    A
    B
    ------
    A -> B
    ```

    where `A` is a premise.

    Short description of the rule of deduction.
    """)

rule_of_modus_ponens = textwrap.dedent("""\
    **The Rule of Modus Ponens**

    *(Elimination of Conditional)*

    ```
    A -> B
    A
    ------
    B
    ```

    Short description of the rule of modus ponens.
    """)

rule_of_biconditional = textwrap.dedent("""\
    **The Rule of Biconditional**

    *(Introduction of Biconditional)*

    ```
    A -> B
    B -> A
    -------
    A <-> B
    ```

    Short description of the rule of biconditional.
    """)

rule_of_converse_conditionals = textwrap.dedent("""\
    **The Rule of Converse Conditionals**

    *(Elimination of Biconditional)*

    ```
    A <-> B
    -------
    A -> B
    ```

    or

    ```
    A <-> B
    -------
    B -> A
    ```

    Short description of the rule of converse conditionals.
    """)

rule_of_conjunction = textwrap.dedent("""\
    **The Rule of Conjunction**

    *(Introduction of Conjunction)*

    ```
    A
    B
    -----
    A & B
    ```

    Short description of the rule of conjunction.
    """)

rule_of_simplification = textwrap.dedent("""\
    **The Rule of Simplification**

    *(Elimination of Conjunction)*

    ```
    A & B
    -----
    A
    ```

    or

    ```
    A & B
    -----
    B
    ```

    Short description of the rule of simplification.
    """)

rule_of_addition = textwrap.dedent("""\
    **The Rule of Addition**

    *(Introduction of Disjunction)*

    ```
    A
    -----
    A | B
    ```

    or

    ```
    A
    -----
    B | A
    ```

    Short description of the rule of addition.
    """)

rule_of_dilemma = textwrap.dedent("""\
    **The Rule of Dilemma**

    *(Elimination of Disjunction)*

    ```
    A | B
    A -> C
    B -> C
    ------
    C
    ```

    Short description of the rule of dilemma.
    """)

rule_of_reductio_ad_absurdum = textwrap.dedent("""\
    **The Rule of Reductio Ad Absurdum**

    *(Introduction of Negation)*

    ```
    A -> B
    A -> ~B
    -------
    ~A
    ```

    Short description of the rule of reductio ad absurdum.
    """)

rule_of_double_negation = textwrap.dedent("""\
    **The Rule of Double Negation**

    *(Elimination of Negation)*

    ```
    ~~A
    ---
    A
    ```

    Short description of the rule of double negation.
    """)

rule_of_explosion = textwrap.dedent("""\
    **The Rule of Explosion**

    *(Introduction of Arbitrary Formula)*

    ```
    A & ~A
    ------
    B
    ```

    Short description of the rule of explosion.
    """)
