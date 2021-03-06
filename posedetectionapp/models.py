from django.db import models
from .utils import output_keypoints, output_keypoints_with_lines
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your models here.
class Pose(models.Model):
    image = models.ImageField(upload_to='image/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # 이미지 열기
        pil_img = Image.open(self.image)

        # np array 변환
        cv_img = np.array(pil_img)


        # 모델 위치
        protoFile_body_25 = os.path.join(BASE_DIR,"model/pose_deploy.prototxt")
        weightsFile_body_25 = os.path.join(BASE_DIR,"model/pose_iter_584000.caffemodel")

        BODY_PARTS_BODY_25 = {0: "Nose", 1: "Neck", 2: "RShoulder", 3: "RElbow", 4: "RWrist",
                              5: "LShoulder", 6: "LElbow", 7: "LWrist", 8: "MidHip", 9: "RHip",
                              10: "RKnee", 11: "RAnkle", 12: "LHip", 13: "LKnee", 14: "LAnkle",
                              15: "REye", 16: "LEye", 17: "REar", 18: "LEar", 19: "LBigToe",
                              20: "LSmallToe", 21: "LHeel", 22: "RBigToe", 23: "RSmallToe", 24: "RHeel",
                              25: "Background"}

        POSE_PAIRS_BODY_25 = [[5, 18], [0, 15], [0, 16], [1, 2], [1, 5], [1, 8], [8, 9], [8, 12], [9, 10], [12, 13],
                              [2, 3],
                              [3, 4], [5, 6], [6, 7], [10, 11], [13, 14], [15, 17], [16, 18], [14, 21], [19, 21],
                              [20, 21],
                              [11, 24], [22, 24], [23, 24]]

        frame_man = output_keypoints(frame=cv_img, proto_file=protoFile_body_25, weights_file=weightsFile_body_25,
                                     threshold=0.1, model_name='', BODY_PARTS=BODY_PARTS_BODY_25)
        img = output_keypoints_with_lines(POSE_PAIRS=POSE_PAIRS_BODY_25, frame=frame_man)

        # convert back to pil image
        im_pil = Image.fromarray(img)

        # 저장
        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()

        self.image.save(str(self.image), ContentFile(image_png), save=False)

        super().save(*args,**kwargs)