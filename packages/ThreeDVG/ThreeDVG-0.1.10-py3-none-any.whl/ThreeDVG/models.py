import torch

from .ThreeDVG.scripts.get_model import get_model
from .ThreeDVG.data.scannet.model_util_scannet import ScannetDatasetConfig
import argparse

class MM3DVG():
    def __init__(self, args=None):
        super().__init__()
        if args == None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--num_proposals", type=int, default=256, help="Proposal number [default: 256]")
            parser.add_argument("--no_lang_cls", action="store_true", help="Do NOT use language classifier.")
            parser.add_argument("--use_bidir", action="store_true", help="Use bi-directional GRU.")
            parser.add_argument("--no_height", action="store_true", help="Do NOT use height signal in input.")
            parser.add_argument("--use_color", action="store_true", help="Use RGB color in input.")
            parser.add_argument("--use_normal", action="store_true", help="Use RGB color in input.")
            parser.add_argument("--use_multiview", action="store_true", help="Use multiview images.")
            
            args = parser.parse_args()
        self.config = ScannetDatasetConfig()
        self.model = get_model(args, self.config)

    @torch.no_grad()
    def inference(self, data_dict):
        data_dict = self.model(data_dict)
        bboxes = data_dict['pred_bboxes'].squeeze(0)
        bboxes = bboxes[data_dict['cluster_ref'].argmax(-1)]

        return bboxes
        