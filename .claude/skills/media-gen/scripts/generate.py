"""Media-gen skill: Fal.ai image and video generation.

Usage (invoked by Claude Code via SKILL.md, but also runnable standalone):

  python generate.py image --prompt "<text>" --title "<slug>" [--model KEY]
                           [--aspect-ratio 16:9] [--resolution 2K]

  python generate.py video --image <path> --prompt "<text>" --title "<slug>"
                           --folder <existing folder> [--model KEY]
                           [--duration 5] [--resolution 1080p]

  python generate.py upscale --input <path> [--target-height 1080] [--factor N]
                             [--fps 30] [--type video|image] [--model KEY]

Returns a JSON line on stdout with paths.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

FAL_UPLOAD_LIMIT_BYTES = 10 * 1024 * 1024


def _import_fal_client():
    """Import fal_client, self-installing it on first run if missing.

    Tries a plain pip install first (works in venvs and on Windows), then
    --user, then --user --break-system-packages (Homebrew/Debian Python
    marks itself externally-managed per PEP 668 and rejects the first two).
    """
    try:
        import fal_client
        return fal_client
    except ImportError:
        pass
    sys.stderr.write("[media-gen] fal-client not installed; installing it now (one-time)...\n")
    sys.stderr.flush()
    base = [sys.executable, "-m", "pip", "install", "--quiet", "fal-client"]
    for extra in ([], ["--user"], ["--user", "--break-system-packages"]):
        try:
            subprocess.run(base + extra, check=True, capture_output=True)
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    try:
        import fal_client
        return fal_client
    except ImportError:
        sys.stderr.write(
            "ERROR: couldn't install fal-client automatically.\n"
            "  Install it manually, then retry:\n"
            "    Windows: python -m pip install fal-client\n"
            "    Mac/Linux: python3 -m pip install --user --break-system-packages fal-client\n"
        )
        sys.exit(2)


fal_client = _import_fal_client()


SKILL_ROOT = Path(__file__).resolve().parent.parent


def load_config() -> tuple[dict, dict]:
    config = json.loads((SKILL_ROOT / "config.json").read_text(encoding="utf-8"))
    models = json.loads((SKILL_ROOT / "models.json").read_text(encoding="utf-8"))
    try:
        from datetime import date
        updated = models.get("last_updated", "")
        age = (date.today() - date.fromisoformat(updated)).days
        sys.stderr.write(f"[media-gen] model registry last updated {updated} ({age} days ago)\n")
    except (ValueError, TypeError):
        pass
    return config, models


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s[:50] or "untitled"


def expand_path(p: str) -> Path:
    return Path(os.path.expanduser(os.path.expandvars(p)))


def get_or_make_folder(output_dir: Path, working_title: str) -> Path:
    date = time.strftime("%Y-%m-%d")
    folder = output_dir / f"{date}-{slugify(working_title)}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def next_index(folder: Path, kind: str, ext: str) -> int:
    """Return next free index for image-NN.png / video-NN.mp4."""
    pat = re.compile(rf"^{kind}-(\d+)\.{ext}$")
    used = []
    for f in folder.iterdir():
        m = pat.match(f.name)
        if m:
            used.append(int(m.group(1)))
    return (max(used) + 1) if used else 1


def download(url: str, dest: Path, timeout: int = 120) -> None:
    """Download with a socket timeout and one retry so a stalled CDN can't hang forever."""
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp, dest.open("wb") as f:
                shutil.copyfileobj(resp, f)
            return
        except Exception:
            if attempt == 2:
                raise
            sys.stderr.write("[media-gen] download stalled; retrying once...\n")
            sys.stderr.flush()


def check_upload_size(path: Path) -> None:
    """Fal rejects reference-image uploads over 10 MB. Fail fast with a fix."""
    size = path.stat().st_size
    if size > FAL_UPLOAD_LIMIT_BYTES:
        sys.stderr.write(
            f"ERROR: {path.name} is {size / (1024 * 1024):.1f} MB — over Fal's 10 MB upload limit.\n"
            "  Downscale the image first (2K resolution is plenty for a reference) and retry.\n"
        )
        sys.exit(7)


def deep_get(obj, dotted: str):
    """Resolve 'images[0].url' or 'video.url' against a dict."""
    cur = obj
    for part in dotted.split("."):
        m = re.match(r"^(\w+)\[(\d+)\]$", part)
        if m:
            cur = cur[m.group(1)][int(m.group(2))]
        else:
            cur = cur[part]
    return cur


