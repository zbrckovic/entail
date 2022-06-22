from antlr4.Token import CommonToken

from entail_core.antlr.EntailParser import EntailParser
from entail_core.text import Position, Range


def is_rule(rule_name, rule_index):
    return rule_name == EntailParser.ruleNames[rule_index]


def get_token_start_position(token):
    return Position(token.line - 1, token.column)


def get_token_end_position(token: CommonToken):
    return Position(token.line - 1, token.column + len(token.text))


def get_token_range(token):
    start = get_token_start_position(token)
    end = get_token_end_position(token)
    return Range(start, end)


def get_tree_range(tree):
    start = get_token_start_position(tree.start)
    end = get_token_end_position(tree.stop)
    return Range(start, end)


def is_inside_tree(position, tree):
    start_pos = get_token_start_position(tree.start)
    if position < start_pos:
        return False
    end_pos = get_token_end_position(tree.stop)
    if position > end_pos:
        return False
    return True


def is_inside_token(position: Position, token: CommonToken):
    token_range = get_token_range(token)
    return token_range.includes(position)
