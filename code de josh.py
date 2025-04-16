"projet labiryth Joshua Ethan"
from microbit import *
from protocole import *
from maprincess import *

# CONSTANTES
MOTOR_FORWARD = 0
MOTOR_BACKWARD = 1
BLACK=1
WHITE=0
SPEED = 50
LOOP=True
userId=14
destId=15
def disco():
    led_rgb(Color.BLUE)
    sleep(100)
    led_rgb(Color.RED)
    sleep(100)
    led_rgb(Color.GREEN)
    sleep(100)
    led_rgb(Color.PURPLE)
    sleep(100)
    led_rgb(Color.BLUE)
    sleep(100)
    led_rgb(Color.YELLOW)
    sleep(100)
def forward():
    motor_run(Motor.ALL,SPEED)
    line_sensor_data_all()
def backward():
    motor_run(Motor.ALL,SPEED,1)
    
def left():
    motor_run(Motor.LEFT,SPEED,1)
    motor_run(Motor.RIGHT,SPEED)
    sleep(500)
    motor_stop()
    
def right():
    motor_run(Motor.LEFT,SPEED)
    motor_run(Motor.RIGHT,SPEED,1)
    sleep(500)
    motor_stop()
def follow_line_L2(speed):
    led_rgb(Color.BLUE)
    if line_sensor(LineSensor.M)==WHITE:
        forward()
    if line_sensor(LineSensor.L2)==BLACK:
         motor_run(Motor.LEFT,speed+20)
         motor_run(Motor.RIGHT,speed,1)
    elif line_sensor(LineSensor.L2)==WHITE:
         motor_run(Motor.RIGHT,speed+20)
         motor_run(Motor.LEFT,speed,1)
    if line_sensor(LineSensor.M)==BLACK:
        motor_stop()
        sleep(10)
    
    
while LOOP:
    sleep(10)
    led_rgb(Color.WHITE)
    print(line_sensor_data_all())
    sleep(10)
    if line_sensor(LineSensor.L2)==BLACK and line_sensor(LineSensor.R2)==WHITE and line_sensor(LineSensor.M)==BLACK:
        led_rgb(Color.PURPLE)
        right()
        sleep(300)
        forward()
        sleep(300)
    if line_sensor(LineSensor.M)==BLACK and line_sensor(LineSensor.L2)==BLACK and line_sensor(LineSensor.R2)==BLACK:
        led_rgb(Color.YELLOW)
        motor_stop()
        right()
        right()
        sleep(100)
        
    else:
        follow_line_L2(SPEED)
    if button_a.is_pressed() or ultrasonic()<=5:
        send_msg(1,[60],userId, destId)
        led_rgb(Color.GREEN)
        motor_stop()
        LOOP=False
while LOOP==False:
    disco()	
