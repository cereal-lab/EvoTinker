import sys
import pickle
import numpy
from scipy.stats import mannwhitneyu, shapiro, ttest_ind
import numpy

#f1_name = input('File #1 - name: ')
#f2_name = input('File #2 - name: ')
#f1_name = sys.argv[1]
#f2_name = sys.argv[2]
for i in range(4):
    root = 'Experiments Logs/'
    f1_name = root + 'OnePlusOneGA-with-recombination/'
    f2_name = root + 'OnePlusOneGA-without-recombination/'
    suffix = f'stat{i}.pickle'
    f1_name += suffix
    f2_name += suffix

    with open(f1_name, 'rb') as f:
        series1 = pickle.load(f)
    with open(f2_name, 'rb') as f:
        series2 = pickle.load(f)


    print('-' * 18)
    print(f'STATISTIC #{i}')
    print('-' * 18)
    print('\tSeries 1 -->', f1_name)
    print('\tSeries 2 -->', f2_name)
    print("\tSeries 1 mean =", numpy.mean(series1))
    print("\tSeries 2 mean =", numpy.mean(series2))

    # Performing statistical test
    # see https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/

    stat, p = shapiro(series1)
    print('\tShapiro: \t stat=%10.3f, p=%10.3f \t --> ' % (stat, p), end="")
    if p > 0.05:
        print('Probably Gaussian')
    else:
        print('Probably not Gaussian')

    stat, p = ttest_ind(series1, series2)
    print('\tStudent T: \t stat=%10.3f, p=%10.3f \t --> ' % (stat, p), end="")
    if p > 0.05:
        print('SAME distribution')
    else:
        print('DIFFERENT distributions')

    stat, p = mannwhitneyu(series1, series2)
    print("\tMann-Whitney: \t stat=%10.3f, p=%10.3f \t --> " % (stat, p), end="")
    if p > 0.05:
        #print('H0 not rejected: samples are from SAME distribution')
        print('SAME distribution')
    else:
        #print('H0 rejected: samples are from DIFFERENT distribution')
        print('DIFFERENT distribution')

