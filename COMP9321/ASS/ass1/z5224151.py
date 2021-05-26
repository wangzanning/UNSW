import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np
import math
import re

studentid = os.path.basename(sys.modules[__name__].__file__)


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


def question_1(exposure, countries):
    """
    :param exposure: the path for the exposure.csv file
    :param countries: the path for the Countries.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    exp_df = pd.read_csv(exposure, sep=';', encoding='ISO-8859-1', low_memory=False)
    cou_df = pd.read_csv(countries, encoding='ISO-8859-1', low_memory=False)
    exp_df = exp_df.rename(columns={'country':'Country'})
    # rename the country may have different name in the csv(there may some country, I do not know)
    exp_df['Country'] = exp_df['Country'].replace({'Korea DPR':'North Korea','Korea, North':'North Korea',
                                               'Korea Republic of':'South Korea','Korea, South':'South Korea',
                                                'US':'United States', 'United States of America':'United States',
                                                'Viet Nam':'Vietnam','Cabo Verde':'Cape Verde','Brunei Darussalam':'Brunei'})
    cou_df['Country'] = cou_df['Country'].replace({'Korea DPR':'North Korea','Korea, North':'North Korea',
                                               'Korea Republic of':'South Korea','Korea, South':'South Korea',
                                                'US':'United States', 'United States of America':'United States',
                                                'Viet Nam':'Vietnam','Cabo Verde':'Cape Verde','Brunei Darussalam':'Brunei'})
    df1 = pd.merge(exp_df, cou_df, how='inner', on='Country')
    df1 = df1[df1['Country'].notna()]
    df1.set_index('Country', inplace=True)
    df1 = df1.sort_index()

    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    df2 = df1.copy(True)
    df_country_dict = df2['Cities'].to_dict()
    country_list = df_country_dict.keys()
    res_longitude = []
    res_latitude = []
    for i in country_list:
        cities_dict = df_country_dict[i].split('|||')
        longitude = []
        latitude = []
        for m in cities_dict:
            m = json.loads(m)
            longitude.append(m['Longitude'])
            latitude.append(m['Latitude'])
        res_longitude.append(sum(longitude)/len(longitude))
        res_latitude.append(sum(latitude)/len(latitude))
        # print(cities_dict)
    df2.insert(loc=0,column='avg_longitude',value=res_longitude)
    df2.insert(loc=1,column='avg_latitude',value=res_latitude)
    # print(df2.head())

    #################################################

    log("QUESTION 2", output_df=df2[["avg_latitude", "avg_longitude"]], other=df2.shape)
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    df3 = df2.copy(True)
    def deg_2red(degree):
        return degree * math.pi / 180.00
    # calculate the distance(red) to wuhan
    avg_latitude2_wuhan = deg_2red(df3['avg_latitude'] - 30.5928)
    avg_longitude2_wuhan = deg_2red(df3['avg_longitude'] - 114.3055)
    np_c = np.sin(avg_latitude2_wuhan/2) * np.sin(avg_latitude2_wuhan/2) + np.cos(deg_2red(30.5928)) *\
           np.cos(deg_2red(df3['avg_latitude'])) * np.sin(avg_longitude2_wuhan/2) * np.sin(avg_longitude2_wuhan/2)
    np_distance_2wuhan = 6373 * 2 * np.arctan2(np.sqrt(np_c),np.sqrt(1-np_c))
    df3.insert(loc=0,column='distance_to_Wuhan',value=np_distance_2wuhan)
    df3.sort_values('distance_to_Wuhan', ascending=True, inplace=True)
    #################################################

    log("QUESTION 3", output_df=df3[['distance_to_Wuhan']], other=df3.shape)
    return df3


def question_4(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    df4 = df2.copy(True)
    continents_df = pd.read_csv(continents, encoding='ISO-8859-1', low_memory=False)
    df4 = pd.merge(df4, continents_df, how='inner', on='Country')
    # print(df4.columns)
    df4 = df4.loc[df4['Covid_19_Economic_exposure_index'] != 'x']
    df4 = df4.loc[df4['Covid_19_Economic_exposure_index'] != '']
    df4['Covid_19_Economic_exposure_index'] = df4['Covid_19_Economic_exposure_index'].apply(lambda x: float(x.replace(',','.')))
    df4 = df4.groupby(['Continent']).mean()
    df4.drop('avg_longitude',axis=1, inplace=True)
    df4.drop('avg_latitude',axis=1, inplace=True)
    df4 = df4.rename(columns={'Covid_19_Economic_exposure_index':'average_covid_19_Economic_exposure_index'})
    df4.sort_values('average_covid_19_Economic_exposure_index',ascending=True, inplace=True)
    #################################################
    log("QUESTION 4", output_df=df4, other=df4.shape)
    return df4


def question_5(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df5
            Data Type: dataframe
            Please read the assignment specs to know how to create the output dataframe
    """
    #################################################
    df5 = df2.copy(True)
    df5 = df5.loc[df5['Foreign direct investment'] != 'x']
    df5 = df5.loc[df5['Foreign direct investment'] != '']
    df5 = df5.loc[df5['Foreign direct investment'] != 'No data']
    df5 = df5.loc[df5['Net_ODA_received_perc_of_GNI'] != 'x']
    df5 = df5.loc[df5['Net_ODA_received_perc_of_GNI'] != '']
    df5 = df5.loc[df5['Net_ODA_received_perc_of_GNI'] != 'No data']
    df5['Foreign direct investment'] = df5['Foreign direct investment'].apply(lambda x: float(x.replace(',','.')))
    df5['Net_ODA_received_perc_of_GNI'] = df5['Net_ODA_received_perc_of_GNI'].apply(lambda x: float(x.replace(',','.')))
    df5 = df5.rename(columns={'Income classification according to WB':'Income Class'})
    df5 = df5.groupby(['Income Class']).mean()
    df5.drop('avg_longitude', axis=1, inplace=True)
    df5.drop('avg_latitude', axis=1, inplace=True)
    df5 = df5.rename(columns={'Foreign direct investment':'Avg Foreign direct investment '})
    df5 = df5.rename(columns={'Net_ODA_received_perc_of_GNI':'Avg_ Net_ODA_received_perc_of_GNI'})
    #################################################

    log("QUESTION 5", output_df=df5, other=df5.shape)
    return df5


