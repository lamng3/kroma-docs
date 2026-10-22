// Shows prompts KROMA builds for real Mouse-Human pairs, with the answers a recorded run gave (demo-data.json,
// exported by demo_data.py). Nothing is asked of a model here.
(function () {
  var root = document.getElementById("demo");
  if (!root) return;
  var el = function (id) { return document.getElementById(id); };
  var TIER = { evidence: "settled by evidence, no model asked", local: "settled by the local model", api: "settled by the API model" };

  function pick(data, i) {
    var p = data.pairs[i];
    Array.prototype.forEach.call(el("tabs").children, function (b, j) { b.setAttribute("aria-selected", j === i ? "true" : "false"); });
    el("prompt").textContent = p.prompt.replace(/Task definition:[\s\S]*?Consider the following:\n\n/, "");
    var v = el("verdict");
    v.innerHTML = '<span class="pill-tier"></span><span>answer <b></b> at confidence <b></b></span><span class="res"></span>';
    v.children[0].textContent = TIER[p.tier] || p.tier;
    var b = v.querySelectorAll("b");
    b[0].textContent = p.answer; b[1].textContent = p.confidence.toFixed(2);
    var r = v.querySelector(".res");
    r.className = "res " + (p.correct ? "ok" : "no");
    r.textContent = p.correct ? "Correct against the reference." : "Wrong against the reference.";
  }

  fetch("demo-data.json").then(function (r) { return r.json(); }).then(function (data) {
    data.pairs.forEach(function (p, i) {
      var b = document.createElement("button");
      b.className = "tab"; b.setAttribute("role", "tab");
      b.textContent = p.source + " ↔ " + p.target;
      b.title = b.textContent;
      b.onclick = function () { pick(data, i); };
      el("tabs").appendChild(b);
    });
    pick(data, 0);
  });
})();
