import matplotlib.pyplot as plt

# 假设有一组坐标数据
# x = [1, 5, 10, 15, 20]
# # y = [23.00, 20.67, 18.67, 10.67, 2.56]
# y=[726.4,1075.3,1005.6,877.2,799.3]

x=[10,20,30,50,100,200,300,400,500]
y=[0,0,6.44,47.80,57.53,62.15,83.96,87.56,91.04]

# 绘制折线图
plt.plot(x, y, marker='o', linestyle='-', color='b', label='data points')

# 设置图表标题和坐标轴标签
plt.title('error & test threads')
plt.xlabel('test_threads_number')
plt.ylabel('error_rate/%')

# 显示图例
plt.legend()

# 显示图表
plt.show()
