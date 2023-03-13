from pulp import LpMaximize, LpMinimize, LpProblem, lpSum, LpVariable, PULP_CBC_CMD, value, LpStatus
import pandas as pd
import shutil
import os

### READ DATA ###
files = r"O:/Tech_zoo/candida/3rd sending - photos F. candida tes ends/x_20230227/data" # Image and txt files
data = pd.read_csv(r"O:/Tech_zoo/candida/3rd sending - photos F. candida tes ends/x_20230227/data/statC.txt")
objects = data['objects'].tolist()
imageNames = data['image'].tolist()

### CALCULATE SPLITS ###
def splitObjects(v):
    """
    Take 30% of total number of annotations
    Round to nearest even
    Split in two -> val, test
    Remainder is train
    """
    
    def roundEven(num):
        return round(num / 2) * 2

    valtest = (v/100)*30
    valtest = roundEven(valtest)
    val = valtest/2
    test = val
    train = v - valtest
    return [train, int(val), int(test)]


perfectImageSplit = splitObjects(len(objects))
perfectObjectSplit = splitObjects(sum(objects))

groupNames = ["train", "val", "test"]
print("Perfect image split: ", perfectImageSplit)
print("Perfect object split: ", perfectObjectSplit)


### SET VARIABLES ###
n_object = len(objects)
object_keys = range(n_object)

group_sum_targets = perfectObjectSplit
group_n_objects = perfectImageSplit

n_group = len(group_sum_targets)
group_keys = range(n_group)

problem_name = 'repex'

### SET UP OPTIMIZATION ###
# Seek to minimise absolute deviation from the target sums
prob = LpProblem(problem_name, LpMinimize)

# Primary Decision variables - the assignments
z = LpVariable.dicts('z',
                     indices = [(i, j) for i in object_keys for j in group_keys],
                     cat='Binary')


# Aux. decision variables - the sum of groups
group_sums = LpVariable.dicts('group_sums', indices=group_keys, cat='Continuous')
group_abs_error = LpVariable.dicts('group_abs_error', indices=group_keys, cat='Continuous')

# Objective - assumes all groups evenly penalised for missing
# their target sum, and penalty for 'over' and 'under' have same
# weighting
prob += lpSum([group_abs_error[j] for j in group_keys])

# Constraints on groups
for j in group_keys:
    prob += group_sums[j] == lpSum([z[(i, j)]*objects[i] for i in object_keys])
    prob += group_abs_error[j] >= group_sums[j] - group_sum_targets[j]
    prob += group_abs_error[j] >= group_sum_targets[j] - group_sums[j]

    # Constrain number of objects used
    prob += lpSum([z[(i, j)] for i in object_keys]) == group_n_objects[j]

# Constraints on objects
for i in object_keys:
    # Every object used exactly once
    prob += lpSum([z[(i, j)] for j in group_keys]) == 1


### SOLVE OPTIMIZATION ###
optimization_result = prob.solve(PULP_CBC_CMD(msg=0))

print("Status:", LpStatus[prob.status])
print("Optimal Solution to the problem: ", round(value(prob.objective),2))
print ("Individual decision_variables: ")
for v in prob.variables():
    print(v.name, "=", v.varValue)

# ### SHOW GROUPS ###
extractGroups = [eval(str(i)[2:].replace("_", "")) for i in prob.variables() if str(i).startswith("z") and i.varValue == 1] # eval converts string to tuple
extractGroups = [[imageNames[i[0]], groupNames[i[1]]] for i in extractGroups]
print(extractGroups)

# ### CREATE GROUPS ###
# for g in extractGroups:
#     image = g[0]
#     group = g[1]
#     x = image[0]

#     srcImage = os.path.join(files,x,image+".jpg")
#     srcTxt = os.path.join(files,x,image+".txt")
#     dst = os.path.join(files,group)
#     print(srcImage, " goes to ", dst)
#     print(srcTxt, " goes to ", dst)

#     if not os.path.exists(dst): # Make directory if it doesn't exist
#         os.makedirs(dst)    
#     shutil.copy(srcImage, dst)
#     shutil.copy(srcTxt, dst)

# print("All good")