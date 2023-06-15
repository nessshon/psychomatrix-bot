from datetime import datetime


class Calculator:

    def __init__(self, date: datetime):
        self.date = date

    def get_birth_numbers(self) -> list[int]:
        return [self.date.day, self.date.month, self.date.year]

    def get_birth_additional_numbers(self) -> list[int]:
        date_to_string = "".join(str(n) for n in self.get_birth_numbers())

        first_numbers = sum(map(int, date_to_string))
        second_numbers = sum(map(int, str(first_numbers)))

        if self.date.year < 2000:
            third_numbers = first_numbers - (2 * int(str(self.date.day)[0]))
            fourth_numbers = sum(map(int, str(third_numbers)))
        else:
            const = 19
            third_numbers = first_numbers + const
            fourth_numbers = sum(map(int, str(third_numbers)))
            third_numbers = int(f"{const}{third_numbers}")

        return [first_numbers, second_numbers, third_numbers, fourth_numbers]

    def get_all_birth_numbers(self) -> list[int]:
        return self.get_birth_numbers() + self.get_birth_additional_numbers()

    def get_numbers(self) -> list[str]:
        numbers = str(self.get_all_birth_numbers())

        square_numbers = [
            ''.join(
                str(num) for _ in range(0, numbers.count(str(num)))
            ) if str(num) in numbers else '-' for num in range(1, 10)
        ]

        return square_numbers

    def get_additional_numbers(self) -> list[str]:
        basic_numbers = self.get_numbers()

        def calculate(index: tuple):
            num = len((basic_numbers[index[0]] +
                       basic_numbers[index[1]] +
                       basic_numbers[index[2]]
                       ).replace('-', ''))

            return str(num) if num > 0 else '-'

        return [calculate((0, 1, 2)), calculate((3, 4, 5)), calculate((6, 7, 8)),
                calculate((2, 4, 6)), calculate((0, 3, 6)),
                calculate((1, 4, 7)), calculate((2, 5, 8)), calculate((0, 4, 8))]

    def get_all_numbers(self) -> list[str]:
        return self.get_numbers() + self.get_additional_numbers()
