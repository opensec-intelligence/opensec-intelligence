# Profile artwork

`gen.py` builds the four SVGs in `assets/`: the banner and the Pi-Bolt card, each in a dark and a light version.

```bash
pip install fonttools brotli
python scripts/gen.py
```

- Text is converted to paths, so GitHub (which serves SVGs as images, without web fonts) shows it the same for every viewer.
- The banner mark recreates the opensec.in sign-in scene: the O as a dot matrix, a colour trail sweeping clockwise every 9 seconds, and a ticked bezel whose tick under the sweep lights. It is CSS animation only, and holds still for viewers who prefer reduced motion.
- `opensec-wordmark.svg` is the wordmark from opensec.in.
- `fonts/` holds the opensec.in typefaces, all under the SIL Open Font License 1.1: Space Grotesk, IBM Plex Mono and Departure Mono.
