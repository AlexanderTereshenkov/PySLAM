import cv2
import numpy as np
import glob
from tqdm import tqdm
import logging

from utils.PinholeCamera import PinholeCamera


class WebcamLoader(object):
    default_config = {
        "root_path": "../test_imgs",
        "sequence": "00",
        "start": 0
    }

    def __init__(self, config={}):
        self.config = self.default_config
        self.config = {**self.config, **config}
        self.images = []
        logging.info("KITTI Dataset config: ")
        logging.info(self.config)

        if self.config["sequence"] in ["00", "01", "02"]:
            self.cam = PinholeCamera(1241.0, 376.0, 718.8560, 718.8560, 607.1928, 185.2157)
        elif self.config["sequence"] in ["03"]:
            self.cam = PinholeCamera(1242.0, 375.0, 721.5377, 721.5377, 609.5593, 172.854)
        elif self.config["sequence"] in ["04", "05", "06", "07", "08", "09", "10"]:
            self.cam = PinholeCamera(1226.0, 370.0, 707.0912, 707.0912, 601.8873, 183.1104)
        else:
            raise ValueError(f"Unknown sequence number: {self.config['sequence']}")

        # read ground truth pose
        self.pose_path = self.config["root_path"] + "/poses/" + self.config["sequence"] + ".txt"
        self.gt_poses = []
        with open(self.pose_path) as f:
            lines = f.readlines()
            for line in lines:
                ss = line.strip().split()
                pose = np.zeros((1, len(ss)))
                for i in range(len(ss)):
                    pose[0, i] = float(ss[i])

                pose.resize([3, 4])
                self.gt_poses.append(pose)

        # image id
        self.img_id = self.config["start"]
        self.img_N = 1_000_000
        self.cap = cv2.VideoCapture(0)

    def get_cur_pose(self):
        return self.gt_poses[self.img_id - 1]

    def __getitem__(self, item):
        #_, img = self.cap.read()
        img = self.images[item]
        return img

    def __iter__(self):
        return self

    def __next__(self):
        if self.img_id < self.img_N:
            img = self.cap.read()[1]
            self.images.append(img)
            self.img_id += 1
            return img
        raise StopIteration()

    def __len__(self):
        return self.img_N - self.config["start"]


if __name__ == "__main__":
    loader = WebcamLoader()

    for img in tqdm(loader):
        cv2.putText(img, "Press any key but Esc to continue, press Esc to exit", (10, 30),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, 8)
        cv2.imshow("img", img)
        # press Esc to exit
        if cv2.waitKey() == 27:
            break
