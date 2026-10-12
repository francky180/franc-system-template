#!/usr/bin/env node
/* Perfect Cuts — self-contained Remotion launcher.
   Lives inside each care package next to the cuts JSON. Writes a minimal
   Remotion project to ~/.perfect-cuts/remotion-studio (cached between runs),
   injects this package's cut data, resolves the source video, installs deps
   on first run, and opens Remotion Studio.

   Requires Node.js only — no skill installation, no other tooling. */

import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath } from "url";
import { spawnSync, spawn } from "child_process";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.join(os.homedir(), ".perfect-cuts", "remotion-studio");

// ---------- embedded Remotion project template ----------
const FILES = {
  "package.json": `{
  "name": "perfect-cuts-remotion",
  "version": "1.0.0",
  "private": true,
  "scripts": { "studio": "remotion studio src/index.ts" },
  "dependencies": {
    "@remotion/cli": "^4.0.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "remotion": "^4.0.0"
  },
  "devDependencies": { "@types/react": "^18.3.1", "typescript": "^5.5.0" }
}
`,
  "tsconfig.json": `{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "strict": false,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "noEmit": true
  },
  "include": ["src"]
}
`,
  "src/index.ts": `import { registerRoot } from "remotion";
import { Root } from "./Root";

registerRoot(Root);
`,
  "src/Root.tsx": `import { Composition } from "remotion";
import { CUTS } from "./cutdata";
import { PerfectCut } from "./PerfectCut";

const totalFrames = CUTS.clips.reduce(
  (sum: number, c: { in_frame: number; out_frame: number }) =>
    sum + (c.out_frame - c.in_frame),
  0,
);

export const Root = () => (
  <Composition
    id="PerfectCut"
    component={PerfectCut}
    fps={CUTS.fps}
    width={CUTS.width}
    height={CUTS.height}
    durationInFrames={totalFrames}
  />
);
`,
  "src/PerfectCut.tsx": `import { OffthreadVideo, Series, staticFile } from "remotion";
import { CUTS } from "./cutdata";

export const PerfectCut = () => (
  <Series>
    {CUTS.clips.map(
      (c: { in_frame: number; out_frame: number }, i: number) => (
        <Series.Sequence key={i} durationInFrames={c.out_frame - c.in_frame}>
          <OffthreadVideo
            src={staticFile("source.mp4")}
            startFrom={c.in_frame}
            endAt={c.out_frame}
          />
        </Series.Sequence>
      ),
    )}
  </Series>
);
`,
};
// ---------------------------------------------------------

function fail(msg) {
  console.error("\n  PROBLEM: " + msg + "\n");
  process.exit(1);
}

// 1. Find the cut data next to this script
const cutsFile = fs.readdirSync(HERE).find((f) => f.toLowerCase().endsWith(".json") && f.toLowerCase().includes("cut"));
if (!cutsFile) fail("No cut data JSON found in this folder. Keep this launcher inside the perfect-cut package folder.");
const cuts = JSON.parse(fs.readFileSync(path.join(HERE, cutsFile), "utf8"));

// 2. Resolve the source video: original path first, then any non-package
//    video dropped into this folder (package outputs carry "(C)" in the name)
let source = cuts.source;
if (!source || !fs.existsSync(source)) {
  const VIDEO_EXT = [".mp4", ".mov", ".m4v", ".mts", ".avi", ".mkv"];
  const local = fs.readdirSync(HERE).find(
    (f) => VIDEO_EXT.includes(path.extname(f).toLowerCase()) && !f.includes("(C)"),
  );
  if (local) {
    source = path.join(HERE, local);
    console.log("Original clip path not found — using " + local + " from this folder.");
  } else {
    fail(
      "Can't find the original video (" + (cuts.source || "unknown") + ").\n" +
      "  Drop the raw clip into this folder and double-click the launcher again.",
    );
  }
}

// 3. Write the project (template + this package's cut data)
for (const [rel, content] of Object.entries(FILES)) {
  const dest = path.join(APP, rel);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, content);
}
fs.writeFileSync(path.join(APP, "src", "cutdata.ts"), "export const CUTS = " + JSON.stringify(cuts, null, 1) + ";\n");

// 4. Make the source video reachable: symlink -> hardlink -> copy
const pub = path.join(APP, "public");
fs.mkdirSync(pub, { recursive: true });
const dest = path.join(pub, "source.mp4");
try { fs.rmSync(dest, { force: true }); } catch {}
try {
  fs.symlinkSync(source, dest);
} catch {
  try {
    fs.linkSync(source, dest);
  } catch {
    console.log("Copying source video (no link support here) — one moment...");
    fs.copyFileSync(source, dest);
  }
}

// 5. Install deps on first run, then open the studio
const sh = { cwd: APP, stdio: "inherit", shell: true };
if (!fs.existsSync(path.join(APP, "node_modules"))) {
  console.log("\nFirst run — installing Remotion (one-time, a few minutes)...\n");
  const r = spawnSync("npm install", sh);
  if (r.status !== 0) fail("npm install failed — check your internet connection and try again.");
}
console.log("\nOpening Remotion Studio... (close this window to stop it)\n");
spawn("npx remotion studio src/index.ts", sh);
