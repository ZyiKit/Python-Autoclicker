import matplotlib.pyplot as plt

x = [1,3,5,10]
#plt.plot(x)


y = [7,12,21,22]

#plt.plot(x, y)

# Let's plot a lovely looking plot

# Line 1 - Points
x = [3, 9, 14]
y = [2,7,30]

# plotting x and y
plt.plot(x, y, c="red", linewidth=2, label="line 1")


x2 = [1,15,18]
y2 = [0,3,12]

plt.plot(x2, y2, c="green", linewidth=2, label="line 2", linestyle="dashed",marker='o',markerfacecolor="orange")
#label the axes and give the plot a title

plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Two lines!")

#Show the legend on the plot
plt.legend()

#Get python to show the plot
plt.show()
