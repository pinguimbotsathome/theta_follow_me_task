#!/usr/bin/env python3

import rospy
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import Twist

from std_msgs.msg import Int16

pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

def callback(data):
    #print data
    if "torso" in data.transforms[0].child_frame_id:
        torso_x = data.transforms[0].transform.translation.x #mais perto do robô fica negativo, mais longe do robô fica positivo
        torso_y = data.transforms[0].transform.translation.y #esquerda fica positivo, direita fica negativo
        
        distancia_seguranca = 0.5
        multiplicador_vel_lin_x = 0.4
        multiplicador_vel_ang_z = 0.8

        ex = torso_x - distancia_seguranca
        ey = torso_y 

        lin_x = 0
        ang_z = 0

        if ex < 0.0:
            lin_x = 0.0
        else:
            lin_x = multiplicador_vel_lin_x * ex
        
        ang_z = multiplicador_vel_ang_z * ey

        cmd_vel = Twist()
        cmd_vel.linear.x = lin_x
        cmd_vel.angular.z = ang_z
        print(cmd_vel)

        pub.publish(cmd_vel)

if __name__ == '__main__':
	rospy.init_node('follow_me_task', anonymous=True)

	rospy.Subscriber('tf', TFMessage, callback)
	
	rospy.spin()