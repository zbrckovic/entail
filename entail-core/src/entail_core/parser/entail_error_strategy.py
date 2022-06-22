from antlr4.error.ErrorStrategy import DefaultErrorStrategy


class EntailErrorStrategy(DefaultErrorStrategy):
    """Creates errors with more human-readable messages."""

    @staticmethod
    def _build_missing_token_msg(expectation_text, token_name):
        return f'missing {expectation_text} at {token_name}'

    @staticmethod
    def _build_extraneous_input_msg(expectation_text, token_name):
        return f'extraneous input {token_name} expecting {expectation_text}'

    symbolicNames = [
        "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
        "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
        "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
        "<INVALID>", "string", "the rule of premise", "the rule of theorem",
        "the rule of universal generalization",
        "the rule of universal instantiation",
        "the rule of existential generalization",
        "the rule of existential instantiation",
        "the rule of deduction", "the rule of modus ponens",
        "the rule of biconditional",
        "the rule of converse conditionals",
        "the rule of conjunction", "the rule of simplification",
        "the rule of addition",
        "the rule of dilemma",
        "the rule of reductio ad absurdum", "the rule of double negation",
        "the rule of explosion",
        "proposition",
        "term", "number", "newline", "whitespace", "negation",
        "conjunction", "disjunction", "conditional",
        "biconditional",
        "UNKNOWN"
    ]
    """User friendly names for error reporting."""

    def reportUnwantedToken(self, recognizer):
        self._report_missing_or_unwanted_token(
            recognizer,
            self._build_extraneous_input_msg)

    def reportMissingToken(self, recognizer):
        self._report_missing_or_unwanted_token(
            recognizer,
            self._build_missing_token_msg)

    def _report_missing_or_unwanted_token(self, recognizer, message_builder):
        if self.inErrorRecoveryMode(recognizer):
            return

        self.beginErrorCondition(recognizer)
        token = recognizer.getCurrentToken()
        token_name = self.getTokenErrorDisplay(token)

        expectation_text = self.getExpectedTokens(recognizer) \
            .toString(recognizer.literalNames, self.symbolicNames)

        msg = message_builder(expectation_text, token_name)

        recognizer.notifyErrorListeners(msg, token, None)

    def reportInputMismatch(self, recognizer, e):
        token = e.offendingToken
        token_name = self.getTokenErrorDisplay(token)

        expectation_text = e.getExpectedTokens() \
            .toString(recognizer.literalNames, self.symbolicNames)

        msg = f'mismatched input {token_name} expecting {expectation_text}'

        recognizer.notifyErrorListeners(msg, e.offendingToken, e)
