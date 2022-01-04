# coding:utf8
import os
import sys
import cv2
import numpy as np
import tensorflow as tf
sys.path.append("..")

from utils import label_map_util
from utils import visualization_utils as vis_util


class TOD(object):
    def __init__(self):
        # Path to frozen detection graph. This is the actual model that is used for the object detection.
        self.PATH_TO_CKPT = os.path.join(os.path.join('myFinalModelPB','frozen_inference_graph.pb'))
        # List of the strings that is used to add correct label for each box.
        self.PATH_TO_LABELS = os.path.join('training', 'object-detection.pbtxt')

        self.NUM_CLASSES = 90

        self.detection_graph = self._load_model()
        self.category_index = self._load_label_map()

    def _load_model(self):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph

    def _load_label_map(self):
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        return category_index

    def detect(self, image):
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image, axis=0)
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    self.category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)

        while True:
            cv2.namedWindow("detection", cv2.WINDOW_NORMAL)
            cv2.imshow("detection", image)
            if cv2.waitKey(110) & 0xff == 27:
                break


if __name__ == '__main__':
    TEST_IMAGE_PATHS=[]
    for filename in os.listdir(r"./test_images"):
        if filename.split('.')[-1]=='jpg':
            #TEST_IMAGE_PATHS.append(os.path.join(os.path.join('test_images',filename)))
            aa=os.path.join(os.path.join('test_images',filename))
            image = cv2.imread(aa)
            detecotr = TOD()
            detecotr.detect(image)
