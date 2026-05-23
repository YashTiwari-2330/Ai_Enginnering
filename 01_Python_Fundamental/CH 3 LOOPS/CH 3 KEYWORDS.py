# BREAK :- USED TO TERMINATE THE LOOP WHEN ENCOUNTERED

#EXAMPLE :-

i = 1

while i <= 10:
    if i == 5:
        break
    print(i)
    i += 1

# CONTINUE :- TERMINATE EXECUTION IN THE CURRENT ITERATION & CONTINUES EXECUTION OF THE LOOPS WITH THE NEXT ITERATION

#EXAMPLE :-

J = 10

while J >= 1:
    if J == 5:
        J -= 1
        continue
    print(J)
    J -= 1

# PASS :- PASS IS NULL STATEMENT THAT DOES NOTHING . IT IS USED AS A PLACEHOLDER FOR FUTURE CODE

for i in range(10):
    pass

else:
    print("END")
