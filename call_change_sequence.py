
import itertools
import named_rows
import numpy as np

class RowScorer(object):
    def __init__( self, bells ):
        self.bells = bells
    
    def row_to_score( self, row ):
        return 0

    def rows_to_scores( self, rows ):
        for row in rows:
            yield self.row_to_score( row )

class BasicScorer(RowScorer):
    def __init__( self, bells ):
        self.bells = bells
        self.scored_changes = [
            ( bells*5, ( named_rows.Queens(bells), named_rows.Kings(bells), named_rows.Tittums(bells), named_rows.Backrounds(bells) ) )
            ]

    
    def row_to_score(self,  row ):
        for (score, changes) in self.scored_changes:
            if row in changes:
                return score

        run_score = np.sum( (np.abs( np.diff( row ) ) - 1) < 0.5 )
        if run_score < 2:
            return 0
        return run_score

def adjacent_changes( start_change ):
    for swap_start in range(len(start_change)-1):
        new_list = list(start_change)
        new_list[swap_start],new_list[swap_start+1] = new_list[swap_start+1],new_list[swap_start]
        yield tuple(new_list)

def change_between( change, start_change, end_change, bells):
    for bell1 in range(1, bells+1):
        for bell2 in range(1, bells+1):
            if bell1 != bell2:
                if ( start_change.index(bell1) < start_change.index(bell2) ) == ( end_change.index(bell1) < end_change.index(bell2) ):
                    if ( start_change.index(bell1) < start_change.index(bell2) ) != ( change.index(bell1) < change.index(bell2) ):
                        return False
    return True

def best_sequence( bells, change_list, start_change=None, scorer=None ):
    if start_change == None:
        start_change = named_rows.Rounds(bells)
    if scorer == None:
        scorer = BasicScorer(bells)
    
    if type(change_list) != list:
        change_list = [ change_list ]

    score = 0
    changes = []

    current_change = start_change
    for end_change in change_list:
        routes = change_route( current_change, end_change, score, [ current_change ], scorer)
        best_route = max( routes, key=lambda x: x[0] )
        score = best_route[0]
        changes.extend( best_route[1] )
        current_change = end_change

    return (score, changes)


def change_route( start_change, end_change, starting_score, visited, scorer ):

    sub_routes = []

    if (start_change == end_change):
        return ( starting_score, visited )

#    print 'Start: ', start_change, 'End: ', end_change, 'Visited: ', visited

    current_change = start_change
    for next_change in adjacent_changes( start_change ):
        if next_change in visited:
#            print next_change, ' eliminated because previously visited'
            continue

        if not change_between(next_change, start_change, end_change, len(start_change)):
#            print next_change, ' eliminated because not on the route'
            continue

        if next_change == end_change:
            sub_routes.append( (starting_score, visited + [ end_change ])  )
#            print next_change, ' end of the road'
            continue

        new_visited = list(visited)
        new_visited.append( next_change )
        new_routes = change_route( next_change, end_change, starting_score + scorer.row_to_score( next_change ), new_visited, scorer)
        if new_routes != None:
#            print next_change, ' generates new routes ', new_routes
            sub_routes.extend( new_routes )

#    print 'Routes == ', sub_routes

    return sub_routes
        

        

