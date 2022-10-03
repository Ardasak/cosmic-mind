import io
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


class StableDiffusion:
    def __init__(self, api_key):
        self.api = client.StabilityInference(key=api_key)

    def generate(
        self, prompt, steps=25, init_image=None, mask_image=None, width=512, height=512
    ):
        if init_image is not None:
            init_image = Image.open(init_image)
            init_image = init_image.resize((width, height))
            init_image = init_image.convert("RGB")

        if mask_image is not None:
            mask_image = Image.open(mask_image)
            mask_image = mask_image.resize((width, height))
            mask_image = mask_image.convert("RGB")

        answers = self.api.generate(
            prompt=prompt,
            steps=steps,
            init_image=init_image,
            mask_image=mask_image,
            width=width,
            height=height,
        )

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    return "Safety filter triggered"
                if artifact.type == generation.ARTIFACT_IMAGE:
                    return Image.open(io.BytesIO(artifact.binary))
