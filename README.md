# Yusra Khan — Portfolio

AI Automation Engineer. Production automation systems across document processing,
CRM workflows, voice agents and content pipelines.

## Design

Swiss Modernism — "Technical Index". Paper and ink with a single cobalt accent, a
12-column grid, and the work presented as a numbered index of rows rather than a
card wall. Light-first, with a dark variant via `prefers-color-scheme`.

- **Type** — Familjen Grotesk (display + body), IBM Plex Mono (metadata, figures, stack)
- **Colour** — paper `#f6f6f4`, ink `#0c0c0d`, accent `#1a3fcb`
- All colours are CSS custom properties at the top of the stylesheet; the dark block
  only restates tokens, so no component hardcodes a colour.

## Editing

`index.html` is **generated** — don't edit it by hand, your changes will be
overwritten on the next build.

| What | Where |
| --- | --- |
| Projects, skills, experience, education, stats | `.content.json` |
| Name, role, lede, email, links, About paragraphs | `SITE` / `ABOUT` in `build.py` |
| Film titles and blurbs | `C:\brag-yusra\work\films.py` |
| Layout, type, colour | `CSS` and the template in `build.py` |

Then:

```bash
python build.py
```

## Films

`demos/<slug>.mp4` with `demos/<slug>.png` as the poster, one per project.
Videos are `preload="none"`, so the page loads posters rather than ~31 MB of video
and nothing streams until a visitor presses play.

## Deploying

Static — no build step on the host. Import the repo at
[vercel.com/new](https://vercel.com/new), framework preset **Other**, and leave the
build command and output directory empty. GitHub Pages also works
(Settings → Pages → deploy from `main` → `/root`).
