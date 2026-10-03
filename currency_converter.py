from forex_python.converter import CurrencyRates

def convert_currency():
    c = CurrencyRates()

    try:
        amount = float(input("Enter amount: "))    
        from_currency1 = input("From currency (e.g. usd): ").upper()
        to_currency1 = input("To currency (e.g. inr): ").upper()

        result = c.convert(from_currency1, to_currency1, amount)
        print(f"\n💱 {amount} {from_currency1} = {result:.2f} {to_currency1}\n")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    convert_currency()