def question_6(df2):
    """
    :param df2: the dataframe created in question 2
    :return: cities_lst
            Data Type: list
            Please read the assignment specs to know how to create the output dataframe
    """
    cities_lst = []
    #################################################
    df6 = df2.copy(True)
    print(df6.columns)
    lic_country = df6[df6['Income classification according to WB'] == 'LIC'].index
    df_country_dict = df2['Cities'].to_dict()
    temp_dict = {}
    for c in lic_country:
        cities_dict = df_country_dict[c].split('|||')
        for m in cities_dict:
            m = json.loads(m)
            if m['Population'] != None:
                temp_dict[m['City']] = m['Population']
    temp_list = sorted(temp_dict.items(), key=lambda item: item[1], reverse=True)
    temp_list = temp_list[:5]
    for i in temp_list:
        cities_lst.append(i[0])

    #################################################

    log("QUESTION 6", output_df=None, other=cities_lst)
    return cities_lst


def question_7(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    df_country_dict = df2['Cities'].to_dict()
    country_list = df_country_dict.keys()
    city_countries_dict = {}
    for c in country_list:
        cities_dict = df_country_dict[c].split('|||')
        for m in cities_dict:
            m = json.loads(m)
            if m['City'] in city_countries_dict:
                city_countries_dict[m['City']].append(m['Country'])
            else:
                city_countries_dict[m['City']] = [m['Country']]
    new_dict = {}
    for i in city_countries_dict:
        if len(city_countries_dict[i]) >= 2:
            new_dict[i] = city_countries_dict[i]
    df7 = pd.DataFrame(new_dict.items(), columns=['city','countries'])

    #################################################

    log("QUESTION 7", output_df=df7, other=df7.shape)
    return df7


def question_8(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :param continents: the path for the Countries-Continents.csv file
    :return: nothing, but saves the figure on the disk
    """

    #################################################

    continents_df = pd.read_csv(continents, encoding='ISO-8859-1', low_memory=False)
    total_population = 0
    # calculate all over world population
    df_country_dict = df2['Cities'].to_dict()
    for i in continents_df['Country']:
        if i in df_country_dict:
            cities_dict = df_country_dict[i].split('|||')
            for m in cities_dict:
                m = json.loads(m)
                if m['Population'] != None:
                    total_population += m['Population']
    # calculate each country population in South America
    continents_df = continents_df.loc[continents_df['Continent'] == 'South America']
    country_list = continents_df['Country']
    population_list = []
    for c in country_list:
        temp_population = 0
        cities_dict = df_country_dict[c].split('|||')
        for m in cities_dict:
            m = json.loads(m)
            if m['Population'] != None:
                temp_population += m['Population']
        population_list.append(temp_population)
    rate_res = list(map (lambda x: x /total_population, population_list))
    plt.figure(figsize=(12, 4))
    plt.barh(country_list,rate_res)
    plt.title('the percentage of the world population is living in each South American country')
    plt.ylabel('Country Name')
    plt.xlabel('the Percentage of the world population')
    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_9(df2):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    df9 = df2.copy(True)
    df9 = df9.loc[df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI'] != 'x']
    df9 = df9.loc[df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI'] != '']
    df9 = df9.loc[df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI'] != 'No data']
    df9 = df9.loc[df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import'] != 'x']
    df9 = df9.loc[df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import'] != '']
    df9 = df9.loc[df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import'] != 'No data']
    df9 = df9.loc[df9['Foreign direct investment, net inflows percent of GDP'] != 'x']
    df9 = df9.loc[df9['Foreign direct investment, net inflows percent of GDP'] != '']
    df9 = df9.loc[df9['Foreign direct investment, net inflows percent of GDP'] != 'No data']
    df9 = df9.loc[df9['Foreign direct investment'] != 'x']
    df9 = df9.loc[df9['Foreign direct investment'] != '']
    df9 = df9.loc[df9['Foreign direct investment'] != 'No data']
    df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI'] = df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI'].apply(lambda x: float(x.replace(',','.')))
    df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import'] = df9['Covid_19_Economic_exposure_index_Ex_aid_and_FDI_and_food_import'].apply(lambda x: float(x.replace(',','.')))
    df9['Foreign direct investment, net inflows percent of GDP'] = df9['Foreign direct investment, net inflows percent of GDP'].apply(lambda x: float(x.replace(',','.')))
    df9['Foreign direct investment'] = df9['Foreign direct investment'].apply(lambda x: float(x.replace(',','.')))
    df9 = df9.groupby(['Income classification according to WB']).mean()
    df9.drop('avg_longitude', axis=1, inplace=True)
    df9.drop('avg_latitude', axis=1, inplace=True)
    name = list(df9[0:1])
    hic = df9.loc['HIC'].tolist()
    lic = df9.loc['LIC'].tolist()
    mic = df9.loc['MIC'].tolist()
    bar_width = 0.3
    x=np.arange(4)
    plt.tick_params(axis='y', labelsize=6)
    plt.figure(figsize=(12, 5))
    plt.barh(x,lic,bar_width,label='LIC')
    plt.barh(x+bar_width,mic,bar_width,label='MIC')
    plt.barh(x+bar_width*2,hic,bar_width,label='HIC')
    plt.legend()
    plt.yticks(x+bar_width/2,name)
    plt.ylabel('different metrics')
    plt.xlabel('different income level countries')
    plt.title('Q9')
    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_10(df2, continents):
    """
    :param df2: the dataframe created in question 2
    :return: nothing, but saves the figure on the disk
    :param continents: the path for the Countries-Continents.csv file
    """

    #################################################


    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("exposure.csv", "Countries.csv")
    df2 = question_2(df1.copy(True))
    df3 = question_3(df2.copy(True))
    df4 = question_4(df2.copy(True), "Countries-Continents.csv")
    df5 = question_5(df2.copy(True))
    lst = question_6(df2.copy(True))
    df7 = question_7(df2.copy(True))
    question_8(df2.copy(True), "Countries-Continents.csv")
    question_9(df2.copy(True))
    question_10(df2.copy(True), "Countries-Continents.csv")
