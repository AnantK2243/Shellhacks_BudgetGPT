import openai as ai

ai_key = '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'
ai.api_key = ai_key

def aiResponse(query):
    response = ai.Completion.create(
        engine = "text-davinci-002",
        prompt = query,
        max_tokens = 300,
        n = 1,
        stop = None,
    )
    return response.choices[0].text.strip()

class BudgetApp:
    def __init__(self):
        self.income = 0.0
        self.expenses = []

    def add_income(self, amount):
        self.income += amount

    def add_expense(self, name, amount):
        self.expenses.append({'name': name, 'amount': amount})

    def calculate_balance(self):
        total_expenses = sum(item['amount'] for item in self.expenses)
        balance = self.income - total_expenses
        return balance

    def display_budget_summary(self):
        print("Budget Summary")
        print("---------------")
        print(f"Income: ${self.income:.2f}")
        print("Expenses:")
        for expense in self.expenses:
            print(f" - {expense['name']}: ${expense['amount']:.2f}")
        print(f"Balance: ${self.calculate_balance():.2f}")

    def get_recommendation(self):
        balance = self.calculate_balance()

        print("You can ask the AI how to spend or invest your money.")
        print("If you would like to learn how to invest, simply type invest.")
        print("If you have any goals in mind, ask, \"My goal is to, ...\"\n")

        question = input("What is your question for the AI: ")
        if "invest" in question.lower():
            response = aiResponse("What is the best method to invest $" + str(balance))
        elif "goal" in question.lower():
            response = aiResponse(question + ". How would I reach this goal if I have " + str(balance) + " currently in the bank")
        else:
            response = aiResponse("I have " + str(balance) + " " + question)

        return response

    def get_review(self):
        query = "I earned " + str(self.income) + " and spent money on "
        for expense in self.expenses:
            query += f"{expense['name']}: ${expense['amount']:.2f}, "
        query += " what areas am I overspending on?"
        response = aiResponse(query)
        return response

def main():
    budget_app = BudgetApp()

    while True:
        print("\nBudget App Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Display Budget Summary")
        print("4. Ask the AI")
        print("5. AI Reviews")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            income = float(input("Enter the income amount: "))
            budget_app.add_income(income)
            print("Income added successfully.")
        elif choice == '2':
            name = input("Enter the expense name: ")
            amount = float(input("Enter the expense amount: "))
            budget_app.add_expense(name, amount)
            print("Expense added successfully.")
        elif choice == '3':
            budget_app.display_budget_summary()
        elif choice == '4':
            while True:
                recommendation = budget_app.get_recommendation()
                print(f"Recommendation: {recommendation}")
                if(input("\nDo you have any more questions? (Enter \"no\" to quit): ").lower() == "no"):
                    break
        elif choice == '5':
            review = budget_app.get_review()
            print("Review: " + review)
        elif choice == '6':
            print("Exiting the Budget App.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
