"""Storage for percept facts and Horn-clause rules."""


class KnowledgeBase:
    """Store unique facts and rules of the form premises imply conclusion."""

    def __init__(self):
        self.facts: set[str] = set()
        self.rules: list[tuple[list[str], str]] = []

    def tell_fact(self, fact_string: str):
        """Add a fact to the knowledge base."""
        self.facts.add(fact_string)

    def tell_rule(self, premise_list: list[str], conclusion_string: str):
        """Add a Horn clause as a (premises, conclusion) tuple."""
        self.rules.append((list(premise_list), conclusion_string))

    def clear_facts(self):
        """Clear current percepts while retaining the rules."""
        self.facts.clear()
