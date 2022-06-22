from unittest import TestCase

from entail_core.deduction.ind_var_dependency_graph import \
    IndVarDependencyGraph, CycleInducingDependencyException, \
    IndVarAlreadyRegisteredAsDependentException
from entail_core.formula.variables import IndVar


class TestIndVarDependencyGraph(TestCase):
    def test_raises_individual_variable_already_registered(self):
        graph = self.graph([('a', set())])

        with self.assertRaisesRegex(
                IndVarAlreadyRegisteredAsDependentException,
                'Individual variable a already registered as dependent'):
            graph.add_dependencies(IndVar('a'), [IndVar('b')], )

    def test_raises_cycle_inducing_dependency_reflexive(self):
        graph = IndVarDependencyGraph()

        with self.assertRaisesRegex(CycleInducingDependencyException,
                                    f'Dependency a -> a causes a cycle in graph'):
            graph.add_dependencies(IndVar('a'), {IndVar('a')})

    def test_raises_cycle_inducing_dependency_direct(self):
        graph = self.graph([('a', {'b'})])

        with self.assertRaisesRegex(
                CycleInducingDependencyException,
                f'Dependency b -> a causes a cycle in graph'):
            graph.add_dependencies(IndVar('b'), {IndVar('a')})

    def test_raises_cycle_inducing_dependency_transitive(self):
        graph = self.graph([
            ('a', {'b'}),
            ('b', {'c'})
        ])

        with self.assertRaisesRegex(
                CycleInducingDependencyException,
                f'Dependency c -> a causes a cycle in graph'):
            graph.add_dependencies(IndVar('c'), {IndVar('a')})

    def test_addition(self):
        graph = IndVarDependencyGraph()
        graph.add_dependencies(IndVar('a'), {IndVar('b'), IndVar('c')})
        graph.add_dependencies(IndVar('c'), {IndVar('d')})

        expected = self.graph([
            ('a', {'b', 'c'}),
            ('c', {'d'})
        ])

        self.assertEqual(graph, expected)

    def test_normalization(self):
        for p in self.generate_normalization_cases():
            actual, expected, dependent, dependency, _ = p
            actual.add_dependencies(dependent, {dependency})

            self.assertEqual(actual, expected)

    def generate_normalization_cases(self):
        yield (
            self.graph([('a', {'b', 'c'})]),
            self.graph([
                ('a', {'b'}),
                ('b', {'c'})
            ]),
            IndVar('b'),
            IndVar('c'),
            (IndVar('a'), IndVar('c'))
        )

    @staticmethod
    def graph(raw=None):
        if raw is None:
            raw = []

        graph_map = dict()

        for dependent_raw, dependencies_raw in raw:
            dependent = IndVar(dependent_raw)
            dependencies = {IndVar(ind_var) for ind_var in dependencies_raw}
            graph_map[dependent] = dependencies

        return IndVarDependencyGraph(graph_map)
