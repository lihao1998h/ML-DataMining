"""
数据探索性分析 EDA_Base.py
输入：数据文件
输出：df_train,df_test
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st


def get_data(path='', data_type='csv', header=0, names=None, nrows=None, sep=' '):
    """
    get_data函数作用：
    读取数据
    参考链接：https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html?highlight=read_csv
    
    参数：
    path：读取文件的路径
    data_type：读取文件的类型
    header：指定哪一行作为列名，若为None则通过names指定，0为默认值，数字表示行数
    names：指定列名，如['a1','a2']
    nrows：指定要读取的行数，None表示无限制
    dtype：数据字段压缩的操作，将字段类型根据取值空间进行修改，压缩内存使用需求。
    sep：分隔符

    例子：若file名为'taxiGps20190531.csv'
    df = get_data('taxiGps20190531.csv')
    """
    if data_type == 'csv':
        df = pd.read_csv(path, header=header, names=names, nrows=nrows)
    if data_type == 'xlsx':
        df = pd.read_excel(path, header=header, names=names, nrows=nrows)
    if data_type == 'arff':
        # 读取arff文件
        from scipy.io import arff
        data, meta = arff.loadarff(path)
        df = pd.DataFrame(data)
    if data_type == 'tsv':
        # tsv文件
        df = pd.read_csv(path, sep='|')
    return df


# def get_more_data():
#     # 多文件读取
#     from tqdm import tqdm
#     df_all = []
#     for file in tqdm(os.listdir(path)):
#         file_path = os.path.join(path, file)
#         df = pd.read_csv(file_path)
#         df_all.append(df)
#
#     bike_track = pd.concat([
#         pd.read_csv(PATH + 'gxdc_gj20201221.csv'),
#         pd.read_csv(PATH + 'gxdc_gj20201222.csv'),
#         pd.read_csv(PATH + 'gxdc_gj20201223.csv'),
#         pd.read_csv(PATH + 'gxdc_gj20201224.csv'),
#         pd.read_csv(PATH + 'gxdc_gj20201225.csv')
#
#     ])


def reduce_mem_usage(df):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.        
    """
    start_mem = df.memory_usage().sum() / 1024 ** 2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))

    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024 ** 2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    return df


# def df_to_h5(df):
#     # 从df转向hdf5，可以加快读取速度
#     df.to_hdf('train_test.h5', '1.0')
#     df = pd.read_hdf('train_test.h5', '1.0')


# 按照单车ID和时间进行排序
# def sort(df, col=[]):
#     bike_track = bike_track.sort_values(['BICYCLE_ID', 'LOCATING_TIME'])
#     taxigps2019 = taxigps2019[taxigps2019.columns[::-1]]
#     taxigps2019.sort_values(by=['CARNO', 'GPS_TIME'], inplace=True)
#     taxigps2019.reset_index(inplace=True, drop=True)


def one_key_EDA(df, output_name):
    # 一键生成EDA
    import pandas_profiling
    pfr = pandas_profiling.ProfileReport(df)
    pfr.to_file(output_name)


def easy_look(df):
    columns = df.columns.values.tolist()  # 获取所有的变量名
    print('变量列表：', columns)
    print('随机给几个样本')
    df.sample(10)
    print('连续变量的一些描述信息，如基本统计量、分布等。')
    df.describe()
    print('分类变量的一些描述信息。')
    df.describe(include=['O'])
    print('重复值统计（todo）')
    is_dup = False
    # idsUnique = len(set(train.Id)) # train['Id'].nunique()
    # idsTotal = train.shape[0]
    # idsDupli = idsTotal - idsUnique
    # print("There are " + str(idsDupli) + " duplicate IDs for " + str(idsTotal) + " total entries")
    # df.duplicated()

    print('缺失值统计')
    ### 需要注意的是有些缺失值可能已经被处理过，可以用下条语句进行替换
    # Train_data['notRepairedDamage'].replace('-', np.nan, inplace=True)
    #
    # credit.isnull().sum()/float(len(credit))
    #
    #
    # bar(todo)
    # missing = train.isnull().sum()
    # missing = missing[missing > 0]
    # missing.sort_values(inplace=True)
    # missing.plot.bar()
    #
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum() / df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    print(missing_data)
    # for col in df.columns:
    #     print(col, df[col].isnull().sum())
    #
    # df_train.isnull().sum().max()# final check
    is_missing = False
    return is_dup, is_missing


