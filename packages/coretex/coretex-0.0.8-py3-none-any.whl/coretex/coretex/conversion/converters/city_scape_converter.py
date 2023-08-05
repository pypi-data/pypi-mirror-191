from typing import Any, Optional
from pathlib import Path

import glob
import os
import json
import logging

import numpy as np

from ..base_converter import BaseConverter
from ...annotation import CoretexImageAnnotation, CoretexSegmentationInstance, BBox


class CityScapeConverter(BaseConverter):

    """
        Represents the Converter from City Scape Format to Cortex Format
    """

    def __init__(self, datasetName: str, projectId: int, datasetPath: str) -> None:
        super().__init__(datasetName, projectId, datasetPath)

        self.__baseImagePath = os.path.join(datasetPath, "leftImg8bit_trainvaltest", "leftImg8bit")
        self.__baseAnnotationsPaths = [
            os.path.join(datasetPath, "gtFine_trainvaltest", "gtFine", "train"),
            os.path.join(datasetPath, "gtFine_trainvaltest", "gtFine", "val")
        ]

        self.__imagePaths: list[str] = []
        self.__imagePaths.extend(glob.glob(f"{self.__baseImagePath}/train/*/*.png"))
        self.__imagePaths.extend(glob.glob(f"{self.__baseImagePath}/val/*/*.png"))

    def __annotationPathFor(self, imagePath: str) -> str:
        # Extract last 2 components of imagePath
        annotationName = os.path.sep.join(Path(imagePath).parts[-2:])

        # Replace image specific name with annotation name
        annotationName = annotationName.replace("leftImg8bit.png", "gtFine_polygons.json")

        for annotationsPath in self.__baseAnnotationsPaths:
            annotationPath = os.path.join(annotationsPath, annotationName)

            if os.path.exists(annotationPath):
                return annotationPath

        raise RuntimeError

    def _dataSource(self) -> list[str]:
        return self.__imagePaths

    def _extractLabels(self) -> set[str]:
        labels: set[str] = set()

        for imagePath in self.__imagePaths:
            annotationPath = self.__annotationPathFor(imagePath)

            with open(annotationPath, mode="r") as annotationFile:
                annotationData: dict[str, Any] = json.load(annotationFile)

                for obj in annotationData["objects"]:
                    labels.add(obj["label"])

        return labels

    def __extractInstance(self, obj: dict[str, Any]) -> Optional[CoretexSegmentationInstance]:
        label = obj["label"]

        coretexClass = self._dataset.classByName(label)
        if coretexClass is None:
            logging.getLogger("coretexpylib").info(f">> [Coretex] Class: ({label}) is not a part of dataset")
            return None

        polygon = np.array(obj["polygon"]).flatten().tolist()

        return CoretexSegmentationInstance.create(
            coretexClass.classIds[0],
            BBox.fromPoly(polygon),
            [polygon]
        )

    def __extractImageAnnotation(self, imagePath: str, annotationData: dict[str, Any]) -> None:
        imageName = Path(imagePath).stem
        width = annotationData["imgWidth"]
        height = annotationData["imgHeight"]

        coretexAnnotation = CoretexImageAnnotation.create(imageName, width, height, [])

        for obj in annotationData["objects"]:
            instance = self.__extractInstance(obj)
            if instance is None:
                continue

            coretexAnnotation.instances.append(instance)

        self._saveImageAnnotationPair(imagePath, coretexAnnotation)

    def _extractSingleAnnotation(self, imagePath: str) -> None:
        annotationPath = self.__annotationPathFor(imagePath)

        with open(annotationPath, mode="r") as annotationFile:
            annotationData: dict[str, Any] = json.load(annotationFile)
            self.__extractImageAnnotation(imagePath, annotationData)
