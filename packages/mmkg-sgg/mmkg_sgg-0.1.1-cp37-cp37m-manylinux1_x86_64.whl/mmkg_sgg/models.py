import torch
import os.path as op
import argparse
import json
from tqdm import tqdm
from typing import Callable, Optional, Tuple
from easydict import EasyDict

from .relation_predictor.relation_predictor import RelationPredictor
from .relation_predictor.AttrRCNN import AttrRCNN
from .maskrcnn_benchmark.data.transforms import build_transforms
from .maskrcnn_benchmark.utils.checkpoint import DetectronCheckpointer
from .maskrcnn_benchmark.config import cfg
from .relation_predictor.config import sg_cfg
from .maskrcnn_benchmark.data.datasets.utils.load_files import \
    config_dataset_file
from .maskrcnn_benchmark.data.datasets.utils.load_files import load_labelmap_file
from .maskrcnn_benchmark.utils.miscellaneous import mkdir
from PIL import Image
from torchvision import transforms 

from .mm.graph import MMGraph
from .mm.graph import ImageViewEntity, HasEntity, Interact

import torch.nn as nn

class SGG(nn.Module):
    def __init__(self):
        super().__init__()

        # parser = argparse.ArgumentParser(description="SGG for Graph")
        args_ = {
            'opts': ['MODEL.DEVICE', 'cuda'],
            'mode': 'relation',
            'ckpt': "",
        }

        args = EasyDict(args_)
        if args.mode == 'entity':
            args.config_file = './mmkg_sgg/sgg_configs/vgattr/vinvl_x152c4.yaml'
        elif args.mode  == 'relation':
            args.config_file = './mmkg_sgg/sgg_configs/vg_vrd/config.yaml'
        else:
            raise NotImplementedError(args)

        cfg.set_new_allowed(True)
        cfg.merge_from_other_cfg(sg_cfg)
        cfg.set_new_allowed(False)
        cfg.merge_from_file(args.config_file)
        cfg.merge_from_list(args.opts)
        cfg.freeze()

        print(cfg)

        # output_dir = cfg.OUTPUT_DIR
        # mkdir(output_dir)

        self.device = cfg.MODEL.DEVICE

        if cfg.MODEL.META_ARCHITECTURE == "RelationPredictor":
            self.model = RelationPredictor(cfg)
        elif cfg.MODEL.META_ARCHITECTURE == "AttrRCNN":
            self.model = AttrRCNN(cfg)
        self.model.to(cfg.MODEL.DEVICE)
        self.model.eval()
        
        # checkpointer = DetectronCheckpointer(cfg, self.model, save_dir=output_dir)
        # checkpointer.load(cfg.MODEL.WEIGHT)

        # dataset labelmap is used to convert the prediction to class labels
        # dataset_labelmap_file = config_dataset_file(cfg.DATA_DIR,
        #                                             cfg.DATASETS.LABELMAP_FILE)
        # assert dataset_labelmap_file
        # self.dataset_allmap = json.load(open(dataset_labelmap_file, 'r'))
        # self.dataset_labelmap = {int(val): key
        #                     for key, val in self.dataset_allmap['label_to_idx'].items()}
        # # visual_labelmap is used to select classes for visualization
        # try:
        #     self.visual_labelmap = load_labelmap_file(args_.labelmap_file)
        # except:
        #     self.visual_labelmap = None

        # if cfg.MODEL.ATTRIBUTE_ON:
        #     self.dataset_attr_labelmap = {
        #             int(val): key for key, val in
        #             self.dataset_allmap['attribute_to_idx'].items()}
        
        # if cfg.MODEL.RELATION_ON:
        #     self.dataset_relation_labelmap = {
        #             int(val): key for key, val in
        #             self.dataset_allmap['predicate_to_idx'].items()}

        # self.transforms = build_transforms(cfg, is_train=False)

    def preprocess(self, image_path, meta):
        image = Image.open(image_path)
        transform = transforms.Compose([
            transforms.Resize(meta['image_size']), 
            transforms.ToTensor(), 
            
        ])
        image = transform(image)
        return image

    @torch.no_grad()
    def inference(self, image_path, meta):
        image = self.preprocess(image_path, meta)
        # image = self.preprocess(image).unsqueeze(0).to(self.device)
        image = image.unsqueeze(0).to(self.device)

        prediction = self.model(image)
        prediction = prediction[0].to(torch.device("cpu"))

        img_height, img_width = meta['image_size']

        prediction_pred = prediction.prediction_pairs
        relations = prediction_pred.get_field("idx_pairs").tolist()
        relation_scores = prediction_pred.get_field("scores").tolist()
        predicates = prediction_pred.get_field("labels").tolist()
        prediction = prediction.predictions

        prediction = prediction.resize((img_width, img_height))
        boxes = prediction.bbox.tolist()
        classes = prediction.get_field("labels").tolist()
        scores = prediction.get_field("scores").tolist()

        rt_box_list = []
        if 'attr_scores' in prediction.extra_fields:
            attr_scores = prediction.get_field("attr_scores")
            attr_labels = prediction.get_field("attr_labels")
            rt_box_list = [
                {"rect": box, "class": cls, "conf": score,
                "attr": attr[attr_conf > 0.01].tolist(),
                "attr_conf": attr_conf[attr_conf > 0.01].tolist()}
                for box, cls, score, attr, attr_conf in
                zip(boxes, classes, scores, attr_labels, attr_scores)
            ]
        else:
            rt_box_list = [
                {"rect": box, "class": cls, "conf": score}
                for box, cls, score in
                zip(boxes, classes, scores)
            ]
        rt_relation_list = [{"subj_id": relation[0], "obj_id":relation[1], "class": predicate+1, "conf": score}
                for relation, predicate, score in
                zip(relations, predicates, relation_scores)]
        return {'objects': rt_box_list, 'relations':rt_relation_list}


if __name__ == "__main__":
    SGG()
    image_path = 'test.jpg'
    meta = {'image_size': (224, 224)}
    output = m.inference(image_path, meta)