def single_variable_EDA(df, label, job):
    # 数字变量和字符变量分开处理
    y = df[label]
    numeric_features = df.select_dtypes(include=[np.number])
    categorical_features = df.select_dtypes(include=[np.object])
    if job == 'category':
        categorical_features.drop(label, axis=1)
        print('分类label分析')
        print(label + "的特征分布如下：")
        print("{}特征有个{}不同的值".format(label, df[label].nunique()))
        print(df[label].value_counts())
    else:
        numeric_features.drop(label, axis=1)
        print('回归label分析')
        print(label + "的特征分布如下：")
        print("{}特征有个{}不同的值".format(label, df[label].nunique()))
        print(df[label].value_counts())

    print('分类特征分析')
    for cat_fea in categorical_features:
        print(cat_fea + "的特征分布如下：")
        print("{}特征有个{}不同的值".format(cat_fea, df[cat_fea].nunique()))
        print(df[cat_fea].value_counts())
        # 箱图（分类变量）
        # var = 'region'
        # data = pd.concat([df['price'], df[var]], axis=1)
        # f, ax = plt.subplots(figsize=(8, 6))
        # fig = sns.boxplot(x=var, y="price", data=data)
        # # fig.axis(ymin=0, ymax=800000);

    print('数字特征分析')
    for num_fea in numeric_features:
        print(num_fea + "的特征分布如下：")
        print('异常值outlier(todo)')

        print('分布和偏态情况(todo)')
        print('{:15}'.format(num_fea),
              '偏度Skewness: {:05.2f}'.format(df[num_fea].skew()),
              '   ',
              '散度Kurtosis: {:06.2f}'.format(df[num_fea].kurt())
              )
        # if skew()
        skew = True
        plt.figure(1)
        plt.title('kdeplot')
        sns.kdeplot(df[num_fea], shade=True)
        plt.figure(2)
        plt.title('Johnson SU')
        sns.distplot(df[num_fea], kde=False, fit=st.johnsonsu)
        plt.figure(3)
        plt.title('Normal')
        sns.distplot(df[num_fea], kde=False, fit=st.norm)
        plt.figure(4)
        plt.title('Log Normal')
        sns.distplot(df[num_fea], kde=False, fit=st.lognorm)
        plt.figure(5)
        res = st.probplot(df[num_fea], plot=plt)


## 4.8 查看具体频数直方图
# plt.hist(Train_data['price'], orientation = 'vertical',histtype = 'bar', color ='red')
# plt.show()


# 5. 多变量探索
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd


## 5.1 列表groupby玩法

def groupby_cnt_ratio(df, col):
    # 单变量聚合
    if isinstance(col, str):
        col = [col]
    key = ['is_train'] + col

    # groupby function
    cnt_stat = df.groupby(key).size().to_frame('count')
    ratio_stat = (cnt_stat / cnt_stat.groupby(['is_train']).sum()).rename(
        columns={'count': 'count_ratio'})
    return pd.merge(cnt_stat, ratio_stat, on=key, how='outer').sort_values(by=['count'], ascending=False)


# df_train[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# #count/sum/mean/median/std/var/min/max/first/last
# def groupby_cnt_ratio(df, col=[]):
#     if isinstance(col, str):
#         col = [col]
#     key = ['is_train', 'buyer_country_id'] + col
#
#     # groupby function
#     cnt_stat = df.groupby(key).size().to_frame('count')
#     ratio_stat = (cnt_stat / cnt_stat.groupby(['is_train', 'buyer_country_id']).sum()).rename(columns={'count':'count_ratio'})
#     return pd.merge(cnt_stat, ratio_stat, on=key, how='outer').sort_values(by=['count'], ascending=False)
## 5.2 相关性分析
# price_numeric = Train_data[numeric_features]
# correlation = price_numeric.corr()
# print(correlation['price'].sort_values(ascending = False),'\n')

