import pandas as pd
data = pd.read_table('dataset.txt',encoding='gbk',sep=' ')

#数据概况
data_des = data.describe(include="all")
print(data_des)

#异常值处理==============================================================================
#缺失值处理---------------

#isCrime列中值为2的数用众数进行替换
data['isCrime'] =data['isCrime'].replace(2,data['isCrime'].mode()[0])


#删除掉data中Default字段为空的行。
#对sex、maritalStatus、threeVerify、idVerify和education字段，将缺失值全部填充为未知。
data.dropna(subset=['Default'],inplace=True)
filling_columns=['sex','maritalStatus','threeVerify','idVerify','education']
for column in filling_columns:
    data[column].fillna('未知',inplace=True)

#异常值处理----------------
# 将网上消费笔数为0时的网上消费金额皆修改为0，去除负数
data1=data['onlineTransCnt']==0
data.loc[data1,'onlineTransAmt']=0

# s大于27000万异常值去除
data = data[data["onlineTransAmt"]>2.0e+07][['onlineTransAmt','onlineTransCnt']]

# 将公共事业缴费笔数为0时的公共事业缴费金额皆修改为0（直接在原始数据上进行修改）
data1=data['publicPayCnt']==0
data.loc[data1,'publicPayAmt']=0

# 从data中筛选总消费笔数小于6000的值，赋值给data
data =data[data["transTotalCnt"]<6.0e+03]


#编码映射=================================================================
#maritalStatus：未知映射为0，未婚映射为1，已婚映射为2
# maritalStatus：未知映射为0，未婚映射为1，已婚映射为2
# education：未知映射为0，小学映射为1，初中映射为2，高中映射为3，本科以上映射为4
# idVerify：未知映射为0，一致映射为1，不一致映射为2
# threeVerify：未知映射为0，一致映射为1，不一致映射为2
# netLength：无效映射为0，0-6个月映射为1，6-12个月映射为2，12-24个月映射为3，24个月以上映射为4
# sex：未知映射为0，男映射为1，女映射为2
# CityId：一线城市为1，二线城市为1，其它映射为3

data["maritalStatus"] = data["maritalStatus"].map({"未知":0,"未婚":1,"已婚":2})
data['education']= data["education"].map({'未知':0,'小学':1,'初中':2,'高中':3,'本科以上':4})
data['idVerify']= data["idVerify"].map({"未知":0,"一致":1,"不一致":2})
data['threeVerify']= data['threeVerify'].map({"未知":0,"一致":1,"不一致":2})
data["netLength"] = data["netLength"].map({"无效":0,"0-6个月":1,"12-24个月":2,'24个月以上':4})
data["sex"] = data["sex"].map({"未知":0,"男":1,"女":2})
data["CityId"] = data["CityId"].map({"一线城市":0,"二线城市":1,"其它":2})

#婚姻状况、教育程度、身份验证、三要素验证、民族、在网时长、性别和城市级别按顺序进行One-Hot编码
data =pd.get_dummies(data,columns=['maritalStatus'])
data =pd.get_dummies(data,columns=['education'])
data =pd.get_dummies(data,columns=['idVerify'])
data =pd.get_dummies(data,columns=['threeVerify'])
data =pd.get_dummies(data,columns=['netLength'])
data =pd.get_dummies(data,columns=['sex'])
data =pd.get_dummies(data,columns=['CityId'])

