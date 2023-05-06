#!/usr/bin/env python3


'''
This is a boiler plate script that contains hint about different services that are to be used
to complete the task.
Use this code snippet in your code or you can also continue adding your code in the same file


This python file runs a ROS-node of name offboard_control which controls the drone in offboard mode. 
See the documentation for offboard mode in px4 here() to understand more about offboard mode 
This node publishes and subsribes the following topics:

	 Services to be called                   Publications                                          Subscriptions				
	/mavros/cmd/arming                       /mavros/setpoint_position/local                       /mavros/state
    /mavros/set_mode                         /mavros/setpoint_velocity/cmd_vel                     /mavros/local_position/pose   
         
    
'''

import rospy
from geometry_msgs.msg import *
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from gazebo_ros_link_attacher.srv import Gripper
import numpy as np
import math as m

X=0

class offboard_control:

    def __init__(self):
        # Initialise rosnode
        rospy.init_node('pick_n_place', anonymous=True)
    
    def setArm(self):
        # Calling to /mavros/cmd/arming to arm the drone and print fail message on failure
        rospy.wait_for_service('mavros/cmd/arming')  # Waiting untill the service starts 
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool) # Creating a proxy service for the rosservice named /mavros/cmd/arming for arming the drone 
            armService(True)
        except rospy.ServiceException as e:
            print ("Service arming call failed: %s"%e)

        # Similarly delacre other service proxies 
   
    def offboard_set_mode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='OFFBOARD')
        except rospy.ServiceException as e:
            print("service set_mode call failed: %s. Offboard Mode could not be set."%e)

    def setAutoLandMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='AUTO.LAND')
        except rospy.ServiceException as e:
            print("service set_mode call failed: %s. Autoland Mode could not be set."%e)

        
        # Call /mavros/set_mode to set the mode the drone to OFFBOARD
        # and print fail message on failure

    # def pakadna(self):
    #     rospy.wait_for_service("activate_gripper")
    #     try:
    #         pakadle = rospy.ServiceProxy('activate_gripper',mavros_msgs.srv.CommandBool)
    #     except rospy.ServiceException as e:
    #         print('Hag diya') 

   
class stateMoniter:
    def __init__(self):
        self.state = State()
        # Instantiate a setpoints message
                
    def stateCb(self, msg):
        # Callback function for topic /mavros/state
        self.state = msg

    def posCb(self, msg):
        self.local_pos=msg
    # Create more callback functions for other subscribers 
    def callback(self,abc):
        global X
        if(abc.data=="True"):
            X=1
        else:
            X=0     
    
               

