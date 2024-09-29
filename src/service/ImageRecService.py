import cv2
import numpy as np
import pickle

from numpy.ma.core import resize

from dao.PoiWIdentifiedImageDao import poi_w_identified_image_dao
from common.uuid import gen_uuid
from entity.po.PoiWIdentifyImagePo import PoiWIdentifyImagePo
from component.LogManager import log_manager

log = log_manager.get_logger(__name__)

# restrict image size
TARGET_WIDTH = 600
TARGET_HEIGHT = 800

HESSIAN_THRESHOLD = 4000


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

    async def recognize_with_select_poi(self, input_image: str, poi_uuid: str):
        """
        USED FOR TEST PURPOSE
        :param input_image:
        :param poi_uuid:
        :return:
        """
        # keypoints, descriptors = self.calculate_feature_orb(input_image)
        image = self.read_img(input_image)
        keypoints, descriptors = self.calculate_feature_surf(image)

        # get features from db
        result = await self.load_features_from_db(poi_uuid=poi_uuid)
        candidate = result[0]

        score = self.match(keypoints, candidate[0], descriptors, candidate[1])
        return score

    def match(self, keypoints1: list[cv2.KeyPoint], keypoints2: list[cv2.KeyPoint], descriptors1: np.ndarray,
              descriptors2: np.ndarray) -> int:
        """
        matching two images using bf matcher algorithm
        :param keypoints1:
        :param keypoints2:
        :param descriptors1:
        :param descriptors2:
        :return:
        """
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

    def show_match(self, image1: np.ndarray, image2: np.ndarray, keypoints1: list[cv2.KeyPoint],
                   keypoints2: list[cv2.KeyPoint], descriptors1: np.ndarray, descriptors2: np.ndarray):
        bf = cv2.BFMatcher(cv2.NORM_L2)

        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key=lambda x: x.distance)

        if len(matches) > 4:
            src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            matchesMask = mask.ravel().tolist()
            similarity_score = sum(matchesMask) / len(matchesMask) if matchesMask else 0
            print(similarity_score)

            matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches, None,
                                            matchesMask=matchesMask)
            cv2.imshow('image matching', matched_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return

    def read_img(self, image_path: str) -> np.ndarray:
        image = cv2.imread(image_path)
        return resize_img(image)

    def calculate_feature_sift(self, image: np.ndarray) -> (cv2.KeyPoint, np.ndarray):
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(image, None)
        return keypoints, descriptors

    def calculate_feature_orb(self, image: np.ndarray) -> (cv2.KeyPoint, np.ndarray):
        orb = cv2.ORB_create()
        keypoints = orb.detect(image, None)
        keypoints, descriptors = orb.compute(image, keypoints)
        return keypoints, descriptors

    def calculate_feature_surf(self, image: np.ndarray) -> (cv2.KeyPoint, np.ndarray):
        surf = cv2.xfeatures2d.SURF_create(hessianThreshold=HESSIAN_THRESHOLD)
        keypoints, descriptors = surf.detectAndCompute(image, None)
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

    async def save_features_to_db(self, keypoints: list[cv2.KeyPoint], descriptors: np.ndarray, poi_uuid: str, algorithm: str):
        serialized_array = pickle.dumps(keypoints_to_array(keypoints))
        serialized_descriptors = pickle.dumps(descriptors)
        new_uuid = gen_uuid()

        await poi_w_identified_image_dao.add(image_url='', algorithm=algorithm, keypoints=serialized_array,
                                             descriptors=serialized_descriptors, poi_uuid=poi_uuid,
                                             image_uuid=new_uuid)

    async def load_features_from_db(self, poi_uuid: str) -> list[tuple[list[cv2.KeyPoint], np.ndarray]]:
        result: list[PoiWIdentifyImagePo] = await poi_w_identified_image_dao.get_identified_images_by_poi(
            poi_uuid=poi_uuid)
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
        keypoints, descriptors = image_service.calculate_feature_sift('../../sample/3.jpeg')
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
        image = image_service.read_img('../../sample/2_crop.jpeg')
        # keypoints, descriptors  = image_service.calculate_feature_sift(image)
        # keypoints, descriptors = image_service.calculate_feature_orb(image)
        keypoints, descriptors = image_service.calculate_feature_surf(image)
        await image_service.save_features_to_db(keypoints, descriptors, 'test_poi2', 'surf')
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
        score = await image_service.recognize_with_select_poi('../../sample/2.jpeg', 'test_poi2_resized_surf_crop')
        print(score)


    def test_resize_img():
        image = cv2.imread('../../sample/2_pos.JPG')
        resized_img = resize_img(image)
        cv2.imshow('Resized Image', resized_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def test_show_orb_image_feature():
        image = image_service.read_img('../../sample/2_pos.jpeg')
        keypoints, descriptors = image_service.calculate_feature_sift(image)
        # 绘制关键点
        image_with_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0),
                                                 flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # 显示图片
        cv2.imshow('ORB Keypoints', image_with_keypoints)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def test_show_surf_image_feature():
        image = image_service.read_img('../../sample/2_crop.jpeg')
        keypoints, descriptors = image_service.calculate_feature_surf(image)
        # 绘制关键点
        image_with_keypoints = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0),
                                                 flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # 显示图片
        cv2.imshow('SURF Keypoints', image_with_keypoints)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def test_show_image_matching_surf():
        image1 = image_service.read_img('../../sample/2_crop.jpeg')
        image2 = image_service.read_img('../../sample/1.jpeg')

        keypoints1, descriptors1 = image_service.calculate_feature_surf(image1)
        keypoints2, descriptors2 = image_service.calculate_feature_surf(image2)

        image_service.show_match(image1, image2, keypoints1, keypoints2, descriptors1, descriptors2)


    def test_show_image_matching_sift():
        image1 = image_service.read_img('../../sample/cow_pos.jpeg')
        image2 = image_service.read_img('../../sample/yuqi_target.jpg')

        keypoints1, descriptors1 = image_service.calculate_feature_surf(image1)
        keypoints2, descriptors2 = image_service.calculate_feature_surf(image2)

        image_service.show_match(image1, image2, keypoints1, keypoints2, descriptors1, descriptors2)
