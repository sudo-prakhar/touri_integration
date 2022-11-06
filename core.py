import time
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os
import keyboard

# ---------------------------------------------------------------------------- #
#                                    HELPERS                                   #
# ---------------------------------------------------------------------------- #

def run_terminal_cmd(cmd, delay_in_sec=0):
    '''
    cmd -> command to run in a new terminal
    delay_in_sec -> delay in seconds [OPTIONAL] [DEFAULT = 0]
    '''
    time.sleep(delay_in_sec)
    os.system("gnome-terminal -- {}".format(cmd))

def sendMsgToUser(msg):
    db.reference("state").update({
        "botMsg" : msg
    })

def setAutonomousMode(value):
    db.reference("state").update({
        "runningAutoCommand" : value,
        })


 # ---------------------------------------------------------------------------- #
 #                                  AUTOSKILLS                                  #
 # ---------------------------------------------------------------------------- #
def autoNavigationCmd(event):
    roomName = None if event.data == "None" else event.data

    if roomName:
        print(roomName)
        db.reference("autoSkills/navigation/").update({'selectedRoom' : "None"})
        sendMsgToUser(f"TOURI: Navigating to {roomName}")
        setAutonomousMode(True)


        # ---------------------------------------------------------------------------- #
        #TODO: @Shruti - Add your ROS terminal commands here
        # run_terminal_cmd("YOUR COMMAND GOES HERE", delay_in_sec = 1)
        time.sleep(3)
        # ---------------------------------------------------------------------------- #

        sendMsgToUser(f"TOURI: Reached {roomName}")
        setAutonomousMode(False)



def autoPickPlaceGetImg(event):
    imgReq = event.data
    if imgReq:
        sendMsgToUser(f"TOURI: Finding objects to pick")
        # ---------------------------------------------------------------------------- #
        #TODO: @Shivani - Add your ROS terminal commands here
        # run_terminal_cmd("YOUR COMMAND GOES HERE", delay_in_sec = 1)
        # ---------------------------------------------------------------------------- #



def pickObj(event):
    imgReq = event.data
    if imgReq:
        x = event.data['x']
        y = event.data['y']
        if x != 0 and y != 0:
            sendMsgToUser(f"TOURI: Picking up the object")
            setAutonomousMode(True)
            time.sleep(3)
        
            # ---------------------------------------------------------------------------- #
            #TODO: @Shivani - Add your ROS terminal commands here
            # run_terminal_cmd("YOUR COMMAND GOES HERE", delay_in_sec = 1)
            # ---------------------------------------------------------------------------- #

            sendMsgToUser(f"TOURI: Picked up Object")
            db.reference("autoSkills/pickPlace").update({
                                                'imgRequested': False,
                                                'imgSrc': "None",
                                                'tapCordinates': {'x': 0, 'y': 0},
                                                })
            setAutonomousMode(False)






if __name__ == "__main__":

    # TODO: Update the path for firebase key
    cred = credentials.Certificate("keys/touri-65f07-firebase-adminsdk-wuv71-b245c875f8.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://touri-65f07-default-rtdb.firebaseio.com/'})

    db.reference("autoSkills/navigation/selectedRoom").listen(autoNavigationCmd)
    db.reference("autoSkills/pickPlace/imgRequested").listen(autoPickPlaceGetImg)
    db.reference("autoSkills/pickPlace/tapCordinates").listen(pickObj)


