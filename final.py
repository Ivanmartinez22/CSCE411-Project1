import pickle
import numpy
user_input = input("Please enter instance file name: ")
print(f"You entered: {user_input}")

with open(user_input, 'rb') as f:
    instance = pickle.load(f)

x_lists = instance.get('x_list')
y_lists = instance.get('y_list')
c_list = instance.get('C_list')
n_list = instance.get('n_list')


class sums_error:
    def __init__(self, xi_sum, yi_sum, xiyi_sum, xi2_sum, yi2_sum, a, b,error, n):
        self.xi_sum = xi_sum
        self.yi_sum = yi_sum
        self.xiyi_sum = xiyi_sum
        self.xi2_sum = xi2_sum
        self.yi2_sum = yi2_sum
        self.a = a
        self.b = b
        self.error = error
        self.n = n



def precalculate_sums_and_error(x_list, y_list):
    n = len(x_list)
    x_list.append(0) # padding 
    y_list.append(0) # padding 
    calculated_sums = sums_error([0] * (n + 1), [0] * (n + 1), [0] * (n + 1), [0] * (n + 1), [0] * (n + 1), [[0]*(n + 1) for _ in range(n + 1)], [[0]*(n + 1) for _ in range(n + 1)], [[0]*(n + 1) for _ in range(n + 1)], n)
    
    for j in range(1, n + 1):
        x, y = x_list[j], y_list[j]
        
        calculated_sums.xi_sum[j] =  (calculated_sums.xi_sum[j-1] + x)
        calculated_sums.yi_sum[j] = (calculated_sums.yi_sum[j-1] + y)
        calculated_sums.xiyi_sum[j] = (calculated_sums.xiyi_sum[j-1] + (x * y))
        calculated_sums.xi2_sum[j] = (calculated_sums.xi2_sum[j-1] + (x * x))
        calculated_sums.yi2_sum[j] = (calculated_sums.yi2_sum[j-1] + (y * y))
        for i in range(1, j + 1):
            n_at_interval = j - i + 1
            xi_sum = calculated_sums.xi_sum[j] - calculated_sums.xi_sum[i - 1]
            yi_sum = calculated_sums.yi_sum[j] - calculated_sums.yi_sum[i - 1]
            xiyi_sum = calculated_sums.xiyi_sum[j] - calculated_sums.xiyi_sum[i - 1]
            xi2_sum = calculated_sums.xi2_sum[j] - calculated_sums.xi2_sum[i - 1]
            yi2_sum = calculated_sums.yi2_sum[j] - calculated_sums.yi2_sum[i - 1]
            
            slope_numerator = n_at_interval * xiyi_sum - (xi_sum * yi_sum)
            slope_denominator = n_at_interval * xi2_sum - (xi_sum * xi_sum)
            if(slope_numerator == 0):
                calculated_sums.a[i][j] = 0
            elif(slope_denominator == 0):
                calculated_sums.a[i][j] = 0
            else:
                calculated_sums.a[i][j] = slope_numerator/slope_denominator
            calculated_sums.b[i][j] = (yi_sum - (calculated_sums.a[i][j] * xi_sum)) / n_at_interval


            calculated_sums.error[i][j] = sum((y_list[k] - calculated_sums.a[i][j] * x_list[k] - calculated_sums.b[i][j]) ** 2 for k in range(i, j + 1))


        
    return calculated_sums


def find_optimal_solution(calculated_sums, C):
    k = 0
    cost = 0
    last_points = []

    minimum_costs = [0 for i in range(calculated_sums.n + 1)]
    optimal_segment = [0 for i in range(calculated_sums.n + 1)]
    minimum = float('inf')
    for j in range(1, calculated_sums.n + 1):
        minimum  = min((calculated_sums.error[i][j] + minimum_costs[i-1], i) for i in range(1, j + 1))
        minimum_costs[j] = minimum [0] + C
        optimal_segment[j] = minimum [1]

    segments = []
    i = calculated_sums.n
    j = optimal_segment[i]
    while i > 0:
        segments.append((i, j))
        i = j - 1
        j = optimal_segment[i]

    cost = minimum_costs[calculated_sums.n]
    
    for seg in reversed(segments):
        i, j = seg

        last_points.append(i)
    k = len(last_points)

    if last_points:
        # Subtract one from the last element to deal with padding 
        last_points[-1] -= 1
    return k, cost, last_points


last_points = []
costs = []
ks = [] 

#loading instances
for i in range(len(x_lists)):
    sums = precalculate_sums_and_error(x_lists[i], y_lists[i])
    ki, ci, lpi =find_optimal_solution(sums, c_list[i])
    last_points.append(lpi)
    costs.append(ci)
    ks.append(ki)

# local testing
with open('examples_of_solutions', 'rb') as f:
    solution = pickle.load(f)

print(ks)

print(last_points)


print(costs)

print("solution: ")
print(solution)


#write output
output = {
    "k_list": ks,
    "last_points": last_points,
    "OPT_list": costs
}

pickle.dump(output, open("output", "wb"))




