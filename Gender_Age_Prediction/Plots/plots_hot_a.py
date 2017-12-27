import matplotlib.pyplot as plt

y_1=[27.2,26.9,26.9,27,25.3,28.2,29.45,30.5,28.31,28.76,29.6,29.2,29] #Fill the accuracies. y_log=[58.38,69.56,...]
#y_2=[-i for i in range(13)]   #For next classifier. y_2=[70.67,34.56,..].


num_sets=13 #Change num_of_feature_subsets accordingly

my_tick=['Grp'+str(i+1) for i in range(num_sets)] #As strings... write the feature subsets. 
#I don't think it'll fit in one plot... if so... write the feature subsets in the report
#above the plots

x_axis=[i+1 for i in range(len(my_tick))]

plt.xticks(x_axis,my_tick)

plt.plot(x_axis,y_1,linestyle='--', marker='o', color='b',label='Logistic Regression')
#plt.plot(x_axis,y_2,linestyle='--', marker='o', color='r',label='Decision Tree')
#Add accordingly... for each CLASSIFIER

dataset='Hotel Reviews' #Change it accordingly
topic='Age' 

plt.title('Accuracies of '+topic+' on '+dataset+' Data')

plt.xlabel('Features used')
plt.ylabel('Accuracy')

plt.legend(loc='upper left')
plt.show()