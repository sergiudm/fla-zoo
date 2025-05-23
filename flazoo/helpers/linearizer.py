from transformers import AutoModel, AutoConfig
from flazoo.helpers.initializer import (
    initialize_custom_mapping
)
import torch
import logging


"""
一些预制函数

This part is to init pre-defined FLA models using pretrained transformers.

This is for people who want to use FLA models. So the parts get inited are components in FLA models.

For example, SigLIP2 has some extra components like head.mlp.fc1.weight and head.mlp.fc12.weight \n

, which are not in FLA models. So they ignored. However, if you use linearized SigLIP2, you can use these extra components.

"""

def init_from_fla_vision_und(
    fla_model,
    another_fla_model,
    train_mlp: bool = True,
    init_embedding: bool = True,
    init_head: bool = True,
    return_pretrained: bool = False,
):
    """
    Initialize a FLA vision und model also from a FLA model \n
    Note that the two models should have the same architecture.

    Args:
        fla_model: FLA models to be initialized
        another_fla_model: FLA models to load
        train_mlp: Whether to train the MLP layers (default: True)
        init_embedding: Whether to initialize the embedding layers (default: True)
        init_head: Whether to initialize the head layers, useful for classification (default: True)
        return_pretrained: Whether to return the pretrained model (default: False)

    Returns:
        Initialized FLA model
    """
    # Define parameter mapping
    param_mapping = {
        "attn.q_proj": "attn.q_proj",
        "attn.k_proj": "attn.k_proj",
        "attn.v_proj": "attn.v_proj",
        "attn.o_proj": "attn.o_proj",
        "ln_1": "ln_1",
        "ln_2": "ln_2",
        "channel_mixer.net.0": "channel_mixer.net.0",
        "channel_mixer.net.2": "channel_mixer.net.2"
    }

    initialize_custom_mapping(
        model_a=fla_model,
        model_b=another_fla_model,
        param_mapping=param_mapping
    )

    if not train_mlp:
        for n, p in fla_model.named_parameters():
            if "channel_mixer" in n:
                p.requires_grad_(False)
    
    if init_embedding:
        logging.info("Initializing embedding layers, make sure your shapes match.")
        fla_model.embeddings.patch_embeddings.projection.weight.data.copy_(
            another_fla_model.embeddings.patch_embeddings.projection.weight.data
        )
        fla_model.embeddings.patch_embeddings.projection.bias.data.copy_(
            another_fla_model.embeddings.patch_embeddings.projection.bias.data
        )
        fla_model.embeddings.position_embeddings.data.copy_(
            another_fla_model.embeddings.position_embeddings.data
        )
        assert torch.equal(
            fla_model.embeddings.patch_embeddings.projection.weight,
            another_fla_model.embeddings.patch_embeddings.projection.weight
        )
        assert torch.equal(
            fla_model.embeddings.patch_embeddings.projection.bias,
            another_fla_model.embeddings.patch_embeddings.projection.bias
        )
        assert torch.equal(
            fla_model.embeddings.position_embeddings,
            another_fla_model.embeddings.position_embeddings
        )
    
    if init_head:
        fla_model.classifier.weight.data.copy_(
            another_fla_model.classifier.weight.data
        )
        if another_fla_model.classifier.bias is not None:
            fla_model.classifier.bias.data.copy_(
                another_fla_model.classifier.bias.data
            )

    if not return_pretrained:
        return fla_model
    else:
        return fla_model, another_fla_model



