import os
import sys
import pandas as pd

def main():
    if len(sys.argv) != 5:
        print("Invalid number of parameters")
        exit(1)

    elif not os.path.isfile(sys.argv[1]):
        print(f"{sys.argv[1]} don't exist")
        exit(1)

    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"{sys.argv[1]} is not csv")
        exit(1)

    else:
        data_2, data_1 = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[1])
        column = len(data_1.columns.values)

        if column < 3:
            print("Less than 3 columns")
            exit(1)

        for i in range(1, column):
            pd.to_numeric(data_2.iloc[:, i], errors='coerce')
            data_2.iloc[:, i].fillna((data_2.iloc[:, i].mean()), inplace=True)

        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("Invalid inputs in weights array")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("Invalid inputs in impact array")
                exit(1)

        if column != len(weights)+1 or column != len(impact)+1:
            print("Number of inputs in weights, impact array and number of columns are not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("Output file is not csv")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])

        e_dist_p_score(data_1, data_2, column, weights, impact)

def weighted_normalized_decision_matrix(data_1, column, weights):
    for i in range(1, column):
        root_sum_square = 0
        for j in range(len(data_1)):
            root_sum_square = root_sum_square + data_1.iloc[j, i]**2
        root_sum_square = root_sum_square**0.5
        for j in range(len(data_1)):
            data_1.iat[j, i] = (data_1.iloc[j, i] / root_sum_square)*weights[i-1]
    return data_1

def ideal_best_worst_values(data_1, column, impact):
    ideal_best = (data_1.max().values)[1:]
    ideal_worst = (data_1.min().values)[1:]
    for i in range(1, column):
        if impact[i-1] == '-':
            ideal_best[i-1], ideal_worst[i-1] = ideal_worst[i-1], ideal_best[i-1]
    return ideal_best, ideal_worst

def e_dist_p_score(data_1, data_2, column, weights, impact):
    data_1 = weighted_normalized_decision_matrix(data_1, column, weights)
    ideal_best, ideal_worst = ideal_best_worst_values(data_1, column, impact)

    topsis_score = []
    for i in range(len(data_1)):
        best_score, worst_score = 0, 0
        for j in range(1, column):
            best_score = best_score + (ideal_best[j-1] - data_1.iloc[i, j])**2
            worst_score = worst_score + (ideal_worst[j-1] - data_1.iloc[i, j])**2
        best_score, worst_score = best_score**0.5, worst_score**0.5
        topsis_score.append(worst_score/(best_score + worst_score))
    data_2['Topsis Score'] = topsis_score
    data_2['Rank'] = (data_2['Topsis Score'].rank(method='max', ascending=False))
    data_2 = data_2.astype({"Rank": int})

    data_2.to_csv(sys.argv[4], index=False)

if __name__ == "__main__":
    main()