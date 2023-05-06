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
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import *
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from gazebo_ros_link_attacher.srv import Gripper
import cv2.aruco as aruco
import sys
import time
import numpy as np
import math as m

X=0
visible=0
golemai=0

px=0
py=0

class offboard_control:

	def __init__(self):
        # Initialise rosnode
		rospy.init_node('pick_n_place_aruco', anonymous=True)

	def setArm(self):
        # Calling to /mavros/cmd/arming to arm the drone and print fail message on failure
		rospy.wait_for_service('mavros/cmd/arming')  # Waiting untill the service starts
		try:
			armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool) # Creating a proxy service for the rosservice named /mavros/cmd/arming for arming the drone
			armService(True)
		except rospy.ServiceException as e:
			print ("Service arming call failed: %s"%e)

	def setDisarm(self):
        # Calling to /mavros/cmd/arming to arm the drone and print fail message on failure
		rospy.wait_for_service('mavros/cmd/arming')  # Waiting untill the service starts
		try:
			armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool) # Creating a proxy service for the rosservice named /mavros/cmd/arming for arming the drone
			armService(False)
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

	def image_callback(self, image):
		global visible,golemai,px,py
		try:
			self.img = self.bridge.imgmsg_to_cv2(image, "bgr8")
		except CvBridgeError as e:
			print(e)
			return
		img = np.asarray(self.img,dtype = np.uint8)
		try:
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		except:
			gray = img.copy()
		aruco_dict = aruco.getPredefinedDictionary( aruco.DICT_5X5_250 )
		parameters = aruco.DetectorParameters_create()
		corners, ids,_ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
		if(ids==None):
			visible = 0
			golemai = 0
			return
		else:
			visible = 1
			Detected_ArUco_markers = corners[0]
			print(corners[0])
			print(self.img.shape)
			centre = Detected_ArUco_markers[0].mean(axis=0)
			print(centre)
			if (abs(200-centre[0])<10 and abs(200-centre[1]<10)):
				golemai=1
				print("gole mai aagya")
			if(centre[0]>210):
				px=1
			elif(centre[0]<190):
				px=-1
			if(centre[1]>210):
				py=1
			elif(centre[1]<190):
				py=-1



