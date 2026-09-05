def calculate(a, b, operator):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        if b != 0:
            return a / b
        else:
            raise ValueError("Невозможно разделить на 0.")
    else:
        raise ValueError(
            "Неизвестная операция. Пожалуйста, выберите '+', '-', '*', или '/'."
        )


a = float(input("Введите первое число: "))
b = float(input("Введите второе число: "))
operator = input("Введите операцию (+, -, *, /): ")

result = calculate(a, b, operator)
print(f"Результат: {result}")
