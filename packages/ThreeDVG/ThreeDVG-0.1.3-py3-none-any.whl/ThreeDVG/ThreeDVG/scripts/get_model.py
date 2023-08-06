import os
import sys
import torch

sys.path.append(os.path.join(os.getcwd())) # HACK add the root folder
from ..lib.config import CONF
from ..models.refnet import RefNet

def get_model(args, config):
    # load model
    input_channels = int(args.use_multiview) * 128 + int(args.use_normal) * 3 + int(args.use_color) * 3 + int(not args.no_height)
    model = RefNet(
        num_class=config.num_class,
        num_heading_bin=config.num_heading_bin,
        num_size_cluster=config.num_size_cluster,
        mean_size_arr=config.mean_size_arr,
        num_proposal=args.num_proposals,
        input_feature_dim=input_channels,
        use_lang_classifier=(not args.no_lang_cls),
        use_bidir=args.use_bidir,
        dataset_config=config,
    ).cuda()

    # model_name = "model_last.pth" if args.detection else "model.pth"
    # path = os.path.join(CONF.PATH.OUTPUT, args.folder, model_name)
    # model.load_state_dict(torch.load(path), strict=False)
    model.eval()

    return model