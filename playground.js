// The KROMA playground: describe two concepts, see the prompt KROMA builds for them, and ask a model you run.
// Prompt building and answer extraction are ports of kroma.tasks.prompts.builders and kroma.agents.utils; the templates
// are exported from the Python (playground-data.json), so the text is the same.
var KP = (function () {
  function cleanTerms(terms) {
    return terms.filter(function (t) { return t.length >= 2 && t.indexOf("_") < 0 && !/\d/.test(t); });
  }
  function listToStr(items) { return items.length ? items.join(", ") : "none"; }
  function unique(list) { var seen = {}, out = []; list.forEach(function (x) { if (!seen[x]) { seen[x] = 1; out.push(x); } }); return out; }
  // side = [name, parents, children, synonyms, labels]; returns {system, user}
  function buildTaskPrompt(templates, source, target) {
    var sLab = cleanTerms(unique((source[4] || []).concat([source[0]]))), tLab = cleanTerms(unique((target[4] || []).concat([target[0]])));
    var fill = {
      demonstrations: "", src_names: listToStr(sLab), src_parents: listToStr(cleanTerms(source[1])), src_children: listToStr(cleanTerms(source[2])), src_synonyms: listToStr(cleanTerms(source[3])),
      tgt_names: listToStr(tLab), tgt_parents: listToStr(cleanTerms(target[1])), tgt_children: listToStr(cleanTerms(target[2])), tgt_synonyms: listToStr(cleanTerms(target[3])),
    };
    var user = templates.task.replace(/\{(\w+)\}/g, function (m, k) { return k in fill ? fill[k] : m; });
    return { system: templates.system.trim(), user: user.trim() };
  }
  function extractYesNo(response) { var m = /<answer>\s*(yes|no)\s*<\/answer>/i.exec(response); return m && m[1].toLowerCase() === "yes" ? 1 : 0; }
  function extractConfidence(response) { var m = /<confidence>\s*(\d{1,2})\s*<\/confidence>/.exec(response), v = m ? parseInt(m[1], 10) : 0; return v >= 0 && v <= 10 ? v : 0; }
  function majorityVote(answers) {
    var counts = {}; answers.forEach(function (a) { (counts[a[0]] = counts[a[0]] || []).push(a[1]); });
    var best = Object.keys(counts).sort(function (x, y) { return counts[y].length - counts[x].length; })[0];
    return [parseInt(best, 10), Math.floor(counts[best].reduce(function (a, b) { return a + b; }, 0) / counts[best].length)];
  }
  return { cleanTerms: cleanTerms, buildTaskPrompt: buildTaskPrompt, extractYesNo: extractYesNo, extractConfidence: extractConfidence, majorityVote: majorityVote };
})();

(async function () {
  var root = document.getElementById("kplay");
  if (!root) return;
  var h = PG.h, templates, pairs;
  var list = function (s) { return s.split(",").map(function (x) { return x.trim(); }).filter(Boolean); };
  var FIELDS = [["name", "Name", "A name for the concept"], ["parents", "Parents", "comma-separated"], ["children", "Children", "comma-separated"], ["synonyms", "Synonyms", "comma-separated"]];
  var inputs = { source: {}, target: {} };
  function side(which, title) {
    return h("div", { class: "pg-panel" }, h("h3", { text: title }),
      FIELDS.map(function (f) {
        var i = h("input", { type: "text", id: "kp-" + which + "-" + f[0], placeholder: f[2], autocomplete: "off", "aria-label": title + " " + f[1].toLowerCase() });
        i.addEventListener("input", update); inputs[which][f[0]] = i;
        return h("label", { class: "pg-field", for: i.id }, f[1], i);
      }));
  }
  var picker = h("select", { id: "kp-pair", "aria-label": "Example pair" });
  var systemBox = h("pre", { class: "pg-pre", id: "kp-system" }), userBox = h("pre", { class: "pg-pre", id: "kp-user" });
  var answer = h("div", { id: "kp-answer", "aria-live": "polite" }), recordedBox = h("p", { class: "pg-line", id: "kp-recorded" });

  function read(which) { var v = inputs[which]; return [v.name.value.trim(), list(v.parents.value), list(v.children.value), list(v.synonyms.value), []]; }
  function fillSide(which, ctx) { var v = inputs[which]; v.name.value = ctx[0]; v.parents.value = ctx[1].join(", "); v.children.value = ctx[2].join(", "); v.synonyms.value = ctx[3].join(", "); }
  function prompt() { return KP.buildTaskPrompt(templates, read("source"), read("target")); }
  function update() { var p = prompt(); systemBox.textContent = p.system; userBox.textContent = p.user; }
  function load(i) {
    answer.replaceChildren();
    if (i < 0) { fillSide("source", ["", [], [], []]); fillSide("target", ["", [], [], []]); recordedBox.textContent = ""; update(); return; }
    var p = pairs[i]; fillSide("source", p.context.source); fillSide("target", p.context.target);
    var tier = { evidence: "settled by evidence, no model asked", local: "settled by the local model", api: "settled by the API model" }[p.tier] || p.tier;
    recordedBox.textContent = "The recorded run answered " + p.answer + " at confidence " + p.confidence.toFixed(2) + " (" + tier + "), and the reference " + (p.correct ? "agrees." : "disagrees.");
    update();
  }
  function showReply(reply) {
    var yes = KP.extractYesNo(reply), conf = KP.extractConfidence(reply), tagged = /<answer>/i.test(reply);
    answer.replaceChildren(h("p", { class: "pg-line" }, "KROMA reads ", h("b", { text: yes ? "Yes" : "No" }), " at confidence ", h("b", { text: conf + " / 10" }), ". ", h("span", { class: "pg-tag " + (tagged ? "ok" : "bad"), text: tagged ? "answer tag found" : "no <answer> tag: KROMA would count this as No" })),
      h("pre", { class: "pg-pre", text: reply.trim() }));
  }
  async function ask() {
    var p = prompt(); answer.replaceChildren(h("p", { class: "pg-line", text: "Asking " + PG.llmConfig().model + "…" }));
    try { showReply(await PG.chat([{ role: "system", content: p.system }, { role: "user", content: p.user }])); }
    catch (e) { answer.replaceChildren(h("div", { class: "pg-error", role: "alert", text: String(e.message || e) })); }
  }
  var paste = h("textarea", { id: "kp-paste", spellcheck: "false", placeholder: "Or paste a model's reply here, for example: <answer>Yes</answer> <confidence>8</confidence>", "aria-label": "A model's reply" });
  function copyPrompt() { var p = prompt(); (navigator.clipboard ? navigator.clipboard.writeText(p.system + "\n\n" + p.user) : Promise.reject()).then(function () { answer.replaceChildren(h("p", { class: "pg-line", text: "Prompt copied (system, then task). Paste it into any chat model, then paste its reply below." })); }, function () { answer.replaceChildren(h("p", { class: "pg-line", text: "Could not copy: select the prompt above and copy it." })); }); }

  root.className = "pg";
  var llm = h("div", { id: "kp-llm" });
  root.replaceChildren(
    h("div", { class: "pg-panel" }, h("h3", { text: "1. Describe two concepts" }), h("p", { class: "pg-sub", text: "Start from a real Mouse–Human pair, or type your own. KROMA gives the model each concept's names, parents, children, and synonyms." }),
      h("div", { class: "pg-row" }, h("label", { for: "kp-pair" }, "Example "), picker), recordedBox),
    h("div", { class: "pg-cols" }, side("source", "Source concept"), side("target", "Target concept")),
    h("div", { class: "pg-panel" }, h("h3", { text: "2. The prompt KROMA builds" }), h("p", { class: "pg-sub", text: "Terms that are short, contain digits, or contain underscores are dropped, as KROMA drops them. The system prompt comes first, then the task." }),
      h("p", { class: "pg-sub", text: "System" }), systemBox, h("p", { class: "pg-sub", text: "Task" }), userBox),
    h("div", { class: "pg-panel" }, h("h3", { text: "3. Ask a model" }), h("p", { class: "pg-sub", text: "Send the prompt to a model you run. KROMA reads the answer from an <answer> tag and the confidence from a <confidence> tag, and treats anything else as No." }),
      h("div", { class: "pg-row" }, h("button", { type: "button", class: "btn solid", id: "kp-ask", onclick: ask }, "Ask my model"), h("button", { type: "button", class: "btn", id: "kp-copy", onclick: copyPrompt }, "Copy the prompt")),
      h("div", { class: "pg-row" }, paste), h("div", { class: "pg-row" }, h("button", { type: "button", class: "btn", id: "kp-use", onclick: function () { showReply(paste.value); } }, "Read this reply")), answer),
    h("details", { class: "pg-panel" }, h("summary", { text: "Your model" }), llm));

  var [t, demo] = await Promise.all([fetch("playground-data.json").then(function (r) { return r.json(); }), fetch("demo-data.json").then(function (r) { return r.json(); })]);
  templates = t; pairs = demo.pairs;
  picker.replaceChildren.apply(picker, [h("option", { value: -1, text: "Blank" })].concat(pairs.map(function (p, i) { return h("option", { value: i, text: p.source + " ↔ " + p.target }); })));
  picker.onchange = function () { load(+picker.value); };
  PG.llmPanel(llm);
  picker.value = 0; load(0);
})();
