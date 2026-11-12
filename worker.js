// Serves the app + a tiny read-only API over your R2 bucket (binding: MANUALS)
export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    if (u.pathname === "/api/list") {
      const out = []; let cursor;
      do {
        const r = await env.MANUALS.list({ cursor, limit: 1000 });
        out.push(...r.objects.map(o => ({ key: o.key, size: o.size, uploaded: o.uploaded })));
        cursor = r.truncated ? r.cursor : undefined;
      } while (cursor);
      return Response.json(out, { headers: { "cache-control": "no-store" } });
    }
    if (u.pathname === "/api/file") {
      const o = await env.MANUALS.get(u.searchParams.get("key") || "");
      if (!o) return new Response("Not found", { status: 404 });
      const h = new Headers(); o.writeHttpMetadata(h); h.set("etag", o.httpEtag);
      h.set("cache-control", "private, max-age=300");
      return new Response(o.body, { headers: h });
    }
    return env.ASSETS.fetch(req);
  },
};
