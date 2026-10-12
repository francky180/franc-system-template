# Character consistency

To keep the same character, face, wardrobe, or visual style across multiple generations, pass earlier output images as references via `--input-image` on the image command.

**Important: use the edit variant when passing references.** The default `nano-banana-pro` is text-to-image only and silently ignores `image_urls`. For reference-driven generation, pass `--model nano-banana-pro-edit` (maps to `fal-ai/nano-banana-pro/edit`).

## Workflow

1. Generate the first image normally (the "anchor" — the character's establishing shot). Save the path.
2. For each subsequent generation of the *same* character, pass the anchor (and optionally other strong prior frames) and switch to the edit model:

   ```bash
   python3 ~/.claude/skills/media-gen/scripts/generate.py image \
     --prompt "<new scene, same character>" \
     --title "<series-title>" \
     --model nano-banana-pro-edit \
     --input-image "<path to anchor image-01.png>" \
     [--input-image "<path to other prior frame>" ...]
   ```

   (Windows: `python` + full script path.)

3. Phrase the prompt as *"the same man from the reference image, now [doing new action / in new setting]"*. Don't redescribe the character's face; let the reference carry it. Describe the new scene, lighting, pose, and mood.
4. The script copies each reference into the output folder as `source-<filename>` for provenance.

## When to use

- Multi-shot Reels/Shorts where the same person appears in different scenes.
- Building a consistent look across a campaign (same palette, same wardrobe).
- Iterating on a single character with small variations of the same anchor.

## When NOT to use

- One-off images with no continuity needs (it just slows the gen).
- When you *want* a different person or style — references will fight your prompt.

## Limits

- Only the **image** command accepts references. Image-to-video models (Kling, Seedance) take a single input image to animate; no additional refs.
- More than ~3 references muddies results. Pass the strongest 1-2 anchors.
- References are uploaded to Fal each run; the script enforces Fal's 10 MB upload limit and will tell you to downscale if an anchor is over it (2K anchors stay well under).
