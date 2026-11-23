// Entry program for make.fun competition "news-image-20261122".
// The picture itself (entry.png, next to this file) is drawn by
// build_image.py; this program's job is only to deliver those exact
// bytes to the grader's output directory, as the starter contract
// specifies: MAKEFUN_OUTPUT_DIR locally, /output inside the grader.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
