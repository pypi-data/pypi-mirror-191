## Function Design

需要实现的功能：
1. calculate_best_randomstate(): return  score_matrix, bestrandoms; // 找出最高的randomstate，返回得分矩阵和randomstate;
2. cut_head_score_matrix_list(): return score_matrix_head; //根据得分矩阵, 输出排名前n的randomstate
3. learning_curve_by_score_matrix_head(): return model_*i[randomstate]; //根据排名前n的randomstate/score_matrix, 求出i个模型， 并输出i个学习率曲线和3d模型
4. return_nice_model(): return model; //根据randomstate求出模型，输出模型得分(All R Square, MSE, RMSE, Max Error)，返回模型对象
5. 绘制3D图，三视图也输出，共四张
6. 绘制2D图，对比同一供应商下不同粒径的模型，x为VF%，Y为TC，同表中不同线为粒径
7. 绘制2D图，对比同一粒径下不同供应商的模型。


## calculate_best_randomstate(degree, algo, x, y, times):
找出最高的randomstate，返回得分矩阵和

参数解析：
- degree: 模型的维度/最高次方/升维指数
- algo: 使用的算法，从sklearn中导入
- x,y: 数据集合输入输出的划分
- times: 最大Randomstate指数, 训练次数

返回参数: return  score_matrix, bestrandoms
- score_matrix: 本次训练所有的分数以及对应的randomstate
- bestrandoms: 在times次循环训练中，得分最高的randomstate


## cut_head_score_matrix_list(score_matrix, top)
根据得分矩阵, 输出排名前n的randomstate
参数解析：
- score_matrix: 从calculate_best_randomstate()返回得到
- top: 输出排在前面的得分

返回参数：return score_matrix_head
- score_matrix_head：排在前top的radomstate以及对应的分数



## learning_curve_by_score_matrix_head()


## return_nice_model(degree, algo, x, y, bestrandoms)
根据randomstate求出模型，输出模型得分(All R Square, MSE, RMSE, Max Error)，返回模型对象

参数解析：
- degree: 模型的维度/最高次方/升维指数
- algo: 使用的算法，从sklearn中导入
- x,y: 数据集合输入输出的划分
- bestrandoms: 得分最高的Randomstate指数, 从calculate_best_randomstate()返回得到

返回参数: 