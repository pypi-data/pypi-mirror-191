from typing import Optional

import os
import logging
import glob
import xml.etree.ElementTree as ET

from .pascal.shared import getTag, getBoxes, toFloat
from ..base_converter import BaseConverter
from ...annotation import CoretexImageAnnotation, CoretexSegmentationInstance, BBox


class VOCConverter(BaseConverter):

    def __init__(self, datasetName: str, projectId: int, datasetPath: str) -> None:
        super().__init__(datasetName, projectId, datasetPath)

        self.__imagesPath = os.path.join(datasetPath, "images")

        annotations = os.path.join(datasetPath, "annotations")
        self.__fileNames = glob.glob(os.path.join(annotations, "*.xml"))

    def _dataSource(self) -> list[str]:
        return self.__fileNames

    def _extractLabels(self) -> set[str]:
        labels: set[str] = set()

        for filename in self.__fileNames:
            tree = ET.parse(filename)
            root = tree.getroot()
            objects = root.findall("object")

            for obj in objects:
                labelElement = obj.find("name")
                if labelElement is None:
                    continue

                label = labelElement.text
                if label is None:
                    continue

                labels.add(label)

        return labels

    def __extractInstance(self, obj: ET.Element) -> Optional[CoretexSegmentationInstance]:
        label = getTag(obj, "name")
        if label is None:
            return None

        coretexClass = self._dataset.classByName(label)
        if coretexClass is None:
            logging.getLogger("coretexpylib").info(f">> [Coretex] Class: ({label}) is not a part of dataset")
            return None

        bboxElement = obj.find('bndbox')
        if bboxElement is None:
            return None

        encodedBbox = getBoxes(bboxElement)
        if encodedBbox is None:
            return None

        bbox = BBox.decode(encodedBbox)
        return CoretexSegmentationInstance.create(coretexClass.classIds[0], bbox, [bbox.polygon])

    def _extractImageAnnotation(self, root: ET.Element) -> None:
        fileName = getTag(root, "filename")
        if fileName is None:
            return

        size = root.find('size')
        if size is None:
            return

        width, height = toFloat(size, "width", "height")
        if width is None or height is None:
            return

        coretexAnnotation = CoretexImageAnnotation.create(fileName, width, height, [])

        for obj in root.findall("object"):
            instance = self.__extractInstance(obj)
            if instance is None:
                continue

            coretexAnnotation.instances.append(instance)

        self._saveImageAnnotationPair(os.path.join(self.__imagesPath, fileName), coretexAnnotation)

    def _extractSingleAnnotation(self, fileName: str) -> None:
        tree = ET.parse(fileName)
        root = tree.getroot()

        self._extractImageAnnotation(root)
