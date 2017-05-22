from collections import namedtuple


class MatchState:

    def __init__(self, previous_match_state):
        self.player_states = {}
        self.time = 0

    def update_positions(self, new_soldier_positions):
        pass

    def spawn_new_soldiers(self, orders):
        pass

    def get_player_visible_area(self, player):
        for soldier in player.soldiers:
            soldier.do()


PlayerState = namedtuple('PlayerState',
                         [
                             'coin',
                             'soldier_positions',
                             'visible_nodes',
                         ])

"""
currently soldier_spawns is just an integer, how many soldiers the player orders to spawn
"""
PlayerOrder = namedtuple('PlayerOrder',
                         [
                             'soldier_orders',
                             'soldier_spawns',
                         ])

SoldierOrder = namedtuple('SoldierOrder',
                          [
                              'soldier_id',
                              'order',
                          ])


def play_round(old_match_state, player_orders):

    new_match_state = MatchState(old_match_state)

    proposed_player_positions = get_proposed_positions_per_player(player_orders, old_match_state)

    resolved_player_positions, player_deaths = resolve_battles(proposed_player_positions)

    new_match_state.update_positions(resolved_player_positions)
    new_match_state.remove_soldiers(player_deaths)
    new_match_state.spawn_new_soldiers(player_orders)

    collect_resources()


    return new_match_state


def get_submitted_orders_from_players():
    return {}


def get_proposed_positions_per_player(player_orders, old_match_state):
    proposed_player_positions = {}
    for player_order in player_orders.items():
        proposed_player_positions[player_order.id] = get_proposed_positions(player_order, old_match_state)
    return proposed_player_positions


def get_proposed_positions(soldier_orders, old_match_state):
    proposed_soldier_positions = {}
    for soldier_id, order in soldier_orders.items():
        if verify_legal_soldier_move(soldier_id, order, old_match_state):
            proposed_soldier_positions[soldier_id] = order
    return proposed_soldier_positions


def verify_legal_soldier_move(soldier_id, order, old_match_state):
    return True


def resolve_battles(proposed_player_positions):
    resolved_player_positions = {}
    player_deaths = {}
    return resolved_player_positions, player_deaths


def battle():
    pass


