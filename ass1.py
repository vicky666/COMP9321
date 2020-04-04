import ast
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

studentid = os.path.basename(sys.modules[__name__].__file__)

#The pandas version I used was '0.24.2'
import re
import numpy as np


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))
    if other is not None:
        print(question, other)
    if output_df is not None:
        print(output_df.head(5).to_string())


def question_1(movies, credits):
    """
    :param movies: the path for the movie.csv file
    :param credits: the path for the credits.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    df_credits = pd.read_csv('credits.csv')
    df_movies = pd.read_csv('movies.csv')
    df1 = pd.merge(df_credits, df_movies, how='inner', on='id')
    
    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    df2 = pd.DataFrame(df1, columns = [ 'id', 'title', 'popularity', 'cast', 'crew', 'budget', 'genres', 'original_language', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'vote_average', 'vote_count'])

    log("QUESTION 2", output_df=df2, other=(len(df2.columns), sorted(df2.columns)))
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    df3 = df2.set_index('id')

    log("QUESTION 3", output_df=df3, other=df3.index.name)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    df4 = df3[df3['budget'] != 0]

    log("QUESTION 4", output_df=df4, other=(df4['budget'].min(), df4['budget'].max(), df4['budget'].mean()))
    return df4


def question_5(df4):
    """
    :param df4: the dataframe created in question 4
    :return: df5
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    df5 = df4.eval('success_impact = (revenue-budget)/budget')

    log("QUESTION 5", output_df=df5,
        other=(df5['success_impact'].min(), df5['success_impact'].max(), df5['success_impact'].mean()))
    return df5


def question_6(df5):
    """
    :param df5: the dataframe created in question 5
    :return: df6
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    MAX_df6= df5.loc[:,"popularity"].max()
    MIN_df6 = df5.loc[:,"popularity"].min()

    tem_df6 = df5["popularity"].apply(lambda x: (x - MIN_df6) / (MAX_df6 - MIN_df6)*100)

    df6 = df5.drop("popularity", axis=1)
    df6["popularity"] = tem_df6

    log("QUESTION 6", output_df=df6, other=(df6['popularity'].min(), df6['popularity'].max(), df6['popularity'].mean()))
    return df6


def question_7(df6):
    """
    :param df6: the dataframe created in question 6
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    df7 = df6
    df7['popularity'] = df7['popularity'].fillna(0).astype('int16')

    log("QUESTION 7", output_df=df7, other=df7['popularity'].dtype)
    return df7


def question_8(df7):
    """
    :param df7: the dataframe created in question 7
    :return: df8
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    df8 = df7
    df8['cast'] = df7['cast'].str.replace("\"","\'").astype(str)
    df8['cast'] = df8['cast'].map( lambda x: re.findall(r'(?<=\'character\': \').+?(?=\,)', str(x)))
    df8['cast'] = df8['cast'].map(lambda x: sorted(x))
    df8['cast'] = df8['cast'].astype(str)
    df8['cast'] = df8['cast'].str.replace("\"","").astype(str)
    df8['cast'] = df8['cast'].str.replace("\',",",").astype(str)
    df8['cast'] = df8['cast'].str.replace("\[","").astype(str)
    df8['cast'] = df8['cast'].str.replace("\]","").astype(str)
    df8['cast'] = df8['cast'].str.replace("\ '","").astype(str)

    log("QUESTION 8", output_df=df8, other=df8["cast"].head(10).values)
    return df8


def question_9(df8):
    """
    :param df9: the dataframe created in question 8
    :return: movies
            Data Type: List of strings (movie titles)
            Please read the assignment specs to know how to create the output
    """

    df9 = df8
    df9['comma'] = df9['cast'].map( lambda x: re.findall(r'\,', str(x)))
    df9['comma'] = df9['comma'].astype(str)
    df9['count'] = df9['comma'].map(lambda x:len(str(x)))
    df9['count'] = df9['count'].astype('int')
    tem_df9 = df9[['title','count']]
    tem_df9 = tem_df9.reindex(tem_df9['count'].sort_values(ascending=False).index)
    tem_df9 = tem_df9.head(10)
    df9 = df9.drop('comma',axis=1)
    df9 = df9.drop('count',axis=1)
    movies = tem_df9['title'].values.tolist()

    log("QUESTION 9", output_df=None, other=movies)
    return movies


def question_10(df8):
    """
    :param df8: the dataframe created in question 8
    :return: df10
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    
    df10 = df8
    df10['year'] = df10['release_date'].map( lambda x: x[-4:])
    df10['month'] = df10['release_date'].map( lambda x: x[-7:-5])
    df10['day'] = df10['release_date'].map( lambda x: x[:-8])
    df10 = df10.sort_values(by=['year', 'month','day'], ascending=(False, False,False))
    df10 = df10.drop('year',axis=1)
    df10 = df10.drop('month',axis=1)
    df10 = df10.drop('day',axis=1)

    log("QUESTION 10", output_df=df10, other=df10["release_date"].head(5).to_string().replace("\n", " "))
    return df10