def require_fal_key() -> None:
    if os.environ.get("FAL_KEY"):
        return
    # Fallback: a plain-text key file in the home folder. Works identically on
    # both OSes and in non-interactive shells where ~/.zshrc never loads.
    key_file = Path.home() / ".fal_key"
    if key_file.is_file():
        key = key_file.read_text(encoding="utf-8").strip()
        if key:
            os.environ["FAL_KEY"] = key
            return
    sys.stderr.write(
        "ERROR: FAL_KEY not set.\n"
        "  Easiest (Mac + Windows): save your key as the only line of a file named `.fal_key`\n"
        "  in your home folder (Mac: ~/.fal_key | Windows: C:\\Users\\<you>\\.fal_key).\n"
        "  Or set the env var:\n"
        "    Windows: setx FAL_KEY \"<your-key>\"  (then restart terminal)\n"
        "    Mac/Linux: add `export FAL_KEY=\"<your-key>\"` to ~/.zshrc, then `source ~/.zshrc`\n"
    )
    sys.exit(3)


def write_prompt_md(folder: Path, payload: dict) -> None:
    """Append-friendly metadata file."""
    md = folder / "prompt.md"
    if not md.exists():
        md.write_text(
            f"# {payload.get('working_title', folder.name)}\n\n"
            f"**Created:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n",
            encoding="utf-8",
        )
    with md.open("a", encoding="utf-8") as f:
        kind = payload["kind"]
        f.write(f"\n## {kind.title()} generation\n\n")
        f.write(f"- **Model:** `{payload['fal_id']}`\n")
        f.write(f"- **File:** `{payload['filename']}`\n")
        for k, v in payload.get("args", {}).items():
            f.write(f"- **{k}:** {v}\n")
        f.write(f"\n### {kind.title()} prompt\n\n{payload['prompt']}\n")


def cmd_image(args) -> None:
    require_fal_key()
    config, models = load_config()
    output_dir = expand_path(config["output_dir"])

    img_cfg = models["image"]
    key = args.model or img_cfg["default"]
    if key not in img_cfg["models"]:
        sys.stderr.write(f"ERROR: unknown image model key '{key}'. Available: {list(img_cfg['models'])}\n")
        sys.exit(4)

    spec = img_cfg["models"][key]
    fal_id = spec["fal_id"]
    call_args = dict(spec.get("default_args", {}))
    call_args["prompt"] = args.prompt
    if args.aspect_ratio:
        call_args["aspect_ratio"] = args.aspect_ratio
    if args.resolution:
        call_args["resolution"] = args.resolution

    input_image_urls: list[str] = []
    if args.input_image:
        for raw in args.input_image:
            ip = expand_path(raw)
            if not ip.is_file():
                sys.stderr.write(f"ERROR: input image not found: {ip}\n")
                sys.exit(5)
            check_upload_size(ip)
            sys.stderr.write(f"[media-gen] Uploading reference image: {ip.name}\n")
            sys.stderr.flush()
            input_image_urls.append(fal_client.upload_file(str(ip)))
        call_args["image_urls"] = input_image_urls

    folder = get_or_make_folder(output_dir, args.title)
    idx = next_index(folder, "image", "png")
    filename = f"image-{idx:02d}.png"
    out_path = folder / filename

    sys.stderr.write(f"[media-gen] Generating image with {fal_id}...\n")
    sys.stderr.flush()

    result = fal_client.subscribe(fal_id, arguments=call_args, with_logs=False)

    try:
        url = deep_get(result, spec["output_path"])
    except (KeyError, IndexError, TypeError) as e:
        sys.stderr.write(
            f"ERROR: couldn't resolve output_path '{spec['output_path']}' on result.\n"
            f"Raw result: {json.dumps(result, default=str)[:1000]}\n"
        )
        raise

    download(url, out_path)
    write_prompt_md(folder, {
        "kind": "image",
        "fal_id": fal_id,
        "filename": filename,
        "prompt": args.prompt,
        "working_title": args.title,
        "args": {k: v for k, v in call_args.items() if k != "prompt"},
    })

    if args.input_image:
        for raw in args.input_image:
            ip = expand_path(raw)
            try:
                shutil.copy2(ip, folder / f"source-{ip.name}")
            except Exception:
                pass

    print(json.dumps({
        "image_path": str(out_path),
        "folder": str(folder),
        "model": fal_id,
        "fal_url": url,
    }))


