# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal portfolio site for Aaron Sofaly. Pure HTML/CSS/JS with no build tooling — the entire site is `index.html`. Deployed on Cloudflare Workers as a static asset.

## Development

Open `index.html` directly in a browser. No build step, no dev server, no local commands to run.

**Deploy:** Push to GitHub — Cloudflare automatically picks up changes and deploys.

## Architecture

**Single-file site:** All HTML, CSS (in `<style>`), and JavaScript (minimal inline) live in `index.html`. The only JS is a one-liner to set the footer copyright year dynamically.

**Design system (all inside `index.html`):**
- CSS custom properties define color palettes for theme variants: default (cream), `paper` (lighter), and `dusk` (dark)
- Card shape variants are controlled via `data-shape` attributes: default (28px radius), `paper` (4px + border), `sticker` (32px + shadow)
- Typography uses Geist (sans-serif) and Geist Mono, loaded from Google Fonts
- Responsive breakpoint at `max-width: 1023px`

**Key layout sections:**
- `.hero` — 2-col grid with headshot and intro text
- `.now-strip` — 4-col "currently" grid (reading, listening, playing, watching)
- `.bento` — 2-col interest cards (Biohacker, Powder Chaser, Case Solver, Retro Gamer), each with a distinct accent color
- `.footer` — copyright year (dynamic), social links, location

## Gotchas

- **Headshot is base64-encoded inline** — the profile image is embedded directly in `index.html` as a base64 JPEG string, not a separate file. To update it, encode the new image to base64 and replace the `src` value on the `<img class="headshot">` element.
