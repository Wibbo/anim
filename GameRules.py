class GameRules:
    """
    The GameRules class defines rule-sets for how cells reproduce. New rules can be added
    by adding a new rule_x function to this class and providing required logic.
    """

    def __init__(self, rows, cols, cell_array, neighbour_array, count_array):
        """
        The constructor for the GameRules class.
        :param rows: The number of rows in the application grid.
        :param cols: The number of columns in the application grid.
        :param cell_array: An array that represents the current status of cells within the grid.
        :param neighbour_array: An array that represents the 8 possible
        neighbouring cells of each element of the application grid.
        """
        self.rule_number = 0
        self.rows = rows
        self.cols = cols
        self.cell_array = cell_array
        self.neighbour_array = neighbour_array
        self.count_array = count_array

    def rule_selector(self, rule_num):
        """
        Returns a rule-set function based on the rule number that is supplied.
        :param rule_num: A number representing the required rule-set (rule_x function).
        """
        self.rule_number = rule_num
        rule_name = 'rule_' + str(self.rule_number)
        rule = getattr(self, rule_name, lambda: 0)
        return rule()

    def rule_1(self):
        """
        Rule-set number 1.
        :return: Nothing.
        """
        # Loop through the entire grid and update each cell.
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                # Process the living cells.
                if self.cell_array[row][col] == 1:
                    if self.neighbour_array[row][col] < 2:
                        self.cell_array[row][col] = 0
                    if self.neighbour_array[row][col] >= 4:
                        self.cell_array[row][col] = 0
                    if self.neighbour_array[row][col] == 3:
                        self.cell_array[row][col] = 1
                    if self.neighbour_array[row][col] == 2:
                        self.cell_array[row][col] = 1
                # Process the dead cells.
                if self.cell_array[row][col] == 0:
                    if self.neighbour_array[row][col] == 3:
                        self.cell_array[row][col] = 1

                if self.cell_array[row][col] == 1:
                    self.count_array[row][col] += 1

    def rule_2(self):
        """
        Rule-set number 2.
        :return: Nothing.
        """
        # Loop through the entire grid and update each cell.
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                # Process the living cells.
                if self.cell_array[row][col] == 1:
                    if self.neighbour_array[row][col] < 2:
                        self.cell_array[row][col] = 0
                    if self.neighbour_array[row][col] >= 4:
                        self.cell_array[row][col] = 0
                    if self.neighbour_array[row][col] == 3:
                        self.cell_array[row][col] = 1
                    if self.neighbour_array[row][col] == 2:
                        self.cell_array[row][col] = 1
                # Process the dead cells.
                if self.cell_array[row][col] == 0:
                    if self.neighbour_array[row][col] == 3 or self.neighbour_array[row][col] == 6:
                        self.cell_array[row][col] = 1

                if self.cell_array[row][col] == 1:
                    self.count_array[row][col] += 1

    def rule_3(self):
        """
        Rule-set number 3.
        :return: Nothing.
        """
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                # Process the living cells.
                if self.cell_array[row][col] == 1:
                    if self.neighbour_array[row][col] < 1 or self.neighbour_array[row][col] > 5:
                        self.cell_array[row][col] = 0
                    else:
                        self.cell_array[row][col] = 1
                # Process the dead cells.
                if self.cell_array[row][col] == 0:
                    if self.neighbour_array[row][col] == 3:
                        self.cell_array[row][col] = 1
                    if self.neighbour_array[row][col] == 6:
                        self.cell_array[row][col] = 1

                if self.cell_array[row][col] == 1:
                    self.count_array[row][col] += 1