def cmd_video(args) -> None:
    require_fal_key()
    config, models = load_config()

    vid_cfg = models["video_image_to_video"]
    key = args.model or vid_cfg["default"]
    if key not in vid_cfg["models"]:
        sys.stderr.write(f"ERROR: unknown video model key '{key}'. Available: {list(vid_cfg['models'])}\n")
        sys.exit(4)

    spec = vid_cfg["models"][key]
    fal_id = spec["fal_id"]

    folder = expand_path(args.folder)
    if not folder.is_dir():
        sys.stderr.write(f"ERROR: folder does not exist: {folder}\n")
        sys.exit(5)

    image_path = expand_path(args.image)
    if not image_path.is_file():
        sys.stderr.write(f"ERROR: image not found: {image_path}\n")
        sys.exit(5)
    check_upload_size(image_path)

    sys.stderr.write(f"[media-gen] Uploading reference image to Fal...\n")
    sys.stderr.flush()
    image_url = fal_client.upload_file(str(image_path))

    call_args = dict(spec.get("default_args", {}))
    call_args["image_url"] = image_url
    call_args["prompt"] = args.prompt
    if args.duration is not None:
        call_args["duration"] = args.duration
    if args.resolution:
        call_args["resolution"] = args.resolution

    idx = next_index(folder, "video", "mp4")
    filename = f"video-{idx:02d}.mp4"
    out_path = folder / filename

    sys.stderr.write(f"[media-gen] Generating video with {fal_id} (this can take 1-3 min)...\n")
    sys.stderr.flush()

    result = fal_client.subscribe(fal_id, arguments=call_args, with_logs=False)

    try:
        url = deep_get(result, spec["output_path"])
    except (KeyError, IndexError, TypeError):
        sys.stderr.write(
            f"ERROR: couldn't resolve output_path '{spec['output_path']}' on result.\n"
            f"Raw result: {json.dumps(result, default=str)[:1000]}\n"
        )
        raise

    download(url, out_path)
    write_prompt_md(folder, {
        "kind": "video",
        "fal_id": fal_id,
        "filename": filename,
        "prompt": args.prompt,
        "working_title": args.title,
        "args": {k: v for k, v in call_args.items() if k not in ("prompt", "image_url")},
    })

    print(json.dumps({
        "video_path": str(out_path),
        "folder": str(folder),
        "model": fal_id,
        "fal_url": url,
    }))


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}


def _ffprobe_stream(path: Path) -> dict:
    """Return {width, height, fps} for a media file via ffprobe. Empty dict if ffprobe missing/fails."""
    if not shutil.which("ffprobe"):
        return {}
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,r_frame_rate",
             "-of", "json", str(path)],
            capture_output=True, text=True, check=True,
        ).stdout
        st = json.loads(out)["streams"][0]
        fps = None
        rate = st.get("r_frame_rate", "")
        if "/" in rate:
            num, den = rate.split("/")
            if float(den) != 0:
                fps = float(num) / float(den)
        return {"width": int(st["width"]), "height": int(st["height"]), "fps": fps}
    except Exception:
        return {}


def _transcode_fps(src: Path, target_fps: int, work_dir: Path) -> Path:
    """Re-encode src to target_fps with libx264 (universal). Returns new path, or src if ffmpeg missing."""
    if not shutil.which("ffmpeg"):
        sys.stderr.write("[media-gen] ffmpeg not found; skipping fps change.\n")
        return src
    dst = work_dir / f"_fps{target_fps}-{src.stem}.mp4"
    sys.stderr.write(f"[media-gen] Pre-converting to {target_fps}fps to control upscale cost...\n")
    sys.stderr.flush()
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-r", str(target_fps),
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-c:a", "copy", str(dst)],
        capture_output=True, check=True,
    )
    return dst


def cmd_upscale(args) -> None:
    require_fal_key()
    config, models = load_config()
    output_dir = expand_path(config["output_dir"])

    in_path = expand_path(args.input)
    if not in_path.is_file():
        sys.stderr.write(f"ERROR: input file not found: {in_path}\n")
        sys.exit(5)

    ext = in_path.suffix.lower()
    if args.type:
        is_video = args.type == "video"
    elif ext in VIDEO_EXTS:
        is_video = True
    elif ext in IMAGE_EXTS:
        is_video = False
    else:
        sys.stderr.write(
            f"ERROR: can't infer media type from extension '{ext}'. Pass --type video or --type image.\n"
        )
        sys.exit(6)
    reg_key = "upscale_video" if is_video else "upscale_image"
    cfg = models[reg_key]
    key = args.model or cfg["default"]
    if key not in cfg["models"]:
        sys.stderr.write(f"ERROR: unknown {reg_key} model key '{key}'. Available: {list(cfg['models'])}\n")
        sys.exit(4)
    spec = cfg["models"][key]
    fal_id = spec["fal_id"]

    # Determine upscale_factor. ALWAYS a single scalar applied to both axes,
    # so aspect ratio is preserved and the result can never stretch.
    probe = _ffprobe_stream(in_path)
    if args.factor is not None:
        factor = float(args.factor)
    elif probe.get("height"):
        factor = round(args.target_height / probe["height"], 4)
    else:
        sys.stderr.write(
            "ERROR: couldn't read source height (ffprobe missing) and no --factor given.\n"
            "  Pass --factor (e.g. 2) or install ffmpeg/ffprobe.\n"
        )
        sys.exit(6)
    factor = max(1.0, min(factor, 8.0))  # Topaz supports up to 8x

    upload_path = in_path
    work_title = args.title or slugify(in_path.stem)
    folder = get_or_make_folder(output_dir, work_title)

    # Optional fps downconvert (video only) to stay on the cheaper Topaz tier.
    if is_video and args.fps is not None and probe.get("fps"):
        if abs(probe["fps"] - args.fps) > 0.5:
            upload_path = _transcode_fps(in_path, args.fps, folder)

    src_dims = f'{probe.get("width","?")}x{probe.get("height","?")}'
    out_h = int(round(probe["height"] * factor)) if probe.get("height") else None
    out_w = int(round(probe["width"] * factor)) if probe.get("width") else None
    sys.stderr.write(
        f"[media-gen] Upscaling {src_dims} by {factor}x"
        + (f" -> ~{out_w}x{out_h}" if out_w else "")
        + f" via {fal_id}...\n"
    )
    sys.stderr.flush()

    src_url = fal_client.upload_file(str(upload_path))
    call_args = dict(spec.get("default_args", {}))
    call_args["upscale_factor"] = factor
    if is_video:
        call_args["video_url"] = src_url
        if args.fps is not None and not (probe.get("fps")):
            call_args["target_fps"] = args.fps
    else:
        call_args["image_url"] = src_url

    result = fal_client.subscribe(fal_id, arguments=call_args, with_logs=False)
    try:
        url = deep_get(result, spec["output_path"])
    except (KeyError, IndexError, TypeError):
        sys.stderr.write(
            f"ERROR: couldn't resolve output_path '{spec['output_path']}' on result.\n"
            f"Raw result: {json.dumps(result, default=str)[:1000]}\n"
        )
        raise

    out_ext = "mp4" if is_video else "png"
    idx = next_index(folder, "upscaled", out_ext)
    filename = f"upscaled-{idx:02d}.{out_ext}"
    out_path = folder / filename
    download(url, out_path)

    # Clean up any temp fps file.
    if upload_path != in_path:
        try:
            upload_path.unlink()
        except Exception:
            pass

    write_prompt_md(folder, {
        "kind": "upscale",
        "fal_id": fal_id,
        "filename": filename,
        "prompt": f"Upscale of {in_path.name} (source {src_dims}, factor {factor}x)",
        "working_title": work_title,
        "args": {k: v for k, v in call_args.items() if k not in ("video_url", "image_url")},
    })

    print(json.dumps({
        "upscaled_path": str(out_path),
        "folder": str(folder),
        "model": fal_id,
        "factor": factor,
        "source_dims": src_dims,
        "fal_url": url,
    }))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="media-gen")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("image", help="Generate an image from a prompt")
    pi.add_argument("--prompt", required=True)
    pi.add_argument("--title", required=True, help="Working title slug")
    pi.add_argument("--model", default=None, help="Override model key from models.json")
    pi.add_argument("--aspect-ratio", dest="aspect_ratio", default=None)
    pi.add_argument("--resolution", default=None)
    pi.add_argument("--input-image", dest="input_image", action="append", default=None,
                    help="Path to a reference image for image-to-image editing. "
                         "Repeat the flag to pass multiple references.")
    pi.set_defaults(func=cmd_image)

    pv = sub.add_parser("video", help="Animate an existing image into video")
    pv.add_argument("--image", required=True, help="Path to reference image")
    pv.add_argument("--prompt", required=True, help="Motion prompt")
    pv.add_argument("--title", required=True, help="Working title (for prompt.md)")
    pv.add_argument("--folder", required=True, help="Existing generation folder")
    pv.add_argument("--model", default=None)
    pv.add_argument("--duration", type=int, default=None)
    pv.add_argument("--resolution", default=None)
    pv.set_defaults(func=cmd_video)

    pu = sub.add_parser("upscale", help="Upscale a video or image with Topaz (aspect-preserving)")
    pu.add_argument("--input", required=True, help="Path to the source video or image")
    pu.add_argument("--target-height", dest="target_height", type=int, default=1080,
                    help="Desired output height in px. Factor is computed from the source so "
                         "aspect ratio is preserved. Default 1080.")
    pu.add_argument("--factor", type=float, default=None,
                    help="Override: explicit upscale factor (applied to both axes). "
                         "Takes precedence over --target-height.")
    pu.add_argument("--fps", type=int, default=None,
                    help="Video only. Re-encode source to this fps before upscaling. "
                         "Use 30 to avoid Topaz's 60fps price-doubling.")
    pu.add_argument("--type", choices=["video", "image"], default=None,
                    help="Force input type. Default: inferred from file extension.")
    pu.add_argument("--model", default=None, help="Override model key from models.json")
    pu.add_argument("--title", default=None, help="Working title slug (default: from filename)")
    pu.set_defaults(func=cmd_upscale)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
