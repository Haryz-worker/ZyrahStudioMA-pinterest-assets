# zyrah-pinterest-assets
Zyrah Studio Pinterest pin images (public assets for Buffer). Example data is fictional.

## Pin refill (Cloudflare Worker)
- `worker/zyrahstudioma-pin-refill.js` + `worker/wrangler.toml`: Worker `zyrahstudioma-pin-refill`, cron `10 * * * *` (hourly at :10 UTC).
- Keeps the ZyrahStudioMA Buffer channel at 10 scheduled pins. Fresh pins first; a pin can come back after 21 days. Only adds posts.
- Slots: UTC hours in `SLOT_HOURS` (default 14,16,18,20,22). Secret `BUFFER_API_KEY` is set in Cloudflare, never in a file.
- Queue: `queue/queue.json` (id, image, title, desc, url, board). Images in `pins/`. Generator: `pins/make_pins3.py`.
- Monitor: `https://zyrahstudioma-pin-refill.<account>.workers.dev/?dry=1` shows the plan without scheduling.
