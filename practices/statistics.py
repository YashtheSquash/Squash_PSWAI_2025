user_input = input("Enter numbers separated by commas: ")
user_input = user_input.split(',')
numbers = [int(num)for num in user_input]
numbers.sort()

Length = len(numbers)
if Length % 2 == 0:
    median1 = numbers[Length // 2]
    median2 = numbers[Length // 2 - 1]
    median = (median1 + median2) / 2
else:
    median = numbers[Length // 2]


print("The median is:", median) 