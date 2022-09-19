##

########################################## LIST COMPREHENSION EXAMPLES #################################


lst: list = []
for x in range(1,4):
    lst.append([x]*4)

# Output: [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
#######################################################


######################### 1 ############################

n_list: list = [       [x for y in range(3)]  # runs SECOND
                   for x in range(5)          # runs FIRST
                ]                     
# Output: [[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]]
#####################################################

               
######################### 2 ############################

a: list = ['Москва', '15000', 'Уфа', '1200', 'Самара', '1090', 'Казань', '1300']
lst: list = [  [a[x-1]] + [int(a[x])]
                for x in range(1, len(a), 2) ]

# Output: [['Москва', 15000], ['Уфа', 1200], ['Самара', 1090], ['Казань', 1300]]
####################################################################


######################### 3 ############################
matrix = [[1,2],[11,12,13,14],[21,22,23,24]]
bb = [ x
        for row in matrix   # runs FIRST
            for x in row    # runs SECOND
    ]
# Output: [1, 2, 11, 12, 13, 14, 21, 22, 23, 24]
#####################################################


######################### 4 ############################
a: list = [ [x,y]
            for x in range(2)           # runs FIRST
                for y in range(3,7)   ]  # runs SECOND
            
# Output: [[0, 3], [0, 4], [0, 5], [0, 6], [1, 3], [1, 4], [1, 5], [1, 6]]
##############################################################################################



######################### 5 ############################
A = [[1, 2, 11], [12, 13, 14], [21, 22, 23]]
A = [       [row[i] for row in A]       # runs SECOND    
        for i in range(len(A[0]))    ]   # runs FIRST            
            
# Output: [[1, 12, 21], [2, 13, 22], [11, 14, 23]]
####################################################################################



######################### 6 ############################
B = [1, 2, 3, 4, 5, 6, 7, 8, 9]
B = [       [B[y] for y in range(x, x+int(len(B)**0.5)) ]   # run second
        for x in range(0, len(B), int(len(B)**0.5))         # run first
    ]
# Output: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
####################################################################################