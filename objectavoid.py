Flag = 0
MarkerInfo = RmList()
SightPos = RmList()

def start():
    global Flag
    global L
    global R
    global P1
    global P2
    global MarkerInfo
    global SightPos

    startSettings()

    while True:
        chassis_ctrl.move(0)
        if Flag == 1:
            Slide()

        if Flag == 2:
            Turn()

        if Flag == 4 or Flag == 5:
            Move()

        if Flag == 6 or Flag == 7:
            Ramp()

        if Flag == 8:
            Deadend()

        if Flag == 10:
            led_ctrl.set_top_led(rm_define.armor_top_all, 0, 0, 0, rm_define.effect_always_on)
            rmexit()
        Flag = 0

def startSettings():
    robot_ctrl.set_mode(rm_define.robot_mode_gimbal_follow)
    gimbal_ctrl.set_follow_chassis_offset(0)
    chassis_ctrl.set_rotate_speed(45)
    chassis_ctrl.set_trans_speed(0.3)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(0.7)
    Flag = 0

def Slide():
    MarkerInfo=RmList(vision_ctrl.get_marker_detection_info())
    SightPos=RmList(media_ctrl.get_sight_bead_position())
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 150, rm_define.effect_always_on)
    if SightPos[1] - MarkerInfo[3] < 0.3 and SightPos[1] - MarkerInfo[3] > -0.3:
        if SightPos[1] <= MarkerInfo[3]:
            chassis_ctrl.move_with_distance(-90,0.3)
        else:
            chassis_ctrl.move_with_distance(90,0.3)

def Turn():
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 50, 0, rm_define.effect_always_on)
    MarkerInfo=RmList(vision_ctrl.get_marker_detection_info())
    SightPos=RmList(media_ctrl.get_sight_bead_position())
    if SightPos[1] <= MarkerInfo[3]:
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise,90)
        time.sleep(3)
    if SightPos[1] >= MarkerInfo[3]:
        chassis_ctrl.rotate_with_degree(rm_define.clockwise,90)
        time.sleep(3)

def Move():
    MarkerInfo=RmList(vision_ctrl.get_marker_detection_info())
    SightPos=RmList(media_ctrl.get_sight_bead_position())
    led_ctrl.set_top_led(rm_define.armor_top_all, 0, 127, 70, rm_define.effect_always_on)
    if MarkerInfo[2] == 5:
        R = SightPos[1] - MarkerInfo[3]
        if R >= 0.2:
            chassis_ctrl.move(0)
        else:
            while not (R >= 0.2 or MarkerInfo[2] == 4):
                chassis_ctrl.move(90)
                MarkerInfo=RmList(vision_ctrl.get_marker_detection_info())
                R = SightPos[1] - MarkerInfo[3]
    if MarkerInfo[2] == 4:
        L = SightPos[1] - MarkerInfo[3]
        if L <= -0.2:
            chassis_ctrl.move(0)
        else:
            while not (L <= -0.2 or MarkerInfo[2] == 5):
                chassis_ctrl.move(-90)
                MarkerInfo=RmList(vision_ctrl.get_marker_detection_info())
                L = SightPos[1] - MarkerInfo[3]

def Ramp():
    MarkerInfo=RmList(vision_ctrl.get_marker_detection_info())
    SightPos=RmList(media_ctrl.get_sight_bead_position())
    led_ctrl.set_top_led(rm_define.armor_top_all, 161, 255, 69, rm_define.effect_always_on)
    chassis_ctrl.set_trans_speed(0.4)
    chassis_ctrl.move_with_time(0,3)
    chassis_ctrl.set_trans_speed(0.2)
    if MarkerInfo[2] == 13:
        R = SightPos[1] - MarkerInfo[3]
        if R >= 0.2:
            chassis_ctrl.move(0)
        else:
            while not (R == 0.2 or MarkerInfo[2] == 14):
                chassis_ctrl.move(90)
                MarkerInfo=RmList(vision_ctrl.get_marker_detection_info())
                R = SightPos[1] - MarkerInfo[3]
    if MarkerInfo[2] == 14:
        L = SightPos[1] - MarkerInfo[3]
        if L <= -0.2:
            chassis_ctrl.move(0)
        else:
            while not (L <= -0.2 or MarkerInfo[2] == 13):
                chassis_ctrl.move(-90)
                MarkerInfo=RmList(vision_ctrl.get_marker_detection_info())
                L = SightPos[1] - MarkerInfo[3]

def Deadend():
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_flash)
    chassis_ctrl.rotate_with_degree(rm_define.clockwise,180)
    time.sleep(6)
    
def vision_recognized_marker_number_one(msg):
    Flag = 1

def vision_recognized_marker_number_two(msg):
    Flag = 2

def vision_recognized_marker_trans_right(msg):
    Flag = 5

def vision_recognized_marker_trans_left(msg):
    Flag = 4

def vision_recognized_marker_number_three(msg):
    Flag = 6

def vision_recognized_marker_number_four(msg):
    Flag = 7

def vision_recognized_marker_trans_red_heart(msg):
    Flag = 8

def vision_recognized_marker_trans_stop(msg):
    Flag = 10

def chassis_impact_detection(msg):
    rmexit()