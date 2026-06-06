
                                    # FUNCTION IN PYTHON
    # :- Block Of Statement That Perform a Specific Task , Create One time execute any time function help you to reduce code redundancy

    # SYNTAX:-
                # def function_name(name 1 , name 2):
                    # SOME WORK
                    # RETURN VALUE
                # function_name(argument 1 , argument 2)
    # EXAMPLE :-
                # def sum(a ,b)     ( def sum :- Function Definition || (a,b) :- Parameters)
                # s = a +b          ( S :- Are variable to store the parameters value in S)
                # return s          ( S :- Return S variable)
                # print(sum(2,3))   (Print the function with arguments)

    # CALCULATE TWO SUM             (use function name to call any time in code)

a = int(input("Enter Number :-"))
b = int(input("Enter Number2 :-"))

def cal_sum(a,b):
    sum = a+b
    print(sum)
    return sum

cal_sum(a , b)

c = int(input("Enter Number:-"))
d = int(input("Enter Number:-"))
cal_sum(c ,d)

cal_sum(10,15)


def print_name():
    return "Hello"

name = print_name()
for name in range(1 , 6):
    print()



    # topic 2:-

                        # # FUNCTION HAVE A- 2 TYPES
                        # 1- BUILT-IN FUNCTION :-(PRINT() , LEN() , TYPE() , RANGE())
                        # 2- USER DEFINED FUNCTION

    # topic 3:-
                # WHEN A PROGRAMMER CAN ASSIGN A VALUE IN FUNCTION DEFINITION SECTION LIKE(A=1 , B=2) , THAN A FUNCTION CALLING TIME YOU CAN NOT ASSIGN A ARGUMENTS THAN A FUNCTION WILL AUTOMATICALLY ASSUME PARAMETERS NUMBER