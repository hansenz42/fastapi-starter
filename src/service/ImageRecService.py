import cv2
import numpy as np
import pickle
from dao.PoiWIdentifiedImageDao import poi_w_identified_image_dao
from common.uuid import gen_uuid
from entity.po.PoiWIdentifyImagePo import PoiWIdentifyImagePo
from component.LogManager import log_manager

log = log_manager.get_logger(__name__)

TARGET_WIDTH = 600
TARGET_HEIGHT = 800

def resize_img(image: np.ndarray) -> np.ndarray:
    orig_width, orig_height = image.shape[1], image.shape[0]
    aspect_ratio = orig_width / orig_height

    if aspect_ratio > 1:  # width larger than height, resize according to width
        new_width = TARGET_WIDTH
        new_height = int(TARGET_WIDTH / aspect_ratio)
    else:  # otherwise...
        new_height = TARGET_HEIGHT
        new_width = int(TARGET_HEIGHT * aspect_ratio)

    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized_image

class ImageRecService:
    def __init__(self):
        pass

    async def recognize_with_select_po(self, input_image: str, poi_uuid: str):
        """
        USED FOR TEST PURPOSE
        :param input_image:
        :param poi_uuid:
        :return:
        """
        input_img = cv2.imread(input_image, cv2.IMREAD_GRAYSCALE)

        # calculated selected image features
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(input_img, None)

        # get features from db
        result = await self.load_features_from_db(poi_uuid=poi_uuid)
        candidate = result[0]

        score = self.match(keypoints, candidate[0], descriptors, candidate[1])
        return score

    def match(self, keypoints1, keypoints2, descriptors1, descriptors2) -> int:
        bf = cv2.BFMatcher(cv2.NORM_L2)

        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key=lambda x: x.distance)

        if len(matches) > 4:
            src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            similarity_score = sum(matchesMask) / len(matchesMask) if matchesMask else 0
        else:
            raise Exception(f"cannot get matches between two images, match num is smaller than 4")

        return similarity_score

    def calculate_feature(self, image_path: str) -> (cv2.KeyPoint, np.ndarray):
        image = cv2.imread(image_path)
        sift = cv2.SIFT_create()

        keypoints, descriptors = sift.detectAndCompute(image, None)
        log.debug("calculated feature from image file, image_path=%s", image_path)
        return keypoints, descriptors

    def save_feature_to_file(self, keypoints: list[cv2.KeyPoint], descriptors: np.ndarray, file_path: str):
        fs = cv2.FileStorage(file_path, cv2.FILE_STORAGE_WRITE)
        # save keypoints object
        kp_array = keypoints_to_array(keypoints)
        fs.write("keypoints", kp_array)
        # save descriptors
        fs.write("descriptors", descriptors)
        fs.release()

    def read_feature_to_file(self, file_path: str) -> (list[cv2.KeyPoint], np.ndarray):
        fs = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)
        # read keypoints object
        kp_array = fs.getNode("keypoints").mat()
        keypoints = array_to_keypoints(kp_array)
        # read descriptors
        descriptors = fs.getNode("descriptors").mat()
        fs.release()
        return keypoints, descriptors

    async def save_features_to_db(self, keypoints: list[cv2.KeyPoint], descriptors: np.ndarray, poi_uuid: str):
        serialized_array = pickle.dumps(keypoints_to_array(keypoints))
        serialized_descriptors = pickle.dumps(descriptors)
        new_uuid = gen_uuid()

        await poi_w_identified_image_dao.add_identified_image(image_url='', keypoints=serialized_array,
                                                              descriptors=serialized_descriptors, poi_uuid=poi_uuid,
                                                              image_uuid=new_uuid)

    async def load_features_from_db(self, poi_uuid: str) -> list[tuple[list[cv2.KeyPoint], np.ndarray]]:
        result: list[PoiWIdentifyImagePo] = await poi_w_identified_image_dao.get_identified_images_by_poi(poi_uuid=poi_uuid)
        ret: list[tuple[list[cv2.KeyPoint], np.ndarray]] = []
        for item in result:
            kp_array = pickle.loads(item.keypoints)
            kp = array_to_keypoints(kp_array)
            descriptors: np.ndarray = pickle.loads(item.descriptors)
            ret.append((kp, descriptors))
        return ret

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


    def test_feature_save_file():
        """
        rec and save files
        :return:
        """
        keypoints, descriptors = image_service.calculate_feature('../../sample/3.jpeg')
        print(keypoints[0].size)
        image_service.save_feature_to_file(keypoints, descriptors, '../../cache/keypoints.xml')


    def test_feature_load_file():
        """
        read image files
        :return:
        """
        keypoints, descriptors = image_service.read_feature_to_file('../../cache/keypoints.xml')
        print(keypoints[0].size)

    @pytest.mark.asyncio
    async def test_feature_save_db():
        """
        :return:
        """
        keypoints, descriptors  = image_service.calculate_feature('../../sample/2.jpg')
        await image_service.save_features_to_db(keypoints, descriptors, 'test_poi2')
        print('done')

    @pytest.mark.asyncio
    async def test_feature_load_db():
        result = await image_service.load_features_from_db('test_poi1')
        print(result)


    @pytest.mark.asyncio
    async def test_recognize_with_select_po():
        """
        :return:
        """
        score = await image_service.recognize_with_select_po('../../sample/2_pos.jpg', 'test_poi2')
        print(score)

    def test_resize_img():
        image = cv2.imread('../../sample/2_pos.JPG')
        resized_img = resize_img(image)
        cv2.imshow('Resized Image', resized_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()