def main():

	stateMt = stateMoniter()
	ofb_ctl = offboard_control()

    # Initialize publishers
	local_pos_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
	local_vel_pub = rospy.Publisher('mavros/setpoint_velocity/cmd_vel', Twist, queue_size=10)
    # Specify the rate
	rate = rospy.Rate(20.0)
	rospy.Subscriber("/mavros/state",State, stateMt.stateCb)
	rospy.Subscriber("/eDrone/camera/image_raw", Image, stateMt.image_callback) #Subscribing to the camera topic
	stateMt.bridge = CvBridge()
	rospy.Subscriber("/mavros/local_position/pose", PoseStamped, stateMt.posCb)
	check=rospy.Subscriber('/gripper_check',std_msgs.msg.String,stateMt.callback)

    # Make the list of setpoints
    # setpoints=[[0,0,0],[0,0,10],[10,0,10],[10,10,10],[0,10,10],[0,0,10],[0,0,0]]
	setpoints = [[0,0,0],[0,0,3],[1,0,3],[2,0,3],[3,0,3],[4,0,3],[5,0,3],[6,0,3],[7,0,3],[8,0,3],[9,0,3],[9,0,0],[9,0,3],[0,0,3],[0,0,0]]#List to setpoints

    # Create empty message containers
	pos =PoseStamped()
	pos.pose.position.x = 0
	pos.pose.position.y = 0
	pos.pose.position.z = 0

	post =PoseStamped()
	post.pose.position.x = 0
	post.pose.position.y = 0
	post.pose.position.z = (-0.4)

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

    #rospy.wait_for_service("activate_gripper")
    #print("pakadne ke liye taiyaar")
	found = 0
	flag=0
	a=1
	b=0
	flag2=0
	grnded=0

    # Publish the setpoints
	while not rospy.is_shutdown() and a<len(setpoints):
		'''
		Step 1: Set the setpoint
		Step 2: Then wait till the drone reaches the setpoint,
		Step 3: Check if the drone has reached the setpoint by checking the topic /mavros/local_position/pose
		Step 4: Once the drone reaches the setpoint, publish the next setpoint , repeat the process until all the setpoints are done

		Write your algorithm here
		'''
		if(b>0):
			print("2nd phase shuru")
			while(stateMt.local_pos.pose.position.z>(-0.5)):
				print('harshit')
				if(golemai==1):
					pos.pose.position.x=stateMt.local_pos.pose.position.x
					pos.pose.position.y=0
					local_pos_pub.publish(post)
					rate.sleep()
				while(visible==1 and golemai!= 1):
					post.pose.position.z=(-0.3)
					# if(visible==1 and px==0 and py>0):
					# 	post.pose.position.y-=0.02
					# elif(visible==1 and px==0 and py<0):
					# 	post.pose.position.y+=0.02
					if(visible==1 and px<0 and py==0):
						post.pose.position.x-=0.01
					elif(visible==1 and px>0 and py==0):
						post.pose.position.x+=0.01
					elif(visible==1 and px>0 and py>0):
						post.pose.position.x+=0.01
						# post.pose.position.y-=0.02
					elif(visible==1 and px<0 and py>0):
						post.pose.position.x-=0.01
						# post.pose.position.y+=0.02
					elif(visible==1 and px>0 and py<0):
						post.pose.position.x+=0.01
						# post.pose.position.y+=0.02
					elif(visible==1 and px<0 and py<0):
						post.pose.position.x-=0.01
						# post.pose.position.y+=0.02
					if(visible==0):
						post.pose.position.x=pos.pose.position.x
					local_pos_pub.publish(post)
					rate.sleep()
				# local_pos_pub.publish(pos)
				post.pose.position.x=6.5
				# post.pose.position.y+=0.005
				local_pos_pub.publish(post)
				rate.sleep()
				print(stateMt.local_pos.pose.position)
				if(X):
					while not stateMt.state.mode=="AUTO.LAND":
						ofb_ctl.setAutoLandMode()
						rate.sleep()
					print("Landed!!")
					try:        
						local_pos_pub.publish(post)
						rate.sleep()
						while(1):
							pakadle = rospy.ServiceProxy('activate_gripper',Gripper)
							if(stateMt.local_pos.pose.position.z>=(-0.4)):
								bsdk = pakadle(True)
								rospy.loginfo(stateMt.local_pos.pose.position)
								if(bsdk.result == True):
									grnded = 1
									a+=1
									break
						while not stateMt.state.mode=="OFFBOARD":
							ofb_ctl.offboard_set_mode()
							rate.sleep()
						break
					except rospy.ServiceException as e:
						rospy.loginfo(stateMt.local_pos.pose.position)
						local_pos_pub.publish(post)
						local_vel_pub.publish(vel)
						rate.sleep()
					
			while(grnded==1 and stateMt.local_pos.pose.position.z<2.97):
				post.pose.position.z=3
				local_pos_pub.publish(post)
				rate.sleep()
			b=0
			a=10
		elif(b==0 and found==1):
			print('yahaan ayaa hai')
			if(visible==1 and flag==0):
				pos.pose.position.x=stateMt.local_pos.pose.position.x
				flag=1
				print('flag :',flag)
			if(flag==1):
				print('flag :',flag)
				if(golemai==1):
					pos.pose.position.x=post.pose.position.x=stateMt.local_pos.pose.position.x
					b=1
					found=0
					print('b :', b)
				# elif(visible==1 and px==0 and py>0):
					# pos.pose.position.x+=0.05
					# pos.pose.position.y=0.01
				# elif(visible==1 and px==0 and py<0):
					# pos.pose.position.x-=0.05
					# pos.pose.position.y=0.01
				elif(visible==1 and px<0 and py==0):
					pos.pose.position.x-=0.03
					# pos.pose.position.y-=0.05
				elif(visible==1 and px>0 and py==0):
					pos.pose.position.x+=0.03
					# pos.pose.position.y+=0.05
				elif(visible==1 and px>0 and py>0):
					pos.pose.position.x+=0.03
					# pos.pose.position.y=0.01
				elif(visible==1 and px<0 and py>0):
					pos.pose.position.x-=0.03
					# pos.pose.position.y+=0.03
				elif(visible==1 and px>0 and py<0):
					pos.pose.position.x+=0.03
					# pos.pose.position.y+=0.03
				elif(visible==1 and px<0 and py<0):
					pos.pose.position.x-=0.03
					# pos.pose.position.y+=0.03					
				local_pos_pub.publish(pos)
				rate.sleep()
			else:
				local_pos_pub.publish(pos)
				# local_vel_pub.publish(vel)
				rate.sleep()

		else:
			threshold=0.1
			if (a==len(setpoints)-1):
				while not stateMt.state.mode=="AUTO.LAND":
					ofb_ctl.setAutoLandMode()
					rate.sleep()
					print("Landed!!")
				while not stateMt.state.armed:
					ofb_ctl.setDisarm()
					rate.sleep()
				print("Disarmed!!")
				break
				
			# if(abs(stateMt.local_pos.pose.position.x-setpoints[a][0])>threshold or abs(stateMt.local_pos.pose.position.y-setpoints[a][1])>threshold or abs(stateMt.local_pos.pose.position.z-setpoints[a][2])>threshold ):
			if(abs(stateMt.local_pos.pose.position.x-setpoints[a][0])<threshold and abs(stateMt.local_pos.pose.position.y-setpoints[a][1])<threshold and abs(stateMt.local_pos.pose.position.z-setpoints[a][2])<threshold):
				a+=1
			
			if visible==1 and flag==0:
				found=1
				pos.pose.position.x=stateMt.local_pos.pose.position.x
			else:
				pos.pose.position.x=setpoints[a][0]
				pos.pose.position.y=setpoints[a][1]
				pos.pose.position.z=setpoints[a][2]

			local_pos_pub.publish(pos)
			# local_vel_pub.publish(vel)
			rate.sleep()

			if(a==11):
				rospy.wait_for_service('activate_gripper')
				print("threesome chalu ho gya")
				while(stateMt.local_pos.pose.position.z>=(-0.5)):
					gandu = 0
					local_pos_pub.publish(pos)
					local_vel_pub.publish(vel)
					rate.sleep()
					print(X)
					if(X):
						# while not stateMt.state.mode=="AUTO.LAND":
						# 	ofb_ctl.setAutoLandMode()
						# 	rate.sleep()
						# 	print("Landed!!")
						try:
							print("hinjada hai")
							local_pos_pub.publish(pos)
							local_vel_pub.publish(vel)
							rate.sleep()
							post.pose.position=pos.pose.position
							while(1):
								pakadle = rospy.ServiceProxy('activate_gripper',Gripper)
								post.pose.position.z=-0.2
								local_pos_pub.publish(post)
								rate.sleep()
								if(stateMt.local_pos.pose.position.z<= (-0.1)):
									bsdk = pakadle(False)
									rate.sleep()
									rospy.loginfo(stateMt.local_pos.pose.position)
									print("on ur left, kosis jaari hai")
									# if(bsdk.result == True):
									print("godd mai aaja")
									gandu = 1
									a+=1
									break
							# while not stateMt.state.mode=="OFFBOARD":
							# 	ofb_ctl.offboard_set_mode()
							# 	rate.sleep()
							print("vapis garam kr diya")
							break
						except rospy.ServiceException as e:
							print('Phirse Hag diya')
							rospy.loginfo(stateMt.local_pos.pose.position)
							local_pos_pub.publish(pos)
							local_vel_pub.publish(vel)
							rate.sleep()
						rospy.loginfo(stateMt.local_pos.pose.position)
					if gandu:
						break
		



if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