def init_from_dino2_base_p14(
    fla_model,
    dino_model: str = 'facebook/dinov2-base',
    train_mlp: bool = False,
    init_embedding: bool = True,
    return_pretrained: bool = False,
):
    """
    Initialize a FLA model from a DINO model. \n
    Note that dinov2-base use patch_size=14

    Args:
        fla_model: FLA models to be initialized
        dino_model: Name or path of the DINO model to load
        train_mlp: Whether to train the MLP layers (default: False)
        init_embedding: Whether to initialize the embedding layers (default: True)
        return_pretrained: Whether to return the pretrained model (default: False)
        
    Returns:
        Initialized FLA model
    """

    dino = AutoModel.from_pretrained(dino_model)
    
    # Define parameter mapping
    param_mapping = {
        "attn.q_proj": "attention.attention.query",
        "attn.k_proj": "attention.attention.key",
        "attn.v_proj": "attention.attention.value",
        "attn.o_proj": "attention.output.dense",
        "ln_1": "norm1",
        "ln_2": "norm2",
        "channel_mixer.net.0": "mlp.fc1",
        "channel_mixer.net.2": "mlp.fc2"
    }

    # Initialize parameters
    initialize_custom_mapping(
        model_a=fla_model,
        model_b=dino,
        param_mapping=param_mapping
    )

    # Optionally freeze MLP layers

    if not train_mlp:
        for n, p in fla_model.named_parameters():
            if "channel_mixer" in n:
                p.requires_grad_(False)

    if not return_pretrained:
        return fla_model
    else:
        return fla_model, dino


def init_from_dino2_small_p14(
        fla_model,
        dino_model: str = 'facebook/dinov2-small',
        train_mlp: bool = False,
        init_embedding: bool = True,
        return_pretrained: bool = False,
):
    """
    Initialize a FLA model from a DINO model. \n
    Note that dinov2-small use patch_size=14

    Args:
        fla_model: FLA models to be initialized
        dino_model: Name or path of the DINO model to load
        train_mlp: Whether to train the MLP layers (default: False)
        init_embedding: Whether to initialize the embedding layers (default: True)
        return_pretrained: Whether to return the pretrained model (default: False)

    Returns:

    """
    dino = AutoModel.from_pretrained(dino_model)

    # Define parameter mapping
    param_mapping = {
        "attn.q_proj": "attention.attention.query",
        "attn.k_proj": "attention.attention.key",
        "attn.v_proj": "attention.attention.value",
        "attn.o_proj": "attention.output.dense",
        "ln_1": "norm1",
        "ln_2": "norm2",
        "channel_mixer.net.0": "mlp.fc1",
        "channel_mixer.net.2": "mlp.fc2"
    }

    # Initialize parameters
    initialize_custom_mapping(
        model_a=fla_model,
        model_b=dino,
        param_mapping=param_mapping
    )

    # Optionally freeze MLP layers

    if not train_mlp:
        for n, p in fla_model.named_parameters():
            if "channel_mixer" in n:
                p.requires_grad_(False)
    
    if not return_pretrained:
        return fla_model
    else:
        return fla_model, dino

def init_from_siglip2_base_p16_224(
    fla_model,
    siglip_model: str = 'google/siglip2-base-patch16-224',
    train_mlp: bool = False,
    init_embedding: bool = True,
    init_head: bool = True,
    return_pretrained: bool = False,
):
    """
    Initialize a FLA model from a SigLIP2 model.

    Args:
        fla_model: FLA models to be initialized
        siglip_model: Name or path of the SigLIP2 model to load
        train_mlp: Whether to train the MLP layers (default: False)
        init_embedding: Whether to initialize the embedding layers (default: True)
        init_head: Whether to initialize the head layers, useful for classification (default: True)
        return_pretrained: Whether to return the pretrained model (default: False)

    Returns:
        Initialized FLA model
    """
    # Load SigLIP2 model and get vision component
    siglip = AutoModel.from_pretrained(siglip_model).vision_model
    
    # Define parameter mapping from FLA to SigLIP2
    param_mapping = {
        "attn.q_proj": "self_attn.q_proj",
        "attn.k_proj": "self_attn.k_proj",
        "attn.v_proj": "self_attn.v_proj",
        "attn.o_proj": "self_attn.out_proj",
        "ln_1": "layer_norm1",
        "ln_2": "layer_norm2",
        "channel_mixer.net.0": "mlp.fc1",
        "channel_mixer.net.2": "mlp.fc2"
    }

    # Initialize parameters
    initialize_custom_mapping(
        model_a=fla_model,
        model_b=siglip,
        param_mapping=param_mapping
    )

    if init_embedding:
        logging.info("Initializing embedding layers, make sure your shapes match.")
        fla_model.embeddings.patch_embeddings.projection.weight.data.copy_(
            siglip.embeddings.patch_embedding.weight.data
        )
        fla_model.embeddings.patch_embeddings.projection.bias.data.copy_(
            siglip.embeddings.patch_embedding.bias.data
        )
        
        fla_model.embeddings.position_embeddings.data.copy_(
            siglip.embeddings.position_embedding.weight.data.unsqueeze(0)
        )

        assert torch.equal(
            fla_model.embeddings.patch_embeddings.projection.weight,
            siglip.embeddings.patch_embedding.weight
        )
        assert torch.equal(
            fla_model.embeddings.patch_embeddings.projection.bias,
            siglip.embeddings.patch_embedding.bias
        )
        assert torch.equal(
            fla_model.embeddings.position_embeddings,
            siglip.embeddings.position_embedding.weight.unsqueeze(0)
        )

    # Optionally freeze MLP layers
    if not train_mlp:
        for n, p in fla_model.named_parameters():
            if "channel_mixer" in n:
                p.requires_grad_(False)
    
    if init_head:
        fla_model.classifier.weight.data.copy_(
            siglip.classifier.weight.data
        )
        if siglip.classifier.bias is not None:
            fla_model.classifier.bias.data.copy_(
                siglip.classifier.bias.data
            )

    if not return_pretrained:
        return fla_model
    else:
        return fla_model, siglip

