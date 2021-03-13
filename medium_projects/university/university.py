import statistics

test_1 = float(input())
test_2 = float(input())
test_3 = float(input())

mean = statistics.mean([test_1, test_2, test_3])
print(mean)
if mean >= 60:
    print('Congratulations, you are accepted!')
else:
    print('We regret to inform you that we will not be able to offer you admission.')