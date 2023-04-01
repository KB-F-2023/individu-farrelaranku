from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

V = TypeVar('V')
D = TypeVar('D')

class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...

class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        first: V = unassigned[0]
        
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None
  
class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2
  
    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2]

if __name__ == "__main__":
    variables: List[str] = ["WA",
                            "NA",
                            "SA",
                            "QA",
                            "NSW",
                            "V",
                            "T"]
     
    domains: Dict[str, List[str]] = {}
     
    for variable in variables:
         domains[variable] = ["R", "G", "B"]
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(MapColoringConstraint("WA","NA"))
    csp.add_constraint(MapColoringConstraint("WA","SA"))
    csp.add_constraint(MapColoringConstraint("SA", "NA"))
    csp.add_constraint(MapColoringConstraint("QA", "NA"))
    csp.add_constraint(MapColoringConstraint("QA", "SA"))
    csp.add_constraint(MapColoringConstraint("QA", "NSW"))
    csp.add_constraint(MapColoringConstraint("NSW", "SA"))
    csp.add_constraint(MapColoringConstraint("V", "SA"))
    csp.add_constraint(MapColoringConstraint("V", "NSW"))
    csp.add_constraint(MapColoringConstraint("V", "T"))
    
solution: Optional[Dict[str, str]] = csp.backtracking_search()
if solution is None:
    print("Tidak ada solusi!")
else:
    print('Solusi Yang Memungkinkan :')
    print(solution)
