# You may need to restart your runtime prior to this, to let your installation take effect
# Some basic setup:
# Setup detectron2 logger


# import some common libraries

# import some common detectron2 utilities
# import detectron2
import cv2
import numpy as np
from src.dataset import check_colab


class HumanDetector:
    __config_manager = None
    __predictor = None

    def __init__(self):
        try:
            from detectron2.utils.logger import setup_logger
            setup_logger()
            self.__init_configuration_model()
        except ImportError:
            print('\nThe environment is not compatible with detectron2 const!!\n')

    def __init_configuration_model(self):
        try:
            from detectron2.config import get_cfg
            from detectron2 import model_zoo

            self.__config_manager = get_cfg()

            # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
            self.__config_manager.merge_from_file(
                model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_C4_3x.yaml"))
            self.__config_manager.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9  # set threshold for this model

            # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
            self.__config_manager.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                "COCO-Detection/faster_rcnn_R_50_C4_3x.yaml")
            self.__predictor = self.__get_model_predictor(self.__config_manager)

        except ImportError as e:
            print('\nThe environment is not compatible with detectron2 init!!\n', str(e))

    def __get_model_predictor(self, config_manager):
        try:
            from detectron2.engine import DefaultPredictor

            predictor = DefaultPredictor(config_manager)
            return predictor
        except ImportError:
            print('\nThe environment is not compatible with detectron2 model!!\n')

    def get_persons_from_model(self, img):
        try:
            outputs = self.__predictor(img)
            classes = outputs['instances'].pred_classes.cpu().numpy()
            # print(classes)
            bbox = outputs['instances'].pred_boxes.tensor.cpu().numpy()
            # print(bbox)
            # identity only persons
            ind = np.where(classes == 0)[0]
            # identify bounding box of only persons
            person = bbox[ind]
            # total no. of persons
            num = len(person)
            # print('Total number of persons in the image: ' + str(num))
            return person
        except:
            return []

    def visualize_predicted_image(self, img):
        try:
            from detectron2.utils.visualizer import Visualizer
            from detectron2.data import MetadataCatalog

            outputs = self.__predictor(img)

            # Use `Visualizer` to draw the predictions on the image.
            visual = Visualizer(img[:, :, ::-1], MetadataCatalog.get(self.__config_manager.DATASETS.TRAIN[0]),
                                scale=1.2)
            visual = visual.draw_instance_predictions(outputs["instances"].to("cpu"))
            if check_colab():
                try:
                    from google.colab.patches import cv2_imshow
                    cv2_imshow(visual.get_image()[:, :, ::-1])
                except ImportError:
                    cv2.imshow('Human Detection', visual.get_image()[:, :, ::-1])
        except ImportError:
            print('\nThe environment is not compatible with detectron2!!\n')
