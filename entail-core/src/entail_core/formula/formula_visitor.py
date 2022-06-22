from abc import abstractmethod, ABC


class FormulaVisitor(ABC):
    @abstractmethod
    def visit_compound_formula(self, formula):
        pass

    @abstractmethod
    def visit_quantified_formula(self, formula):
        pass

    @abstractmethod
    def visit_atomic_formula(self, formula):
        pass

    def visit(self, formula):
        return formula.accept(self)
