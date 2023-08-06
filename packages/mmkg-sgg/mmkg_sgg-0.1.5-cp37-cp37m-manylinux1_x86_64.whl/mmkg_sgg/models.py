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
from pathlib import Path
class SGG(nn.Module):
    def __init__(self):
        super().__init__()

        # parser = argparse.ArgumentParser(description="SGG for Graph")
        args_ = {
            'opts': [
                'MODEL.DEVICE', 'cuda',
                'MODEL.META_ARCHITECTURE', "RelationPredictor",
                'MODEL.USE_FREQ_PRIOR', False,
                'MODEL.FREQ_PRIOR', "visualgenome/label_danfeiX_clipped.freq_prior.npy",
                'MODEL.RESNETS.TRANS_FUNC', "BottleneckWithFixedBatchNorm",
                'MODEL.RESNETS.BACKBONE_OUT_CHANNELS', 256,
                'MODEL.BACKBONE.CONV_BODY', "R-50-FPN",
                'MODEL.ATTRIBUTE_ON', False,
                'MODEL.RELATION_ON', True,
                'MODEL.RPN.USE_FPN', True,
                'MODEL.RPN.ANCHOR_STRIDE', (4, 8, 16, 32, 64),
                'MODEL.RPN.PRE_NMS_TOP_N_TRAIN', 2000,
                'MODEL.RPN.PRE_NMS_TOP_N_TEST', 1000,
                'MODEL.RPN.POST_NMS_TOP_N_TEST', 1000,
                'MODEL.RPN.FPN_POST_NMS_TOP_N_TEST', 1000,
                'MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE', 512,
                'MODEL.ROI_HEADS.POSITIVE_FRACTION', 0.5,
                'MODEL.ROI_HEADS.USE_FPN', True,
                'MODEL.ROI_HEADS.SCORE_THRESH', 0.05,
                'MODEL.ROI_HEADS.DETECTIONS_PER_IMG', 100,
                'MODEL.ROI_HEADS.MIN_DETECTIONS_PER_IMG', 1,
                'MODEL.ROI_BOX_HEAD.NUM_CLASSES', 151,
                'MODEL.ROI_BOX_HEAD.POOLER_RESOLUTION', 7,
                'MODEL.ROI_BOX_HEAD.POOLER_SCALES', (0.25, 0.125, 0.0625, 0.03125),
                'MODEL.ROI_BOX_HEAD.POOLER_SAMPLING_RATIO', 2,
                'MODEL.ROI_BOX_HEAD.FEATURE_EXTRACTOR', "FPN2MLPFeatureExtractor",
                'MODEL.ROI_BOX_HEAD.PREDICTOR', "FPNPredictor",
                'MODEL.ROI_BOX_HEAD.MLP_HEAD_DIM', 1024,
                'MODEL.ATTRIBUTE_ON', False,
                'MODEL.RELATION_ON', True,
                'MODEL.ROI_RELATION_HEAD.DETECTOR_PRE_CALCULATED', False,
                'MODEL.ROI_RELATION_HEAD.FORCE_RELATIONS', False,
                'MODEL.ROI_RELATION_HEAD.ALGORITHM', "sg_imp",
                'MODEL.ROI_RELATION_HEAD.MODE', 'sgdet',
                'MODEL.ROI_RELATION_HEAD.USE_BIAS', False,
                'MODEL.ROI_RELATION_HEAD.FILTER_NON_OVERLAP', True,
                'MODEL.ROI_RELATION_HEAD.UPDATE_BOX_REG', False,
                'MODEL.ROI_RELATION_HEAD.SHARE_CONV_BACKBONE', False,
                'MODEL.ROI_RELATION_HEAD.SHARE_BOX_FEATURE_EXTRACTOR', False,
                'MODEL.ROI_RELATION_HEAD.SEPERATE_SO_FEATURE_EXTRACTOR', False,
                'MODEL.ROI_RELATION_HEAD.NUM_CLASSES', 51,
                'MODEL.ROI_RELATION_HEAD.POOLER_RESOLUTION', 7,
                'MODEL.ROI_RELATION_HEAD.POOLER_SCALES', (0.25, 0.125, 0.0625, 0.03125),
                'MODEL.ROI_RELATION_HEAD.POOLER_SAMPLING_RATIO', 2,
                'MODEL.ROI_RELATION_HEAD.FEATURE_EXTRACTOR', "FPN2MLPRelationFeatureExtractor",
                'MODEL.ROI_RELATION_HEAD.PREDICTOR', "FPNRelationPredictor",
                'MODEL.ROI_RELATION_HEAD.CONTRASTIVE_LOSS.USE_FLAG', False,
                'MODEL.ROI_RELATION_HEAD.TRIPLETS_PER_IMG', 100,
                'MODEL.ROI_RELATION_HEAD.POSTPROCESS_METHOD', 'constrained',
                'MODEL.ROI_RELATION_HEAD.IMP_FEATURE_UPDATE_STEP', 2,
                'INPUT.MIN_SIZE_TRAIN', (600,),
                'INPUT.MAX_SIZE_TRAIN', 1000,
                'INPUT.MIN_SIZE_TEST', 600,
                'INPUT.MAX_SIZE_TEST', 1000,
                'INPUT.PIXEL_MEAN', [103.530, 116.280, 123.675],
                'DATASETS.FACTORY_TRAIN', ("VGTSVDataset",),
                'DATASETS.FACTORY_TEST', ("VGTSVDataset",),
                'DATASETS.TRAIN', ("visualgenome/train_danfeiX_relation_nm.yaml",),
                'DATASETS.TEST', ("visualgenome/test_danfeiX_relation.yaml",),
                'DATALOADER.SIZE_DIVISIBILITY', 32,
                'DATALOADER.NUM_WORKERS', 4,
                'SOLVER.BASE_LR', 0.015,
                'SOLVER.WEIGHT_DECAY', 0.0001,
                'SOLVER.MAX_ITER', 40000,
                'SOLVER.STEPS', (20000,30000),
                'SOLVER.IMS_PER_BATCH', 16,
                'SOLVER.CHECKPOINT_PERIOD', 5000,
                'TEST.IMS_PER_BATCH', 8,
                'TEST.SAVE_PREDICTIONS', False,
                'TEST.SAVE_RESULTS_TO_TSV', True,
                'TEST.TSV_SAVE_SUBSET', ['rect', 'class', 'conf', 'relations', 'relation_scores', 'relation_scores_all'],
                'TEST.GATHER_ON_CPU', True,
                'TEST.SKIP_PERFORMANCE_EVAL', False,
                'TEST.OUTPUT_RELATION_FEATURE', False,
                'TEST.OUTPUT_FEATURE', True,
                'OUTPUT_DIR', "./models/relation_danfeiX_FPN50/",
                'DATA_DIR', ".",
                'DISTRIBUTED_BACKEND', 'gloo'
            ],
            'mode': 'relation',
            'ckpt': "",
        }

        args = EasyDict(args_)
        # if args.mode == 'entity':
        #     args.config_file = str(Path(__file__).parent / "sgg_configs" / "vgattr" / "vinvl_x152c4.yaml")
        # elif args.mode  == 'relation':
        #     args.config_file = str(Path(__file__).parent / "sgg_configs" / "vg_vrd" /"config.yaml")
        # else:
        #     raise NotImplementedError(args)

        cfg.set_new_allowed(True)
        cfg.merge_from_other_cfg(sg_cfg)
        cfg.set_new_allowed(False)
        # print(args.config_file, type(args.config_file))
        # cfg.merge_from_file(args.config_file)

        cfg.merge_from_list(args.opts)
        cfg.freeze()

        # print(cfg)

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