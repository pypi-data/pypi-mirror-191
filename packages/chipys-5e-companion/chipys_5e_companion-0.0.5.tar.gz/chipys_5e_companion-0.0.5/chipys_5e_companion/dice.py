import random as rng

class Dice:
    """General dice object to collect and run dice formulas 
    """
    def __init__(self):
        pass

    def r(self, in_str="1d20+1", advantage=False):
        """"alias for self.formula()"""
        return self.formula(in_str, advantage)

    def f(self, in_str="1d20+1", advantage=False):
        """"alias for self.formula()"""
        return self.formula(in_str, advantage)

    def formula(self, in_str="1d20+1", advantage=False):
        """Pairs with the Dice class to allow for formula/string dice rolls like
        2d20+5

        Args:
            in_str (String): Dice formula in the #d##+# formula

        Returns:
            int: rolled value of formula
        """
        adv_rolled = False
        int_value = 0
        formula = in_str.split("+")  # | (pipe) separates delimiters
        for element in formula:
            if "d" in element:
                if advantage and not adv_rolled:
                    int_value += self.roll(element, advantage=True)
                    adv_rolled = True
                else:
                    int_value += self.roll(element)
            else:
                int_value += int(element)
        return int_value
    
    def roll(self, dice_string="1d20", advantage=False ):
        """Rolls Dice of #d## format string

        Args:
            dice_string (String): A dice roll string in the #d## format
            advantage (Bool): A toggle indicating if there should be advantage (it'll roll one extra dice and drop lowest)

        Returns:
            int: value the dice rolled 
        """
        # int_value=0
        adv_rolled = False
        dice_rolls = []
        dice_array = dice_string.split("d")
        for i in range(int(dice_array[0])):
            if advantage and not adv_rolled:
                dice_rolls.append(self._roll_value(dice_array[1]))
                adv_rolled = True
            dice_rolls.append(self._roll_value(dice_array[1]))
        
        if advantage:
            dice_rolls.sort()
            lowest_roll_dropped = dice_rolls[1:]
            return sum(lowest_roll_dropped)
        else:
            return sum(dice_rolls)

    def _roll_value(self, sides_to_roll=0):
        """Most basic roll command to generate a random number within the range

        Returns:
            int: face value of this roll
        """
        if not sides_to_roll:
            sides_to_roll = self.sides
        return int(rng.randrange(1,int(sides_to_roll)+1))


if __name__ == "__main__":
    d = Dice()
    print("1d20 ", d.r("1d20"))
    print("1d20+1 ", d.r("1d20+1"))
    print("2d20 ", d.r("2d20"))
    print("2d20 a", d.r("2d20",True))