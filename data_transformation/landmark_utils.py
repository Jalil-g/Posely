import cv2
import mediapipe as mp
import numpy as np
import os

mp_pose = mp.solutions.pose

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

        land_arr = np.array(landmark_list, dtype=np.float64) # Original picture landmarks

        return land_arr





def draw_landmarks(image_path,land_arr):
        
    
        image_frame = cv2.imread(image_path)
        image_frame = cv2.resize(image_frame, (480, 480))
        image_frame_rgb = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
        image_frame_rgb.flags.writeable = False

        
        connections = [
            (1,3),(1,2),(1,7),(2,4),(2,8),(3,5),(4,6),(7,8),(7,9),(8,10),(9,11),(10,12)
        ]

        # Draw landmarks on the image
        image_frame_rgb.flags.writeable = True
        image_frame_rgb = cv2.cvtColor(image_frame_rgb, cv2.COLOR_RGB2BGR)
        for i, landmark in enumerate(land_arr):
            a, b, _ = landmark.astype(int)
            # Convert the relative coordinates to absolute coordinates
            x, y, _ = (landmark * [480, 480, 1]).astype(int)
            # Draw a small circle at each landmark position
            cv2.circle(image_frame_rgb, (x, y), 5, (0, 255, 0), -1)
            # Write the coordinates on the image
            cv2.putText(image_frame_rgb, f"({a:.2f}, {b:.2f})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

        # Draw lines between the connected landmarks
        # TODO: Make the lines of different colors for different body parts
        for i, j in connections:
            x1, y1, _ = (land_arr[i] * [480, 480, 1]).astype(int)
            x2, y2, _ = (land_arr[j] * [480, 480, 1]).astype(int)
            cv2.line(image_frame_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)

        cv2.imshow('Landmarks', image_frame_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return land_arr

def generate_pose_array(image_folder_path):
    # Generate an array of arrays of landmarks of the poses
    # image_folder_path is the path of the folder that contains the images of the poses
    # return the array of arrays of landmarks of the poses
    pose_arr = []
    for image in os.listdir(image_folder_path):
        pose_arr.append(generate_landmarks(os.path.join(image_folder_path, image)))
    return pose_arr

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
    for i in range(len(pose_arr)):
        if np.linalg.norm(pose - pose_arr[i]) < np.linalg.norm(pose - pose_arr[result]):
            result = i

    return result


if __name__ == "__main__":
    arr = generate_landmarks('unsplash.jpg')
    print(arr.shape,arr.dtype, arr)
    draw_landmarks('unsplash.jpg',arr)
