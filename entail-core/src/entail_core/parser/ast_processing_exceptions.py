from entail_core.substitution import DuplicatePredVarException


class ASTProcessingException(Exception):
    """Exception which can happen during the processing of AST."""

    def __init__(self, ctx, msg=None):
        super().__init__(msg)

        self.ctx = ctx
        """AST - the point where problem was found."""


class UnexpectedLineNumberException(ASTProcessingException):
    """When a line number in the deduction is out of order."""

    def __init__(self, ctx, line_number, expected_line_number, msg=None):
        if msg is None:
            msg = f'found line number {line_number} while ' \
                  f'{expected_line_number} was expected'

        super().__init__(ctx, msg)

        self.line_number = line_number
        """Line number which occurred in the deduction."""

        self.expected_line_number = expected_line_number
        """Expected line number for that line."""


class DependencyLineNumberOutOfRangeException(ASTProcessingException):
    """When a rule of inference refers to lines which previously did not
    occur in the deduction."""

    def __init__(self, ctx, index, line_number, msg=None):
        if msg is None:
            msg = 'dependency line number out of range'

        self.index = index
        """Index of the offending dependency."""

        self.line_number = line_number

        super().__init__(ctx, msg)

    @property
    def token(self):
        return self.ctx.lineNumbers[self.index]


class DuplicateDependencyException(ASTProcessingException):
    """When a rule of inference refers two times to the same line."""

    def __init__(self, ctx, index1, index2, line_number, msg=None):
        if msg is None:
            msg = f'duplicate dependency {line_number}'

        super().__init__(ctx, msg)

        self.index1 = index1
        """Index of the first occurrence of line number."""

        self.index2 = index2
        """Index of the duplicate occurrence of line number."""

        self.line_number = line_number

    @property
    def token1(self):
        return self.ctx.lineNumbers[self.index1]

    @property
    def token2(self):
        return self.ctx.lineNumbers[self.index2]


class InvalidDependencyPremisesException(ASTProcessingException):
    """When dependencies for a rule of inference include lines which do not
    belong to the same branch of the deduction."""

    def __init__(
            self, ctx,
            line_number, premises,
            dependency_line_number, dependency_premises, msg=None):
        if msg is None:
            msg = f'dependency  {dependency_premises} not a subset ' \
                  f'of premises currently in force {premises}'
        self.line_number = line_number
        self.premises = premises
        self.dependency_line_number = dependency_line_number
        self.dependency_premises = dependency_premises

        super().__init__(ctx, msg)

    @property
    def offending_premises(self):
        return self.dependency_premises - self.premises


class PremiseEliminationException(ASTProcessingException):
    """When a rule of inference which eliminates a premise is used, but there
    are no premises in force at that line."""

    def __init__(self, ctx, msg=None):
        if msg is None:
            msg = f'eliminating premise when no premise is in force'
        super().__init__(ctx, msg)


class RuleArityException(ASTProcessingException):
    """When rule of inference is used with incorrect number of dependencies."""

    def __init__(self, ctx, rule, arity, msg=None):
        if msg is None:
            msg = 'invalid rule arity'

        super().__init__(ctx, f'{rule.name}: {msg}')

        self.rule = rule
        self.arity = arity


class DuplicatePredVarInSubstitutionException(ASTProcessingException):
    """When the same predicate variable is specified multiple times in the
    substitution."""

    def __init__(self, ctx, cause: DuplicatePredVarException):
        self.cause = cause

        super().__init__(ctx, f'predicate variable {self.cause.pred_var} '
                              f'occurs multiple times in the substitution.')
