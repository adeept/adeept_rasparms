'''
本程序需要放在树莓派中运行
'''
import json
import os

'''
获取该.py文件的绝对路径，以此来找到plan.json
'''
curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath) + "/"

'''
打开plan.json
'''
planJsonFileHere = open(thisPath + 'plan.json', 'r')

'''
读取plan.json的内容
'''
contentPlanGose  = planJsonFileHere.read()

'''
将读取到的内容解码为原有格式
'''
planGoseList = json.loads(contentPlanGose)

'''
此时你可以像使用普通数组一样使用planGoseList
'''
print(planGoseList)


'''
将需要保存的数组转换为json字符串
'''
content2write = json.dumps(planGoseList)

'''
你可以更改newPlans.json的文件名，新建这个文件
'''
file2write = open('newPlan.json', 'w')

'''
在新建的文件内写入json字符串
'''
file2write.write(content2write)

'''
保存并关闭刚才新建的文件
你可以发现文件夹内出现了一个名为newPlan.json的文件
你可以使用上述方法将这个文件导入
'''
file2write.close()