import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import sys
# sys.path.append(os.path.join(os.getcwd()))
# sys.path.append(os.path.join(os.getcwd(), 'scripts'))

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
        """ Forward pass of the network

        Args:
            data_dict: dict
                {
                    point_clouds,
                    lang_feat
                }

                point_clouds: Variable(torch.cuda.FloatTensor)
                    (B, N, 3 + input_channels) tensor
                    Point cloud to run predicts on
                    Each point in the point-cloud MUST
                    be formated as (x, y, z, features...)
        Returns:
            end_points: dict
        """
        data_dict = self.model(data_dict)
        return data_dict

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--num_proposals", type=int, default=256, help="Proposal number [default: 256]")
#     parser.add_argument("--no_lang_cls", action="store_true", help="Do NOT use language classifier.")
#     parser.add_argument("--use_bidir", action="store_true", help="Use bi-directional GRU.")
#     parser.add_argument("--no_height", action="store_true", help="Do NOT use height signal in input.")
#     parser.add_argument("--use_color", action="store_true", help="Use RGB color in input.")
#     parser.add_argument("--use_normal", action="store_true", help="Use RGB color in input.")
#     parser.add_argument("--use_multiview", action="store_true", help="Use multiview images.")

#     args = parser.parse_args()
#     MM3DVG()
        