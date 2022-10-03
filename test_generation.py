import stable_diffusion as sd
import dotenv
import os
from argparse import ArgumentParser


def main():
    args = ArgumentParser()
    args.add_argument("--prompt", type=str)
    args.add_argument("--steps", type=int, default=25)
    args.add_argument("--init_image", type=str, default=None)
    args.add_argument("--mask_image", type=str, default=None)
    args.add_argument("--width", type=int, default=512)
    args.add_argument("--height", type=int, default=512)
    args.add_argument("--output", type=str, default="output2.png")
    args = args.parse_args()

    dotenv.load_dotenv()
    generator = sd.StableDiffusion(os.getenv("api_key"))

    image = generator.generate(
        prompt=args.prompt,
        steps=args.steps,
        init_image=args.init_image,
        mask_image=args.mask_image,
        width=args.width,
        height=args.height,
    )
    image.save(args.output)


if __name__ == "__main__":
    main()
