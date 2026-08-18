# Vendored third-party code

Everything here is committed to the repo and served from disk. PRODUCT.md chose
the single-file, no-build stack for STAGE RELIABILITY; a CDN in the critical path
contradicts that, so nothing below is fetched at runtime.

| File | Version | Licence |
|---|---|---|
| `leaflet.js` / `leaflet.css` / `images/` | 1.9.4 | BSD-2-Clause |
| `three.r128.min.js` | r128 | MIT |
| `motion.min.js` | Motion One 13.1.0 (UMD, global `Motion`) | MIT — see `motion.LICENSE.md` |
| `gsap.min.js` | GSAP 3.15.0 (UMD, global `gsap`) | GreenSock Standard "no charge" licence — https://gsap.com/standard-license (header retained in file) |
| `fonts/` + `fonts.css` | Archivo, IBM Plex Sans, IBM Plex Mono, Noto Sans Malayalam | OFL 1.1 |

**Scope discipline for the two animation libraries** (DIRECTION.md §2.4):

- **Motion One** drives interactive state — panel disclosure, acknowledge-pulse
  stopping, button press feedback, sweep CTA. Springs, not duration-eased
  transitions, and every animation retargets from the current value.
- **GSAP** is scoped to the two-hour sweep ONLY — the staggered feed drops, the
  fill/opacity interpolation as zones cross thresholds, and the pulse-ring
  emission. Its timeline and stagger utilities are the right tool for that one
  sequence. It is not used anywhere else in the product.

Lenis was considered and rejected: this is a console with no scroll narrative.
