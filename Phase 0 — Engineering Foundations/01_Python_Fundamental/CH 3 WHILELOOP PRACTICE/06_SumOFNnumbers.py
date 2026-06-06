# Prompt the user for input
n = int(input("Enter a positive integer (N): "))

# Initialize variables
current_number = 1
sum_of_numbers = 0

# Use a while loop to calculate the sum
while current_number <= n:
    sum_of_numbers += current_number
    current_number += 1

# Display the result
print(f"The sum of the first {n} natural numbers is: {sum_of_numbers}")

