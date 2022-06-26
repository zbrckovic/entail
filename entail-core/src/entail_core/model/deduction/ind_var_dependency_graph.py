from dataclasses import dataclass, field

from entail_core.model.formula.variables import IndVar


@dataclass
class IndVarDependencyGraph:
    """A mapping between individual variable (dependent) and a set of
    individual variables on which it depends (dependencies)."""

    map: dict[IndVar, set[IndVar]] = field(default_factory=dict)

    def __getitem__(self, dependent):
        return self.map[dependent]

    def __setitem__(self, dependent, dependencies=None):
        if dependencies is None:
            dependencies = set()
        self.map[dependent] = dependencies

    def __delitem__(self, dependent):
        del self.map[dependent]

    def __contains__(self, dependent):
        return dependent in self.map

    def has_direct_dependency(self, dependent, dependency):
        dependencies = self.map.get(dependent)

        if dependencies is None:
            return False

        return dependency in dependencies

    def has_dependency(self, dependent, dependency):
        return dependency in self.get_dependencies(dependent)

    def get_dependencies(self, dependent):
        return self._get_dependencies(dependent)

    def _get_dependencies(self, dependent, traversed=None):
        """Finds all direct or transitive dependency individual variables of
        the specified individual variable."""

        if traversed is None:
            traversed = set()

        if dependent in traversed:
            # this shouldn't happen because cyclic dependencies are not allowed
            raise Exception('infinite recursion')

        traversed.add(dependent)

        direct_dependencies = self.map.get(dependent)
        if direct_dependencies is not None:
            for direct_dependency in direct_dependencies:
                yield direct_dependency
                yield from self._get_dependencies(direct_dependency, traversed)

    def get_direct_dependents(self, dependency):
        """Finds all direct dependent individual variables of the specified
        dependency."""

        for dependent, dependencies in self.map.items():
            if dependency in dependencies:
                yield dependent

    def get_dependents(self, dependency):
        return self._get_dependents(dependency)

    def _get_dependents(self, dependency, traversed=None):
        """Finds all direct or transitive dependent variables of the specified
        individual variable."""

        if traversed is None:
            traversed = set()

        if dependency in traversed:
            # This shouldn't happen because cyclic dependencies are not
            # allowed.
            raise Exception('infinite recursion')
        traversed.add(dependency)

        direct_dependents = self.get_direct_dependents(dependency)
        if direct_dependents is not None:
            for direct_dependent in direct_dependents:
                yield direct_dependent
                yield from self._get_dependents(direct_dependent, traversed)

    def normalize(self, dependent, dependency, on_remove=None):
        """Removes direct dependencies which would become redundant if a direct
        dependency between `dependent` and `dependency` was introduced to the
        graph."""

        self._normalize(dependent, dependency, on_remove, True)

    def _normalize(self, dependent, dependency, on_remove=None, is_root=False):
        self._normalize_downwards(dependent, dependency, on_remove, is_root)

        further_dependents = self.get_direct_dependents(dependent)

        for further_dependent in further_dependents:
            self._normalize(further_dependent, dependency, on_remove, False)

    def _normalize_downwards(self, dependent, dependency, on_remove=None,
                             is_root=False):
        """Removes direct dependencies which would become redundant if a direct
        dependency between `dependent` and `dependency` was introduced. It
        looks only downstream from `dependent` i.e. it considers only its
        descendants. Calls `onRemove` whenever dependency is removed."""

        if not is_root and self.has_direct_dependency(dependent, dependency):
            if on_remove is not None:
                on_remove(dependent, dependency)
            self.map.get(dependent).remove(dependency)
            return

        transitive_dependencies = self.map.get(dependency)
        if transitive_dependencies is None:
            return

        for transitive_dependency in transitive_dependencies:
            self._normalize_downwards(dependent, transitive_dependency,
                                      on_remove, False)

    def add_dependencies(self, dependent, dependencies, on_remove=None):
        """Adds a direct dependency between `dependent` and `dependency` and
        normalizes the graph."""

        if dependent in dependencies:
            raise CycleInducingDependencyException(self, dependent, dependent)

        if dependent in self:
            raise IndVarAlreadyRegisteredAsDependentException(dependent)

        for dependency in dependencies:
            if self.has_dependency(dependency, dependent):
                raise CycleInducingDependencyException(self,
                                                       dependent,
                                                       dependency)

        self[dependent] = set()

        for dependency in dependencies:
            self.normalize(dependent, dependency, on_remove)

            if dependent not in self:
                # We deleted all its relations, so it disappeared completely
                # from the graph.
                self[dependent] = set()

            self[dependent].add(dependency)

    def __repr__(self):
        result = ''
        for dependent, dependencies in self.map.items():
            dependencies_str = ', '.join(str(d) for d in dependencies)
            result += f'{dependent} -> {{{dependencies_str}}}\n'
        return result


class CycleInducingDependencyException(Exception):
    """When introducing dependency to the individual variable graph, but this
    dependency which would result in cyclic dependencies."""

    def __init__(self, graph, dependent, dependency):
        self.dependent = dependent
        self.dependency = dependency
        self.graph = graph
        super().__init__(f'Dependency {self.dependent} -> {self.dependency} '
                         f'causes a cycle in graph:\n{graph}')


class IndVarAlreadyRegisteredAsDependentException(Exception):
    """When introducing an individual variable to the individual variable
    graph, but this individual variable has already been registered in it as a
    dependent."""

    def __init__(self, ind_var):
        self.ind_var = ind_var
        super().__init__(f'Individual variable {self.ind_var} already '
                         f'registered as dependent.')
