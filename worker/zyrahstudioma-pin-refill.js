// ZyrahStudioMA — Buffer pin refill Worker (Cloudflare, cron hourly)
// Keeps the ZyrahStudioMA Buffer channel at LIMIT scheduled pins.
// Fresh pins first (never posted before); then reuse pins whose last post is
// older than REUSE_DAYS. Only adds posts: never edits or deletes anything.
// Secret: BUFFER_API_KEY (Cloudflare secret, never in a file).
// Monitor: GET /?dry=1 shows the plan without scheduling anything.

const ORG = "6abe8710180cf2273f9691cd";      // Buffer org: ZyrahStudioMA
const CHANNEL = "6abeb7c3ea19ca0bde4852e1";  // Buffer channel: ZyrahStudioMA (Pinterest)
const QUEUE_URL =
  "https://raw.githubusercontent.com/Haryz-worker/ZyrahStudioMA-pinterest-assets/main/queue/queue.json";
const API = "https://api.buffer.com";
const LIMIT = 10;          // Buffer free plan: max 10 scheduled posts
const REUSE_DAYS = 21;     // a pin can come back after 21 days
const DAYS_AHEAD = 14;     // how far ahead to look for a free slot
const DEFAULT_SLOTS = "14,16,18,20,22"; // UTC hours; override with env SLOT_HOURS

const q = (s) => JSON.stringify(String(s)); // GraphQL string literal

async function gql(env, query) {
  const r = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${env.BUFFER_API_KEY}` },
    body: JSON.stringify({ query }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || j.errors) throw new Error(`Buffer ${r.status}: ${JSON.stringify(j.errors || j).slice(0, 400)}`);
  return j.data;
}

async function listPosts(env, statuses) {
  const out = [];
  let after = null;
  for (let page = 0; page < 20; page++) {
    const data = await gql(env, `query {
      posts(first: 100${after ? `, after: ${q(after)}` : ""},
        input: { organizationId: ${q(ORG)}, filter: { status: [${statuses.join(", ")}], channelIds: [${q(CHANNEL)}] } }) {
        edges { node { id text dueAt status } }
        pageInfo { hasNextPage endCursor }
      }
    }`);
    const p = data.posts;
    for (const e of p.edges) out.push(e.node);
    if (!p.pageInfo.hasNextPage) break;
    after = p.pageInfo.endCursor;
  }
  return out;
}

function nextSlots(taken, n, hours, now) {
  const takenSet = new Set(taken.filter(Boolean).map((d) => new Date(d).toISOString().slice(0, 13)));
  const slots = [];
  const start = new Date(now.getTime() + 30 * 60 * 1000); // at least 30 min ahead
  for (let d = 0; d < DAYS_AHEAD && slots.length < n; d++) {
    for (const h of hours) {
      const t = new Date(Date.UTC(start.getUTCFullYear(), start.getUTCMonth(), start.getUTCDate() + d, h, 0, 0));
      if (t <= start) continue;
      const key = t.toISOString().slice(0, 13);
      if (takenSet.has(key)) continue;
      slots.push(t.toISOString()); takenSet.add(key);
      if (slots.length >= n) break;
    }
  }
  return slots;
}

async function run(env, dry) {
  const log = [];
  const now = new Date();
  const hours = (env.SLOT_HOURS || DEFAULT_SLOTS).split(",").map((x) => parseInt(x, 10)).filter((x) => x >= 0 && x < 24);

  // 1. How many are already waiting?
  const pending = await listPosts(env, ["scheduled", "sending"]);
  const free = LIMIT - pending.length;
  log.push(`scheduled+sending: ${pending.length}/${LIMIT}`);
  if (free <= 0) { log.push(`${LIMIT}/${LIMIT} full, nothing to do`); return log; }

  // 2. Queue + history
  const queue = await (await fetch(QUEUE_URL, { cf: { cacheTtl: 300 } })).json();
  const done = await listPosts(env, ["sent", "error"]);
  const pendingTexts = new Set(pending.map((p) => p.text));
  const lastUsed = new Map(); // text -> latest dueAt
  for (const p of [...done, ...pending]) {
    const t = p.dueAt ? Date.parse(p.dueAt) : 0;
    if (!lastUsed.has(p.text) || lastUsed.get(p.text) < t) lastUsed.set(p.text, t);
  }

  // 3-5. Fresh first, then reuse after REUSE_DAYS
  const fresh = queue.filter((x) => !lastUsed.has(x.desc));
  const cutoff = now.getTime() - REUSE_DAYS * 86400000;
  const reuse = queue
    .filter((x) => lastUsed.has(x.desc) && !pendingTexts.has(x.desc) && lastUsed.get(x.desc) < cutoff)
    .sort((a, b) => lastUsed.get(a.desc) - lastUsed.get(b.desc));
  log.push(`queue ${queue.length} · fresh left ${fresh.length} · reusable ${reuse.length}`);
  if (fresh.length < 10) log.push(`WARNING: only ${fresh.length} fresh pins left — add new images to queue.json`);

  const picks = [...fresh, ...reuse].slice(0, free);
  if (!picks.length) { log.push("nothing eligible to schedule"); return log; }

  // 6. Free hourly slots
  const slots = nextSlots(pending.map((p) => p.dueAt), picks.length, hours, now);

  // 7. Create posts (customScheduled only)
  for (let i = 0; i < picks.length && i < slots.length; i++) {
    const p = picks[i];
    const line = `${slots[i]} · ${p.id} · ${p.title}`;
    if (dry) { log.push(`[dry] would schedule ${line}`); continue; }
    try {
      const data = await gql(env, `mutation {
        createPost(input: {
          text: ${q(p.desc)}
          channelId: ${q(CHANNEL)}
          schedulingType: automatic
          mode: customScheduled
          dueAt: ${q(slots[i])}
          assets: [{ image: { url: ${q(p.image)} } }]
          metadata: { pinterest: { boardServiceId: ${q(p.board)}, title: ${q(p.title)}, url: ${q(p.url)} } }
        }) {
          ... on PostActionSuccess { post { id dueAt } }
          ... on MutationError { message }
        }
      }`);
      const res = data.createPost;
      if (res.post) log.push(`scheduled ${line} → ${res.post.id}`);
      else {
        log.push(`ERROR ${line}: ${res.message}`);
        if (/limit/i.test(res.message || "")) break; // Buffer limit reached
      }
    } catch (e) {
      log.push(`ERROR ${line}: ${e.message}`);
    }
  }
  return log;
}

export default {
  async scheduled(event, env, ctx) {
    const log = await run(env, false).catch((e) => [`FATAL ${e.message}`]);
    console.log(log.join("\n"));
  },
  async fetch(request, env) {
    const dry = new URL(request.url).searchParams.get("dry") === "1";
    if (!dry) return new Response("ZyrahStudioMA pin refill. Use ?dry=1 to see the plan.\n");
    const log = await run(env, true).catch((e) => [`FATAL ${e.message}`]);
    return new Response(log.join("\n") + "\n", { headers: { "content-type": "text/plain; charset=utf-8" } });
  },
};
