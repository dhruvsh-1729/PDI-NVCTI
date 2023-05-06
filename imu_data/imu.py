import serial
import time
import matplotlib.pyplot as plt
# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('/dev/ttyUSB0', 9800, timeout=1)
time.sleep(2)

vx,vy,x,y=0,0,0,0
acc_x=[]
acc_y=[]
vel_x=[]
vel_y=[]
pos_x=[]
pos_y=[]
Time=[]
t=0
dt=0.0001
thresh=-0.5
prev_ax=0
prev_ay=0
p=0.4
for i in range(300):
    line = ser.readline()   # read a byte
    # print(line)
    if line and i>50:
        string = line.decode()  # convert the byte string to a unicode string
        aval = string.split()
        # print(aval)
        ax = float(aval[0])
        ay = float(aval[1])
        # if ax<thresh:
        #     ax=int(ax)-1
        # if ay<thresh:
        #     ay=int(ay)-1
        # else:    
        #     ax=int(ax)
        #     ay=int(ay)
        print(ax,ay)
        ax=p*ax + (1-p)*prev_ax
        ay=p*ay + (1-p)*prev_ax
        vx+=ax*dt
        vy+=ay*dt
        x+=vx*dt
        y+=vy*dt
        t+=dt
        prev_ax=ax
        prev_ay=ay
        acc_x.append(ax)
        acc_y.append(ay)
        vel_x.append(vx)
        vel_y.append(vy)
        pos_x.append(x)
        pos_y.append(y)
        Time.append(t)

plt.figure(1)
plt.plot(Time, acc_x,label='ax',color='green', linestyle='dashed',marker='o', markerfacecolor='blue',markersize=1)
plt.plot(Time, acc_y,label='ay',color='red', linestyle='dashed',marker='o', markerfacecolor='blue',markersize=1)
# plt.plot(Time, vel_x,label='vx',color='yellow', linestyle='dashed',marker='o', markerfacecolor='blue',markersize=1)
# plt.plot(Time, vel_y,label='vy',color='orange', linestyle='dashed',marker='o', markerfacecolor='blue',markersize=1)
# plt.plot(Time, pos_x,label='x',color='aqua', linestyle='dashed',marker='o', markerfacecolor='blue',markersize=1)
# plt.plot(Time, pos_y,label='y',color='magenta', linestyle='dashed',marker='o', markerfacecolor='blue',markersize=1)
plt.title("Kinematics of the robot")
plt.xlim(1)
plt.ylim(1)
plt.legend()
plt.xlabel("time")
plt.ylabel("Kinematics")

plt.figure(2)
plt.plot(vel_x,vel_y)
plt.title("Velocity diagram")
plt.xlim(1)
plt.ylim(1)
plt.xlabel("Vel_x")
plt.ylabel("Vel_y")

plt.figure(3)
plt.plot(pos_x,pos_y)
plt.title("Position diagram")
plt.xlim(1)
plt.ylim(1)
plt.xlabel("Pos_x")
plt.ylabel("Pos_y")

plt.axis('equal')
plt.show()

ser.close()