def main():

    stateMt = stateMoniter()
    ofb_ctl = offboard_control()

    # Initialize publishers
    local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
    local_vel_pub = rospy.Publisher('mavros/setpoint_velocity/cmd_vel', Twist, queue_size=10)
    # Specify the rate 
    rate = rospy.Rate(20.0)
    rospy.Subscriber("/mavros/state",State, stateMt.stateCb)
    rospy.Subscriber("/mavros/local_position/pose", PoseStamped, stateMt.posCb)
    check=rospy.Subscriber('/gripper_check',std_msgs.msg.String,stateMt.callback)

    # Make the list of setpoints 
    # setpoints=[[0,0,0],[0,0,10],[10,0,10],[10,10,10],[0,10,10],[0,0,10],[0,0,0]]
    setpoints = [[0,0,0],[0,0,3],[3,0,3],[3,0,0.05],[3,0,3],[3,3,3],[3,3,0],[3,3,3],[0,3,3],[0,0,3],[0,0,0]]#List to setpoints

    # Similarly initialize other publishers 

    # Create empty message containers 
    pos =PoseStamped()
    pos.pose.position.x = 0
    pos.pose.position.y = 0
    pos.pose.position.z = 0

    # Set your velocity here
    vel = Twist()
    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    
    # Similarly add other containers 
    # stepsize=2
    # threshold=0.5
    # Initialize subscriber 
    
    # Similarly initialize other subscribers 

    '''
    NOTE: To set the mode as OFFBOARD in px4, it needs atleast 100 setpoints at rate > 10 hz, so before changing the mode to OFFBOARD, send some dummy setpoints  
    '''
    for i in range(100):
        local_pos_pub.publish(pos)
        rate.sleep()
    
    # Arming the drone
    while not stateMt.state.armed:
        ofb_ctl.setArm()
        rate.sleep()
    print("Armed!!")

    # Switching the state to auto mode
    while not stateMt.state.mode=="OFFBOARD":
        ofb_ctl.offboard_set_mode()
        rate.sleep()
    print ("OFFBOARD mode activated")

    rospy.wait_for_service("activate_gripper")
    print("pakadne ke liye taiyaar")
    

    a=1
    
    # Publish the setpoints 
    while not rospy.is_shutdown() and a<len(setpoints):
        '''
        Step 1: Set the setpoint 
        Step 2: Then wait till the drone reaches the setpoint, 
        Step 3: Check if the drone has reached the setpoint by checking the topic /mavros/local_position/pose 
        Step 4: Once the drone reaches the setpoint, publish the next setpoint , repeat the process until all the setpoints are done  

        Write your algorithm here 
        '''
        threshold=0.1
        pos.pose.position.x=setpoints[a][0]
        pos.pose.position.y=setpoints[a][1]
        pos.pose.position.z=setpoints[a][2]

        if(abs(stateMt.local_pos.pose.position.x-setpoints[a][0])>threshold or abs(stateMt.local_pos.pose.position.y-setpoints[a][1])>threshold or abs(stateMt.local_pos.pose.position.z-setpoints[a][2])>threshold ):
            local_pos_pub.publish(pos)
            local_vel_pub.publish(vel) 
            rate.sleep()
            if(a==3 or a==7):
                print("threesome ya sixsome hai")
                while(stateMt.local_pos.pose.position.z>=(-0.1)):
                    gandu = 0
                    local_pos_pub.publish(pos)
                    local_vel_pub.publish(vel)
                    rate.sleep()
                    print(X)
                    if(X and a==3):
                        while not stateMt.state.mode=="AUTO.LAND":
                            ofb_ctl.setAutoLandMode()
                            rate.sleep()
                        print("Lunded!!")
                        try:
                            print("tesra hai")
                            local_pos_pub.publish(pos)
                            local_vel_pub.publish(vel)
                            rate.sleep()
                            while(1):
                                pakadle = rospy.ServiceProxy('activate_gripper',Gripper)
                                bsdk = pakadle(True)
                                rospy.loginfo(stateMt.local_pos.pose.position)
                                print("on ur left, kosis jaari hai")
                                if(bsdk.result == True):
                                    a+=1
                                    gandu = 1
                                    break
                            while not stateMt.state.mode=="OFFBOARD":
                                ofb_ctl.offboard_set_mode()
                                rate.sleep()
                            print("vapis garam kr diya")
                            break
                        except rospy.ServiceException as e:
                            print('Hag diya')
                            rospy.loginfo(stateMt.local_pos.pose.position)
                            local_pos_pub.publish(pos)
                            local_vel_pub.publish(vel)
                            rate.sleep()   
                        
                    elif(X and a==7):
                        print("chatha hai")
                        while(1):
                            try:
                                while not stateMt.state.mode=="AUTO.LAND":
                                    ofb_ctl.setAutoLandMode()
                                    rate.sleep()
                                print("Lunded!!")
                                while(1):
                                    pakadle = rospy.ServiceProxy('activate_gripper',Gripper)
                                    bsdk = pakadle(False)
                                    rospy.loginfo(stateMt.local_pos.pose.position)
                                    print("on ur left, bacche xhod rhe hai")
                                    if(bsdk.result == True):
                                        gandu = 1
                                        break
                                while not stateMt.state.mode=="OFFBOARD":
                                    ofb_ctl.offboard_set_mode()
                                    rate.sleep()
                                print("vapis garam kr diya")
                            except rospy.ServiceException as e:
                                print('Phirse Hag diya')  
                                rospy.loginfo(stateMt.local_pos.pose.position) 
                                local_pos_pub.publish(pos)
                                local_vel_pub.publish(vel)
                                rate.sleep()
                        print("hd hinjada hai")
                        local_pos_pub.publish(pos)
                        local_vel_pub.publish(vel)
                        rate.sleep()
                    rospy.loginfo(stateMt.local_pos.pose.position)    
                    if gandu:
                        break
        else:
            a+=1
            rate.sleep()

        
        
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass