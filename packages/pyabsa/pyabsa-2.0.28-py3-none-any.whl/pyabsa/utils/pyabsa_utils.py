# -*- coding: utf-8 -*-
# file: pyabsa_utils.py
# time: 2021/5/20 0020
# author: yangheng <hy345@exeter.ac.uk>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os
import sys
import time

import torch
from autocuda import auto_cuda, auto_cuda_name
from termcolor import colored

from pyabsa import __version__ as pyabsa_version
from pyabsa.framework.flag_class.flag_template import DeviceTypeOption


def save_args(config, save_path):
    f = open(os.path.join(save_path), mode="w", encoding="utf8")
    for arg in config.args:
        if config.args_call_count[arg]:
            f.write("{}: {}\n".format(arg, config.args[arg]))
    f.close()


def print_args(config, logger=None):
    args = [key for key in sorted(config.args.keys())]
    for arg in args:
        if arg != "dataset" and arg != "dataset_dict" and arg != "embedding_matrix":
            if logger:
                try:
                    logger.info(
                        "{0}:{1}\t-->\tCalling Count:{2}".format(
                            arg, config.args[arg], config.args_call_count[arg]
                        )
                    )
                except:
                    logger.info(
                        "{0}:{1}\t-->\tCalling Count:{2}".format(
                            arg, config.args[arg], 0
                        )
                    )
            else:
                try:
                    fprint(
                        "{0}:{1}\t-->\tCalling Count:{2}".format(
                            arg, config.args[arg], config.args_call_count[arg]
                        )
                    )
                except:
                    fprint(
                        "{0}:{1}\t-->\tCalling Count:{2}".format(
                            arg, config.args[arg], 0
                        )
                    )


def validate_example(text: str, aspect: str, polarity: str, config):
    if len(text) < len(aspect):
        raise ValueError(
            "AspectLengthExceedTextError -> <aspect: {}> is longer than <text: {}>, <polarity: {}>".format(
                aspect, text, polarity
            )
        )

    if aspect.strip().lower() not in text.strip().lower():
        raise ValueError(
            "AspectNotInTextError -> <aspect: {}> is not in <text: {}>>".format(
                aspect, text
            )
        )

    warning = False

    if len(aspect.split(" ")) > 10:
        config.logger.warning(
            "AspectTooLongWarning -> <aspect: {}> is too long, <text: {}>, <polarity: {}>".format(
                aspect, text, polarity
            )
        )
        warning = True

    if not aspect.strip():
        raise ValueError(
            "AspectIsNullError -> <text: {}>, <aspect: {}>, <polarity: {}>".format(
                aspect, text, polarity
            )
        )

    if len(polarity.split(" ")) > 3:
        config.logger.warning(
            "LabelTooLongWarning -> <polarity: {}> is too long, <text: {}>, <aspect: {}>".format(
                polarity, text, aspect
            )
        )
        warning = True

    if not polarity.strip():
        raise ValueError(
            "PolarityIsNullError -> <text: {}>, <aspect: {}>, <polarity: {}>".format(
                aspect, text, polarity
            )
        )

    if text.strip() == aspect.strip():
        config.logger.warning(
            "AspectEqualsTextWarning -> <aspect: {}> equals <text: {}>, <polarity: {}>".format(
                aspect, text, polarity
            )
        )
        warning = True

    if not text.strip():
        raise ValueError(
            "TextIsNullError -> <text: {}>, <aspect: {}>, <polarity: {}>".format(
                aspect, text, polarity
            )
        )

    return warning


