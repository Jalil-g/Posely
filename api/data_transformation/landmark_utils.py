import cv2
import mediapipe as mp
import numpy as np
import math
import os
import json

mp_pose = mp.solutions.pose
# Define connections between landmarks to represent a stickman
connections = [
            (1,3),(1,2),(1,7),(2,4),(2,8),(3,5),(4,6),(7,8),(7,9),(8,10),(9,11),(10,12)
        ]

def generate_landmarks(image_path):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # open picture and represent it as an array
        image_frame = cv2.imread(image_path)
        image_frame = cv2.resize(image_frame, (256, 256))
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

def draw_blank_image(image_path):
    image_frame = cv2.imread(image_path)
    transparent_img = np.zeros((image_frame.shape[0], image_frame.shape[1], 4), dtype=np.uint8)
    land_arr = generate_landmarks(image_path)
    
    for i, landmark in enumerate(land_arr):
        # Convert the relative coordinates to absolute coordinates
        x, y, _ = (landmark * [image_frame.shape[1], image_frame.shape[0], 1]).astype(int)
        # Draw a small circle at each landmark position
        cv2.circle(transparent_img, (x, y), 5, (0, 255, 0, 255), -1)
        
    #Draw lines between the connected landmarks
    for i, j in connections:
        if not ((land_arr[i][0] == 0 and land_arr[i][1] == 0) or (land_arr[j][0] == 0 and land_arr[j][1] == 0)):
            x1, y1, _ = (land_arr[i] * [image_frame.shape[1], image_frame.shape[0], 1]).astype(int)
            x2, y2, _ = (land_arr[j] * [image_frame.shape[1], image_frame.shape[0], 1]).astype(int)
            cv2.line(transparent_img, (x1, y1), (x2, y2), (255, 0, 0, 255), 5)

    cv2.imwrite("static/transparent.png", transparent_img)

def draw_landmarks(image_path, land_arr = [], write_image_path="static/processed_image.jpg", blank=False):
        if len(land_arr) == 0:
            land_arr = generate_landmarks(image_path)
        image_frame = cv2.imread(image_path)
        #image_frame = cv2.resize(image_frame, (480, 480))

        for i, landmark in enumerate(land_arr):
            # Convert the relative coordinates to absolute coordinates
            x, y, _ = (landmark * [image_frame.shape[1], image_frame.shape[0], 1]).astype(int)
            # Draw a small circle at each landmark position
            cv2.circle(image_frame, (x, y), 5, (0, 255, 0), -1)
         
        #Draw lines between the connected landmarks
        for i, j in connections:
            if not ((land_arr[i][0] == 0 and land_arr[i][1] == 0) or (land_arr[j][0] == 0 and land_arr[j][1] == 0)):
                x1, y1, _ = (land_arr[i] * [image_frame.shape[1], image_frame.shape[0], 1]).astype(int)
                x2, y2, _ = (land_arr[j] * [image_frame.shape[1], image_frame.shape[0], 1]).astype(int)
                cv2.line(image_frame, (x1, y1), (x2, y2), (255, 0, 0), 5)

        cv2.imwrite(write_image_path, image_frame)

# draw_landmarks("static/img1.jpeg", generate_landmarks("static/img1.jpeg"))
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
    #print(dist)
    scale = sum(dist)/len(dist)
    arr3 = []
    for item in arr1:
        arr3.append([item[0]/scale, item[1]/scale, item[2]/scale])

    vector_distances = sum([arr3[7] - arr1[7], arr3[8] - arr1[8]])/2
    arr4 = []
    for item in arr3:
        if (item[0] == 0 and item[1] == 0):
            arr4.append([0, 0, 0])
        else:
            arr4.append([item[0] - vector_distances[0], item[1] - vector_distances[1], item[2] - vector_distances[2]])
    final_arr = np.array(arr4, dtype=np.float64)
    draw_landmarks(image2, final_arr)
# scale_image("static/img1.jpeg", "static/image.jpg")
def scale_image_predict(image, arr):
    arr1 = arr
    arr2 = generate_landmarks(image)
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
        if (item[0] == 0 and item[1] == 0):
            arr4.append([0, 0, 0])
        else:
            arr4.append([item[0] - vector_distances[0], item[1] - vector_distances[1], item[2] - vector_distances[2]])
    final_arr = np.array(arr4, dtype=np.float64)
    print("final_arr", final_arr)
    draw_landmarks(image, final_arr)
def generate_pose_array(image_folder_path):
    # Generate an array of arrays of landmarks of the poses
    # image_folder_path is the path of the folder that contains the images of the poses
    # return the array of arrays of landmarks of the poses
    pose_arr = []
    for image in os.listdir(image_folder_path):
        pose_arr.append(generate_landmarks(os.path.join(image_folder_path, image)))
    return pose_arr

def generate_name_array(image_folder_path):
    name_arr = []
    for image in os.listdir(image_folder_path):
        name_arr.append(image)
    return name_arr

def save_name_arr(image_folder_path, save_path):
    # save the array of names of the images in the folder in json format
    name_arr = generate_name_array(image_folder_path)
    with open(save_path, 'w') as f:
        json.dump(name_arr, f)
    return name_arr

def load_name_array(name_arr_path):
    # name_arr_path is the path of the file that contains the array of names of the images in the folder
    # return the array of names of the images in the folder
    with open(name_arr_path, 'r') as f:
        return json.load(f)

def save_pos_arr(image_folder_path, save_path):
    # Generate an array of arrays of landmarks of the poses
    # image_folder_path is the path of the folder that contains the images of the poses
    # return the array of arrays of landmarks of the poses
    pose_arr = generate_pose_array(image_folder_path)
    np.save(save_path, pose_arr)
    return pose_arr

def load_pose_array(pose_arr_path):
    # pose_arr_path is the path of the file that contains the array of arrays of landmarks of the poses
    # return the array of arrays of landmarks of the poses
    return np.load(pose_arr_path)

def most_similar_pose(pose, pose_arr):
    # pose is the array of landmarks of the image
    # pose_arr is the array of arrays of landmarks of the poses
    # return the index of the most similar pose
    result = 0
    pose = np.reshape(pose, (13, 3))
    for i in range(len(pose_arr)):
        if np.linalg.norm(pose - pose_arr[i]) < np.linalg.norm(pose - pose_arr[result]):
            result = i

    return result

