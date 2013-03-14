import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

h = 1.0/10
START = 0.0
END = 60.0

m = 10.0
c = 15.0
k = 100.0

def func_zero(t):
  return 0


def func_sin(t):
  return math.sin(t)


def func_sin_cos_inst(t):
  return 100 * math.sin(t) + 70 * math.cos(t * 5)


def func_sin_cos_st(t):
  return math.sin(t) + math.cos(t * 2)

def euler_sdm(h, start, end, m, c, k, f):
  t = np.linspace(START, END, num=((1/h)* (END-START)))
  x = [ [0] * 2 ] * int((1/h) * 60)
  k1 = [0, 0]

  x[0][0] = 1
  x[0][1] = 0
  plotx = [x[0][0]]

  for i in range(1, len(x)):
    k1[0] = x[i-1][1]
    k1[1] = (f(t[i]) - c * x[i-1][1] - k * x[i-1][0]) / m

    x[i][0] = x[i-1][0] + k1[0] * h
    x[i][1] = x[i-1][1] + k1[1] * h
    plotx.insert(i, x[i][0])

  return t, plotx

if __name__ == "__main__":
  x, y = euler_sdm(h, START, END, m, c, k, func_zero)
  fig, ax = plt.subplots()

  for i in range(len(x)):
    points, = ax.plot(x[i], y[i], marker='.', color='r')
    ax.set_xlim(0, 60)
    ax.set_ylim(-0.7, 1.2)
    plt.pause(0.00001)


  plt.plot(x, y)
  plt.show()

  # Export for Vladimir Tribusean
  k = range(len(y))
  dictzip = dict(zip(k, y))
  import json
  json_str = json.dumps(dictzip)
  text_file = open("data.json", "w")
  text_file.write(json_str)
  text_file.close()

