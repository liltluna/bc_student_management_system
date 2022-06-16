import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def construct():
   pathY = 'labels.csv'
   pathX='features.csv'
   dataX = pd.read_csv(pathX)
   dataY=pd.read_csv(pathY)
   x=dataX[['x']]
   #print(x)
   y=dataY[['y']]
# 生成图像
# 默认风格
   #tx=[]
   #ty=[]
   #for e in x:
    #  tx.append(e*100)
   #for e in y:
    #  ty.append(e*100)   
   plt.style.use('fivethirtyeight')
# 设置布局
   fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize = (8,5))
   fig.autofmt_xdate(rotation = 50)

# 标签值
   ax1.scatter(x, y,s=10)
   ax1.set_xlabel('Live online number')
   ax1.set_ylabel('')
   ax1.set_title('Online head count')

   plt.tight_layout(pad=2)
  
   plt.savefig('sinc.png')
   plt.show()
construct()
