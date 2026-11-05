from pydantic import BaseModel

from stream_notifier.shared import request_model_config, response_model_config

DEFAULT_VK_API_VERSION = "5.199"


class VKSendMessageRequest(BaseModel):
    message: str
    from_group: int
    owner_id: int
    v: str = DEFAULT_VK_API_VERSION

    model_config = request_model_config


class CreatedPost(BaseModel):
    post_id: int

    model_config = response_model_config


class VKSendMessageResponse(BaseModel):
    response: CreatedPost

    model_config = response_model_config
