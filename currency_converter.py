def convert_currency(amount, exchange_rate):
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    return amount * exchange_rate


amount = float(input("Enter amount: "))
exchange_rate = float(input("Enter exchange rate: "))

try:
    converted_amount = convert_currency(amount, exchange_rate)
    print(f"Converted amount: {converted_amount:.2f}")
except ValueError as error:
    print(f"Error: {error}")
