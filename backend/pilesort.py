from copy import deepcopy
from itertools import permutations
import logging

import pandas as pd

class Pilesort:
    def __init__(self):
        self.freelist = set()
        self.orig_freelist = set()
        self.groupings = list()
        self.dist_matrix = None
        self.logger = logging.getLogger("PilesortLogger")
    
    def add_freelist_item(self, item):
        """
        Add entity to freelist set

        Params:
            self (Pilesort)
            item (str): new item/entity for freelist
        """
        if item in self.freelist:
            self.logger.warning("Item %s already exists in freelist", item)
        self.freelist.add(item)
    
    def remove_freelist_item(self, item):
        """
        Remove entity from freelist set

        Params:
            self (Pilesort)
            item (str): item/entity to remove from freelist
        """
        try:
            self.freelist.remove(item)
        except KeyError:
            self.logger.warning("Item %s does not exist in freelist", item)
    
    def finalize_freelist(self):
        self.orig_freelist = deepcopy(self.freelist)
        self._init_dist_matrix()

    def _init_dist_matrix(self):
        self.dist_matrix = pd.DataFrame(0, columns=list(self.freelist), index=list(self.freelist))
        for item in self.orig_freelist:
            self.dist_matrix[item][item] += 1

    def add_freelist_item_to_grouping(self, grouping, item):
        """
        Add item/entity to grouping.
        At beginning 'grouping' will also be another 'item'
        
        Params:
            self (Pilesort)
            grouping (tuple if self.groupings not empty, str if self.groupings is empty)
        """ 
        try:
            if grouping in self.groupings:
                grouping_index = self.groupings.index(grouping)
                new_grouping = list(grouping)
            else:
                new_grouping = [grouping]
                self.freelist.remove(grouping)
            if isinstance(item, tuple):
                new_grouping.extend(list(item))
            else:
                new_grouping.append(item)
            new_grouping = tuple(new_grouping)
            self.remove_freelist_item(item)
            if isinstance(grouping, tuple):
                new_groups = list(self.groupings[grouping_index])
                del new_groups[grouping_index]
                new_groups[grouping_index] = new_grouping
                self.groupings = new_groups
            else:
                new_groups = []
                new_groups.append(new_grouping)
                self.groupings = new_groups
            self._increment_matrix_pairs()
        except Exception as e:
            raise self.logger.critical("Fatal exception adding item to grouping: %s", e)

    def _increment_matrix_pairs(self):
        for item in self.orig_freelist:
            self.dist_matrix[item][item] += 1   
        for grouping in self.groupings:
            combinations = permutations(grouping)
            for combo in combinations:
                self.dist_matrix[combo[0]][combo[1]] += 1
                #first = combo[0]
                #for item in combo:
                #    if item != first:
                #        self.dist_matrix[first][item] += 1

    def _check_valid_item_to_grouping(self, grouping, item):
        if not self.groupings:
            grouping_is_valid = self._check_item_in_freelist(grouping)
        else:
            grouping_is_valid = self._check_grouping_in_groupings(grouping)
        item_is_valid = self._check_item_in_freelist(item)
        return grouping_is_valid and item_is_valid

    def _check_item_in_freelist(self, item):
        """
        Checks if provided item is in freelist

        Params
            self (Pilesort)
            item (str)
        Returns
            bool
        """
        valid = item in self.freelist
        if not valid:
            self.logger.warning("Invalid item: %s is not in freelist", item)
        return valid

    def _check_grouping_in_groupings(self, grouping):
        """
        Params
            grouping (tuple)
        Returns
            bool
        """
        valid = grouping in self.groupings
        if not valid:
            self.logger.warning("Invalid grouping: %s is not in groupings", grouping)
        return valid

if __name__=='__main__':
    ps = Pilesort()
    ps.add_freelist_item('hello')
    ps.add_freelist_item('howdy')
    ps.add_freelist_item('goodbye')
    ps.finalize_freelist()
    ps.add_freelist_item_to_grouping('hello', 'howdy')