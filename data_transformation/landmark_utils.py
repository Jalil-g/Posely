import cv2
import mediapipe as mp
import numpy as np
mp_pose = mp.solutions.pose
def generate_landmarks(image_path):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # open picture and represent it as an array
        image_frame = cv2.imread(image_path)
        image_frame = cv2.resize(image_frame, (480, 480))
        image_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
        image_frame.flags.writeable = False

        # Make detection
        processed = pose.process(image_frame)

        # Extract landmarks
        try:
            landmark = processed.pose_landmarks.landmark
        except:
            print("---------------------LANDMARK NOT DETECTED ERROR----------------------")
            return -1

        landmark_list = []
        delete_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 29, 30, 31, 32]
        for i in range(len(landmark)):
            if i not in delete_list:
                if landmark[i].visibility > 0.6:
                    landmark_list.append([landmark[i].x, landmark[i].y, landmark[i].z])
                else:
                    landmark_list.append([0, 0, 0])

        land_arr = np.array(landmark_list, dtype=np.float64)
        return land_arr