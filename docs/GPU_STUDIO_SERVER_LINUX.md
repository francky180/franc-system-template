# PHIMIND GPU STUDIO SERVER — rebuild from zero (Linux, proven 2026-10-20)

What it is: Database Mart GPU VPS, RTX A4000 16 GB, 24 cores, 27 GB RAM, 320 GB SSD, $149/mo monthly.
Image: "Operating System & Software" → **GPU Container Runtime (Ubuntu Server 24)** ($0). Windows is NOT offered on this plan.
Pick any server name; user `administrator`. Secrets (password, IP, CRD PIN) live ONLY in the laptop's `~/.config/databasemart/.env`
(keys `GPU_SERVER_IP`, `GPU_SERVER_USER`, `GPU_SERVER_PASSWORD`, `CRD_PIN`). Never commit them.

## 1. First login + lock it down (5 min)
```bash
pip install --user paramiko
python bootstrap.py key      # password login once, add ~/.ssh/id_ed25519.pub, prove key login works
python bootstrap.py harden   # ONLY after key works: PasswordAuthentication no (sshd_config.d/00-keys-only.conf)
python bootstrap.py info     # Ubuntu, GPU, Docker, disk, RAM
```
First boot runs cloud-init ~4 min: it installs NVIDIA driver 560 (CUDA 12.6), Docker, nvidia-container-runtime. Wait for
`systemctl is-active cloud-final` = active before testing `nvidia-smi`.
`srun.py "<cmd>"` = run a command with sudo on the server (password read from the env file, never printed).

## 2. Base tools
```bash
python srun.py 'apt-get install -y git curl wget unzip ffmpeg python3-pip python3-venv python3-dev build-essential rubberband-cli jq htop gh tmux'
python srun.py 'curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs'
ssh administrator@<IP> 'curl -fsSL https://claude.ai/install.sh | bash; curl -LsSf https://astral.sh/uv/install.sh | sh'
```
Francky logs Claude in once (server Terminal → `claude`).

## 3. Blender 5.2.2 (GPU)
```bash
mkdir -p ~/apps && cd ~/apps && curl -sSLo b.tar.xz https://download.blender.org/release/Blender5.2/blender-5.2.2-linux-x64.tar.xz && tar -xf b.tar.xz && rm b.tar.xz
blender -b scene.blend --python ~/work/gpu_cuda.py -o //out_### -F PNG -f 72
```
- **Use CUDA. OptiX fails on driver 560** ("Internal compilation error"). Fix would be nvidia-driver-595 + reboot (he chose CUDA).
- Pack textures before upload (laptop scenes use absolute Windows paths): `bpy.ops.file.pack_all()` then save a copy.
- Benchmark: slum tower 1080x1920, Cycles 64 spp + OIDN GPU = **20-30 s/frame** (laptop EEVEE 2+ min).

## 4. AI tools (each in its own venv, logs in ~/logs)
- `setup_comfy.sh` → ComfyUI + torch cu126 + HunyuanVideo 1.5 fp8 (~36 GB): 720p i2v cfg-distilled, 480p i2v step-distilled,
  1080p SR, qwen 2.5 VL 7B fp8, byt5, VAE, sigclip. Start: `cd ~/apps/ComfyUI && .venv/bin/python main.py --listen 127.0.0.1 --port 8188`.
  Run a clip: `python3 hunyuan_i2v.py <image in ComfyUI/input> "<motion>" 720 1280 121 20 video/name [unet]`.
  Speed: 720p, 121 frames, 20 steps = ~145 s/step ≈ 48 min per 5 s clip. Use the 480p step-distilled model for drafts.
- `setup_voice_genjutsu.sh` → Chatterbox TTS venv + Genjutsu-OSS repo + venv (transformers, demucs, mediapipe, torch cu126).
  **Chatterbox fix:** `~/apps/chatterbox/bin/pip install "setuptools<81"` (perth watermarker needs pkg_resources).
  Voice test: `clone_test.py` (reference = ~/work/clone-kit/voice_sample.wav). Spell PHIMIND as "Fye Mind" in scripts.
- One heavy GPU job at a time (Blender OR ComfyUI). Check `nvidia-smi` first.

