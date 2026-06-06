# FOR LOOP :- WHEN YOU WANT LINE BY LINE CODE EXECUTION , SO YOU GO WITH FOR LOOP A WHILE LOOP ARE EXECUTE WHENEVER CONDITION CAN;T REACH , AND FOR LOOP ARE EXECUTE INDEX LINE BY LINE
# RANGE() :- RANGE FUNCTION RETURNS A SEQUENCE OF NUMBERS, STARTING FROM 0 BY DEFAULT , INCREMENT BY 1 (BY DEFAULT) , AND STOPS BEFORE A SPECIFIED NUMBER.
# RANGE() :- range(start? , stop , step?)


#WHILE LOOP AND FOR LOOP USES :-
                            # WHILE LOOP:- IF YOU HAVE SOME VARIABLE AND YOU DO SOME EDIT ,FUNCTIONS AND YOU GET STOPPING CONDITION SO USE WHILE LOOP
                            # FOR LOOP :- IF YOU TRAVEL ANY DATA TYPES AND HIS VALUE SO YOU GO WITH FOR LOOP
#EX :- FOR LOOP USING LIST

num = [1 , 2 , 3 , 4 , 5]

for val in num:
    print([val])


# EX:-2 FOR LOOP USING TUPLE

tup = (1 , 2 , 3, 4 , 5 , 6 , 7 , 8 , 9)

for i in range(2 , 10 , 2):       # range(2:-starting point , 10:- Ending point , 2:-increment)
    print(i)


#EX3 :- FOR LOOP USING STRING

st = str(input("Enter Any name:-"))

for ch in st:
    print(ch)

else:
    print("End String")