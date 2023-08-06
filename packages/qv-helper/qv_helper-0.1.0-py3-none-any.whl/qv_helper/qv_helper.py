import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from tabulate import tabulate

def qv_groups(value, group, data, title=None, xlabel=None, ylabel=None, stat=True):
    if title == None:
        title = f'{value} vs {group}'
    if xlabel == None:
        xlabel = value
    if ylabel == None:
        ylabel = group


    fix, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    sns.histplot(x=value, data=data, ax=axes[0]).set(
        title=title, xlabel=xlabel, ylabel='Count'
    )
    sns.boxplot(x=value, y=group, data=data, ax=axes[1]).set(
        title=title, xlabel=xlabel, ylabel=ylabel
    )

    if (data[value].isnull().any() | data[group].isnull().any()):
            data = data.dropna()
            print('Null values are dropped in statistical tests.')
    
    group_list = data[group].unique()
    n_group = len(group_list)

    if n_group == 0:
        raise Exception('Pleaes use a data frame with data inside.')
    elif n_group == 1:
        raise Exception('Please consider using qv_dist in the package when only 1 class is used.')
    elif stat == True:
        if n_group == 2:
            if np.var(data[value]) == 0:
                raise Exception('A t test is not performed as the total variance is 0.')
            else:
                group_a = data[data[group] == group_list[0]]
                group_b = data[data[group] == group_list[0]]
                t_eq, p_eq = stats.ttest_ind(group_a[value], group_b[value])
                t_w, p_w = stats.ttest_ind(group_a[value], group_b[value], equal_var=False)
                table = [['Equal var. assumed', t_eq, p_eq], ['Equal var. not assumed', t_w, p_w]]
                print(tabulate(table, headers=['Test', 't', 'p'], floatfmt=('', '.2f', '.4f')))
        elif n_group > 2:
            vectors = dict()
            for i in group_list:
                vectors[i] = data[data[group] == i][value]
            if (np.array([np.var(i) for i in list(vectors.values())]) == 0).any():
                raise Exception('F statistic is not defined when within group variance is 0 in at least one of the groups.')
            else:
                F, p = stats.f_oneway(*[list(i) for i in vectors.values()])
                table = [['One-way ANOVA', F, p]]
                print(tabulate(table, headers=['Test', 'F', 'p'], floatfmt=('', '.2f', '.4f')))

def qv_scatter(valuex, valuey, data, title=None, xlabel=None, ylabel=None, stat=True):
    if title == None:
        title = f'{valuex} vs {valuey}'
    if xlabel == None:
        xlabel = valuex
    if ylabel == None:
        ylabel = valuey

    plt.figure(figsize=(5,4))
    sns.scatterplot(x=valuex, y=valuey, data=data).set(
        title=title, xlabel=xlabel, ylabel=ylabel
    )

    if (data[valuex].isnull().any() | data[valuey].isnull().any()):
            data = data.dropna()
            print('Null values are dropped in statistical tests.')
    
    r_pearson, p_pearson = stats.pearsonr(data[valuex], data[valuey])
    r_spearman, p_spearman = stats.spearmanr(data[valuex], data[valuey])
    table = [['Pearson\'s r', r_pearson, p_pearson], ['Spearman\'s r', r_spearman, p_spearman]]
    print( tabulate( table, headers=['Test', 'r', 'p'], floatfmt=['', '.4f', '.4f']))

def qv_2cat(groupx, groupy, data, title_heatmap=None, title_bar=None, xlabel=None, ylabel=None, stat=True, cmap='YlGn'):
    if title_heatmap == None:
        title_heatmap = f'{groupx} vs {groupy}'
    if title_bar == None:
        title_bar = f'% of {groupx} by {groupy}'
    if xlabel == None:
        xlabel = groupx
    if ylabel == None:
        ylabel = groupy

    if (data[groupx].isnull().any() | data[groupy].isnull().any()):
        data = data.dropna()
        print('Null values are dropped in statistical tests.')

    fix, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)

    data['dummy']=0 # Creating a dummy column for counting
    table_count = pd.pivot_table(data, index=groupy, columns=groupx, values='dummy', aggfunc='count').fillna(0)

    sns.heatmap(table_count, cmap=cmap, ax=axes[0]).set(
        title=title_heatmap, xlabel=xlabel, ylabel=ylabel
    )

    sums = table_count.sum( axis = 1)
    row_sums = pd.DataFrame() # Creating a dummy data frame for division
    for i in table_count.columns:
        row_sums[i]=sums

    table_prop = table_count.div(row_sums)

    table_prop.plot(kind='bar', stacked=True, ax=axes[1])
    plt.xticks(rotation=0)
    plt.legend(title=xlabel, bbox_to_anchor=(1, 1))
    plt.title(title_bar)
    plt.xlabel(ylabel)
    plt.ylabel('Cumalative %')

    if stat == True:
        if table_count.shape == (2,2):
            chi_result = stats.chi2_contingency(table_count)
            chi, p, df = chi_result.statistic, chi_result.pvalue, chi_result.dof
            bar_result = stats.barnard_exact(table_count)
            wald, bar_p = bar_result.statistic, bar_result.pvalue
            fisher_result = stats.fisher_exact(table_count)
            odds_ratio, fisher_p = fisher_result.statistic, fisher_result.pvalue

            table = [['Chi-squared test', 'Chi-squared', chi, df, p],
                    ['Barnard exact test', 'Wald statistic', wald, '--', bar_p],
                    ['Fisher exact test', 'Prior odds raio', odds_ratio, '--', fisher_p]]
            print(tabulate(table, headers=['Test', 'Test statistic', 'Value', 'df', 'p'], floatfmt=('', '', '.2f', '', '.4f')))
        else:
            chi_result = stats.chi2_contingency(table_count)
            chi, p, df = chi_result.statistic, chi_result.pvalue, chi_result.dof
            table = [['Chi-squared test', 'Chi-squared', chi, df, p]]
            print(tabulate(table, headers=['Test', 'Test statistic', 'Value', 'df', 'p'], floatfmt=('', '', '.2f', '', '.4f')))

def qv_count(value, data, title=None, label=None, stat=True):
    if title == None:
        title = f'Distribution of {value}'
    if label == None:
        label = value

    plt.figure(figsize=(5,4))
    sns.countplot(x=value, data=data).set(
        title=title, xlabel=label, ylabel='Count'
    )

    if data[value].isnull().any():
            print('Null values are dropped in the chart.')
    
    if stat == True:
        counts = data[value].value_counts()
        counts = np.array( [counts.index, counts]).T
        nas = [['NA', data[value].isna().sum()]]
        print( tabulate( np.concatenate((counts, nas)), headers=['Group', 'Count']))

def qv_dist(value, data, title=None, label=None, kde=True, bins='auto', hue=None, stat=True):
    if title == None:
        title = f'Distribution of {value}'
    if label == None:
        label = value

    plt.figure(figsize=(5,4))
    sns.histplot(x=value, data=data, kde=kde, bins=bins, hue=hue).set(
        title=title, xlabel=label, ylabel='Count'
    )

    if data[value].isnull().any():
        data = data.dropna()
        print('Null values are dropped in the chart and statistics.')
    
    mean = np.mean(data[value])
    variance = np.var(data[value])
    n = (~data[value].isna()).sum()
    na = data[value].isna().sum()
    skewness = stats.skew(data[value])
    table = [['Mean', mean], ['Variance', variance], ['Sample size', n], ['# of NAs', na], ['Skewness', skewness]]
    print( tabulate(table, headers=['Statistics', 'Value'], floatfmt='.2f'))