## 5. Claude brain on the server
- Stream `~/.claude/{skills,agents,hooks,CLAUDE.md}` with tar over ssh, EXCLUDING node_modules, .git, *.exe, *.dll, *.node
  (gstack Windows binaries are 1.4 GB). Memory → `~/.claude/projects/-home-administrator/memory`.
- `~/CLAUDE.md` + `SERVER_CLAUDE_SECTION.md` appended (the server master prompt: tools, money rules, how he works).
- Do NOT copy the laptop settings.json (Windows hook paths).
- MCP (`~/.claude.json` mcpServers): remote HTTP copied as-is (fal, higgsfield, higgsfield-bridge, canva, motionsites,
  adadvisor, transcript-api; openart/viewmax/restream left logged out on purpose). Linux local: `npm i -g @playwright/mcp
  @upstash/context7-mcp @modelcontextprotocol/server-sequential-thinking @jpisnice/shadcn-ui-mcp-server
  @robinson_ai_systems/vercel-mcp @colbymchenry/codegraph` + `npx playwright install --with-deps chromium`;
  `uv tool install "scrapling[ai]" blender-mcp`; minimax-mcp folder copied (needs NVIDIA_API_KEY env).
  OAuth MCPs: Francky runs `/mcp` in the server terminal and logs in (copying tokens between machines is blocked).
- Telegram: copy `~/.telegram.env` (chmod 600).

## 6. Seeing it (desktop) + access from anywhere
- Desktop: `apt-get install -y xfce4 xfce4-goodies xrdp dbus-x11`, `echo xfce4-session > ~/.xsession`, Google Chrome .deb,
  desktop shortcuts for Blender, Chrome, Terminal, ~/work.
- **Chrome Remote Desktop (main way in):** install chrome-remote-desktop .deb,
  `echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session`, add user to group
  chrome-remote-desktop, run `start-host --code=<from remotedesktop.google.com/headless> --redirect-url=... --name=<your-server-name> --pin=<6 digits>`,
  then `systemctl enable --now chrome-remote-desktop@administrator`. The headless page gives a WINDOWS command; take the
  code from it and use the Linux `start-host`. Codes expire in minutes.
- **Tailscale (backup, Termux):** `curl -fsSL https://tailscale.com/install.sh | sh`, `nohup tailscale up --ssh --hostname=<your-server-name> &`,
  he opens the printed link. Then `ssh administrator@<your-server-name>` from any tailnet device.
- Firewall (ufw): OpenSSH anywhere (key-only), 3389 only from the home IP, 3389 + 22 on tailscale0.

## 7. Laptop space
`move_to_server.sh` copies folders to `~/archive/laptop-downloads/`, verifies file count + bytes, then deletes the laptop copy.

## 8. Overnight pipeline (PC can be off) — added 2026-10-26
The server finishes long batches by itself; the PC is only the command center.
1. **GPU chain** (`~/work/films/real`): `real_jobs.py` (Blender frame -> Qwen-Image-Edit photoreal still -> HunyuanVideo i2v; `SHOTS=batch.json`, `WH=1280x720` for landscape) -> `overnight.sh` (ESRGAN x4 + RIFE x2 upscale -> reveal edits, build only) -> more chains. Each step writes a `*.status` file.
2. **Server Claude Code** (`~/.local/bin/claude`, logged in once; not on the ssh PATH, so call it by full path):
   - tmux `night` -> `night_watch.sh` wakes `claude -p` with `NIGHT_PLAN.md` every 10 min: QC each video on a contact sheet, fix or skip, send only clean ones to Telegram, ledger `sent.txt`, never post.
   - tmux `super` -> `super_watch.sh` runs `claude -p` with `SERVER_SUPERVISOR_PROMPT.md` every 30 min: health check, crash recovery, keep the GPU busy, 2-hourly Telegram status.
   - `SAME_PAGE.md` = the shared plan both server jobs and the PC Claude read first; every change adds a LOG line.
3. **Rules that prevent the crashes we hit:** the GPU belongs to the AI queue, so Blender and TTS run CPU-only (`CUDA_VISIBLE_DEVICES=`) while it runs; a still only counts as done if its image exists, and a missing one skips the shot instead of crashing the queue; never `pkill -f` over ssh (it matches your own shell).
4. Starting an unattended agent needs the owner's explicit go: Claude Code's auto mode blocks it otherwise, so the owner runs the `tmux new -d -s ...` line once.
