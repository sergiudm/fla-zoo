# -*- coding: utf-8 -*-

from typing import Dict, Optional, Union, List

from transformers.configuration_utils import PretrainedConfig

class RWKV7VisionConfig(PretrainedConfig):

    model_type = 'rwkv7_vision'

    def __init__(
        self,
        # RWKV7 core parameters
        attn_mode: str = "chunk",
        hidden_size: int = 2048,
        num_hidden_layers: int = 24,
        head_dim: Optional[int] = 64,
        num_heads: Optional[int] = None,
        decay_low_rank_dim: int = 64,
        gate_low_rank_dim: int = 128,
        a_low_rank_dim: int = 64,
        v_low_rank_dim: int = 16,
        hidden_act: str = "sqrelu",
        norm_first: bool = True,
        norm_bias: bool = True,
        norm_eps: float = 1e-5,
        attn: Optional[Dict] = None,
        initializer_range: float = 0.006,
        fuse_norm: bool = True,
        fuse_cross_entropy: bool = True,
        value_dim: Optional[Union[int, List[int]]] = None,
        attn_type: str = "full_attn", # attention type, default to "full_attn"
        gradient_checkpointing: bool = False,
        # Vision specific parameters
        image_size: int = 224,
        patch_size: int = 16,
        num_channels: int = 3,
        num_classes: int = 1000,
        qkv_bias: bool = True,
        hidden_dropout_prob: float = 0.0,
        use_mask_token: bool = False,
        layer_norm_eps: float = 1e-6,
        interpolate_pos_encoding: bool = False,
        channel_mixer_dim: int = None,
        encoder_stride=16,
        train_scan_type: str = "uni-scan", # scaning type, "uni-scan" or "bi-scan" or "cross-scan", default to "uni-scan"
        test_scan_type: str = None, # scaning type, "uni-scan" or "bi-scan" or "cross-scan", default to "uni-scan"
        **kwargs
    ):
        # Initialize RWKV7 core parameters
        self.attn_mode = attn_mode
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.head_dim = head_dim
        self.num_heads = num_heads
        self.decay_low_rank_dim = decay_low_rank_dim
        self.gate_low_rank_dim = gate_low_rank_dim
        self.a_low_rank_dim = a_low_rank_dim
        self.v_low_rank_dim = v_low_rank_dim
        self.hidden_act = hidden_act
        self.norm_first = norm_first
        self.norm_bias = norm_bias
        self.norm_eps = norm_eps
        self.initializer_range = initializer_range
        self.fuse_norm = fuse_norm
        self.fuse_cross_entropy = fuse_cross_entropy
        self.value_dim = value_dim
        self.attn_type = attn_type
        self.gradient_checkpointing = gradient_checkpointing

        # Initialize vision specific parameters
        self.image_size = image_size
        self.patch_size = patch_size
        self.num_channels = num_channels
        self.num_classes = num_classes
        self.qkv_bias = qkv_bias
        self.hidden_dropout_prob = hidden_dropout_prob
        self.use_mask_token = use_mask_token
        self.layer_norm_eps = layer_norm_eps
        self.interpolate_pos_encoding = interpolate_pos_encoding
        self.train_scan_type = train_scan_type
        
        if test_scan_type is None:
            self.test_scan_type = train_scan_type
        else:
            self.test_scan_type = test_scan_type
        self.encoder_stride = encoder_stride

        if attn is not None:
            if not isinstance(attn, Dict):
                raise ValueError("attn must be a dictionary")
            if 'layers' not in attn:
                raise ValueError("Layer indices must be provided to initialize hybrid attention layers")
            if 'num_heads' not in attn:
                raise ValueError("Number of heads must be provided to initialize hybrid attention layers")
            attn['num_kv_heads'] = attn.get('num_kv_heads', attn['num_heads'])
            attn['window_size'] = attn.get('window_size', None)

        if value_dim is None:
            value_dim = [hidden_size] * num_hidden_layers
        elif isinstance(value_dim, int):
            assert value_dim >= hidden_size, "value_dim must be greater than hidden_size"
            assert value_dim % hidden_size == 0, "value_dim must be divisible by hidden_size"
            value_dim = [value_dim] * num_hidden_layers
        else:
            assert len(value_dim) == num_hidden_layers, "value_dim must have the same length as num_hidden_layers"
            for v in value_dim:
                assert v >= hidden_size, "value_dim must be greater than hidden_size"
                assert v % hidden_size == 0, "value_dim must be divisible by hidden_size"
        
        self.value_dim = value_dim

        self.attn = attn

        if channel_mixer_dim is None:
            self.channel_mixer_dim = 4 * hidden_size # default value set to 4 * hidden_size
        else:
            self.channel_mixer_dim = channel_mixer_dim
        
        super().__init__(**kwargs)