def init_from_clip_base_p16_224(
        fla_model,
        clip_model: str = 'openai/clip-vit-base-patch16',
        train_mlp: bool = False,
        init_embedding: bool = True,
        return_pretrained: bool = False,
):
    """
    Initialize a FLA model from a CLIP model.

    Args:
        fla_model: FLA models to be initialized
        clip_model: Name or path of the clip model to load
        train_mlp: Whether to train the MLP layers (default: False)
        init_embedding: Whether to initialize the embedding layers (default: True)
        return_pretrained: Whether to return the pretrained model (default: False)

    Returns:
        Initialized FLA model
    """

    clip = AutoModel.from_pretrained(clip_model).vision_model

    param_mapping = {
        "attn.q_proj": "self_attn.q_proj",
        "attn.k_proj": "self_attn.k_proj",
        "attn.v_proj": "self_attn.v_proj",
        "attn.o_proj": "self_attn.out_proj",
        "ln_1": "layer_norm1",
        "ln_2": "layer_norm2",
        "channel_mixer.net.0": "mlp.fc1",
        "channel_mixer.net.2": "mlp.fc2"
    }

    initialize_custom_mapping(
        model_a=fla_model,
        model_b=clip,
        param_mapping=param_mapping
    )

    if init_embedding:
        # Copy patch embedding weights
        fla_model.embeddings.patch_embeddings.projection.weight.data.copy_(
            clip.embeddings.patch_embedding.weight.data
        )
        fla_model.embeddings.patch_embeddings.projection.bias.data.copy_(
            clip.embeddings.patch_embedding.bias.data
        )
        
        # Copy position embeddings, skipping the class token position (first token)
        # CLIP shape: (197, 768) -> (196, 768) -> (1, 196, 768)
        position_embeddings = clip.embeddings.position_embedding.weight.data[1:].unsqueeze(0)
        fla_model.embeddings.position_embeddings.data.copy_(position_embeddings)

        # Verify the copying was successful
        assert torch.equal(
            fla_model.embeddings.patch_embeddings.projection.weight,
            clip.embeddings.patch_embedding.weight
        )
        assert torch.equal(
            fla_model.embeddings.patch_embeddings.projection.bias,
            clip.embeddings.patch_embedding.bias
        )
        assert torch.equal(
            fla_model.embeddings.position_embeddings,
            clip.embeddings.position_embedding.weight[1:].unsqueeze(0)
        )

    # Optionally freeze MLP layers
    if not train_mlp:
        for n, p in fla_model.named_parameters():
            if "channel_mixer" in n:
                p.requires_grad_(False)

    if not return_pretrained:
        return fla_model
    else:
        return fla_model, clip
