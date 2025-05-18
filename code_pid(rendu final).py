from microbit import *
from miniprotocole import *
from maprincess import *
# CONSTANTES
MOTOR_FORWARD = 0
MOTOR_BACKWARD = 1
BLACK=1
WHITE=0
SPEED = 160
LOOP=False
WAIT=True
other_time=0
elapsed_time=0
userId=14
destId=14
def forward():
    motor_run(Motor.ALL,SPEED)
def backward():
    motor_run(Motor.ALL,SPEED,1)
    
def left():
    motor_stop()
    motor_run(Motor.LEFT,SPEED,1)
    motor_run(Motor.RIGHT,SPEED)
    sleep(200)
def right():
    motor_stop()
    motor_run(Motor.LEFT,SPEED)
    motor_run(Motor.RIGHT,SPEED,1)
    sleep(200)
    
class PIDController:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.last_error = 0

    def update(self, measurement, dt):
        error = self.setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        self.last_error = error
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        return output

# Setpoint for tracking black line (IR sensor value ~55)
pid = PIDController(kp=0.5, ki=0.02, kd=0.8, setpoint=100)


def follow_line_step():
    base_speed = 160
    max_speed = 255
    ir_value = line_sensor_data(LineSensor.L2)
    dt = 0.05
    correction = pid.update(ir_value, dt)

    threshold = 70  # threshold for sharp correction

    if abs(correction) < threshold:
        # Small correction: adjust speeds normally
        left_speed = int(max(min(base_speed + correction, max_speed), 0))
        right_speed = int(max(min(base_speed - correction, max_speed), 0))
        motor_run(Motor.LEFT, left_speed)
        motor_run(Motor.RIGHT, right_speed)

    elif correction >= threshold:
        # Sharp turn right: reverse right motor
        motor_run(Motor.LEFT, base_speed)
        motor_run(Motor.RIGHT, base_speed//2, 1)  # reverse right

    elif correction <= -threshold:
        # Sharp turn left: reverse left motor
        motor_run(Motor.RIGHT, base_speed)
        motor_run(Motor.LEFT, base_speed//2, 1)  # reverse left
    sleep(dt)
motor_stop()
while True:
    while WAIT:
        if button_b.is_pressed():
                display.show(3)
                sleep(1000)
                display.show(2)
                sleep(1000)
                display.show(1)
                sleep(1000)
                display.show(0)
                sleep(10)
                display.clear()
                start_time = running_time()
                LOOP=True
                WAIT=False
        m = receive_msg(userId)
        if m:
             start_time=running_time()
             other_time = m.payload[0]
             print(other_time,"s")
             LOOP=True
             WAIT=False
             
    while LOOP:
            fin=False
            R1 = line_sensor(LineSensor.R1)
            R2 = line_sensor(LineSensor.R2)
            L1 = line_sensor(LineSensor.L1)
            L2 = line_sensor(LineSensor.L2)
            M = line_sensor(LineSensor.M)

            led_rgb(Color.WHITE)
            if M==BLACK and L1==BLACK:
                led_rgb(Color.PURPLE)
                right() 
            else:
                follow_line_step()
            if 2 < ultrasonic()<=5:
                motor_stop()
                led_rgb(Color.GREEN)
                end_time=running_time()
                elapsed_time=(end_time-start_time)
                print(elapsed_time//1000,"s")
                total_time=(elapsed_time//1000+other_time)
                print(total_time,"s")
                if other_time==0:
                    send_msg(1,[elapsed_time//1000],userId, destId)
                    print("msg sent")
                display.scroll(str(total_time)+"s")
                display.scroll(str(total_time)+"s")
                LOOP=False
            if button_a.is_pressed():
                motor_stop()
                LOOP=False
                WAIT=True