class RWKV7VideoConfig(PretrainedConfig):

    model_type = 'rwkv7_video'

    def __init__(
        self,
        # RWKV7 core parameters
        attn_mode: str = "chunk",
        hidden_size: int = 2048,
        num_hidden_layers: int = 24,
        head_dim: Optional[int] = 64,
        num_heads: Optional[int] = None,
        decay_low_rank_dim: int = 64,
        gate_low_rank_dim: int = 128,
        a_low_rank_dim: int = 64,
        v_low_rank_dim: int = 16,
        hidden_act: str = "sqrelu",
        norm_first: bool = True,
        norm_bias: bool = True,
        norm_eps: float = 1e-5,
        attn: Optional[Dict] = None,
        initializer_range: float = 0.006,
        fuse_norm: bool = True,
        fuse_cross_entropy: bool = True,
        value_dim: Optional[Union[int, List[int]]] = None,
        attn_type: str = "full_attn", # attention type, default to "full_attn"
        gradient_checkpointing: bool = False,
        # Video specific parameters
        image_size: int = 224,
        patch_size: int = 16,
        num_channels: int = 3,
        num_classes: int = 1000,
        hidden_dropout_prob: float = 0.0,
        use_mask_token: bool = False,
        layer_norm_eps: float = 1e-6,
        interpolate_pos_encoding: bool = False,
        encoder_stride=16,
        channel_mixer_dim: int = None,
        train_scan_type: str = "uni-scan", # scaning type, "uni-scan" or "bi-scan" or "cross-scan", default to "uni-scan"
        test_scan_type: str = None, # scaning type, "uni-scan" or "bi-scan" or "cross-scan", default to "uni-scan"
        norm_pix_loss: bool = True,
        num_frames: int = 16,
        tubelet_size: int = 2,

        # decoder specific parameters
        decoder_num_heads: int = 6,
        decoder_hidden_size: int = 256,
        decoder_num_hidden_layers: int = 4,
        decoder_channel_mixer_dim: int = None,
        **kwargs
    ):
        # Initialize RWKV7 core parameters
        self.attn_mode = attn_mode
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.head_dim = head_dim
        self.num_heads = num_heads
        self.decay_low_rank_dim = decay_low_rank_dim
        self.gate_low_rank_dim = gate_low_rank_dim
        self.a_low_rank_dim = a_low_rank_dim
        self.v_low_rank_dim = v_low_rank_dim
        self.hidden_act = hidden_act
        self.norm_first = norm_first
        self.norm_bias = norm_bias
        self.norm_eps = norm_eps
        self.initializer_range = initializer_range
        self.fuse_norm = fuse_norm
        self.fuse_cross_entropy = fuse_cross_entropy
        self.value_dim = value_dim
        self.attn_type = attn_type
        self.gradient_checkpointing = gradient_checkpointing

        # Initialize video specific parameters
        self.image_size = image_size
        self.patch_size = patch_size
        self.num_channels = num_channels
        self.num_classes = num_classes
        self.hidden_dropout_prob = hidden_dropout_prob
        self.use_mask_token = use_mask_token
        self.layer_norm_eps = layer_norm_eps
        self.interpolate_pos_encoding = interpolate_pos_encoding
        self.train_scan_type = train_scan_type
        
        if test_scan_type is None:
            self.test_scan_type = train_scan_type
        else:
            self.test_scan_type = test_scan_type
        self.encoder_stride = encoder_stride
        self.norm_pix_loss = norm_pix_loss
        self.num_frames = num_frames
        self.tubelet_size = tubelet_size

        # Initialize decoder specific parameters
        self.decoder_num_heads = decoder_num_heads
        self.decoder_hidden_size = decoder_hidden_size
        self.decoder_num_hidden_layers = decoder_num_hidden_layers


        if attn is not None:
            if not isinstance(attn, Dict):
                raise ValueError("attn must be a dictionary")
            if 'layers' not in attn:
                raise ValueError("Layer indices must be provided to initialize hybrid attention layers")
            if 'num_heads' not in attn:
                raise ValueError("Number of heads must be provided to initialize hybrid attention layers")
            attn['num_kv_heads'] = attn.get('num_kv_heads', attn['num_heads'])
            attn['window_size'] = attn.get('window_size', None)
        
        self.attn = attn


        if value_dim is None:
            value_dim = [hidden_size] * num_hidden_layers
        elif isinstance(value_dim, int):
            assert value_dim >= hidden_size, "value_dim must be greater than hidden_size"
            assert value_dim % hidden_size == 0, "value_dim must be divisible by hidden_size"
            value_dim = [value_dim] * num_hidden_layers
        else:
            assert len(value_dim) == num_hidden_layers, "value_dim must have the same length as num_hidden_layers"
            for v in value_dim:
                assert v >= hidden_size, "value_dim must be greater than hidden_size"
                assert v % hidden_size == 0, "value_dim must be divisible by hidden_size"

        self.value_dim = value_dim

        if channel_mixer_dim is None:
            self.channel_mixer_dim = 4 * hidden_size # default value set to 4 * hidden_size
        else:
            self.channel_mixer_dim = channel_mixer_dim
        
        if decoder_channel_mixer_dim is None:
            self.decoder_channel_mixer_dim = 4 * decoder_hidden_size
        else:
            self.decoder_channel_mixer_dim = decoder_channel_mixer_dim # default value set to 4 * decoder_hidden_size

        super().__init__(**kwargs)