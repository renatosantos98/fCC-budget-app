class Category:
    def __init__(self, name):
        """Class initialisation: assigns each category object a name, creates an empty list to be used as the ledger, and another empty list to calculate the total balance in each object."""
        self.name = name
        self.ledger = list()
        self.total = list()

    def __str__(self):
        """Definition of the string representation of the objects in the `Category` class."""
        budget_string = f"{self.name:*^30}\n"
        for item in self.ledger:
            budget_string += f"{item['description'][0:23]:23}{item['amount']:>7.2f}\n"
        budget_string += f"Total: " + str(self.get_balance())
        return budget_string

    def deposit(self, amount, description=""):
        """A `deposit` method that accepts an amount and description. If no description is given, it defaults to an empty string. The method appends an object to the ledger list in the form of `{"amount": amount, "description": description}`."""
        self.ledger.append({"amount": amount, "description": description})
        self.total.append(float(amount))

    def withdraw(self, amount, description=""):
        """A `withdraw` method that is similar to the `deposit` method, but the amount passed in is stored in the ledger as a negative number. If there are not enough funds, nothing is added to the ledger. This method returns `True` if the withdrawal took place, and `False` otherwise."""
        if self.check_funds(amount) is True:
            self.ledger.append({"amount": -amount, "description": description})
            self.total.append(float(-amount))
            return True
        else:
            return False

    def get_balance(self):
        """A `get_balance` method that returns the current balance of the budget category based on the deposits and withdrawals that have occurred."""
        return sum(self.total)

    def transfer(self, amount, category):
        """A `transfer` method that accepts an amount and another budget category as arguments. The method adds a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". The method then adds a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". If there are not enough funds, nothing is added to either ledgers. This method returns `True` if the transfer took place, and `False` otherwise."""
        if self.check_funds(amount) is True:
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        else:
            return False

    def check_funds(self, amount):
        """A `check_funds` method that accepts an amount as an argument. It returns `False` if the amount is greater than the balance of the budget category and returns `True` otherwise. This method is used by both the `withdraw` method and `transfer` method."""
        if amount > self.get_balance():
            return False
        else:
            return True


def create_spend_chart(categories):
    """`create_spend_chart` takes a list of categories as an argument and returns a string that is a bar chart. The chart shows the percentage spent in each category passed in to the function as a fraction of all the withdrawals made."""
    chart = "Percentage spent by category\n"
    percent_list = list()
    total_spent = 0

    # Calculate total amount of money spent.
    for category in categories:
        withdraw_amount = -(category.ledger[1]["amount"])
        total_spent += withdraw_amount

    # Calculate the percentage of money spent for each transaction.
    for category in categories:
        withdraw_amount = -(category.ledger[1]["amount"])
        percent_list.append(int((withdraw_amount / total_spent) * 100))

    # Create the graph bars.
    top = 100
    while top >= 0:
        i = 0
        if len(str(top)) < 3:
            while i < (3 - len(str(top))):
                chart += " "
                i += 1
        chart = chart + str(top) + "|"
        i = 0
        while i < len(categories):
            if percent_list[i] >= top:
                chart += " o "
            else:
                chart += "   "
            i += 1
        chart += " \n"
        top -= 10

    # Create the x axis line.
    chart = chart + "    " + ("---" * len(categories)) + "-"

    # Write the category names vertically.
    max_length = 0
    for category in categories:
        if len(category.name) > max_length:
            max_length = len(category.name)
    i = 0
    while i < max_length:
        chart += "\n    "
        for category in categories:
            try:
                chart = chart + " " + category.name[i] + " "
            except:
                chart += "   "
        chart += " "
        i += 1
    return chart
