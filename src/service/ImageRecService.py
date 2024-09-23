import cv2
import numpy as np


class ImageRecService:
    def __init__(self):
        pass

    def recognize(self, input_img: np.ndarray):
        image1 = cv2.imread('sample_in.jpeg', cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread('sample_neg_1.jpg', cv2.IMREAD_GRAYSCALE)

        # 创建SIFT对象
        sift = cv2.SIFT_create()

        # 找到关键点和描述符
        keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

        # 创建BFMatcher对象
        bf = cv2.BFMatcher(cv2.NORM_L2)

        # 进行匹配
        matches = bf.match(descriptors1, descriptors2)

        # 根据距离排序
        matches = sorted(matches, key=lambda x: x.distance)

        # 计算相似度分数，这里使用匹配点对距离的平均值
        if matches:
            similarity_score = np.mean([match.distance for match in matches])
        else:
            similarity_score = 0

        print(f"相似度分数（平均距离）: {similarity_score}")

    def calculate_feature(self, image_path: str) -> (cv2.KeyPoint, np.ndarray):
        image = cv2.imread(image_path)
        sift = cv2.SIFT_create()

        keypoints, descriptors = sift.detectAndCompute(image, None)
        return keypoints, descriptors

    def save_feature(self, keypoints: list[cv2.KeyPoint], descriptors: np.ndarray, file_path: str):
        fs = cv2.FileStorage(file_path, cv2.FILE_STORAGE_WRITE)
        # save keypoints object
        kp_array = keypoints_to_array(keypoints)
        fs.write("keypoints", kp_array)
        # save descriptors
        fs.write("descriptors", descriptors)
        fs.release()

    def read_feature(self, file_path: str) -> (list[cv2.KeyPoint], np.ndarray):
        fs = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)
        # read keypoints object
        kp_array = fs.getNode("keypoints").mat()
        keypoints = array_to_keypoints(kp_array)
        # read descriptors
        descriptors = fs.getNode("descriptors").mat()
        fs.release()
        return keypoints, descriptors




def keypoints_to_array(keypoints: list[cv2.KeyPoint]) -> np.ndarray:
    kp_list = [[kp.pt[0], kp.pt[1], kp.size, kp.angle, kp.response, kp.octave, kp.class_id] for kp in keypoints]
    kp_array = np.array(kp_list)
    return kp_array


def array_to_keypoints(kp_array: np.ndarray) -> list[cv2.KeyPoint]:
    keypoints = [
        cv2.KeyPoint(
            x=kp[0],
            y=kp[1],
            size=kp[2],
            angle=kp[3],
            response=kp[4],
            octave=int(kp[5]),
            class_id=int(kp[6])
        ) for kp in kp_array]
    return keypoints


image_service: ImageRecService = ImageRecService()

import sys

if 'pytest' in sys.modules:
    import pytest
    def test_feature_write():
        """
        rec and save files
        :return:
        """
        keypoints, desriptors = image_service.calculate_feature('../../sample/3.jpeg')
        print(keypoints[0].size)
        image_service.save_feature(keypoints, desriptors, '../../cache/keypoints.xml')


    def test_feature_read():
        """
        read image files
        :return:
        """
        keypoints, desriptors = image_service.read_feature('../../cache/keypoints.xml')
        print(keypoints[0].size)