def question_11(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """
    plt.clf()
    df11 = df10
    df11['tem_g'] = df11['genres'].str.replace("\"","\'").astype(str)
    df11['tem_g'] = df11['tem_g'].map(lambda x: re.findall(r'(?<=\'name\': \').+?(?=\')', str(x)))
    df11['tem_g'] = df11['tem_g'].astype(str)
    df11['tem_g'] = df11['tem_g'].str.replace("\'","").astype(str)
    df11['tem_g'] = df11['tem_g'].str.replace("\[","").astype(str)
    df11['tem_g'] = df11['tem_g'].str.replace("\]","").astype(str)
    df11_string = df11['tem_g'].to_string().replace("\n", " ")
    df11_string1 = re.findall(r'(?<!\S)\w+(?!\S)',df11_string)
    df11_string1 = df11_string1[1:]
    df11_list = []
    for i in range(len(df11_string1)):
        if df11_string1[i].isdigit() == False:
            df11_list.append(df11_string1[i])

    df11_dict = {}
    for key in df11_list:
        df11_dict[key] = df11_dict.get(key, 0) + 1
    df11_dict2 = sorted(df11_dict.items(), key=lambda item:item[1])
    #Take out the four smallest keys in the dictionary,And calculate their sum
    df11_dict3 = df11_dict2[0:4]
    a = 0
    for i in range(4):
        a += df11_dict3[i][1]
    #Delete the four smallest keys from the original dictionary
    for i in range(4):
        df11_dict.pop(df11_dict3[i][0])
    df11_dict['other genres'] = a
    key_list = []
    value_list = []
    size = []
    for key in df11_dict:
        key_list.append(key)        
        value_list.append(df11_dict[key])
    total = sum(value_list)
    for i in value_list:
        result = i/total
        size.append(result)
        plt.plot(size)

    color=['orange','red','pink','blue','purple']
    plt.pie(x=size,labels=key_list,colors=color,autopct='%3.1f%%',pctdistance=1.2,labeldistance=1.4)

    plt.savefig("{}-Q11.png".format(studentid))


def question_12(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """
    plt.clf()
    df12 = df10
    df12['country'] = df12['production_countries'].str.replace("\"","\'").astype(str)
    df12['country'] = df12['country'].map(lambda x: re.findall(r'(?<=\'name\': \').+?(?=\')', str(x)))
    df12['country'] = df12['country'].astype(str)
    df12['country'] = df12['country'].str.replace("\[","").astype(str)
    df12['country'] = df12['country'].str.replace("\]","").astype(str)
    df12['country'] = df12['country'].str.replace("\ ",".").astype(str)
    df12_string = df12['country'].to_string().replace("\n", " ")
    df12_string2 = re.sub("[\d]","  ",df12_string)
    df12_list = re.findall(r'\'\S*?\'',df12_string2)
    df12_string3 = ','.join(df12_list)
    df12_string4 = ''
    for i in range(len(df12_string3)):
        if df12_string3[i]!='.':
            if df12_string3[i] != "'":
                df12_string4 += df12_string3[i]
            else:
                df12_string4 += ""
        else:
            df12_string4 += " "
    df12_list2 = df12_string4.split(',')
    df12_list2 = sorted(df12_list2,key= lambda i:i[0])
    df12_dic={}
    for key in df12_list2:
        df12_dic[key] = df12_dic.get(key, 0) + 1
    fig2 = plt.figure(2,figsize=(10,6))
    for a,b in df12_dic.items():
        plt.text(a,b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    x_axis = tuple(df12_dic.keys())
    y_axis = tuple(df12_dic.values())
    plt.bar(x_axis, y_axis, color='rgb') 
    plt.xticks(rotation='vertical')
    plt.xticks(fontsize=8)
    plt.title("Production Country") 
    #plt.show()

    plt.savefig("{}-Q12.png".format(studentid))


def question_13(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """
    plt.clf()
    df13 = df10
    df13_array = np.array(df13['original_language'])
    df13_list=df13_array.tolist()
    
    #Gets all scatter names
    df13_list1 = []
    for i in range(len(df13_list)):
        if df13_list[i] not in df13_list1:
            df13_list1.append(df13_list[i])
            
    df13['original_language'] = df13['original_language'].astype(str)
    fig1 = plt.figure(1,figsize=(10,6))
    colors = ['b','g','r','orange','blueviolet','brown','gold','goldenrod','gray','green','tan','teal','thistle','tomato','turquoise','violet','skyblue','purple','pink']
    for i in range(len(df13_list1)):
        success_impact = df13.loc[df13['original_language'] == df13_list1[i]]['success_impact']
        vote_average = df13.loc[df13['original_language'] == df13_list1[i]]['vote_average'] 
        plt.scatter(x = vote_average,y = success_impact, c=colors[i], cmap='brg', s=50, alpha=1, marker='8', linewidth=0)
    ax = fig1.gca()

    #len(df13_list1)
    x_min = df13['vote_average'].min()
    x_max = df13['vote_average'].max()
    y_min = df13['success_impact'].min()
    y_max = df13['success_impact'].max()
    plt.xlabel('vote_average')
    plt.ylabel('success_impact')
    plt.title("vote_average vs. success_impact")
    handles,labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels = df13_list1, loc='right')

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("movies.csv", "credits.csv")
    df2 = question_2(df1)
    df3 = question_3(df2)
    df4 = question_4(df3)
    df5 = question_5(df4)
    df6 = question_6(df5)
    df7 = question_7(df6)
    df8 = question_8(df7)
    movies = question_9(df8)
    df10 = question_10(df8)
    question_11(df10)
    question_12(df10)
    question_13(df10)
