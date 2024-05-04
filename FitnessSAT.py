import random


formula = []



def update_formula(file_name):
    file1 = open(file_name, 'r')
    count = 0
    global formula
    formula = []
    while True:
        count += 1
        line = file1.readline()
        if not line:
            break
        if line[0] == '%':
            break
        if line[0] != 'c' and line[0] != 'p':
            liner = []
            #print("Line{}: {}".format(count, line.strip()))
            liner = line.strip().split(' ')
            #print(liner)
            formula.append(liner[:-1])
    file1.close()


def evaluate_formula(genotype: list):
    evaluation = [None for _ in range(len(formula))]

    for i in range(len(formula)):
        clause = formula[i]
        result = False
        for t in range(len(clause)):
            index = abs(int(clause[t])) - 1
            value = True if genotype[index] == 1 else False
            if int(clause[t]) < 0: 
                value = not value
            result = result or value
        evaluation[i] = result

    fitness = sum([1 if val == True else 0 for val in evaluation])
    return fitness, evaluation


#91 clauses, 20 vars
MAX_FITNESS = 91
update_formula('uf20-04.cnf')

#430 clauses, 100 vars
#file1 = open('uf100-04.cnf', 'r')
#MAX_FITNESS = 430

#1065 clauses, 250 vars
# file1 = open('uf250-032.cnf', 'r')
# MAX_FITNESS = 1065


if __name__ == '__main__':
    pass