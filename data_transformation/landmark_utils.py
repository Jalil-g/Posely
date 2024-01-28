import cv2
import mediapipe as mp
import numpy as np
import math

mp_pose = mp.solutions.pose
# Define connections between landmarks to represent a stickman
connections = [
            (1,3),(1,2),(1,7),(2,4),(2,8),(3,5),(4,6),(7,8),(7,9),(8,10),(9,11),(10,12)
        ]

def generate_landmarks(image_path):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # open picture and represent it as an array
        image_frame = cv2.imread(image_path)
        image_frame = cv2.resize(image_frame, (480, 480))
        image_frame_rgb = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
        image_frame_rgb.flags.writeable = False

        # Make detection
        processed = pose.process(image_frame_rgb)

        # Extract landmarks
        try:
            landmarks = processed.pose_landmarks.landmark
        except:
            print("---------------------LANDMARK NOT DETECTED ERROR----------------------")
            return -1

        landmark_list = []
        delete_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 29, 30, 31, 32]
        for i in range(len(landmarks)):
            if i not in delete_list:
                if landmarks[i].visibility > 0.6:
                    landmark_list.append([landmarks[i].x, landmarks[i].y, landmarks[i].z])
                else:
                    landmark_list.append([0, 0, 0])

        land_arr = np.array(landmark_list, dtype=np.float64)

        return land_arr


def draw_landmarks(image_path,land_arr):
        image_frame = cv2.imread(image_path)
        image_frame = cv2.resize(image_frame, (480, 480))

        for i, landmark in enumerate(land_arr):
            # Convert the relative coordinates to absolute coordinates
            x, y, _ = (landmark * [480, 480, 1]).astype(int)
            # Draw a small circle at each landmark position
            cv2.circle(image_frame, (x, y), 5, (0, 255, 0), -1)
         
        #Draw lines between the connected landmarks
        for i, j in connections:
            x1, y1, _ = (land_arr[i] * [480, 480, 1]).astype(int)
            x2, y2, _ = (land_arr[j] * [480, 480, 1]).astype(int)
            if not ((x1 == 0 and y1 == 0) or (x2 == 0 and y2 == 0)):
                cv2.line(image_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        cv2.imshow('Landmarks', image_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def scale_image(image1, image2):
    arr1 = generate_landmarks(image1)
    arr2 = generate_landmarks(image2)
    dist = []
    for i, j in connections:
        if (arr1[i][0] == 0 and arr1[j][0] == 0) or (arr2[i][0] == 0 and arr2[j][0] == 0):
            continue
        else:    
            dist1 = math.dist(arr1[i], arr1[j])
            dist2 = math.dist(arr2[i], arr2[j])
            dist.append(dist1/dist2)
    print(dist)
    scale = sum(dist)/len(dist)
    arr3 = []
    for item in arr1:
        arr3.append([item[0]/scale, item[1]/scale, item[2]/scale])

    vector_distances = sum([arr3[7] - arr1[7], arr3[8] - arr1[8]])/2
    arr4 = []
    for item in arr3:
        arr4.append([item[0] - vector_distances[0], item[1] - vector_distances[1], item[2] - vector_distances[2]])
    final_arr = np.array(arr4, dtype=np.float64)
    draw_landmarks(image2, final_arr)

