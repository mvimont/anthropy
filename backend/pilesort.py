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
        """
        Once freelist finished,
        generates copy of original
        and initializes distance matrix
        """
        self.orig_freelist = deepcopy(self.freelist)
        self._init_dist_matrix()

    def _init_dist_matrix(self):
        """
        Based on freelist, constructs distance matrix,
        incrementing each identical item by 1
        """
        self.dist_matrix = pd.DataFrame(0, columns=list(self.freelist), index=list(self.freelist))
        for item in self.orig_freelist:
            self.dist_matrix[item][item] += 1

    def add_freelist_item_to_grouping(self, grouping, item):
        """
        Add item/entity to grouping.
        A 'grouping' can also be another 'item'
        
        Params:
            self (Pilesort)
            grouping (tuple if len(freelist) <= 1, else str)
        """
        groupings = list(self.groupings)
        new_group = list()
        if item in groupings:
            if len(self.freelist) >= 1:
                self.logger.warning("Warning: All items must be in a group before multiple groups can be combined")
                return
            groupings.remove(item)
            new_group.extend(item)
        else:
            self.remove_freelist_item(item)
            new_group.append(item)
        if grouping in self.groupings:
            new_group.extend(grouping)
            groupings.remove(grouping)
        else:
            new_group.append(grouping)
            self.remove_freelist_item(grouping)
        groupings.append(tuple(new_group))
        self.groupings = groupings
        self._increment_matrix_pairs()

    def _increment_matrix_pairs(self):
        """
        Increments value of all grouped items
        by one.
        """
        for item in self.orig_freelist:
            self.dist_matrix[item][item] += 1
        for grouping in self.groupings:
            combinations = self._all_possible_pairs(grouping)
            for first, second in combinations:
                self.dist_matrix[first][second] += 1
                self.dist_matrix[second][first] += 1

    def _all_possible_pairs(self, l):
        """
        PARAMS:
            self(Pilesort)
            l: List of items
        RETURNS:
            (list): all possible pairs in list l
        """
        return [(a, b) for idx, a in enumerate(l) for b in l[idx + 1:]]             

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
