import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()

def process_frame(_, frame):
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    # left_pupil = gaze.pupil_left_coords()
    # right_pupil = gaze.pupil_right_coords()
    data={
        'is_blinking':False,
        'is_right':False,
        'is_left':False,
        'is_center':False,
        # 'left_pupil_x':int(left_pupil[0]),
        # 'left_pupil_y':int(left_pupil[1]),
        # 'right_pupil_x':int(right_pupil[0]),
        # 'right_pupil_y':int(right_pupil[1])
    }

    if gaze.is_blinking():
        data['is_blinking']=True
    elif gaze.is_right():
        data['is_right']=True
    elif gaze.is_left():
        data['is_left']=True
    elif gaze.is_center():
        data['is_center']=True

    print(data)    
    return data
