from controller import Robot
from controller import Camera

TIME_STEP = 32
robot = Robot()

ds = []
wheels = []
ir=[]

dsNames = ['ds_right', 'ds_left']
irNames=["RIGHT_S","MID_S","LEFT_S"]
irVal=[0]*len(irNames)
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']

cm=robot.getCamera("cam")
cm.enable(TIME_STEP)
cm.recognitionEnable(TIME_STEP)

for i in range(len(dsNames)):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)


for i in range(3):
    ir.append(robot.getDevice(irNames[i]))
    ir[i].enable(TIME_STEP)
    
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0    


kp=0.6
ki=0.1
kd=0.1


base_speed=2


for i in range(len(wheels)):
    wheels[i].setVelocity(base_speed)

last_position=0



while robot.step(TIME_STEP) != -1:
        for i in range(len(ir)):
            irVal[i] = ir[i].getValue()
    
        print("left: {} right: {} mid: {}".format(irVal[2], irVal[0], irVal[1]))
        
        if irVal[0]<800:
            right_ir_dg=0
        else:
            right_ir_dg=1
        
        if irVal[2]<800:
            left_ir_dg=0
        else:
            left_ir_dg=1
        
        if irVal[1]<800:
            mid_ir_dg=0
        else:
            mid_ir_dg=1
        
        weight=(10)*left_ir_dg+0*mid_ir_dg+(-10)*right_ir_dg
        
        sum=left_ir_dg+right_ir_dg+mid_ir_dg
        
        if sum==0:
            position=last_position
        else:
            position=weight/sum
                    
        
        print("left: {} mid: {} right: {}".format(irVal[2],irVal[1],irVal[0]))
        print("sum:{} weight:{}".format(sum,weight))
        print("pos:{} last_pos:{}".format(position,last_position))
       
        motorCorrection=kp*position+ki*position+kd*(position-last_position)
        last_position=position
        print("MotorCorrection",motorCorrection)
         
        right_speed=base_speed-motorCorrection
        left_speed=base_speed+motorCorrection
                    
       
        wheels[0].setVelocity(left_speed)
        wheels[1].setVelocity(right_speed)
        wheels[2].setVelocity(left_speed)
        wheels[3].setVelocity(right_speed) 
        pass                 
    
    