## 5.5 作图
# def plot(X,y,X_cols,y_col,plot_type='scatter'):
#     #scatter:散点图，pairplot:sns.pairplot，box：箱图，hist：直方图，heatmap：相关分析，热度图，list:列表汇总
#     if plot_type=='scatter':
#         # 散点图（num+num）
#         data = pd.concat([X, y], axis=1)
#         data.plot.scatter(x=X_cols, y=y_col);
#     if plot_type=='pairplot':
#         #sns.pairplot
#         sns.set()
#         columns = ['price', 'v_12', 'v_8' , 'v_0', 'power', 'v_5',  'v_2', 'v_6', 'v_1', 'v_14']
#         sns.pairplot(Train_data[columns],size = 2 ,kind ='scatter',diag_kind='kde')
#         """
#         参数：
#         size=2.5表示大小，
#         aspect=0.8表示，
#         kind='reg'添加拟合直线和95%置信区间 'scatter'表示散点图
#         """
#         plt.show();
#     if plot_type=='box':
#         # 箱图（num+clas）
#         var = 'region'
#         data = pd.concat([df[y_col], df[var]], axis=1)
#         f, ax = plt.subplots(figsize=(8, 6))
#         fig = sns.boxplot(x=var, y=y_col, data=data)
#         # fig.axis(ymin=0, ymax=800000);
#     if plot_type=='hist':
#         # 对比，直方图
#         g = sns.FacetGrid(train_df, col='Survived') # row='Pclass', size=2.2, aspect=1.6
#         g.map(plt.hist, 'Age', bins=20)
#     if plot_type=='heatmap':
#         # 相关分析，热度图heatmaps1
#         corrmat = df_train.corr()
#         f, ax = plt.subplots(figsize=(12, 9))
#         sns.heatmap(corrmat, vmax=.8, square=True);
#         # 选出和目标变量最相关的k个变量
#         k = 10 #number of variables for heatmap
#         cols = corrmat.nlargest(k, 'SalePrice')['SalePrice'].index
#         cm = np.corrcoef(df_train[cols].values.T)
#         sns.set(font_scale=1.25)
#         hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
#         plt.show()
#     if plot_type=='list':
#         # 列表汇总（分类变量+数字变量）
#         train_df[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)

## 5.3 动图制作
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
#
# import matplotlib.pyplot as plt
# from matplotlib import animation


def barlist(n):
    taxiorder2019 = pd.read_csv(paths[n], nrows=None,
                                dtype={
                                    'GETON_LONGITUDE': np.float32,
                                    'GETON_LATITUDE': np.float32,
                                    'GETOFF_LONGITUDE': np.float32,
                                    'GETOFF_LATITUDE': np.float32,
                                    'PASS_MILE': np.float16,
                                    'NOPASS_MILE': np.float16,
                                    'WAITING_TIME': np.float16
                                })

    taxiorder2019['GETON_DATE'] = pd.to_datetime(taxiorder2019['GETON_DATE'])
    taxiorder2019['GETON_Hour'] = taxiorder2019['GETON_DATE'].dt.hour

    return taxiorder2019.groupby(['GETON_Hour'])['PASS_MILE'].mean().values


# fig=plt.figure()
#
# paths = glob.glob('../input/taxiOrder20190*.csv')
# paths.sort()
# n = len(paths) #Number of frames
# x = range(24)
# barcollection = plt.bar(x,barlist(0))
# plt.ylim(0, 8)

def animate(i):
    print(i)
    y = barlist(i + 1)
    for idx, b in enumerate(barcollection):
        b.set_height(y[idx])
    plt.ylim(0, 8)

    print(i + 1)
    plt.title(paths[i + 1].split('/')[-1])
    plt.ylabel('PASS_MILE / KM')
    plt.xlabel('Hour')

# anim=animation.FuncAnimation(fig,animate,repeat=False,blit=False,frames=n-1,
#                              interval=500)
#
# anim.save('order.gif', dpi=150)
