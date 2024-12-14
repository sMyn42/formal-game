'''
This file contains a sample in GDL I created to showcase non probabilistic 
'''

class Action:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class Proposition:
    def __init__(self, name, value=True):
        self.name = name
        self.value = value

class GameState:
    def __init__(self):
        self.base = {}
        self.actions = []

    def set_proposition(self, proposition):
        self.base[proposition.name] = proposition

    def get_proposition(self, name):
        return self.base.get(name, Proposition(name, False))

    def update_state(self, next_state):
        self.base = next_state.base.copy()

    def is_terminal(self):
        # Example terminal condition: no blank cells
        return all(
            p.name.startswith("cell") and p.value != "b"
            for p in self.base.values()
        )

class Game:
    def __init__(self):
        self.roles = []
        self.actions = []
        self.initial_state = GameState()
        self.current_state = GameState()
        self.legal_actions = {}

    def add_role(self, role):
        self.roles.append(role)

    def add_base_proposition(self, name, value=True):
        self.initial_state.set_proposition(Proposition(name, value))

    def init_game(self):
        self.current_state.update_state(self.initial_state)

    def compute_legal_actions(self):
        self.legal_actions.clear()
        for role in self.roles:
            self.legal_actions[role] = []
            if self.current_state.get_proposition(f"control({role})").value:
                for x in range(1, 4):
                    for y in range(1, 4):
                        if self.current_state.get_proposition(f"cell({x},{y},b)").value:
                            self.legal_actions[role].append(Action(f"mark({x},{y})", role))
            self.legal_actions[role].append(Action("noop", role))

    def perform_action(self, role, action):
        self.current_state.actions.append((role, action))
        if action.name.startswith("mark"):
            _, coordinates = action.name.split("(")
            x, y = map(int, coordinates.strip(")").split(","))
            self.current_state.set_proposition(Proposition(f"cell({x},{y},{role})", True))

        # Update control alternation
        next_control = "o" if role == "x" else "x"
        self.current_state.set_proposition(Proposition(f"control({role})", False))
        self.current_state.set_proposition(Proposition(f"control({next_control})", True))

    def is_terminal(self):
        return self.current_state.is_terminal()

    def get_goals(self):
        if self.is_terminal():
            # Example goal computation
            x_wins = self.check_line("x")
            o_wins = self.check_line("o")
            if x_wins and not o_wins:
                return {"x": 100, "o": 0}
            elif o_wins and not x_wins:
                return {"x": 0, "o": 100}
            else:
                return {"x": 50, "o": 50}
        return {"x": 0, "o": 0}

    def check_line(self, mark):
        # Check rows, columns, and diagonals
        for i in range(1, 4):
            if all(self.current_state.get_proposition(f"cell({i},{j},{mark})").value for j in range(1, 4)):
                return True
            if all(self.current_state.get_proposition(f"cell({j},{i},{mark})").value for j in range(1, 4)):
                return True
        if all(self.current_state.get_proposition(f"cell({i},{i},{mark})").value for i in range(1, 4)):
            return True
        if all(self.current_state.get_proposition(f"cell({i},{4-i},{mark})").value for i in range(1, 4)):
            return True
        return False

# Example usage:
game = Game()
game.add_role("x")
game.add_role("o")

# Initialize board state
for x in range(1, 4):
    for y in range(1, 4):
        game.add_base_proposition(f"cell({x},{y},b)")
game.add_base_proposition("control(x)")
game.add_base_proposition("control(o)", False)

game.init_game()
game.compute_legal_actions()