def check_and_fix_labels(label_set: set, label_name, all_data, config):
    # update output_dim, init model behind execution of this function!
    if "-100" in label_set:
        label_to_index = {
            origin_label: int(idx) - 1 if origin_label != "-100" else -100
            for origin_label, idx in zip(sorted(label_set), range(len(label_set)))
        }
        index_to_label = {
            int(idx) - 1 if origin_label != "-100" else -100: origin_label
            for origin_label, idx in zip(sorted(label_set), range(len(label_set)))
        }
    else:
        label_to_index = {
            origin_label: int(idx)
            for origin_label, idx in zip(sorted(label_set), range(len(label_set)))
        }
        index_to_label = {
            int(idx): origin_label
            for origin_label, idx in zip(sorted(label_set), range(len(label_set)))
        }
    if "index_to_label" not in config.args:
        config.index_to_label = index_to_label
        config.label_to_index = label_to_index

    if config.index_to_label != index_to_label:
        # raise KeyError('Fail to fix the labels, the number of labels are not equal among all datasets!')
        config.index_to_label.update(index_to_label)
        config.label_to_index.update(label_to_index)
    num_label = {label: 0 for label in label_set}
    num_label["Sum"] = len(all_data)
    for item in all_data:
        try:
            num_label[item[label_name]] += 1
            item[label_name] = label_to_index[item[label_name]]
        except Exception as e:
            # fprint(e)
            num_label[item.polarity] += 1
            item.polarity = label_to_index[item.polarity]
    config.logger.info("Dataset Label Details: {}".format(num_label))


def check_and_fix_IOB_labels(label_map, config):
    # update output_dim, init model behind execution of this function!
    index_to_IOB_label = {
        int(label_map[origin_label]): origin_label for origin_label in label_map
    }
    config.index_to_IOB_label = index_to_IOB_label


def set_device(config, auto_device):
    device_name = "Unknown"
    if isinstance(auto_device, str) and auto_device == DeviceTypeOption.ALL_CUDA:
        device = "cuda"
    elif isinstance(auto_device, str):
        device = auto_device
    elif isinstance(auto_device, bool):
        device = auto_cuda() if auto_device else DeviceTypeOption.CPU
    else:
        device = auto_cuda()
        try:
            torch.device(device)
        except RuntimeError as e:
            print(
                colored("Device assignment error: {}, redirect to CPU".format(e), "red")
            )
            device = DeviceTypeOption.CPU
    if device != DeviceTypeOption.CPU:
        device_name = auto_cuda_name()
    config.device = device
    config.device_name = device_name
    fprint("Set Model Device: {}".format(device))
    fprint("Device Name: {}".format(device_name))
    return device, device_name


def fprint(*objects, sep=" ", end="\n", file=sys.stdout, flush=False):
    print(
        time.strftime(
            "[%Y-%m-%d %H:%M:%S] ({})".format(pyabsa_version),
            time.localtime(time.time()),
        ),
        *objects,
        sep=sep,
        end=end,
        file=file,
        flush=flush
    )


def rprint(*objects, sep=" ", end="\n", file=sys.stdout, flush=False):
    print(
        time.strftime(
            "\n[%Y-%m-%d %H:%M:%S] ({})\n".format(pyabsa_version),
            time.localtime(time.time()),
        ),
        *objects,
        sep=sep,
        end=end,
        file=file,
        flush=flush
    )


def init_optimizer(optimizer):
    optimizers = {
        "adadelta": torch.optim.Adadelta,  # default lr=1.0
        "adagrad": torch.optim.Adagrad,  # default lr=0.01
        "adam": torch.optim.Adam,  # default lr=0.001
        "adamax": torch.optim.Adamax,  # default lr=0.002
        "asgd": torch.optim.ASGD,  # default lr=0.01
        "rmsprop": torch.optim.RMSprop,  # default lr=0.01
        "sgd": torch.optim.SGD,
        "adamw": torch.optim.AdamW,
        torch.optim.Adadelta: torch.optim.Adadelta,  # default lr=1.0
        torch.optim.Adagrad: torch.optim.Adagrad,  # default lr=0.01
        torch.optim.Adam: torch.optim.Adam,  # default lr=0.001
        torch.optim.Adamax: torch.optim.Adamax,  # default lr=0.002
        torch.optim.ASGD: torch.optim.ASGD,  # default lr=0.01
        torch.optim.RMSprop: torch.optim.RMSprop,  # default lr=0.01
        torch.optim.SGD: torch.optim.SGD,
        torch.optim.AdamW: torch.optim.AdamW,
    }
    if optimizer in optimizers:
        return optimizers[optimizer]
    elif hasattr(torch.optim, optimizer.__name__):
        return optimizer
    else:
        raise KeyError(
            "Unsupported optimizer: {}. "
            "Please use string or the optimizer objects in torch.optim as your optimizer".format(
                optimizer
            )
        )
