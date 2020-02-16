import matplotlib.pyplot as plt
import matplotlib.animation as animation

dms = []

def plotTest(fileName):
    f = open(fileName,"r")
    for line in f.readlines():
        line_data = line.split()
        if line_data[1] == "100":
            dms.append(line_data[10])
    f.close()
    sendData(dms)

def sendData(table):
    x_len = len(dms)
    y_range = [int(min(dms)) - 2, 20]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = list(range(0, len(dms)))
    ys = [0] * x_len
    ax.set_ylim(y_range)
    line, = ax.plot(xs, ys)
    #fig = plt.figure()

    def animate(i, ys):
        ys.append(table[0])
        del table[0]
        ys = ys[-x_len:]
        line.set_ydata(ys)
        return line,

    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,),
        interval=0,
        blit=True)

    plt.show()
