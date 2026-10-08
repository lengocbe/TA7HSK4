"use strict";
const $ = (s) => document.querySelector(s);
const ICONS = {
  book: '<path d="M12 7c-3-3-7-3-10-2v14c3-1 7-1 10 2 3-3 7-3 10-2V5c-3-1-7-1-10 2zm0 0v14"/>',
  home: '<path d="m3 10 9-7 9 7v11h-6v-7H9v7H3z"/>',
  layers: '<path d="m12 3 10 6-10 6L2 9zM2 14l10 6 10-6M2 19l10 6 10-6"/>',
  chart: '<path d="M4 20V10m8 10V4m8 16v-7M2 22h20"/>',
  settings: '<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="8" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="10" cy="18" r="2"/>',
  sound: '<path d="m3 9 4 0 5-4v14l-5-4H3zM16 8c3 2 3 6 0 8M19 5c5 4 5 10 0 14"/>',
  arrow: '<path d="M5 12h14m-5-5 5 5-5 5"/>',
  back: '<path d="m15 5-7 7 7 7"/>',
  chevron: '<path d="m9 5 7 7-7 7"/>',
  check: '<path d="m5 12 4 4L19 6"/>',
  offline: '<path d="m3 4 18 17M2 9a17 17 0 0 1 5-3m3-1a17 17 0 0 1 12 4M5 13a12 12 0 0 1 5-2m4 0a12 12 0 0 1 5 2M8 17a6 6 0 0 1 8 0"/><circle cx="12" cy="21" r="1"/>',
  search: '<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/>',
  star: '<path d="m12 3 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z"/>',
  close: '<path d="m5 5 14 14M5 19 19 5"/>',
  trophy: '<path d="M7 3h10v7a5 5 0 0 1-10 0zM7 5H3v3c0 3 2 4 5 4m9-7h4v3c0 3-2 4-5 4M12 15v5M7 21h10"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
  download: '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
  upload: '<path d="M12 16V4m-5 5 5-5 5 5M4 16v5h16v-5"/>',
  moon: '<path d="M20 15A9 9 0 0 1 9 4a9 9 0 1 0 11 11z"/>',
  flame: '<path d="M12 3c1 5 7 6 7 12a7 7 0 0 1-14 0c0-3 2-5 4-7 0 3 2 4 3 4 2-3 1-6 0-9z"/>'
};
function icon(name, cls = "") {
  return '<svg class="icon '.concat(cls, '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">').concat(ICONS[name] || ICONS.book, "</svg>");
}
function esc(value) {
  return String(value != null ? value : "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}
const LESSONS = DATA.lessons;
const WORDS = DATA.words;
const BYID = WORDS.reduce((map, w) => {
  map[w.id] = w;
  return map;
}, /* @__PURE__ */ Object.create(null));
const defaults = () => ({ schema: 1, progress: {}, favorites: [], last: {}, daily: {}, settings: { dark: false, slow: false, goal: 15 } });
let state = defaults(), page = "home", lang = "en", lessonId = null, currentWord = null, section = "units", study = null, search = "", wordFilter = "all", lastDetail = "lesson", saveError = false;
let browserAudio = null;
function readState() {
  try {
    const raw = window.Android ? Android.load() : localStorage.getItem("lingo-state");
    if (raw) state = validateState(JSON.parse(raw));
  } catch (e) {
    state = defaults();
    toast("Kh\xF4ng \u0111\u1ECDc \u0111\u01B0\u1EE3c ti\u1EBFn \u0111\u1ED9 c\u0169. H\xE3y kh\xF4i ph\u1EE5c b\u1EA3n sao l\u01B0u n\u1EBFu c\xF3.");
  }
}
function validateState(input) {
  var _a, _b, _c, _d;
  if (!input || input.schema !== 1 || typeof input.progress !== "object" || Array.isArray(input.progress) || !input.progress) throw Error("Invalid backup");
  const out = defaults();
  for (const [id, p] of Object.entries(input.progress)) {
    if (!BYID[id]) continue;
    if (!p || !Number.isFinite(p.due) || !Number.isFinite(p.interval) || p.interval < 0 || p.interval > 365 || !Number.isInteger(p.reps) || p.reps < 0 || !Number.isInteger(p.lapses) || p.lapses < 0) throw Error("Invalid progress");
    out.progress[id] = { due: p.due, interval: p.interval, reps: p.reps, lapses: p.lapses, last: typeof p.last === "string" ? p.last : "" };
  }
  out.favorites = Array.isArray(input.favorites) ? [...new Set(input.favorites.filter((id) => BYID[id]))] : [];
  for (const l of ["en", "zh"]) if (((_a = input.last) == null ? void 0 : _a[l]) && LESSONS.some((x) => x.id === input.last[l] && x.lang === l)) out.last[l] = input.last[l];
  if (input.daily && typeof input.daily === "object") {
    for (const [key, value] of Object.entries(input.daily)) if (/^\d{4}-\d{2}-\d{2}$/.test(key) && Number.isInteger(value) && value >= 0 && value < 1e5) out.daily[key] = value;
  }
  out.settings = { dark: !!((_b = input.settings) == null ? void 0 : _b.dark), slow: !!((_c = input.settings) == null ? void 0 : _c.slow), goal: [5, 10, 15, 20, 30].includes((_d = input.settings) == null ? void 0 : _d.goal) ? input.settings.goal : 15 };
  return out;
}
function save() {
  try {
    if (window.Android) {
      if (!Android.save(JSON.stringify(state))) throw Error("Save failed");
    } else localStorage.setItem("lingo-state", JSON.stringify(state));
    saveError = false;
  } catch (e) {
    if (!saveError) toast("Kh\xF4ng l\u01B0u \u0111\u01B0\u1EE3c ti\u1EBFn \u0111\u1ED9. H\xE3y xu\u1EA5t b\u1EA3n sao l\u01B0u.");
    saveError = true;
  }
}
function localDay(date = /* @__PURE__ */ new Date()) {
  return "".concat(date.getFullYear(), "-").concat(String(date.getMonth() + 1).padStart(2, "0"), "-").concat(String(date.getDate()).padStart(2, "0"));
}
function todayCount() {
  return state.daily[localDay()] || 0;
}
function languageName(l) {
  return l === "en" ? "Ti\u1EBFng Anh" : "Ti\u1EBFng Hoa";
}
function lessonWords(id) {
  const lesson = LESSONS.find((l) => l.id === id);
  return lesson ? lesson.words.map((id2) => BYID[id2]).filter(Boolean) : [];
}
function learned(words) {
  return words.filter((w) => {
    var _a;
    return (((_a = state.progress[w.id]) == null ? void 0 : _a.reps) || 0) > 0;
  }).length;
}
function dueWords(l) {
  return WORDS.filter((w) => (!l || w.lang === l) && state.progress[w.id] && state.progress[w.id].due <= Date.now());
}
function streak() {
  let n = 0, d = /* @__PURE__ */ new Date();
  if (!state.daily[localDay(d)]) d.setDate(d.getDate() - 1);
  while (state.daily[localDay(d)]) {
    n++;
    d.setDate(d.getDate() - 1);
  }
  return n;
}
function percentage(n, total) {
  return total ? Math.round(n * 100 / total) : 0;
}
function toast(message) {
  const el = $("#toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove("show"), 3500);
}
function stopAudio() {
  if (window.Android) Android.stop();
  if (browserAudio) {
    browserAudio.pause();
    browserAudio = null;
  }
}
function playWord(id) {
  if (!BYID[id]) return;
  if (window.Android) {
    Android.play(id, state.settings.slow);
    return;
  }
  stopAudio();
  browserAudio = new Audio("audio/".concat(id, ".mp3"));
  browserAudio.playbackRate = state.settings.slow ? 0.78 : 1;
  browserAudio.play().catch(() => toast("Ch\u01B0a ph\xE1t \u0111\u01B0\u1EE3c \xE2m thanh. H\xE3y th\u1EED l\u1EA1i."));
}
window.audioFailed = () => toast("Kh\xF4ng ph\xE1t \u0111\u01B0\u1EE3c \xE2m thanh. H\xE3y th\u1EED l\u1EA1i.");
function applyTheme() {
  document.body.classList.toggle("dark", state.settings.dark);
  if (window.Android) Android.theme(state.settings.dark);
}
function nav() {
  return '<nav class="nav" aria-label="\u0110i\u1EC1u h\u01B0\u1EDBng">'.concat([["home", "home", "Trang ch\u1EE7"], ["library", "book", "B\xE0i h\u1ECDc"], ["words", "layers", "Kho t\u1EEB"], ["stats", "chart", "Ti\u1EBFn \u0111\u1ED9"], ["settings", "settings", "C\xE0i \u0111\u1EB7t"]].map(([p, i, t]) => '<button data-action="nav" data-page="'.concat(p, '" class="').concat(page === p || p === "library" && page === "lesson" ? "selected" : "", '">').concat(icon(i), "<span>").concat(t, "</span></button>")).join(""), "</nav>");
}
function audioButton(id) {
  return '<button class="iconbtn audio" data-action="audio" data-id="'.concat(id, '" aria-label="Nghe ph\xE1t \xE2m">').concat(icon("sound"), "</button>");
}
function languagePills() {
  return '<div class="pillbar"><button class="pill '.concat(lang === "en" ? "active" : "", '" data-action="lang" data-lang="en">Ti\u1EBFng Anh</button><button class="pill ').concat(lang === "zh" ? "active" : "", '" data-action="lang" data-lang="zh">Ti\u1EBFng Hoa</button></div>');
}
function backButton(text = "Quay l\u1EA1i") {
  return '<button class="back" data-action="back">'.concat(icon("back")).concat(text, "</button>");
}
function home() {
  const count = todayCount(), goal = state.settings.goal;
  return '<div class="topbar"><div class="brand"><b>lingo</b><small>S\u1ED4 T\u1EEA V\u1EF0NG C\u1EE6A B\u1EA0N</small></div><button class="iconbtn avatar" data-action="nav" data-page="stats" aria-label="Xem chu\u1ED7i ng\xE0y h\u1ECDc">'.concat(icon("flame"), '</button></div>\n <div class="welcome"><div class="eyebrow">M\u1ED7i ng\xE0y m\u1ED9t b\u01B0\u1EDBc ti\u1EBFn</div><h1 style="margin-top:8px">H\xF4m nay, h\u1ECDc g\xEC nh\u1EC9?</h1><p>Ch\u1ECDn ng\xF4n ng\u1EEF v\xE0 b\u1EAFt \u0111\u1EA7u h\xE0nh tr\xECnh c\u1EE7a b\u1EA1n.</p></div>\n <div class="card goal-card"><div class="goal-ring" style="--pct:').concat(Math.min(100, count / goal * 100), '%"><span>').concat(Math.min(count, goal), "/").concat(goal, "</span></div><div><h3>").concat(count >= goal ? "B\u1EA1n \u0111\xE3 \u0111\u1EA1t m\u1EE5c ti\xEAu h\xF4m nay!" : "M\u1ED9t ch\xFAt m\u1ED7i ng\xE0y, nh\u1EDB l\xE2u h\u01A1n", "</h3><p>").concat(count, " l\u01B0\u1EE3t \xF4n h\xF4m nay \xB7 M\u1EE5c ti\xEAu ").concat(goal, ' l\u01B0\u1EE3t</p><button class="link-button" data-action="nav" data-page="settings">\u0110i\u1EC1u ch\u1EC9nh m\u1EE5c ti\xEAu ').concat(icon("chevron", "chevron"), '</button></div></div>\n <div class="section-head"><h2>Ch\u1ECDn ng\xF4n ng\u1EEF</h2><span>2 h\xE0nh tr\xECnh</span></div><div class="stack languages">').concat(["en", "zh"].map((l) => {
    const words = WORDS.filter((w) => w.lang === l), done = learned(words), lesson = LESSONS.find((x) => x.id === state.last[l]);
    return '<button class="language-card '.concat(l, '" data-action="open-language" data-lang="').concat(l, '"><div class="lang-top"><div class="language-symbol">').concat(l === "en" ? "Aa" : "\u6C49", "</div><div><h2>").concat(languageName(l), "</h2><p>").concat(l === "en" ? "Global Success \xB7 L\u1EDBp 7" : "HSK 4 \xB7 Ch\u1EEF gi\u1EA3n th\u1EC3", '</p></div></div><span class="badge">').concat(LESSONS.filter((x) => x.lang === l && x.kind === "unit").length, " ").concat(l === "en" ? "Unit" : "b\xE0i", " \xB7 ").concat(words.length, ' t\u1EEB v\u1EF1ng</span><div class="progress"><i style="width:').concat(percentage(done, words.length), '%"></i></div><div class="row between small muted"><span>').concat(done, " t\u1EEB \u0111\xE3 h\u1ECDc</span><span>").concat(percentage(done, words.length), '%</span></div><div class="continue"><span>').concat(lesson ? "H\u1ECDc ti\u1EBFp \xB7 " + esc(lesson.short) : "Kh\xE1m ph\xE1 b\xE0i h\u1ECDc", "</span>").concat(icon("arrow"), "</div></button>");
  }).join(""), "</div>").concat(dueWords().length ? '<div class="review-banner"><div><b>'.concat(dueWords().length, ' t\u1EEB \u0111\u1EBFn h\u1EA1n \xF4n</b><span>C\u1EE7ng c\u1ED1 nh\u1EEFng t\u1EEB b\u1EA1n \u0111\xE3 h\u1ECDc</span></div><button data-action="review" data-lang="all">\xD4n ngay</button></div>') : "", '<div class="offline-note">').concat(icon("offline"), "T\u1EEB v\u1EF1ng v\xE0 gi\u1ECDng \u0111\u1ECDc c\xF3 s\u1EB5n \xB7 H\u1ECDc ngo\u1EA1i tuy\u1EBFn</div>");
}
function lessonTile(l) {
  const words = lessonWords(l.id), n = learned(words);
  return '<button class="lesson" data-action="lesson" data-id="'.concat(l.id, '"><div class="lesson-icon">').concat(esc(l.symbol || l.number || "\u21BB"), '</div><div class="lesson-main"><div class="eyebrow">').concat(esc(l.short), "</div><h3>").concat(esc(l.title), "</h3><p>").concat(words.length, " t\u1EEB \xB7 ").concat(n, " \u0111\xE3 h\u1ECDc").concat(dueWords(l.lang).filter((w) => l.words.includes(w.id)).length ? " \xB7 C\xF3 t\u1EEB c\u1EA7n \xF4n" : "", '</p><div class="progress"><i style="width:').concat(percentage(n, words.length), '%"></i></div></div>').concat(icon("chevron", "chevron"), "</button>");
}
function library() {
  const filtered = LESSONS.filter((l) => l.lang === lang && l.kind === ({ units: "unit", review: "review", tests: "test" }[section] || "unit"));
  return '<div class="page-head">'.concat(backButton("Trang ch\u1EE7"), "<h1>").concat(languageName(lang), "</h1><p>").concat(lang === "en" ? "T\u1EEB v\u1EF1ng theo s\xE1ch Global Success l\u1EDBp 7" : "B\xE0i h\u1ECDc bi\xEAn so\u1EA1n t\u1EEB 13 \u0111\u1EC1 HSK 4", "</p></div>").concat(languagePills(), '<div class="pillbar"><button class="pill ').concat(section === "units" ? "active" : "", '" data-action="section" data-section="units">').concat(lang === "en" ? "12 Unit" : "Theo ch\u1EE7 \u0111\u1EC1", '</button><button class="pill ').concat(section === (lang === "en" ? "review" : "tests") ? "active" : "", '" data-action="section" data-section="').concat(lang === "en" ? "review" : "tests", '">').concat(lang === "en" ? "\xD4n t\u1EADp Review" : "Theo \u0111\u1EC1 HSK", '</button></div><div class="stack">').concat(filtered.map(lessonTile).join(""), "</div>");
}
function wordRow(w) {
  const p = state.progress[w.id];
  return '<div class="word-row"><span class="word-status '.concat((p == null ? void 0 : p.reps) ? "learned" : "", '" title="').concat((p == null ? void 0 : p.reps) ? "\u0110\xE3 h\u1ECDc" : "Ch\u01B0a h\u1ECDc", '"></span><button class="word-info" data-action="word" data-id="').concat(w.id, '"><b>').concat(esc(w.text), "</b><span>").concat(esc(w.pron), " \xB7 ").concat(esc(w.meaning), "</span></button>").concat(audioButton(w.id), "</div>");
}
function lessonPage() {
  const l = LESSONS.find((x) => x.id === lessonId);
  if (!l) return library();
  const words = lessonWords(l.id), newCount = words.filter((w) => {
    var _a;
    return !((_a = state.progress[w.id]) == null ? void 0 : _a.reps);
  }).length, reviewCount = words.filter((w) => {
    var _a;
    return ((_a = state.progress[w.id]) == null ? void 0 : _a.due) <= Date.now();
  }).length;
  return '<div class="page-head">'.concat(backButton("Danh s\xE1ch b\xE0i"), '<div class="card hero-lesson" style="margin-top:13px"><div class="eyebrow">').concat(esc(l.short), "</div><h2>").concat(esc(l.title), "</h2><p>").concat(esc(l.description), '</p><div class="progress"><i style="width:').concat(percentage(learned(words), words.length), '%"></i></div><p>').concat(learned(words), "/").concat(words.length, " t\u1EEB \u0111\xE3 h\u1ECDc \xB7 ").concat(reviewCount, ' \u0111\u1EBFn h\u1EA1n \xF4n</p></div></div>\n <div class="actions"><button class="primary" data-action="learn" data-mode="new">').concat(icon("book"), " ").concat(newCount ? "H\u1ECDc t\u1EEB m\u1EDBi \xB7 ".concat(newCount, " t\u1EEB") : "H\u1ECDc l\u1EA1i to\xE0n b\u1ED9 b\xE0i", '</button><div class="two"><button class="secondary" data-action="learn" data-mode="due">').concat(icon("clock"), "\xD4n \u0111\u1EBFn h\u1EA1n (").concat(reviewCount, ')</button><button class="secondary" data-action="quiz-menu">').concat(icon("layers"), 'Luy\u1EC7n t\u1EADp</button></div></div><div class="section-head"><h2>T\u1EEB v\u1EF1ng trong b\xE0i</h2><span>').concat(words.length, ' t\u1EEB</span></div><div class="card list-panel">').concat(words.map(wordRow).join(""), '</div><p class="source">').concat(esc(l.source), "</p>");
}
function wordsPage() {
  let words = WORDS.filter((w) => w.lang === lang);
  const q = search.trim().toLocaleLowerCase("vi").normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  if (q) words = words.filter((w) => [w.text, w.meaning, w.pron].join(" ").toLocaleLowerCase("vi").normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes(q));
  if (wordFilter === "saved") words = words.filter((w) => state.favorites.includes(w.id));
  if (wordFilter === "new") words = words.filter((w) => {
    var _a;
    return !((_a = state.progress[w.id]) == null ? void 0 : _a.reps);
  });
  if (wordFilter === "due") words = words.filter((w) => {
    var _a;
    return ((_a = state.progress[w.id]) == null ? void 0 : _a.due) <= Date.now();
  });
  return '<div class="page-head"><div class="eyebrow">T\u1EEB \u0111i\u1EC3n nh\u1ECF c\u1EE7a b\u1EA1n</div><h1>Kho t\u1EEB v\u1EF1ng</h1><p>T\xECm t\u1EEB, nghe ph\xE1t \xE2m v\xE0 l\u01B0u nh\u1EEFng t\u1EEB c\u1EA7n nh\u1EDB.</p></div>'.concat(languagePills(), '<label class="search">').concat(icon("search"), '<input id="search" value="').concat(esc(search), '" placeholder="T\xECm t\u1EEB, ngh\u0129a ho\u1EB7c pinyin\u2026" aria-label="T\xECm t\u1EEB v\u1EF1ng" autocomplete="off"></label><div class="pillbar">').concat([["all", "T\u1EA5t c\u1EA3"], ["saved", "\u0110\xE3 l\u01B0u"], ["new", "Ch\u01B0a h\u1ECDc"], ["due", "C\u1EA7n \xF4n"]].map(([v, t]) => '<button class="pill '.concat(wordFilter === v ? "active" : "", '" data-action="filter" data-filter="').concat(v, '">').concat(t, "</button>")).join(""), '</div><p class="filter-count">').concat(words.length, ' t\u1EEB ph\xF9 h\u1EE3p</p><div class="card list-panel" id="word-results">').concat(words.length ? words.map(wordRow).join("") : '<div class="empty">Ch\u01B0a c\xF3 t\u1EEB ph\xF9 h\u1EE3p.</div>', "</div>");
}
function detailPage() {
  const w = BYID[currentWord];
  return "".concat(backButton(lastDetail === "words" ? "Kho t\u1EEB v\u1EF1ng" : "T\u1EEB v\u1EF1ng trong b\xE0i"), '<div class="word-detail">').concat(wordCard(w, true, true), '</div><button class="secondary" data-action="review-word" data-id="').concat(w.id, '">').concat(icon("book"), "\xD4n t\u1EEB n\xE0y</button>");
}
function wordCard(w, reveal, detail = false) {
  return '<div class="card study-card">'.concat(detail ? '<button class="favorite '.concat(state.favorites.includes(w.id) ? "saved" : "", '" data-action="favorite" data-id="').concat(w.id, '" aria-label="').concat(state.favorites.includes(w.id) ? "B\u1ECF l\u01B0u t\u1EEB" : "L\u01B0u t\u1EEB", '">').concat(icon("star"), "</button>") : "", '<div class="eyebrow">').concat(w.lang === "en" ? "English vocabulary" : "\u6C49\u8BED\u8BCD\u6C47", '</div><div class="word">').concat(esc(w.text), "</div>").concat(w.lang === "en" || reveal ? '<div class="pronunciation">'.concat(esc(w.pron), "</div>") : '<div class="pronunciation">\u0110o\xE1n c\xE1ch \u0111\u1ECDc v\xE0 ngh\u0129a</div>').concat(audioButton(w.id)).concat(reveal ? '<div class="meaning">'.concat(esc(w.meaning), '</div><div class="type-tag">').concat(esc(w.pos), "</div>").concat(w.example ? '<div class="example"><b>'.concat(esc(w.example), "</b>").concat(w.examplePron ? '<p class="small muted">'.concat(esc(w.examplePron), "</p>") : "", '<p class="translation">').concat(esc(w.translation), "</p></div>") : "", '<p class="source">').concat(esc(w.source), "</p>") : "", "</div>");
}
function shuffle(array) {
  const out = [...array];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}
function startStudy(words, mode = "cards", label = "\xD4n t\u1EADp", context = "lesson") {
  if (!words.length) {
    toast("Ch\u01B0a c\xF3 t\u1EEB \u0111\u1EBFn h\u1EA1n \xF4n trong m\u1EE5c n\xE0y.");
    return;
  }
  stopAudio();
  study = { queue: mode === "cards" ? [...words] : shuffle(words), index: 0, reveal: false, mode, label, context, correct: 0, answered: false, choice: null, options: null };
  page = "study";
  render();
}
function quizMenu() {
  const l = LESSONS.find((x) => x.id === lessonId);
  return '<div class="page-head">'.concat(backButton("V\u1EC1 b\xE0i h\u1ECDc"), "<h1>Luy\u1EC7n t\u1EADp</h1><p>").concat(esc(l.title), ' \xB7 Ch\u1ECDn c\xE1ch b\u1EA1n mu\u1ED1n luy\u1EC7n</p></div><div class="stack">').concat([["meaning", "Ch\u1ECDn ngh\u0129a \u0111\xFAng", "Nh\xECn t\u1EEB v\xE0 ch\u1ECDn ngh\u0129a ti\u1EBFng Vi\u1EC7t.", "book"], ["reverse", "Nh\u1EDB t\u1EEB qua ngh\u0129a", "Ch\u1ECDn t\u1EEB ph\xF9 h\u1EE3p v\u1EDBi ngh\u0129a cho tr\u01B0\u1EDBc.", "layers"], ["listening", "Nghe v\xE0 nh\u1EADn di\u1EC7n", "Nghe ph\xE1t \xE2m r\u1ED3i ch\u1ECDn t\u1EEB \u0111\xFAng.", "sound"], ["typing", lang === "en" ? "Luy\u1EC7n ch\xEDnh t\u1EA3" : "Nh\u1EADp ch\u1EEF H\xE1n", "Nh\xECn ngh\u0129a v\xE0 nh\u1EADp t\u1EEB b\u1EB1ng b\xE0n ph\xEDm.", "settings"]].map(([mode, title, desc, i]) => '<button class="lesson" data-action="start-quiz" data-mode="'.concat(mode, '"><div class="lesson-icon">').concat(icon(i), '</div><div class="lesson-main"><h3>').concat(title, "</h3><p>").concat(desc, "</p></div>").concat(icon("chevron", "chevron"), "</button>")).join(""), "</div>");
}
function makeOptions(w) {
  const pool = shuffle(WORDS.filter((x) => x.lang === w.lang && x.id !== w.id && x.meaning !== w.meaning));
  return shuffle([w, ...pool.slice(0, 3)]);
}
function studyPage() {
  if (study.index >= study.queue.length) return donePage();
  const w = study.queue[study.index];
  lang = w.lang;
  const header = '<div class="study-top"><button class="iconbtn" data-action="exit-study" aria-label="Tho\xE1t l\u01B0\u1EE3t h\u1ECDc">'.concat(icon("close"), "</button><span>").concat(esc(study.label), '</span><b class="small">').concat(study.index + 1, "/").concat(study.queue.length, '</b></div><div class="progress"><i style="width:').concat(percentage(study.index, study.queue.length), '%"></i></div>');
  if (study.mode === "cards") return "".concat(header).concat(wordCard(w, study.reveal), '<button class="speed-toggle ').concat(state.settings.slow ? "active" : "", '" data-action="slow">').concat(icon("sound"), "Gi\u1ECDng \u0111\u1ECDc ").concat(state.settings.slow ? "ch\u1EADm" : "b\xECnh th\u01B0\u1EDDng", " \xB7 B\u1EA5m \u0111\u1EC3 \u0111\u1ED5i</button>").concat(study.reveal ? '<p class="hint">B\u1EA1n nh\u1EDB t\u1EEB n\xE0y \u1EDF m\u1EE9c n\xE0o?</p><div class="ratings">'.concat([["again", "Qu\xEAn", "10 ph\xFAt"], ["hard", "Kh\xF3", "1 ng\xE0y"], ["good", "Nh\u1EDB", "Gi\xE3n l\u1ECBch \xF4n"], ["easy", "D\u1EC5", "\xD4n xa h\u01A1n"]].map(([v, t, d]) => '<button class="rating" data-action="rate" data-rating="'.concat(v, '">').concat(t, "<small>").concat(d, "</small></button>")).join(""), "</div>") : '<p class="hint">Th\u1EED nh\u1EDB ngh\u0129a tr\u01B0\u1EDBc khi m\u1EDF th\u1EBB nh\xE9.</p><button class="primary" data-action="reveal">Hi\u1EC7n ngh\u0129a '.concat(icon("arrow"), "</button>"));
  const mode = study.mode;
  if (!study.options) study.options = makeOptions(w);
  const prompt = mode === "meaning" ? w.text : mode === "listening" ? "Nghe v\xE0 ch\u1ECDn t\u1EEB \u0111\xFAng" : w.meaning;
  const question = '<div class="card study-card" style="min-height:210px"><div class="eyebrow">'.concat(mode === "typing" ? "Nh\u1EADp t\u1EEB ph\xF9 h\u1EE3p" : "Ch\u1ECDn m\u1ED9t \u0111\xE1p \xE1n", '</div><div class="word" style="font-size:').concat(mode === "meaning" && lang === "zh" ? 42 : 27, 'px">').concat(esc(prompt), "</div>").concat(mode === "listening" ? audioButton(w.id) : "", "</div>");
  const answer = mode === "typing" ? '<input class="answer-input" id="typed-answer" aria-label="Nh\u1EADp t\u1EEB tr\u1EA3 l\u1EDDi" placeholder="'.concat(lang === "en" ? "Nh\u1EADp t\u1EEB ti\u1EBFng Anh\u2026" : "Nh\u1EADp ch\u1EEF H\xE1n gi\u1EA3n th\u1EC3\u2026", '" autocapitalize="off" autocomplete="off" spellcheck="false" ').concat(study.answered ? "disabled" : "", '><button class="primary" data-action="check-typing" ').concat(study.answered ? "disabled" : "", ">Ki\u1EC3m tra</button>") : study.options.map((o) => '<button class="choice '.concat(study.answered ? o.id === w.id ? "correct" : o.id === study.choice ? "wrong" : "" : "", '" data-action="answer" data-id="').concat(o.id, '" ').concat(study.answered ? "disabled" : "", ">").concat(esc(mode === "meaning" ? o.meaning : o.text), "</button>")).join("");
  return "".concat(header).concat(question).concat(answer).concat(study.answered ? '<div class="feedback"><b>'.concat(study.choice === w.id ? "Ch\xEDnh x\xE1c!" : "M\xECnh c\xF9ng ghi nh\u1EDB l\u1EA1i nh\xE9.", '</b><p style="margin-top:8px">').concat(esc(w.text), " \xB7 ").concat(esc(w.pron), "<br>").concat(esc(w.meaning), '</p><div style="margin-top:10px">').concat(audioButton(w.id), '</div></div><button class="primary" data-action="next-question">').concat(study.index === study.queue.length - 1 ? "Xem k\u1EBFt qu\u1EA3" : "C\xE2u ti\u1EBFp theo", " ").concat(icon("arrow"), "</button>") : "");
}
function markRated(id, rating) {
  const p = state.progress[id] || { interval: 0, reps: 0, lapses: 0 };
  let interval;
  if (rating === "again") interval = 10 / 1440;
  else if (rating === "hard") interval = 1;
  else if (rating === "good") interval = p.reps ? Math.max(2, Math.ceil(p.interval * 2)) : 2;
  else interval = p.reps ? Math.max(4, Math.ceil(p.interval * 3)) : 4;
  interval = Math.min(365, interval);
  state.progress[id] = { interval, due: Date.now() + interval * 864e5, reps: p.reps + 1, lapses: p.lapses + (rating === "again" ? 1 : 0), last: localDay() };
  state.daily[localDay()] = (state.daily[localDay()] || 0) + 1;
  save();
}
function donePage() {
  return '<div class="done"><div class="big-symbol">'.concat(icon("trophy"), '</div><div class="eyebrow">M\u1ED9t b\u01B0\u1EDBc ti\u1EBFn m\u1EDBi</div><h1 style="margin-top:10px">B\u1EA1n l\xE0m t\u1ED1t l\u1EAFm!</h1><p>').concat(study.mode === "cards" ? "\u0110\xE3 \xF4n ".concat(study.queue.length, " t\u1EEB. App \u0111\xE3 l\u01B0u ti\u1EBFn \u0111\u1ED9 v\xE0 l\xEAn l\u1ECBch \xF4n ti\u1EBFp.") : "B\u1EA1n tr\u1EA3 l\u1EDDi \u0111\xFAng ".concat(study.correct, "/").concat(study.queue.length, " c\xE2u. C\xE1c t\u1EEB \u0111\xE3 \u0111\u01B0\u1EE3c c\u1EADp nh\u1EADt l\u1ECBch \xF4n."), '</p></div><div class="stats-grid"><div class="card stat"><strong>').concat(study.queue.length, "</strong><span>").concat(study.mode === "cards" ? "T\u1EEB v\u1EEBa \xF4n" : "C\xE2u luy\u1EC7n t\u1EADp", '</span></div><div class="card stat"><strong>').concat(streak(), '</strong><span>Ng\xE0y h\u1ECDc li\xEAn ti\u1EBFp</span></div></div><button class="primary" data-action="exit-study">V\u1EC1 b\xE0i h\u1ECDc ').concat(icon("arrow"), "</button>");
}
function statsPage() {
  const words = WORDS.filter((w) => w.lang === lang), n = learned(words), due = dueWords(lang).length;
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = /* @__PURE__ */ new Date();
    d.setDate(d.getDate() - i);
    days.push({ label: d.getDate() + "/" + (d.getMonth() + 1), value: state.daily[localDay(d)] || 0 });
  }
  const max = Math.max(...days.map((x) => x.value), state.settings.goal);
  return '<div class="page-head"><div class="eyebrow">T\xEDch l\u0169y t\u1EEBng ng\xE0y</div><h1>Ti\u1EBFn \u0111\u1ED9 c\u1EE7a b\u1EA1n</h1><p>'.concat(streak(), " ng\xE0y h\u1ECDc li\xEAn ti\u1EBFp \xB7 ").concat(todayCount(), " l\u01B0\u1EE3t \xF4n h\xF4m nay</p></div>").concat(languagePills(), '<div class="stats-grid">').concat([[n, "T\u1EEB \u0111\xE3 h\u1ECDc", "book"], [due, "T\u1EEB \u0111\u1EBFn h\u1EA1n \xF4n", "clock"], [words.length - n, "T\u1EEB ch\u01B0a h\u1ECDc", "layers"], [percentage(n, words.length) + "%", "Ti\u1EBFn \u0111\u1ED9 h\u1ECDc t\u1EEB", "chart"]].map(([v, t, i]) => '<div class="card stat">'.concat(icon(i), "<strong>").concat(v, "</strong><span>").concat(t, "</span></div>")).join(""), '</div><div class="card"><h3>7 ng\xE0y g\u1EA7n \u0111\xE2y</h3><p class="small muted">L\u01B0\u1EE3t \xF4n c\u1EE7a c\u1EA3 hai ng\xF4n ng\u1EEF</p><div class="daily-bars">').concat(days.map((x) => '<div class="day-bar"><b>'.concat(x.value, '</b><i style="height:').concat(Math.max(4, x.value / max * 65), 'px"></i><span>').concat(x.label, "</span></div>")).join(""), "</div></div>").concat(due ? '<button class="primary" style="margin-top:18px" data-action="review" data-lang="'.concat(lang, '">\xD4n ').concat(due, " t\u1EEB \u0111\u1EBFn h\u1EA1n ").concat(icon("arrow"), "</button>") : "", '<div class="section-head"><h2>Theo b\xE0i h\u1ECDc</h2></div><div class="stack">').concat(LESSONS.filter((l) => l.lang === lang && l.kind === "unit").map(lessonTile).join(""), "</div>");
}
function settingsPage() {
  return '<div class="page-head"><div class="eyebrow">Theo c\xE1ch c\u1EE7a b\u1EA1n</div><h1>C\xE0i \u0111\u1EB7t</h1><p>M\u1ED9t kh\xF4ng gian h\u1ECDc tho\u1EA3i m\xE1i v\xE0 ri\xEAng t\u01B0.</p></div><div class="card"><div class="setting-row"><div><b>Giao di\u1EC7n t\u1ED1i</b><p>D\u1ECBu m\u1EAFt khi h\u1ECDc bu\u1ED5i t\u1ED1i</p></div><button class="toggle '.concat(state.settings.dark ? "on" : "", '" data-action="dark" aria-label="Giao di\u1EC7n t\u1ED1i" aria-pressed="').concat(state.settings.dark, '"><span></span></button></div><div class="setting-row"><div><b>\u0110\u1ECDc ch\u1EADm</b><p>Gi\u1EA3m t\u1ED1c \u0111\u1ED9, gi\u1EEF nguy\xEAn cao \u0111\u1ED9 gi\u1ECDng</p></div><button class="toggle ').concat(state.settings.slow ? "on" : "", '" data-action="slow" aria-label="\u0110\u1ECDc ch\u1EADm" aria-pressed="').concat(state.settings.slow, '"><span></span></button></div><div class="setting-row"><div><b>M\u1EE5c ti\xEAu m\u1ED7i ng\xE0y</b><p>S\u1ED1 l\u01B0\u1EE3t \xF4n t\u1EEB v\u1EF1ng</p></div><select id="daily-goal" aria-label="M\u1EE5c ti\xEAu m\u1ED7i ng\xE0y">').concat([5, 10, 15, 20, 30].map((n) => '<option value="'.concat(n, '" ').concat(state.settings.goal === n ? "selected" : "", ">").concat(n, " l\u01B0\u1EE3t</option>")).join(""), '</select></div></div><div class="section-head"><h2>Sao l\u01B0u ti\u1EBFn \u0111\u1ED9</h2></div><div class="stack"><button class="secondary" data-action="export">').concat(icon("download"), 'Xu\u1EA5t b\u1EA3n sao l\u01B0u</button><button class="secondary" data-action="import">').concat(icon("upload"), 'Kh\xF4i ph\u1EE5c t\u1EEB b\u1EA3n sao l\u01B0u</button></div><div class="notice">B\u1EA3n sao l\u01B0u g\u1ED3m ti\u1EBFn \u0111\u1ED9, t\u1EEB \u0111\xE3 l\u01B0u v\xE0 c\xE0i \u0111\u1EB7t. Kh\xF4i ph\u1EE5c s\u1EBD thay th\u1EBF ti\u1EBFn \u0111\u1ED9 hi\u1EC7n t\u1EA1i sau khi b\u1EA1n x\xE1c nh\u1EADn. N\xEAn sao l\u01B0u tr\u01B0\u1EDBc khi \u0111\u1ED5i \u0111i\u1EC7n tho\u1EA1i ho\u1EB7c g\u1EE1 app.</div><div class="section-head"><h2>V\u1EC1 Lingo</h2><span>Phi\xEAn b\u1EA3n 1.0.0</span></div><div class="card stack"><div><b>Ti\u1EBFng Anh</b><p class="small muted">T\u1EEB tr\u1ECDng t\xE2m theo Glossary c\u1EE7a s\xE1ch Ti\u1EBFng Anh 7 Global Success. C\xE2u v\xED d\u1EE5 trong app \u0111\u01B0\u1EE3c bi\xEAn so\u1EA1n b\u1ED5 sung.</p></div><div><b>Ti\u1EBFng Hoa</b><p class="small muted">Ch\u1EEF gi\u1EA3n th\u1EC3, pinyin v\xE0 ngh\u0129a ti\u1EBFng Vi\u1EC7t. T\u1EEB v\xE0 c\xE2u ngu\u1ED3n \u0111\u01B0\u1EE3c \u0111\u1ED1i chi\u1EBFu v\u1EDBi 13 PDF \u0111\u1EC1 HSK 4 \u0111\xE3 cung c\u1EA5p; \u0111\xE2y kh\xF4ng ph\u1EA3i danh s\xE1ch \u0111\u1EA7y \u0111\u1EE7 m\u1ECDi t\u1EEB HSK 4.</p></div><div><b>Gi\u1ECDng \u0111\u1ECDc ngo\u1EA1i tuy\u1EBFn</b><p class="small muted">\xC2m thanh t\u1ED5ng h\u1EE3p cho t\u1EEBng t\u1EEB \u0111\u01B0\u1EE3c \u0111\xF3ng g\xF3i s\u1EB5n. Kh\xF4ng c\u1EA7n t\u1EA3i gi\u1ECDng \u0111\u1ECDc, kh\xF4ng c\u1EA7n t\xE0i kho\u1EA3n hay k\u1EBFt n\u1ED1i m\u1EA1ng. C\xE2u v\xED d\u1EE5 hi\u1EC7n hi\u1EC3n th\u1ECB b\u1EB1ng ch\u1EEF.</p></div></div>');
}
function render() {
  applyTheme();
  let body;
  switch (page) {
    case "home":
      body = home();
      break;
    case "library":
      body = library();
      break;
    case "lesson":
      body = lessonPage();
      break;
    case "words":
      body = wordsPage();
      break;
    case "detail":
      body = detailPage();
      break;
    case "quiz-menu":
      body = quizMenu();
      break;
    case "study":
      body = studyPage();
      break;
    case "stats":
      body = statsPage();
      break;
    case "settings":
      body = settingsPage();
      break;
    default:
      page = "home";
      body = home();
  }
  $("#app").innerHTML = '<main class="screen '.concat(page === "home" ? "home-screen" : "", " ").concat(lang === "zh" && page !== "home" ? "zh-tone" : "", " ").concat(page === "study" ? "study-screen" : "", '">').concat(body, "</main>").concat(["study", "detail", "quiz-menu"].includes(page) ? "" : nav());
  window.scrollTo(0, 0);
}
function openLesson(id) {
  const l = LESSONS.find((x) => x.id === id);
  if (!l) return;
  lessonId = id;
  lang = l.lang;
  state.last[lang] = id;
  save();
  page = "lesson";
  render();
}
function back() {
  if (page === "home") return false;
  if (page === "study") {
    if (study.index < study.queue.length && !confirm("Tho\xE1t l\u01B0\u1EE3t h\u1ECDc? Ti\u1EBFn \u0111\u1ED9 c\xE1c t\u1EEB \u0111\xE3 tr\u1EA3 l\u1EDDi v\u1EABn \u0111\u01B0\u1EE3c l\u01B0u.")) return true;
    stopAudio();
    page = study.context;
    study = null;
  } else if (page === "detail") page = lastDetail;
  else if (page === "quiz-menu") page = "lesson";
  else if (page === "lesson") page = "library";
  else page = "home";
  render();
  return true;
}
window.handleBack = back;
function backup() {
  return JSON.stringify({ ...state, app: "Lingo", exportedAt: (/* @__PURE__ */ new Date()).toISOString() }, null, 2);
}
window.receiveBackup = (raw) => {
  try {
    const proposed = validateState(JSON.parse(raw));
    if (!confirm("Kh\xF4i ph\u1EE5c b\u1EA3n sao l\u01B0u v\xE0 thay th\u1EBF ti\u1EBFn \u0111\u1ED9 hi\u1EC7n t\u1EA1i?")) return;
    state = proposed;
    save();
    render();
    toast("\u0110\xE3 kh\xF4i ph\u1EE5c ti\u1EBFn \u0111\u1ED9.");
  } catch (e) {
    toast("B\u1EA3n sao l\u01B0u kh\xF4ng h\u1EE3p l\u1EC7 ho\u1EB7c kh\xF4ng t\u01B0\u01A1ng th\xEDch.");
  }
};
document.addEventListener("click", (e) => {
  const el = e.target.closest("[data-action]");
  if (!el || el.disabled) return;
  const a = el.dataset.action;
  switch (a) {
    case "nav":
      stopAudio();
      page = el.dataset.page;
      search = "";
      render();
      break;
    case "open-language":
      lang = el.dataset.lang;
      section = "units";
      if (state.last[lang]) openLesson(state.last[lang]);
      else {
        page = "library";
        render();
      }
      break;
    case "lang":
      lang = el.dataset.lang;
      section = "units";
      render();
      break;
    case "section":
      section = el.dataset.section;
      render();
      break;
    case "lesson":
      openLesson(el.dataset.id);
      break;
    case "back":
      back();
      break;
    case "audio":
      playWord(el.dataset.id);
      break;
    case "word":
      lastDetail = page;
      currentWord = el.dataset.id;
      page = "detail";
      render();
      break;
    case "favorite": {
      const id = el.dataset.id;
      state.favorites = state.favorites.includes(id) ? state.favorites.filter((x) => x !== id) : [...state.favorites, id];
      save();
      render();
      break;
    }
    case "filter":
      wordFilter = el.dataset.filter;
      render();
      break;
    case "learn": {
      let words = lessonWords(lessonId);
      if (el.dataset.mode === "due") words = words.filter((w) => {
        var _a;
        return ((_a = state.progress[w.id]) == null ? void 0 : _a.due) <= Date.now();
      });
      else if (el.dataset.mode === "new") {
        const fresh = words.filter((w) => {
          var _a;
          return !((_a = state.progress[w.id]) == null ? void 0 : _a.reps);
        });
        if (fresh.length) words = fresh;
      }
      startStudy(words, "cards", LESSONS.find((x) => x.id === lessonId).short);
      break;
    }
    case "review": {
      const l = el.dataset.lang === "all" ? null : el.dataset.lang;
      startStudy(dueWords(l), "cards", l ? languageName(l) + " \xB7 \xD4n t\u1EADp" : "\xD4n t\u1EADp h\u1EB1ng ng\xE0y", page);
      break;
    }
    case "review-word":
      startStudy([BYID[el.dataset.id]], "cards", "\xD4n m\u1ED9t t\u1EEB", "detail");
      break;
    case "reveal":
      study.reveal = true;
      render();
      break;
    case "rate":
      if (!(study == null ? void 0 : study.reveal)) break;
      markRated(study.queue[study.index].id, el.dataset.rating);
      stopAudio();
      study.index++;
      study.reveal = false;
      render();
      break;
    case "quiz-menu":
      page = "quiz-menu";
      render();
      break;
    case "start-quiz":
      startStudy(lessonWords(lessonId), el.dataset.mode, LESSONS.find((x) => x.id === lessonId).short);
      break;
    case "answer":
      if (study.answered) break;
      answerQuestion(el.dataset.id);
      break;
    case "check-typing": {
      if (study.answered) break;
      const text = $("#typed-answer").value.trim();
      if (!text) {
        toast("B\u1EA1n nh\u1EADp c\xE2u tr\u1EA3 l\u1EDDi tr\u01B0\u1EDBc nh\xE9.");
        break;
      }
      const w = study.queue[study.index];
      answerQuestion(normalizeAnswer(text) === normalizeAnswer(w.text) ? w.id : "wrong");
      break;
    }
    case "next-question":
      stopAudio();
      study.index++;
      study.answered = false;
      study.options = null;
      study.choice = null;
      render();
      break;
    case "exit-study":
      if (study.index >= study.queue.length) {
        stopAudio();
        page = study.context;
        study = null;
        render();
      } else back();
      break;
    case "dark":
      state.settings.dark = !state.settings.dark;
      save();
      render();
      break;
    case "slow":
      state.settings.slow = !state.settings.slow;
      save();
      render();
      break;
    case "export":
      if (window.Android) Android.exportBackup(backup());
      else {
        const url = URL.createObjectURL(new Blob([backup()], { type: "application/json" }));
        const a2 = document.createElement("a");
        a2.href = url;
        a2.download = "Lingo-backup.json";
        a2.click();
        setTimeout(() => URL.revokeObjectURL(url), 1e3);
      }
      break;
    case "import":
      if (window.Android) Android.importBackup();
      else $("#backup-file").click();
      break;
  }
});
function normalizeAnswer(s) {
  return s.normalize("NFKC").toLowerCase().replace(/[’‘]/g, "'").replace(/[.,!?。！？]/g, "").replace(/\s+/g, " ").trim();
}
function answerQuestion(id) {
  const w = study.queue[study.index];
  study.choice = id;
  study.answered = true;
  if (id === w.id) study.correct++;
  markRated(w.id, id === w.id ? "good" : "again");
  render();
}
document.addEventListener("input", (e) => {
  if (e.target.id === "search") {
    const position = e.target.selectionStart;
    search = e.target.value;
    const scroll = window.scrollY;
    render();
    const field = $("#search");
    field.focus();
    field.setSelectionRange(position, position);
    window.scrollTo(0, scroll);
  }
});
document.addEventListener("change", (e) => {
  if (e.target.id === "daily-goal") {
    state.settings.goal = Number(e.target.value);
    save();
    toast("\u0110\xE3 c\u1EADp nh\u1EADt m\u1EE5c ti\xEAu.");
  }
  if (e.target.id === "backup-file" && e.target.files[0]) {
    const f = e.target.files[0];
    if (f.size > 5 * 1024 * 1024) {
      toast("B\u1EA3n sao l\u01B0u qu\xE1 l\u1EDBn.");
      return;
    }
    f.text().then(window.receiveBackup);
    e.target.value = "";
  }
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && e.target.id === "typed-answer" && !study.answered) {
    $('[data-action="check-typing"]').click();
  }
});
window.nativeReady = () => {
  readState();
  render();
};
readState();
render();
