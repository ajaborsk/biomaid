(function(win, vue, axios2, primevue2) {
  "use strict";
  var __vite_style__ = document.createElement("style");
  __vite_style__.textContent = `.vue-grid-item{transition:all .2s ease;transition-property:left,top,right}.vue-grid-item.no-touch{-ms-touch-action:none;touch-action:none}.vue-grid-item.cssTransforms{transition-property:transform;left:0;right:auto}.vue-grid-item.cssTransforms.render-rtl{left:auto;right:0}.vue-grid-item.resizing{opacity:.6;z-index:3}.vue-grid-item.vue-draggable-dragging{transition:none;z-index:3}.vue-grid-item.vue-grid-placeholder{background:red;opacity:.2;transition-duration:.1s;z-index:2;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;-o-user-select:none;user-select:none}.vue-grid-item>.vue-resizable-handle{position:absolute;width:20px;height:20px;bottom:0;right:0;background:url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/Pg08IS0tIEdlbmVyYXRvcjogQWRvYmUgRmlyZXdvcmtzIENTNiwgRXhwb3J0IFNWRyBFeHRlbnNpb24gYnkgQWFyb24gQmVhbGwgKGh0dHA6Ly9maXJld29ya3MuYWJlYWxsLmNvbSkgLiBWZXJzaW9uOiAwLjYuMSAgLS0+DTwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+DTxzdmcgaWQ9IlVudGl0bGVkLVBhZ2UlMjAxIiB2aWV3Qm94PSIwIDAgNiA2IiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjojZmZmZmZmMDAiIHZlcnNpb249IjEuMSINCXhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiDQl4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjZweCIgaGVpZ2h0PSI2cHgiDT4NCTxnIG9wYWNpdHk9IjAuMzAyIj4NCQk8cGF0aCBkPSJNIDYgNiBMIDAgNiBMIDAgNC4yIEwgNCA0LjIgTCA0LjIgNC4yIEwgNC4yIDAgTCA2IDAgTCA2IDYgTCA2IDYgWiIgZmlsbD0iIzAwMDAwMCIvPg0JPC9nPg08L3N2Zz4=);background-position:bottom right;padding:0 3px 3px 0;background-repeat:no-repeat;background-origin:content-box;box-sizing:border-box;cursor:se-resize}.vue-grid-item>.vue-rtl-resizable-handle{bottom:0;left:0;background:url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAuMDAwMDAwMDAwMDAwMDAyIiBoZWlnaHQ9IjEwLjAwMDAwMDAwMDAwMDAwMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KIDwhLS0gQ3JlYXRlZCB3aXRoIE1ldGhvZCBEcmF3IC0gaHR0cDovL2dpdGh1Yi5jb20vZHVvcGl4ZWwvTWV0aG9kLURyYXcvIC0tPgogPGc+CiAgPHRpdGxlPmJhY2tncm91bmQ8L3RpdGxlPgogIDxyZWN0IGZpbGw9Im5vbmUiIGlkPSJjYW52YXNfYmFja2dyb3VuZCIgaGVpZ2h0PSIxMiIgd2lkdGg9IjEyIiB5PSItMSIgeD0iLTEiLz4KICA8ZyBkaXNwbGF5PSJub25lIiBvdmVyZmxvdz0idmlzaWJsZSIgeT0iMCIgeD0iMCIgaGVpZ2h0PSIxMDAlIiB3aWR0aD0iMTAwJSIgaWQ9ImNhbnZhc0dyaWQiPgogICA8cmVjdCBmaWxsPSJ1cmwoI2dyaWRwYXR0ZXJuKSIgc3Ryb2tlLXdpZHRoPSIwIiB5PSIwIiB4PSIwIiBoZWlnaHQ9IjEwMCUiIHdpZHRoPSIxMDAlIi8+CiAgPC9nPgogPC9nPgogPGc+CiAgPHRpdGxlPkxheWVyIDE8L3RpdGxlPgogIDxsaW5lIGNhbnZhcz0iI2ZmZmZmZiIgY2FudmFzLW9wYWNpdHk9IjEiIHN0cm9rZS1saW5lY2FwPSJ1bmRlZmluZWQiIHN0cm9rZS1saW5lam9pbj0idW5kZWZpbmVkIiBpZD0ic3ZnXzEiIHkyPSItNzAuMTc4NDA3IiB4Mj0iMTI0LjQ2NDE3NSIgeTE9Ii0zOC4zOTI3MzciIHgxPSIxNDQuODIxMjg5IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSIjMDAwIiBmaWxsPSJub25lIi8+CiAgPGxpbmUgc3Ryb2tlPSIjNjY2NjY2IiBzdHJva2UtbGluZWNhcD0idW5kZWZpbmVkIiBzdHJva2UtbGluZWpvaW49InVuZGVmaW5lZCIgaWQ9InN2Z181IiB5Mj0iOS4xMDY5NTciIHgyPSIwLjk0NzI0NyIgeTE9Ii0wLjAxODEyOCIgeDE9IjAuOTQ3MjQ3IiBzdHJva2Utd2lkdGg9IjIiIGZpbGw9Im5vbmUiLz4KICA8bGluZSBzdHJva2UtbGluZWNhcD0idW5kZWZpbmVkIiBzdHJva2UtbGluZWpvaW49InVuZGVmaW5lZCIgaWQ9InN2Z183IiB5Mj0iOSIgeDI9IjEwLjA3MzUyOSIgeTE9IjkiIHgxPSItMC42NTU2NCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2U9IiM2NjY2NjYiIGZpbGw9Im5vbmUiLz4KIDwvZz4KPC9zdmc+);background-position:bottom left;padding-left:3px;background-repeat:no-repeat;background-origin:content-box;cursor:sw-resize;right:auto}.vue-grid-item.disable-userselect{user-select:none}.vue-grid-layout{position:relative;transition:height .2s ease}

.cockpit-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
}
.cockpit-palette {
  height: 100%;
  width: 240px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  border: #ddd 1px solid;
}
.p-accordion .p-accordion-content {
  display: flex;
  padding: 5px;
  flex-direction: row;
  flex-wrap: wrap;
  align-content: flex-start;
  align-items: flex-start;
  justify-content: flex-start;
}
.p-button {
  margin: 10px;
}
.palette-item {
  margin: 5px;
  width: 80px;
  height: 80px;
  border: solid 1px #ddd;
  background-color: #fafafa;
  padding: 10px;
}
.grid-container {
  width: 100%;
  height: 100%;
  flex: auto;
}
.vue-grid-layout {
  background: none;
}
.vue-grid-item {
  touch-action: none;
  transition: none;
  /* display: grid;* */
  /* grid-template-columns: minmax(0, 1fr) auto;
    grid-template-rows: max-content auto; */
}
.vue-resizable {
  box-sizing: border-box;
}
.vue-grid-item:not(.vue-grid-placeholder):not(.editing) {
  background: #fff;
}

/*
.vue-grid-item.add-border:not(.vue-grid-placeholder) {
  border: 2px solid #eee;
    border-radius: 5px;
}
*/
.vue-grid-item.editing {
  background-color: lightpink;
}
.vue-grid-item.resizing {
  opacity: 0.9;
}
.vue-grid-item.static {
  background: #aaa;
}
.vue-grid-item .frame {
  width: 100%;
  height: 100%;
}

/*
.vue-grid-item .frame.with-title {
}
*/
.vue-grid-item .content {
  width: 100%;
  height: 100%;
}
.vue-grid-item .content.with-title {
  width: 100%;
  height: 100%;
  margin-top: 20px;
}
.vue-grid-item .frame-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;

  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  grid-template-rows: auto minmax(0, 1fr);
}
.vue-grid-item .frame-overlay.without-title {
  pointer-events: none;
}
.vue-grid-item .frame.editable .frame-overlay {
  pointer-events: initial;
}
.vue-grid-item .frame.editable .frame-overlay {
  border: solid #ddd 1px;
  border-radius: 5px;
}
.vue-grid-item .frame.with-title .frame-overlay {
  border: solid #ddd 1px;
  border-radius: 5px;
}
.vue-grid-item .frame-overlay .window {
  grid-column: 1/3;
}
.vue-grid-item .title {
  grid-row: 1;
  grid-column: 1;
  font-size: 16px;
  text-align: center;
  padding: 4px;
  background: #eee;
  opacity: 40%;
}
.vue-grid-item .frame.with-title .title {
  opacity: 100%;
}
.vue-grid-item .remove {
  grid-row: 1;
  grid-column: 2;
  cursor: pointer;
  padding: 2px;
  background: #eee;
  opacity: 50%;
}
.vue-grid-item .frame.with-title .remove {
  opacity: 100%;
}
.vue-grid-item .remove i {
  margin: 4px;
}
.vue-grid-item .content {
  font-size: 16px;
  grid-row: 2;
  grid-column: 1/3;
  overflow: hidden;
}
.vue-grid-item .no-drag {
  height: 100%;
  width: 100%;
}
.vue-grid-item .minMax {
  font-size: 12px;
}
.vue-grid-item .add {
  cursor: pointer;
}
.vue-draggable-handle {
  position: absolute;
  width: 20px;
  height: 20px;
  top: 0;
  left: 0;
  background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><circle cx='5' cy='5' r='5' fill='#999999'/></svg>")
    no-repeat bottom right;
  padding: 0 8px 8px 0;
  background-origin: content-box;
  box-sizing: border-box;
  cursor: pointer;
}
.vue-grid-layout div.grid-menu {
  background: #ddd;
  border: none;
  padding: 10px 2px 2px 2px;
  box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.4);
}
.vue-grid-layout div.grid-menu span {
  font-size: 20px;
  padding: 12px;
  font-weight: bold;
  text-align: center;
}
.vue-grid-layout ul.grid-menu {
  background: #eee;
  border: none;
  padding: 0;
  margin: 10px 0 0 0;
}
.vue-grid-layout li.grid-menu-entry {
  cursor: pointer;
  font-size: 20px;
  padding: 12px;
  list-style: none inside;
  display: block;
}
.vue-grid-layout li.grid-menu-entry:hover {
  background: #fff;
}
`;
  document.head.appendChild(__vite_style__);
  const style = "";
  var ki = Object.defineProperty;
  var Ai = (e, t, n) => t in e ? ki(e, t, { enumerable: true, configurable: true, writable: true, value: n }) : e[t] = n;
  var p = (e, t, n) => (Ai(e, typeof t != "symbol" ? t + "" : t, n), n);
  function ji(e) {
    let t = 0, n;
    for (let i = 0, o = e.length; i < o; i++)
      n = e[i].y + e[i].h, n > t && (t = n);
    return t;
  }
  function Ye(e) {
    const t = Array(e.length);
    for (let n = 0, i = e.length; n < i; n++)
      t[n] = Yi(e[n]);
    return t;
  }
  function Yi(e) {
    return JSON.parse(JSON.stringify(e));
  }
  function qn(e, t) {
    return !(e === t || e.x + e.w <= t.x || e.x >= t.x + t.w || e.y + e.h <= t.y || e.y >= t.y + t.h);
  }
  function qt(e, t, n) {
    const i = Vn(e), o = Kn(e), r = Array(e.length);
    for (let s = 0, a = o.length; s < a; s++) {
      let l = o[s];
      l.static || (l = Xi(i, l, t, n), i.push(l)), r[e.indexOf(l)] = l, l.moved = false;
    }
    return r;
  }
  function Xi(e, t, n, i) {
    if (n)
      for (; t.y > 0 && !ae(e, t); )
        t.y--;
    else if (i) {
      const r = i[t.i].y;
      for (; t.y > r && !ae(e, t); )
        t.y--;
    }
    let o;
    for (; o = ae(e, t); )
      t.y = o.y + o.h;
    return t;
  }
  function Gi(e, t) {
    const n = Vn(e);
    for (let i = 0, o = e.length; i < o; i++) {
      const r = e[i];
      if (r.x + r.w > t.cols && (r.x = t.cols - r.w), r.x < 0 && (r.x = 0, r.w = t.cols), !r.static)
        n.push(r);
      else
        for (; ae(n, r); )
          r.y++;
    }
    return e;
  }
  function gn(e, t) {
    for (let n = 0, i = e.length; n < i; n++)
      if (e[n].i === t)
        return e[n];
  }
  function ae(e, t) {
    for (let n = 0, i = e.length; n < i; n++)
      if (qn(e[n], t))
        return e[n];
  }
  function Un(e, t) {
    return e.filter((n) => qn(n, t));
  }
  function Vn(e) {
    return e.filter((t) => t.static);
  }
  function Xe(e, t, n, i, o, r) {
    if (t.static)
      return e;
    const s = t.x, a = t.y, l = i && t.y > i;
    typeof n == "number" && (t.x = n), typeof i == "number" && (t.y = i), t.moved = true;
    let c = Kn(e);
    l && (c = c.reverse());
    const u = Un(c, t);
    if (r && u.length)
      return t.x = s, t.y = a, t.moved = false, e;
    for (let f = 0, v = u.length; f < v; f++) {
      const y = u[f];
      y.moved || t.y > y.y && t.y - y.y > y.h / 4 || (y.static ? e = vn(e, y, t, o) : e = vn(e, t, y, o));
    }
    return e;
  }
  function vn(e, t, n, i) {
    if (i) {
      const r = {
        x: n.x,
        y: n.y,
        w: n.w,
        h: n.h,
        i: "-1"
      };
      if (r.y = Math.max(t.y - n.h, 0), !ae(e, r))
        return Xe(e, n, void 0, r.y, false);
    }
    return Xe(e, n, void 0, n.y + 1, false);
  }
  function qi(e, t, n, i) {
    const o = "translate3d(" + t + "px," + e + "px, 0)";
    return {
      transform: o,
      WebkitTransform: o,
      MozTransform: o,
      msTransform: o,
      OTransform: o,
      width: n + "px",
      height: i + "px",
      position: "absolute"
    };
  }
  function Ui(e, t, n, i) {
    const o = "translate3d(" + t * -1 + "px," + e + "px, 0)";
    return {
      transform: o,
      WebkitTransform: o,
      MozTransform: o,
      msTransform: o,
      OTransform: o,
      width: n + "px",
      height: i + "px",
      position: "absolute"
    };
  }
  function Vi(e, t, n, i) {
    return {
      top: e + "px",
      left: t + "px",
      width: n + "px",
      height: i + "px",
      position: "absolute"
    };
  }
  function Ki(e, t, n, i) {
    return {
      top: e + "px",
      right: t + "px",
      width: n + "px",
      height: i + "px",
      position: "absolute"
    };
  }
  function Kn(e) {
    return [].concat(e).sort(function(n, i) {
      return n.y === i.y && n.x === i.x ? 0 : n.y > i.y || n.y === i.y && n.x > i.x ? 1 : -1;
    });
  }
  function Ji(e, t) {
    t = t || "Layout";
    const n = ["x", "y", "w", "h"], i = [];
    if (!Array.isArray(e))
      throw new Error(t + " must be an array!");
    for (let o = 0, r = e.length; o < r; o++) {
      const s = e[o];
      for (let a = 0; a < n.length; a++)
        if (typeof s[n[a]] != "number")
          throw new Error(
            "VueGridLayout: " + t + "[" + o + "]." + n[a] + " must be a number!"
          );
      if (s.i === void 0 || s.i === null)
        throw new Error("VueGridLayout: " + t + "[" + o + "].i cannot be null!");
      if (typeof s.i != "number" && typeof s.i != "string")
        throw new Error("VueGridLayout: " + t + "[" + o + "].i must be a string or number!");
      if (i.indexOf(s.i) >= 0)
        throw new Error("VueGridLayout: " + t + "[" + o + "].i must be unique!");
      if (i.push(s.i), s.static !== void 0 && typeof s.static != "boolean")
        throw new Error("VueGridLayout: " + t + "[" + o + "].static must be a boolean!");
    }
  }
  function mn(e) {
    return Zi(e);
  }
  function Zi(e) {
    const t = e.target, n = t.offsetParent || document.body, i = t.offsetParent === document.body ? { left: 0, top: 0 } : n.getBoundingClientRect(), o = e.clientX + n.scrollLeft - i.left, r = e.clientY + n.scrollTop - i.top;
    return { x: o, y: r };
  }
  function yn(e, t, n, i) {
    return Qi(e) ? {
      deltaX: n - e,
      deltaY: i - t,
      lastX: e,
      lastY: t,
      x: n,
      y: i
    } : {
      deltaX: 0,
      deltaY: 0,
      lastX: n,
      lastY: i,
      x: n,
      y: i
    };
  }
  function Qi(e) {
    return typeof e == "number" && !isNaN(e);
  }
  function to(e, t) {
    const n = Jn(e);
    let i = n[0];
    for (let o = 1, r = n.length; o < r; o++) {
      const s = n[o];
      t > e[s] && (i = s);
    }
    return i;
  }
  function Ge(e, t) {
    if (!t[e])
      throw new Error(
        "ResponsiveGridLayout: `cols` entry for breakpoint " + e + " is missing!"
      );
    return t[e];
  }
  function eo(e, t, n, i, o, r, s) {
    if (t[i])
      return Ye(t[i]);
    let a = e;
    const l = Jn(n), c = l.slice(l.indexOf(i));
    for (let u = 0, f = c.length; u < f; u++) {
      const v = c[u];
      if (t[v]) {
        a = t[v];
        break;
      }
    }
    return a = Ye(a || []), qt(Gi(a, { cols: r }), s);
  }
  function Jn(e) {
    return Object.keys(e).sort(function(n, i) {
      return e[n] - e[i];
    });
  }
  let no = "auto";
  function io() {
    return typeof document < "u";
  }
  function Zn() {
    return typeof window < "u";
  }
  function bn() {
    return io() ? typeof document.dir < "u" ? document.dir : document.getElementsByTagName("html")[0].getAttribute("dir") || "auto" : no;
  }
  function oo(e, t) {
    return Zn ? (window.addEventListener(e, t), true) : (t(), false);
  }
  function ro(e, t) {
    !Zn || window.removeEventListener(e, t);
  }
  const gt = {
    init: so,
    document: null,
    DocumentFragment: null,
    SVGElement: null,
    SVGSVGElement: null,
    SVGElementInstance: null,
    Element: null,
    HTMLElement: null,
    Event: null,
    Touch: null,
    PointerEvent: null
  };
  function Gt() {
  }
  const ut = gt;
  function so(e) {
    const t = e;
    gt.document = t.document, gt.DocumentFragment = t.DocumentFragment || Gt, gt.SVGElement = t.SVGElement || Gt, gt.SVGSVGElement = t.SVGSVGElement || Gt, gt.SVGElementInstance = t.SVGElementInstance || Gt, gt.Element = t.Element || Gt, gt.HTMLElement = t.HTMLElement || gt.Element, gt.Event = t.Event, gt.Touch = t.Touch || Gt, gt.PointerEvent = t.PointerEvent || t.MSPointerEvent;
  }
  const Qn = (e) => !!(e && e.Window) && e instanceof e.Window;
  let ti, Ot;
  function ei(e) {
    ti = e;
    const t = e.document.createTextNode("");
    t.ownerDocument !== e.document && typeof e.wrap == "function" && e.wrap(t) === t && (e = e.wrap(e)), Ot = e;
  }
  typeof window < "u" && !!window && ei(window);
  function Ft(e) {
    return Qn(e) ? e : (e.ownerDocument || e).defaultView || Ot.window;
  }
  const ao = (e) => e === Ot || Qn(e), lo = (e) => Ee(e) && e.nodeType === 11, Ee = (e) => !!e && typeof e == "object", ni = (e) => typeof e == "function", co = (e) => typeof e == "number", uo = (e) => typeof e == "boolean", fo = (e) => typeof e == "string", ho = (e) => {
    if (!e || typeof e != "object")
      return false;
    const t = Ft(e) || Ot;
    return /object|function/.test(typeof Element) ? e instanceof Element || e instanceof t.Element : e.nodeType === 1 && typeof e.nodeName == "string";
  }, po = (e) => Ee(e) && !!e.constructor && /function Object\b/.test(e.constructor.toString()), go = (e) => Ee(e) && typeof e.length < "u" && ni(e.splice), g = {
    window: ao,
    docFrag: lo,
    object: Ee,
    func: ni,
    number: co,
    bool: uo,
    string: fo,
    element: ho,
    plainObject: po,
    array: go
  }, vt = {
    init: vo,
    supportsTouch: null,
    supportsPointerEvent: null,
    isIOS7: null,
    isIOS: null,
    isIe9: null,
    isOperaMobile: null,
    prefixedMatchesSelector: null,
    pEventTypes: null,
    wheelEvent: null
  };
  function vo(e) {
    const t = ut.Element, n = e.navigator || {};
    vt.supportsTouch = "ontouchstart" in e || g.func(e.DocumentTouch) && ut.document instanceof e.DocumentTouch, vt.supportsPointerEvent = n.pointerEnabled !== false && !!ut.PointerEvent, vt.isIOS = /iP(hone|od|ad)/.test(n.platform), vt.isIOS7 = /iP(hone|od|ad)/.test(n.platform) && /OS 7[^\d]/.test(n.appVersion), vt.isIe9 = /MSIE 9/.test(n.userAgent), vt.isOperaMobile = n.appName === "Opera" && vt.supportsTouch && /Presto/.test(n.userAgent), vt.prefixedMatchesSelector = "matches" in t.prototype ? "matches" : "webkitMatchesSelector" in t.prototype ? "webkitMatchesSelector" : "mozMatchesSelector" in t.prototype ? "mozMatchesSelector" : "oMatchesSelector" in t.prototype ? "oMatchesSelector" : "msMatchesSelector", vt.pEventTypes = vt.supportsPointerEvent ? ut.PointerEvent === e.MSPointerEvent ? {
      up: "MSPointerUp",
      down: "MSPointerDown",
      over: "mouseover",
      out: "mouseout",
      move: "MSPointerMove",
      cancel: "MSPointerCancel"
    } : {
      up: "pointerup",
      down: "pointerdown",
      over: "pointerover",
      out: "pointerout",
      move: "pointermove",
      cancel: "pointercancel"
    } : null, vt.wheelEvent = ut.document && "onmousewheel" in ut.document ? "mousewheel" : "wheel";
  }
  const mt = vt, mo = (e, t) => e.indexOf(t) !== -1, ii = (e, t) => {
    for (const n of t)
      e.push(n);
    return e;
  }, oi = (e) => ii([], e), Ie = (e, t) => {
    for (let n = 0; n < e.length; n++)
      if (t(e[n], n, e))
        return n;
    return -1;
  }, qe = (e, t) => e[Ie(e, t)];
  function Jt(e) {
    const t = {};
    for (const n in e) {
      const i = e[n];
      g.plainObject(i) ? t[n] = Jt(i) : g.array(i) ? t[n] = oi(i) : t[n] = i;
    }
    return t;
  }
  function D(e, t) {
    for (const i in t)
      e[i] = t[i];
    return e;
  }
  let xn = 0, Tt, Wt;
  function yo(e) {
    if (Tt = e.requestAnimationFrame, Wt = e.cancelAnimationFrame, !Tt) {
      const t = ["ms", "moz", "webkit", "o"];
      for (const n of t)
        Tt = e[`${n}RequestAnimationFrame`], Wt = e[`${n}CancelAnimationFrame`] || e[`${n}CancelRequestAnimationFrame`];
    }
    Tt = Tt && Tt.bind(e), Wt = Wt && Wt.bind(e), Tt || (Tt = (t) => {
      const n = Date.now(), i = Math.max(0, 16 - (n - xn)), o = e.setTimeout(() => {
        t(n + i);
      }, i);
      return xn = n + i, o;
    }, Wt = (t) => clearTimeout(t));
  }
  const Ut = {
    request: (e) => Tt(e),
    cancel: (e) => Wt(e),
    init: yo
  };
  function Vt(e, t, n) {
    if (n = n || {}, g.string(e) && e.search(" ") !== -1 && (e = wn(e)), g.array(e))
      return e.reduce((i, o) => D(i, Vt(o, t, n)), n);
    if (g.object(e) && (t = e, e = ""), g.func(t))
      n[e] = n[e] || [], n[e].push(t);
    else if (g.array(t))
      for (const i of t)
        Vt(e, i, n);
    else if (g.object(t))
      for (const i in t) {
        const o = wn(i).map((r) => `${e}${r}`);
        Vt(o, t[i], n);
      }
    return n;
  }
  function wn(e) {
    return e.trim().split(/ +/);
  }
  function Sn(e, t) {
    for (const n of t) {
      if (e.immediatePropagationStopped)
        break;
      n(e);
    }
  }
  class ri {
    constructor(t) {
      p(this, "options");
      p(this, "types", {});
      p(this, "propagationStopped", false);
      p(this, "immediatePropagationStopped", false);
      p(this, "global");
      this.options = D({}, t || {});
    }
    fire(t) {
      let n;
      const i = this.global;
      (n = this.types[t.type]) && Sn(t, n), !t.propagationStopped && i && (n = i[t.type]) && Sn(t, n);
    }
    on(t, n) {
      const i = Vt(t, n);
      for (t in i)
        this.types[t] = ii(this.types[t] || [], i[t]);
    }
    off(t, n) {
      const i = Vt(t, n);
      for (t in i) {
        const o = this.types[t];
        if (!(!o || !o.length))
          for (const r of i[t]) {
            const s = o.indexOf(r);
            s !== -1 && o.splice(s, 1);
          }
      }
    }
    getRect(t) {
      return null;
    }
  }
  function Lt(e, t) {
    if (e.contains)
      return e.contains(t);
    for (; t; ) {
      if (t === e)
        return true;
      t = t.parentNode;
    }
    return false;
  }
  function si(e, t) {
    for (; g.element(e); ) {
      if (Nt(e, t))
        return e;
      e = Rt(e);
    }
    return null;
  }
  function Rt(e) {
    let t = e.parentNode;
    if (g.docFrag(t)) {
      for (; (t = t.host) && g.docFrag(t); )
        ;
      return t;
    }
    return t;
  }
  function Nt(e, t) {
    return Ot !== ti && (t = t.replace(/\/deep\//g, " ")), e[mt.prefixedMatchesSelector](t);
  }
  function Ue(e, t, n) {
    for (; g.element(e); ) {
      if (Nt(e, t))
        return true;
      if (e = Rt(e), e === n)
        return Nt(e, t);
    }
    return false;
  }
  function En(e) {
    return e.correspondingUseElement || e;
  }
  function bo(e) {
    return e = e || Ot, {
      x: e.scrollX || e.document.documentElement.scrollLeft,
      y: e.scrollY || e.document.documentElement.scrollTop
    };
  }
  function en(e) {
    const t = e instanceof ut.SVGElement ? e.getBoundingClientRect() : e.getClientRects()[0];
    return t && {
      left: t.left,
      right: t.right,
      top: t.top,
      bottom: t.bottom,
      width: t.width || t.right - t.left,
      height: t.height || t.bottom - t.top
    };
  }
  function nn(e) {
    const t = en(e);
    if (!mt.isIOS7 && t) {
      const n = bo(Ft(e));
      t.left += n.x, t.right += n.x, t.top += n.y, t.bottom += n.y;
    }
    return t;
  }
  function In(e) {
    return g.string(e) ? (ut.document.querySelector(e), true) : false;
  }
  function ai(e, t, n) {
    return e === "parent" ? Rt(n) : e === "self" ? t.getRect(n) : si(n, e);
  }
  function ce(e, t, n, i) {
    let o = e;
    return g.string(o) ? o = ai(o, t, n) : g.func(o) && (o = o(...i)), g.element(o) && (o = nn(o)), o;
  }
  function ze(e) {
    return e && {
      x: "x" in e ? e.x : e.left,
      y: "y" in e ? e.y : e.top
    };
  }
  function xo(e) {
    return e && !("left" in e && "top" in e) && (e = D({}, e), e.left = e.x || 0, e.top = e.y || 0, e.right = e.right || e.left + e.width, e.bottom = e.bottom || e.top + e.height), e;
  }
  function zn(e) {
    return e && !("x" in e && "y" in e) && (e = D({}, e), e.x = e.left || 0, e.y = e.top || 0, e.width = e.width || (e.right || 0) - e.x, e.height = e.height || (e.bottom || 0) - e.y), e;
  }
  function on(e, t, n) {
    e.left && (t.left += n.x), e.right && (t.right += n.x), e.top && (t.top += n.y), e.bottom && (t.bottom += n.y), t.width = t.right - t.left, t.height = t.bottom - t.top;
  }
  function rn(e, t, n) {
    const i = e.options[n], r = i && i.origin || e.options.origin, s = ce(r, e, t, [e && t]);
    return ze(s) || {
      x: 0,
      y: 0
    };
  }
  const Te = (e, t) => Math.sqrt(e * e + t * t);
  class li {
    constructor(t) {
      p(this, "immediatePropagationStopped", false);
      p(this, "propagationStopped", false);
      this._interaction = t;
    }
    preventDefault() {
    }
    stopPropagation() {
      this.propagationStopped = true;
    }
    stopImmediatePropagation() {
      this.immediatePropagationStopped = this.propagationStopped = true;
    }
  }
  Object.defineProperty(li.prototype, "interaction", {
    get() {
      return this._interaction._proxy;
    },
    set() {
    }
  });
  const ci = {
    base: {
      preventDefault: "auto",
      deltaSource: "page"
    },
    perAction: {
      enabled: false,
      origin: {
        x: 0,
        y: 0
      }
    },
    actions: {}
  };
  class sn extends li {
    constructor(n, i, o, r, s, a, l) {
      super(n);
      p(this, "relatedTarget", null);
      p(this, "screenX");
      p(this, "screenY");
      p(this, "button");
      p(this, "buttons");
      p(this, "ctrlKey");
      p(this, "shiftKey");
      p(this, "altKey");
      p(this, "metaKey");
      p(this, "page");
      p(this, "client");
      p(this, "delta");
      p(this, "rect");
      p(this, "x0");
      p(this, "y0");
      p(this, "t0");
      p(this, "dt");
      p(this, "duration");
      p(this, "clientX0");
      p(this, "clientY0");
      p(this, "velocity");
      p(this, "speed");
      p(this, "swipe");
      p(this, "axes");
      p(this, "preEnd");
      s = s || n.element;
      const c = n.interactable, u = (c && c.options || ci).deltaSource, f = rn(c, s, o), v = r === "start", y = r === "end", x = v ? this : n.prevEvent, S = v ? n.coords.start : y ? {
        page: x.page,
        client: x.client,
        timeStamp: n.coords.cur.timeStamp
      } : n.coords.cur;
      this.page = D({}, S.page), this.client = D({}, S.client), this.rect = D({}, n.rect), this.timeStamp = S.timeStamp, y || (this.page.x -= f.x, this.page.y -= f.y, this.client.x -= f.x, this.client.y -= f.y), this.ctrlKey = i.ctrlKey, this.altKey = i.altKey, this.shiftKey = i.shiftKey, this.metaKey = i.metaKey, this.button = i.button, this.buttons = i.buttons, this.target = s, this.currentTarget = s, this.preEnd = a, this.type = l || o + (r || ""), this.interactable = c, this.t0 = v ? n.pointers[n.pointers.length - 1].downTime : x.t0, this.x0 = n.coords.start.page.x - f.x, this.y0 = n.coords.start.page.y - f.y, this.clientX0 = n.coords.start.client.x - f.x, this.clientY0 = n.coords.start.client.y - f.y, v || y ? this.delta = {
        x: 0,
        y: 0
      } : this.delta = {
        x: this[u].x - x[u].x,
        y: this[u].y - x[u].y
      }, this.dt = n.coords.delta.timeStamp, this.duration = this.timeStamp - this.t0, this.velocity = D({}, n.coords.velocity[u]), this.speed = Te(this.velocity.x, this.velocity.y), this.swipe = y || r === "inertiastart" ? this.getSwipe() : null;
    }
    getSwipe() {
      const n = this._interaction;
      if (n.prevEvent.speed < 600 || this.timeStamp - n.prevEvent.timeStamp > 150)
        return null;
      let i = 180 * Math.atan2(n.prevEvent.velocityY, n.prevEvent.velocityX) / Math.PI;
      const o = 22.5;
      i < 0 && (i += 360);
      const r = 135 - o <= i && i < 225 + o, s = 225 - o <= i && i < 315 + o, a = !r && (315 - o <= i || i < 45 + o), l = !s && 45 - o <= i && i < 135 + o;
      return {
        up: s,
        down: l,
        left: r,
        right: a,
        angle: i,
        speed: n.prevEvent.speed,
        velocity: {
          x: n.prevEvent.velocityX,
          y: n.prevEvent.velocityY
        }
      };
    }
    preventDefault() {
    }
    stopImmediatePropagation() {
      this.immediatePropagationStopped = this.propagationStopped = true;
    }
    stopPropagation() {
      this.propagationStopped = true;
    }
  }
  Object.defineProperties(sn.prototype, {
    pageX: {
      get() {
        return this.page.x;
      },
      set(e) {
        this.page.x = e;
      }
    },
    pageY: {
      get() {
        return this.page.y;
      },
      set(e) {
        this.page.y = e;
      }
    },
    clientX: {
      get() {
        return this.client.x;
      },
      set(e) {
        this.client.x = e;
      }
    },
    clientY: {
      get() {
        return this.client.y;
      },
      set(e) {
        this.client.y = e;
      }
    },
    dx: {
      get() {
        return this.delta.x;
      },
      set(e) {
        this.delta.x = e;
      }
    },
    dy: {
      get() {
        return this.delta.y;
      },
      set(e) {
        this.delta.y = e;
      }
    },
    velocityX: {
      get() {
        return this.velocity.x;
      },
      set(e) {
        this.velocity.x = e;
      }
    },
    velocityY: {
      get() {
        return this.velocity.y;
      },
      set(e) {
        this.velocity.y = e;
      }
    }
  });
  function ue(e, t) {
    let n = false;
    return function() {
      return n || (Ot.console.warn(t), n = true), e.apply(this, arguments);
    };
  }
  function ui(e, t) {
    return e.name = t.name, e.axis = t.axis, e.edges = t.edges, e;
  }
  function fi(e, t) {
    e.__set || (e.__set = {});
    for (const n in t)
      typeof e[n] != "function" && n !== "__set" && Object.defineProperty(e, n, {
        get() {
          return n in e.__set ? e.__set[n] : e.__set[n] = t[n];
        },
        set(i) {
          e.__set[n] = i;
        },
        configurable: true
      });
    return e;
  }
  function Re(e, t) {
    e.page = e.page || {}, e.page.x = t.page.x, e.page.y = t.page.y, e.client = e.client || {}, e.client.x = t.client.x, e.client.y = t.client.y, e.timeStamp = t.timeStamp;
  }
  function wo(e, t, n) {
    e.page.x = n.page.x - t.page.x, e.page.y = n.page.y - t.page.y, e.client.x = n.client.x - t.client.x, e.client.y = n.client.y - t.client.y, e.timeStamp = n.timeStamp - t.timeStamp;
  }
  function So(e, t) {
    const n = Math.max(t.timeStamp / 1e3, 1e-3);
    e.page.x = t.page.x / n, e.page.y = t.page.y / n, e.client.x = t.client.x / n, e.client.y = t.client.y / n, e.timeStamp = n;
  }
  function Eo(e) {
    e.page.x = 0, e.page.y = 0, e.client.x = 0, e.client.y = 0;
  }
  function di(e) {
    return e instanceof ut.Event || e instanceof ut.Touch;
  }
  function be(e, t, n) {
    return n = n || {}, e = e || "page", n.x = t[e + "X"], n.y = t[e + "Y"], n;
  }
  function Io(e, t) {
    return t = t || {
      x: 0,
      y: 0
    }, mt.isOperaMobile && di(e) ? (be("screen", e, t), t.x += window.scrollX, t.y += window.scrollY) : be("page", e, t), t;
  }
  function zo(e, t) {
    return t = t || {}, mt.isOperaMobile && di(e) ? be("screen", e, t) : be("client", e, t), t;
  }
  function xe(e) {
    return g.number(e.pointerId) ? e.pointerId : e.identifier;
  }
  function To(e, t, n) {
    const i = t.length > 1 ? hi(t) : t[0];
    Io(i, e.page), zo(i, e.client), e.timeStamp = n;
  }
  function an(e) {
    const t = [];
    return g.array(e) ? (t[0] = e[0], t[1] = e[1]) : e.type === "touchend" ? e.touches.length === 1 ? (t[0] = e.touches[0], t[1] = e.changedTouches[0]) : e.touches.length === 0 && (t[0] = e.changedTouches[0], t[1] = e.changedTouches[1]) : (t[0] = e.touches[0], t[1] = e.touches[1]), t;
  }
  function hi(e) {
    const t = {
      pageX: 0,
      pageY: 0,
      clientX: 0,
      clientY: 0,
      screenX: 0,
      screenY: 0
    };
    for (const n of e)
      for (const i in t)
        t[i] += n[i];
    for (const n in t)
      t[n] /= e.length;
    return t;
  }
  function Mo(e) {
    if (!e.length)
      return null;
    const t = an(e), n = Math.min(t[0].pageX, t[1].pageX), i = Math.min(t[0].pageY, t[1].pageY), o = Math.max(t[0].pageX, t[1].pageX), r = Math.max(t[0].pageY, t[1].pageY);
    return {
      x: n,
      y: i,
      left: n,
      top: i,
      right: o,
      bottom: r,
      width: o - n,
      height: r - i
    };
  }
  function _o(e, t) {
    const n = t + "X", i = t + "Y", o = an(e), r = o[0][n] - o[1][n], s = o[0][i] - o[1][i];
    return Te(r, s);
  }
  function Co(e, t) {
    const n = t + "X", i = t + "Y", o = an(e), r = o[1][n] - o[0][n], s = o[1][i] - o[0][i];
    return 180 * Math.atan2(s, r) / Math.PI;
  }
  function Do(e) {
    return g.string(e.pointerType) ? e.pointerType : g.number(e.pointerType) ? [void 0, void 0, "touch", "pen", "mouse"][e.pointerType] : /touch/.test(e.type || "") || e instanceof ut.Touch ? "touch" : "mouse";
  }
  function pi(e) {
    const t = g.func(e.composedPath) ? e.composedPath() : e.path;
    return [En(t ? t[0] : e.target), En(e.currentTarget)];
  }
  function ie() {
    return {
      page: {
        x: 0,
        y: 0
      },
      client: {
        x: 0,
        y: 0
      },
      timeStamp: 0
    };
  }
  function Ve(e, t) {
    if (t.phaselessTypes[e])
      return true;
    for (const n in t.map)
      if (e.indexOf(n) === 0 && e.substr(n.length) in t.phases)
        return true;
    return false;
  }
  function Po(e) {
    const t = (n, i) => {
      let o = e.interactables.get(n, i);
      return o || (o = e.interactables.new(n, i), o.events.global = t.globalEvents), o;
    };
    return t.getPointerAverage = hi, t.getTouchBBox = Mo, t.getTouchDistance = _o, t.getTouchAngle = Co, t.getElementRect = nn, t.getElementClientRect = en, t.matchesSelector = Nt, t.closest = si, t.globalEvents = {}, t.version = "1.10.17", t.scope = e, t.use = function(n, i) {
      return this.scope.usePlugin(n, i), this;
    }, t.isSet = function(n, i) {
      return !!this.scope.interactables.get(n, i && i.context);
    }, t.on = ue(function(i, o, r) {
      if (g.string(i) && i.search(" ") !== -1 && (i = i.trim().split(/ +/)), g.array(i)) {
        for (const s of i)
          this.on(s, o, r);
        return this;
      }
      if (g.object(i)) {
        for (const s in i)
          this.on(s, i[s], o);
        return this;
      }
      return Ve(i, this.scope.actions) ? this.globalEvents[i] ? this.globalEvents[i].push(o) : this.globalEvents[i] = [o] : this.scope.events.add(this.scope.document, i, o, {
        options: r
      }), this;
    }, "The interact.on() method is being deprecated"), t.off = ue(function(i, o, r) {
      if (g.string(i) && i.search(" ") !== -1 && (i = i.trim().split(/ +/)), g.array(i)) {
        for (const s of i)
          this.off(s, o, r);
        return this;
      }
      if (g.object(i)) {
        for (const s in i)
          this.off(s, i[s], o);
        return this;
      }
      if (Ve(i, this.scope.actions)) {
        let s;
        i in this.globalEvents && (s = this.globalEvents[i].indexOf(o)) !== -1 && this.globalEvents[i].splice(s, 1);
      } else
        this.scope.events.remove(this.scope.document, i, o, r);
      return this;
    }, "The interact.off() method is being deprecated"), t.debug = function() {
      return this.scope;
    }, t.supportsTouch = function() {
      return mt.supportsTouch;
    }, t.supportsPointerEvent = function() {
      return mt.supportsPointerEvent;
    }, t.stop = function() {
      for (const n of this.scope.interactions.list)
        n.stop();
      return this;
    }, t.pointerMoveTolerance = function(n) {
      return g.number(n) ? (this.scope.interactions.pointerMoveTolerance = n, this) : this.scope.interactions.pointerMoveTolerance;
    }, t.addDocument = function(n, i) {
      this.scope.addDocument(n, i);
    }, t.removeDocument = function(n) {
      this.scope.removeDocument(n);
    }, t;
  }
  class ko {
    constructor(t, n, i, o) {
      p(this, "options");
      p(this, "_actions");
      p(this, "target");
      p(this, "events", new ri());
      p(this, "_context");
      p(this, "_win");
      p(this, "_doc");
      p(this, "_scopeEvents");
      p(this, "_rectChecker");
      this._actions = n.actions, this.target = t, this._context = n.context || i, this._win = Ft(In(t) ? this._context : t), this._doc = this._win.document, this._scopeEvents = o, this.set(n);
    }
    get _defaults() {
      return {
        base: {},
        perAction: {},
        actions: {}
      };
    }
    setOnEvents(t, n) {
      return g.func(n.onstart) && this.on(`${t}start`, n.onstart), g.func(n.onmove) && this.on(`${t}move`, n.onmove), g.func(n.onend) && this.on(`${t}end`, n.onend), g.func(n.oninertiastart) && this.on(`${t}inertiastart`, n.oninertiastart), this;
    }
    updatePerActionListeners(t, n, i) {
      (g.array(n) || g.object(n)) && this.off(t, n), (g.array(i) || g.object(i)) && this.on(t, i);
    }
    setPerAction(t, n) {
      const i = this._defaults;
      for (const o in n) {
        const r = o, s = this.options[t], a = n[r];
        r === "listeners" && this.updatePerActionListeners(t, s.listeners, a), g.array(a) ? s[r] = oi(a) : g.plainObject(a) ? (s[r] = D(s[r] || {}, Jt(a)), g.object(i.perAction[r]) && "enabled" in i.perAction[r] && (s[r].enabled = a.enabled !== false)) : g.bool(a) && g.object(i.perAction[r]) ? s[r].enabled = a : s[r] = a;
      }
    }
    getRect(t) {
      return t = t || (g.element(this.target) ? this.target : null), g.string(this.target) && (t = t || this._context.querySelector(this.target)), nn(t);
    }
    rectChecker(t) {
      return g.func(t) ? (this._rectChecker = t, this.getRect = (n) => {
        const i = D({}, this._rectChecker(n));
        return "width" in i || (i.width = i.right - i.left, i.height = i.bottom - i.top), i;
      }, this) : t === null ? (delete this.getRect, delete this._rectChecker, this) : this.getRect;
    }
    _backCompatOption(t, n) {
      if (In(n) || g.object(n)) {
        this.options[t] = n;
        for (const i in this._actions.map)
          this.options[i][t] = n;
        return this;
      }
      return this.options[t];
    }
    origin(t) {
      return this._backCompatOption("origin", t);
    }
    deltaSource(t) {
      return t === "page" || t === "client" ? (this.options.deltaSource = t, this) : this.options.deltaSource;
    }
    context() {
      return this._context;
    }
    inContext(t) {
      return this._context === t.ownerDocument || Lt(this._context, t);
    }
    testIgnoreAllow(t, n, i) {
      return !this.testIgnore(t.ignoreFrom, n, i) && this.testAllow(t.allowFrom, n, i);
    }
    testAllow(t, n, i) {
      return t ? g.element(i) ? g.string(t) ? Ue(i, t, n) : g.element(t) ? Lt(t, i) : false : false : true;
    }
    testIgnore(t, n, i) {
      return !t || !g.element(i) ? false : g.string(t) ? Ue(i, t, n) : g.element(t) ? Lt(t, i) : false;
    }
    fire(t) {
      return this.events.fire(t), this;
    }
    _onOff(t, n, i, o) {
      g.object(n) && !g.array(n) && (o = i, i = null);
      const r = t === "on" ? "add" : "remove", s = Vt(n, i);
      for (let a in s) {
        a === "wheel" && (a = mt.wheelEvent);
        for (const l of s[a])
          Ve(a, this._actions) ? this.events[t](a, l) : g.string(this.target) ? this._scopeEvents[`${r}Delegate`](this.target, this._context, a, l, o) : this._scopeEvents[r](this.target, a, l, o);
      }
      return this;
    }
    on(t, n, i) {
      return this._onOff("on", t, n, i);
    }
    off(t, n, i) {
      return this._onOff("off", t, n, i);
    }
    set(t) {
      const n = this._defaults;
      g.object(t) || (t = {}), this.options = Jt(n.base);
      for (const i in this._actions.methodDict) {
        const o = i, r = this._actions.methodDict[o];
        this.options[o] = {}, this.setPerAction(o, D(D({}, n.perAction), n.actions[o])), this[r](t[o]);
      }
      for (const i in t)
        g.func(this[i]) && this[i](t[i]);
      return this;
    }
    unset() {
      if (g.string(this.target))
        for (const t in this._scopeEvents.delegatedEvents) {
          const n = this._scopeEvents.delegatedEvents[t];
          for (let i = n.length - 1; i >= 0; i--) {
            const {
              selector: o,
              context: r,
              listeners: s
            } = n[i];
            o === this.target && r === this._context && n.splice(i, 1);
            for (let a = s.length - 1; a >= 0; a--)
              this._scopeEvents.removeDelegate(this.target, this._context, t, s[a][0], s[a][1]);
          }
        }
      else
        this._scopeEvents.remove(this.target, "all");
    }
  }
  class Ao {
    constructor(t) {
      p(this, "list", []);
      p(this, "selectorMap", {});
      p(this, "scope");
      this.scope = t, t.addListeners({
        "interactable:unset": ({
          interactable: n
        }) => {
          const {
            target: i,
            _context: o
          } = n, r = g.string(i) ? this.selectorMap[i] : i[this.scope.id], s = Ie(r, (a) => a.context === o);
          r[s] && (r[s].context = null, r[s].interactable = null), r.splice(s, 1);
        }
      });
    }
    new(t, n) {
      n = D(n || {}, {
        actions: this.scope.actions
      });
      const i = new this.scope.Interactable(t, n, this.scope.document, this.scope.events), o = {
        context: i._context,
        interactable: i
      };
      return this.scope.addDocument(i._doc), this.list.push(i), g.string(t) ? (this.selectorMap[t] || (this.selectorMap[t] = []), this.selectorMap[t].push(o)) : (i.target[this.scope.id] || Object.defineProperty(t, this.scope.id, {
        value: [],
        configurable: true
      }), t[this.scope.id].push(o)), this.scope.fire("interactable:new", {
        target: t,
        options: n,
        interactable: i,
        win: this.scope._win
      }), i;
    }
    get(t, n) {
      const i = n && n.context || this.scope.document, o = g.string(t), r = o ? this.selectorMap[t] : t[this.scope.id];
      if (!r)
        return null;
      const s = qe(r, (a) => a.context === i && (o || a.interactable.inContext(t)));
      return s && s.interactable;
    }
    forEachMatch(t, n) {
      for (const i of this.list) {
        let o;
        if ((g.string(i.target) ? g.element(t) && Nt(t, i.target) : t === i.target) && i.inContext(t) && (o = n(i)), o !== void 0)
          return o;
      }
    }
  }
  function Oo(e) {
    var t;
    const n = [], i = {}, o = [], r = {
      add: s,
      remove: a,
      addDelegate: l,
      removeDelegate: c,
      delegateListener: u,
      delegateUseCapture: f,
      delegatedEvents: i,
      documents: o,
      targets: n,
      supportsOptions: false,
      supportsPassive: false
    };
    (t = e.document) == null || t.createElement("div").addEventListener("test", null, {
      get capture() {
        return r.supportsOptions = true;
      },
      get passive() {
        return r.supportsPassive = true;
      }
    }), e.events = r;
    function s(v, y, x, S) {
      const z = oe(S);
      let H = qe(n, (T) => T.eventTarget === v);
      H || (H = {
        eventTarget: v,
        events: {}
      }, n.push(H)), H.events[y] || (H.events[y] = []), v.addEventListener && !mo(H.events[y], x) && (v.addEventListener(y, x, r.supportsOptions ? z : z.capture), H.events[y].push(x));
    }
    function a(v, y, x, S) {
      const z = oe(S), H = Ie(n, (d) => d.eventTarget === v), T = n[H];
      if (!T || !T.events)
        return;
      if (y === "all") {
        for (y in T.events)
          T.events.hasOwnProperty(y) && a(v, y, "all");
        return;
      }
      let _ = false;
      const m = T.events[y];
      if (m) {
        if (x === "all") {
          for (let d = m.length - 1; d >= 0; d--)
            a(v, y, m[d], z);
          return;
        } else
          for (let d = 0; d < m.length; d++)
            if (m[d] === x) {
              v.removeEventListener(y, x, r.supportsOptions ? z : z.capture), m.splice(d, 1), m.length === 0 && (delete T.events[y], _ = true);
              break;
            }
      }
      _ && !Object.keys(T.events).length && n.splice(H, 1);
    }
    function l(v, y, x, S, z) {
      const H = oe(z);
      if (!i[x]) {
        i[x] = [];
        for (const m of o)
          s(m, x, u), s(m, x, f, true);
      }
      const T = i[x];
      let _ = qe(T, (m) => m.selector === v && m.context === y);
      _ || (_ = {
        selector: v,
        context: y,
        listeners: []
      }, T.push(_)), _.listeners.push([S, H]);
    }
    function c(v, y, x, S, z) {
      const H = oe(z), T = i[x];
      let _ = false, m;
      if (!!T)
        for (m = T.length - 1; m >= 0; m--) {
          const d = T[m];
          if (d.selector === v && d.context === y) {
            const {
              listeners: R
            } = d;
            for (let w = R.length - 1; w >= 0; w--) {
              const [N, {
                capture: K,
                passive: A
              }] = R[w];
              if (N === S && K === H.capture && A === H.passive) {
                R.splice(w, 1), R.length || (T.splice(m, 1), a(y, x, u), a(y, x, f, true)), _ = true;
                break;
              }
            }
            if (_)
              break;
          }
        }
    }
    function u(v, y) {
      const x = oe(y), S = new Ro(v), z = i[v.type], [H] = pi(v);
      let T = H;
      for (; g.element(T); ) {
        for (let _ = 0; _ < z.length; _++) {
          const m = z[_], {
            selector: d,
            context: R
          } = m;
          if (Nt(T, d) && Lt(R, H) && Lt(R, T)) {
            const {
              listeners: w
            } = m;
            S.currentTarget = T;
            for (const [N, {
              capture: K,
              passive: A
            }] of w)
              K === x.capture && A === x.passive && N(S);
          }
        }
        T = Rt(T);
      }
    }
    function f(v) {
      return u.call(this, v, true);
    }
    return r;
  }
  class Ro {
    constructor(t) {
      p(this, "currentTarget");
      p(this, "originalEvent");
      p(this, "type");
      this.originalEvent = t, fi(this, t);
    }
    preventOriginalDefault() {
      this.originalEvent.preventDefault();
    }
    stopPropagation() {
      this.originalEvent.stopPropagation();
    }
    stopImmediatePropagation() {
      this.originalEvent.stopImmediatePropagation();
    }
  }
  function oe(e) {
    if (!g.object(e))
      return {
        capture: !!e,
        passive: false
      };
    const t = D({}, e);
    return t.capture = !!e.capture, t.passive = !!e.passive, t;
  }
  const Ho = {
    id: "events",
    install: Oo
  };
  class $o {
    constructor(t, n, i, o, r) {
      p(this, "id");
      p(this, "pointer");
      p(this, "event");
      p(this, "downTime");
      p(this, "downTarget");
      this.id = t, this.pointer = n, this.event = i, this.downTime = o, this.downTarget = r;
    }
  }
  let Ke;
  (function(e) {
    e.interactable = "", e.element = "", e.prepared = "", e.pointerIsDown = "", e.pointerWasMoved = "", e._proxy = "";
  })(Ke || (Ke = {}));
  let Je;
  (function(e) {
    e.start = "", e.move = "", e.end = "", e.stop = "", e.interacting = "";
  })(Je || (Je = {}));
  let Bo = 0;
  class Wo {
    constructor({
      pointerType: t,
      scopeFire: n
    }) {
      p(this, "interactable", null);
      p(this, "element", null);
      p(this, "rect", null);
      p(this, "_rects");
      p(this, "edges", null);
      p(this, "_scopeFire");
      p(this, "prepared", {
        name: null,
        axis: null,
        edges: null
      });
      p(this, "pointerType");
      p(this, "pointers", []);
      p(this, "downEvent", null);
      p(this, "downPointer", {});
      p(this, "_latestPointer", {
        pointer: null,
        event: null,
        eventTarget: null
      });
      p(this, "prevEvent", null);
      p(this, "pointerIsDown", false);
      p(this, "pointerWasMoved", false);
      p(this, "_interacting", false);
      p(this, "_ending", false);
      p(this, "_stopped", true);
      p(this, "_proxy", null);
      p(this, "simulation", null);
      p(this, "doMove", ue(function(t2) {
        this.move(t2);
      }, "The interaction.doMove() method has been renamed to interaction.move()"));
      p(this, "coords", {
        start: ie(),
        prev: ie(),
        cur: ie(),
        delta: ie(),
        velocity: ie()
      });
      p(this, "_id", Bo++);
      this._scopeFire = n, this.pointerType = t;
      const i = this;
      this._proxy = {};
      for (const o in Ke)
        Object.defineProperty(this._proxy, o, {
          get() {
            return i[o];
          }
        });
      for (const o in Je)
        Object.defineProperty(this._proxy, o, {
          value: (...r) => i[o](...r)
        });
      this._scopeFire("interactions:new", {
        interaction: this
      });
    }
    get pointerMoveTolerance() {
      return 1;
    }
    pointerDown(t, n, i) {
      const o = this.updatePointer(t, n, i, true), r = this.pointers[o];
      this._scopeFire("interactions:down", {
        pointer: t,
        event: n,
        eventTarget: i,
        pointerIndex: o,
        pointerInfo: r,
        type: "down",
        interaction: this
      });
    }
    start(t, n, i) {
      return this.interacting() || !this.pointerIsDown || this.pointers.length < (t.name === "gesture" ? 2 : 1) || !n.options[t.name].enabled ? false : (ui(this.prepared, t), this.interactable = n, this.element = i, this.rect = n.getRect(i), this.edges = this.prepared.edges ? D({}, this.prepared.edges) : {
        left: true,
        right: true,
        top: true,
        bottom: true
      }, this._stopped = false, this._interacting = this._doPhase({
        interaction: this,
        event: this.downEvent,
        phase: "start"
      }) && !this._stopped, this._interacting);
    }
    pointerMove(t, n, i) {
      !this.simulation && !(this.modification && this.modification.endResult) && this.updatePointer(t, n, i, false);
      const o = this.coords.cur.page.x === this.coords.prev.page.x && this.coords.cur.page.y === this.coords.prev.page.y && this.coords.cur.client.x === this.coords.prev.client.x && this.coords.cur.client.y === this.coords.prev.client.y;
      let r, s;
      this.pointerIsDown && !this.pointerWasMoved && (r = this.coords.cur.client.x - this.coords.start.client.x, s = this.coords.cur.client.y - this.coords.start.client.y, this.pointerWasMoved = Te(r, s) > this.pointerMoveTolerance);
      const a = this.getPointerIndex(t), l = {
        pointer: t,
        pointerIndex: a,
        pointerInfo: this.pointers[a],
        event: n,
        type: "move",
        eventTarget: i,
        dx: r,
        dy: s,
        duplicate: o,
        interaction: this
      };
      o || So(this.coords.velocity, this.coords.delta), this._scopeFire("interactions:move", l), !o && !this.simulation && (this.interacting() && (l.type = null, this.move(l)), this.pointerWasMoved && Re(this.coords.prev, this.coords.cur));
    }
    move(t) {
      (!t || !t.event) && Eo(this.coords.delta), t = D({
        pointer: this._latestPointer.pointer,
        event: this._latestPointer.event,
        eventTarget: this._latestPointer.eventTarget,
        interaction: this
      }, t || {}), t.phase = "move", this._doPhase(t);
    }
    pointerUp(t, n, i, o) {
      let r = this.getPointerIndex(t);
      r === -1 && (r = this.updatePointer(t, n, i, false));
      const s = /cancel$/i.test(n.type) ? "cancel" : "up";
      this._scopeFire(`interactions:${s}`, {
        pointer: t,
        pointerIndex: r,
        pointerInfo: this.pointers[r],
        event: n,
        eventTarget: i,
        type: s,
        curEventTarget: o,
        interaction: this
      }), this.simulation || this.end(n), this.removePointer(t, n);
    }
    documentBlur(t) {
      this.end(t), this._scopeFire("interactions:blur", {
        event: t,
        type: "blur",
        interaction: this
      });
    }
    end(t) {
      this._ending = true, t = t || this._latestPointer.event;
      let n;
      this.interacting() && (n = this._doPhase({
        event: t,
        interaction: this,
        phase: "end"
      })), this._ending = false, n === true && this.stop();
    }
    currentAction() {
      return this._interacting ? this.prepared.name : null;
    }
    interacting() {
      return this._interacting;
    }
    stop() {
      this._scopeFire("interactions:stop", {
        interaction: this
      }), this.interactable = this.element = null, this._interacting = false, this._stopped = true, this.prepared.name = this.prevEvent = null;
    }
    getPointerIndex(t) {
      const n = xe(t);
      return this.pointerType === "mouse" || this.pointerType === "pen" ? this.pointers.length - 1 : Ie(this.pointers, (i) => i.id === n);
    }
    getPointerInfo(t) {
      return this.pointers[this.getPointerIndex(t)];
    }
    updatePointer(t, n, i, o) {
      const r = xe(t);
      let s = this.getPointerIndex(t), a = this.pointers[s];
      return o = o === false ? false : o || /(down|start)$/i.test(n.type), a ? a.pointer = t : (a = new $o(r, t, n, null, null), s = this.pointers.length, this.pointers.push(a)), To(this.coords.cur, this.pointers.map((l) => l.pointer), this._now()), wo(this.coords.delta, this.coords.prev, this.coords.cur), o && (this.pointerIsDown = true, a.downTime = this.coords.cur.timeStamp, a.downTarget = i, fi(this.downPointer, t), this.interacting() || (Re(this.coords.start, this.coords.cur), Re(this.coords.prev, this.coords.cur), this.downEvent = n, this.pointerWasMoved = false)), this._updateLatestPointer(t, n, i), this._scopeFire("interactions:update-pointer", {
        pointer: t,
        event: n,
        eventTarget: i,
        down: o,
        pointerInfo: a,
        pointerIndex: s,
        interaction: this
      }), s;
    }
    removePointer(t, n) {
      const i = this.getPointerIndex(t);
      if (i === -1)
        return;
      const o = this.pointers[i];
      this._scopeFire("interactions:remove-pointer", {
        pointer: t,
        event: n,
        eventTarget: null,
        pointerIndex: i,
        pointerInfo: o,
        interaction: this
      }), this.pointers.splice(i, 1), this.pointerIsDown = false;
    }
    _updateLatestPointer(t, n, i) {
      this._latestPointer.pointer = t, this._latestPointer.event = n, this._latestPointer.eventTarget = i;
    }
    destroy() {
      this._latestPointer.pointer = null, this._latestPointer.event = null, this._latestPointer.eventTarget = null;
    }
    _createPreparedEvent(t, n, i, o) {
      return new sn(this, t, this.prepared.name, n, this.element, i, o);
    }
    _fireEvent(t) {
      var n;
      (n = this.interactable) == null || n.fire(t), (!this.prevEvent || t.timeStamp >= this.prevEvent.timeStamp) && (this.prevEvent = t);
    }
    _doPhase(t) {
      const {
        event: n,
        phase: i,
        preEnd: o,
        type: r
      } = t, {
        rect: s
      } = this;
      if (s && i === "move" && (on(this.edges, s, this.coords.delta[this.interactable.options.deltaSource]), s.width = s.right - s.left, s.height = s.bottom - s.top), this._scopeFire(`interactions:before-action-${i}`, t) === false)
        return false;
      const l = t.iEvent = this._createPreparedEvent(n, i, o, r);
      return this._scopeFire(`interactions:action-${i}`, t), i === "start" && (this.prevEvent = l), this._fireEvent(l), this._scopeFire(`interactions:after-action-${i}`, t), true;
    }
    _now() {
      return Date.now();
    }
  }
  const Lo = Wo;
  function Fo(e) {
    return /^(always|never|auto)$/.test(e) ? (this.options.preventDefault = e, this) : g.bool(e) ? (this.options.preventDefault = e ? "always" : "never", this) : this.options.preventDefault;
  }
  function No(e, t, n) {
    const i = e.options.preventDefault;
    if (i !== "never") {
      if (i === "always") {
        n.preventDefault();
        return;
      }
      if (t.events.supportsPassive && /^touch(start|move)$/.test(n.type)) {
        const o = Ft(n.target).document, r = t.getDocOptions(o);
        if (!(r && r.events) || r.events.passive !== false)
          return;
      }
      /^(mouse|pointer|touch)*(down|start)/i.test(n.type) || g.element(n.target) && Nt(n.target, "input,select,textarea,[contenteditable=true],[contenteditable=true] *") || n.preventDefault();
    }
  }
  function jo({
    interaction: e,
    event: t
  }) {
    e.interactable && e.interactable.checkAndPreventDefault(t);
  }
  function Yo(e) {
    const {
      Interactable: t
    } = e;
    t.prototype.preventDefault = Fo, t.prototype.checkAndPreventDefault = function(n) {
      return No(this, e, n);
    }, e.interactions.docEvents.push({
      type: "dragstart",
      listener(n) {
        for (const i of e.interactions.list)
          if (i.element && (i.element === n.target || Lt(i.element, n.target))) {
            i.interactable.checkAndPreventDefault(n);
            return;
          }
      }
    });
  }
  const Xo = {
    id: "core/interactablePreventDefault",
    install: Yo,
    listeners: ["down", "move", "up", "cancel"].reduce((e, t) => (e[`interactions:${t}`] = jo, e), {})
  }, Ze = {
    methodOrder: ["simulationResume", "mouseOrPen", "hasPointer", "idle"],
    search(e) {
      for (const t of Ze.methodOrder) {
        const n = Ze[t](e);
        if (n)
          return n;
      }
      return null;
    },
    simulationResume({
      pointerType: e,
      eventType: t,
      eventTarget: n,
      scope: i
    }) {
      if (!/down|start/i.test(t))
        return null;
      for (const o of i.interactions.list) {
        let r = n;
        if (o.simulation && o.simulation.allowResume && o.pointerType === e)
          for (; r; ) {
            if (r === o.element)
              return o;
            r = Rt(r);
          }
      }
      return null;
    },
    mouseOrPen({
      pointerId: e,
      pointerType: t,
      eventType: n,
      scope: i
    }) {
      if (t !== "mouse" && t !== "pen")
        return null;
      let o;
      for (const r of i.interactions.list)
        if (r.pointerType === t) {
          if (r.simulation && !Tn(r, e))
            continue;
          if (r.interacting())
            return r;
          o || (o = r);
        }
      if (o)
        return o;
      for (const r of i.interactions.list)
        if (r.pointerType === t && !(/down/i.test(n) && r.simulation))
          return r;
      return null;
    },
    hasPointer({
      pointerId: e,
      scope: t
    }) {
      for (const n of t.interactions.list)
        if (Tn(n, e))
          return n;
      return null;
    },
    idle({
      pointerType: e,
      scope: t
    }) {
      for (const n of t.interactions.list) {
        if (n.pointers.length === 1) {
          const i = n.interactable;
          if (i && !(i.options.gesture && i.options.gesture.enabled))
            continue;
        } else if (n.pointers.length >= 2)
          continue;
        if (!n.interacting() && e === n.pointerType)
          return n;
      }
      return null;
    }
  };
  function Tn(e, t) {
    return e.pointers.some(({
      id: n
    }) => n === t);
  }
  const Go = Ze, gi = ["pointerDown", "pointerMove", "pointerUp", "updatePointer", "removePointer", "windowBlur"];
  function qo(e) {
    const t = {};
    for (const r of gi)
      t[r] = vi(r, e);
    const n = mt.pEventTypes;
    let i;
    ut.PointerEvent ? i = [{
      type: n.down,
      listener: o
    }, {
      type: n.down,
      listener: t.pointerDown
    }, {
      type: n.move,
      listener: t.pointerMove
    }, {
      type: n.up,
      listener: t.pointerUp
    }, {
      type: n.cancel,
      listener: t.pointerUp
    }] : i = [{
      type: "mousedown",
      listener: t.pointerDown
    }, {
      type: "mousemove",
      listener: t.pointerMove
    }, {
      type: "mouseup",
      listener: t.pointerUp
    }, {
      type: "touchstart",
      listener: o
    }, {
      type: "touchstart",
      listener: t.pointerDown
    }, {
      type: "touchmove",
      listener: t.pointerMove
    }, {
      type: "touchend",
      listener: t.pointerUp
    }, {
      type: "touchcancel",
      listener: t.pointerUp
    }], i.push({
      type: "blur",
      listener(r) {
        for (const s of e.interactions.list)
          s.documentBlur(r);
      }
    }), e.prevTouchTime = 0, e.Interaction = class extends Lo {
      get pointerMoveTolerance() {
        return e.interactions.pointerMoveTolerance;
      }
      set pointerMoveTolerance(r) {
        e.interactions.pointerMoveTolerance = r;
      }
      _now() {
        return e.now();
      }
    }, e.interactions = {
      list: [],
      new(r) {
        r.scopeFire = (a, l) => e.fire(a, l);
        const s = new e.Interaction(r);
        return e.interactions.list.push(s), s;
      },
      listeners: t,
      docEvents: i,
      pointerMoveTolerance: 1
    };
    function o() {
      for (const r of e.interactions.list)
        if (!(!r.pointerIsDown || r.pointerType !== "touch" || r._interacting))
          for (const s of r.pointers)
            e.documents.some(({
              doc: a
            }) => Lt(a, s.downTarget)) || r.removePointer(s.pointer, s.event);
    }
    e.usePlugin(Xo);
  }
  function vi(e, t) {
    return function(n) {
      const i = t.interactions.list, o = Do(n), [r, s] = pi(n), a = [];
      if (/^touch/.test(n.type)) {
        t.prevTouchTime = t.now();
        for (const l of n.changedTouches) {
          const c = l, u = xe(c), f = {
            pointer: c,
            pointerId: u,
            pointerType: o,
            eventType: n.type,
            eventTarget: r,
            curEventTarget: s,
            scope: t
          }, v = Mn(f);
          a.push([f.pointer, f.eventTarget, f.curEventTarget, v]);
        }
      } else {
        let l = false;
        if (!mt.supportsPointerEvent && /mouse/.test(n.type)) {
          for (let c = 0; c < i.length && !l; c++)
            l = i[c].pointerType !== "mouse" && i[c].pointerIsDown;
          l = l || t.now() - t.prevTouchTime < 500 || n.timeStamp === 0;
        }
        if (!l) {
          const c = {
            pointer: n,
            pointerId: xe(n),
            pointerType: o,
            eventType: n.type,
            curEventTarget: s,
            eventTarget: r,
            scope: t
          }, u = Mn(c);
          a.push([c.pointer, c.eventTarget, c.curEventTarget, u]);
        }
      }
      for (const [l, c, u, f] of a)
        f[e](l, n, c, u);
    };
  }
  function Mn(e) {
    const {
      pointerType: t,
      scope: n
    } = e, o = {
      interaction: Go.search(e),
      searchDetails: e
    };
    return n.fire("interactions:find", o), o.interaction || n.interactions.new({
      pointerType: t
    });
  }
  function He({
    doc: e,
    scope: t,
    options: n
  }, i) {
    const {
      interactions: {
        docEvents: o
      },
      events: r
    } = t, s = r[i];
    t.browser.isIOS && !n.events && (n.events = {
      passive: false
    });
    for (const l in r.delegatedEvents)
      s(e, l, r.delegateListener), s(e, l, r.delegateUseCapture, true);
    const a = n && n.events;
    for (const {
      type: l,
      listener: c
    } of o)
      s(e, l, c, a);
  }
  const Uo = {
    id: "core/interactions",
    install: qo,
    listeners: {
      "scope:add-document": (e) => He(e, "add"),
      "scope:remove-document": (e) => He(e, "remove"),
      "interactable:unset": ({
        interactable: e
      }, t) => {
        for (let n = t.interactions.list.length - 1; n >= 0; n--) {
          const i = t.interactions.list[n];
          i.interactable === e && (i.stop(), t.fire("interactions:destroy", {
            interaction: i
          }), i.destroy(), t.interactions.list.length > 2 && t.interactions.list.splice(n, 1));
        }
      }
    },
    onDocSignal: He,
    doOnInteractions: vi,
    methodNames: gi
  }, Vo = Uo;
  class Ko {
    constructor() {
      p(this, "id", `__interact_scope_${Math.floor(Math.random() * 100)}`);
      p(this, "isInitialized", false);
      p(this, "listenerMaps", []);
      p(this, "browser", mt);
      p(this, "defaults", Jt(ci));
      p(this, "Eventable", ri);
      p(this, "actions", {
        map: {},
        phases: {
          start: true,
          move: true,
          end: true
        },
        methodDict: {},
        phaselessTypes: {}
      });
      p(this, "interactStatic", Po(this));
      p(this, "InteractEvent", sn);
      p(this, "Interactable");
      p(this, "interactables", new Ao(this));
      p(this, "_win");
      p(this, "document");
      p(this, "window");
      p(this, "documents", []);
      p(this, "_plugins", {
        list: [],
        map: {}
      });
      p(this, "onWindowUnload", (t2) => this.removeDocument(t2.target));
      const t = this;
      this.Interactable = class extends ko {
        get _defaults() {
          return t.defaults;
        }
        set(n) {
          return super.set(n), t.fire("interactable:set", {
            options: n,
            interactable: this
          }), this;
        }
        unset() {
          super.unset();
          const n = t.interactables.list.indexOf(this);
          n < 0 || (super.unset(), t.interactables.list.splice(n, 1), t.fire("interactable:unset", {
            interactable: this
          }));
        }
      };
    }
    addListeners(t, n) {
      this.listenerMaps.push({
        id: n,
        map: t
      });
    }
    fire(t, n) {
      for (const {
        map: {
          [t]: i
        }
      } of this.listenerMaps)
        if (!!i && i(n, this, t) === false)
          return false;
    }
    init(t) {
      return this.isInitialized ? this : Jo(this, t);
    }
    pluginIsInstalled(t) {
      return this._plugins.map[t.id] || this._plugins.list.indexOf(t) !== -1;
    }
    usePlugin(t, n) {
      if (!this.isInitialized)
        return this;
      if (this.pluginIsInstalled(t))
        return this;
      if (t.id && (this._plugins.map[t.id] = t), this._plugins.list.push(t), t.install && t.install(this, n), t.listeners && t.before) {
        let i = 0;
        const o = this.listenerMaps.length, r = t.before.reduce((s, a) => (s[a] = true, s[_n(a)] = true, s), {});
        for (; i < o; i++) {
          const s = this.listenerMaps[i].id;
          if (r[s] || r[_n(s)])
            break;
        }
        this.listenerMaps.splice(i, 0, {
          id: t.id,
          map: t.listeners
        });
      } else
        t.listeners && this.listenerMaps.push({
          id: t.id,
          map: t.listeners
        });
      return this;
    }
    addDocument(t, n) {
      if (this.getDocIndex(t) !== -1)
        return false;
      const i = Ft(t);
      n = n ? D({}, n) : {}, this.documents.push({
        doc: t,
        options: n
      }), this.events.documents.push(t), t !== this.document && this.events.add(i, "unload", this.onWindowUnload), this.fire("scope:add-document", {
        doc: t,
        window: i,
        scope: this,
        options: n
      });
    }
    removeDocument(t) {
      const n = this.getDocIndex(t), i = Ft(t), o = this.documents[n].options;
      this.events.remove(i, "unload", this.onWindowUnload), this.documents.splice(n, 1), this.events.documents.splice(n, 1), this.fire("scope:remove-document", {
        doc: t,
        window: i,
        scope: this,
        options: o
      });
    }
    getDocIndex(t) {
      for (let n = 0; n < this.documents.length; n++)
        if (this.documents[n].doc === t)
          return n;
      return -1;
    }
    getDocOptions(t) {
      const n = this.getDocIndex(t);
      return n === -1 ? null : this.documents[n].options;
    }
    now() {
      return (this.window.Date || Date).now();
    }
  }
  function Jo(e, t) {
    return e.isInitialized = true, g.window(t) && ei(t), ut.init(t), mt.init(t), Ut.init(t), e.window = t, e.document = t.document, e.usePlugin(Vo), e.usePlugin(Ho), e;
  }
  function _n(e) {
    return e && e.replace(/\/.*$/, "");
  }
  const mi = new Ko(), Zo = mi.interactStatic, _t = Zo, Qo = typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : globalThis;
  mi.init(Qo);
  function tr(e) {
    const {
      Interactable: t
    } = e;
    t.prototype.getAction = function(i, o, r, s) {
      const a = er(this, o, r, s, e);
      return this.options.actionChecker ? this.options.actionChecker(i, o, a, this, s, r) : a;
    }, t.prototype.ignoreFrom = ue(function(n) {
      return this._backCompatOption("ignoreFrom", n);
    }, "Interactable.ignoreFrom() has been deprecated. Use Interactble.draggable({ignoreFrom: newValue})."), t.prototype.allowFrom = ue(function(n) {
      return this._backCompatOption("allowFrom", n);
    }, "Interactable.allowFrom() has been deprecated. Use Interactble.draggable({allowFrom: newValue})."), t.prototype.actionChecker = ir, t.prototype.styleCursor = nr;
  }
  function er(e, t, n, i, o) {
    const r = e.getRect(i), s = t.buttons || {
      0: 1,
      1: 4,
      3: 8,
      4: 16
    }[t.button], a = {
      action: null,
      interactable: e,
      interaction: n,
      element: i,
      rect: r,
      buttons: s
    };
    return o.fire("auto-start:check", a), a.action;
  }
  function nr(e) {
    return g.bool(e) ? (this.options.styleCursor = e, this) : e === null ? (delete this.options.styleCursor, this) : this.options.styleCursor;
  }
  function ir(e) {
    return g.func(e) ? (this.options.actionChecker = e, this) : e === null ? (delete this.options.actionChecker, this) : this.options.actionChecker;
  }
  const or = {
    id: "auto-start/interactableMethods",
    install: tr
  };
  function rr(e) {
    const {
      interactStatic: t,
      defaults: n
    } = e;
    e.usePlugin(or), n.base.actionChecker = null, n.base.styleCursor = true, D(n.perAction, {
      manualStart: false,
      max: 1 / 0,
      maxPerElement: 1,
      allowFrom: null,
      ignoreFrom: null,
      mouseButtons: 1
    }), t.maxInteractions = (i) => wi(i, e), e.autoStart = {
      maxInteractions: 1 / 0,
      withinInteractionLimit: Me,
      cursorElement: null
    };
  }
  function sr({
    interaction: e,
    pointer: t,
    event: n,
    eventTarget: i
  }, o) {
    if (e.interacting())
      return;
    const r = bi(e, t, n, i, o);
    xi(e, r, o);
  }
  function ar({
    interaction: e,
    pointer: t,
    event: n,
    eventTarget: i
  }, o) {
    if (e.pointerType !== "mouse" || e.pointerIsDown || e.interacting())
      return;
    const r = bi(e, t, n, i, o);
    xi(e, r, o);
  }
  function lr(e, t) {
    const {
      interaction: n
    } = e;
    if (!n.pointerIsDown || n.interacting() || !n.pointerWasMoved || !n.prepared.name)
      return;
    t.fire("autoStart:before-start", e);
    const {
      interactable: i
    } = n, o = n.prepared.name;
    o && i && (i.options[o].manualStart || !Me(i, n.element, n.prepared, t) ? n.stop() : (n.start(n.prepared, i, n.element), Si(n, t)));
  }
  function cr({
    interaction: e
  }, t) {
    const {
      interactable: n
    } = e;
    n && n.options.styleCursor && Qe(e.element, "", t);
  }
  function yi(e, t, n, i, o) {
    return t.testIgnoreAllow(t.options[e.name], n, i) && t.options[e.name].enabled && Me(t, n, e, o) ? e : null;
  }
  function ur(e, t, n, i, o, r, s) {
    for (let a = 0, l = i.length; a < l; a++) {
      const c = i[a], u = o[a], f = c.getAction(t, n, e, u);
      if (!f)
        continue;
      const v = yi(f, c, u, r, s);
      if (v)
        return {
          action: v,
          interactable: c,
          element: u
        };
    }
    return {
      action: null,
      interactable: null,
      element: null
    };
  }
  function bi(e, t, n, i, o) {
    let r = [], s = [], a = i;
    function l(c) {
      r.push(c), s.push(a);
    }
    for (; g.element(a); ) {
      r = [], s = [], o.interactables.forEachMatch(a, l);
      const c = ur(e, t, n, r, s, i, o);
      if (c.action && !c.interactable.options[c.action.name].manualStart)
        return c;
      a = Rt(a);
    }
    return {
      action: null,
      interactable: null,
      element: null
    };
  }
  function xi(e, {
    action: t,
    interactable: n,
    element: i
  }, o) {
    t = t || {
      name: null
    }, e.interactable = n, e.element = i, ui(e.prepared, t), e.rect = n && t.name ? n.getRect(i) : null, Si(e, o), o.fire("autoStart:prepared", {
      interaction: e
    });
  }
  function Me(e, t, n, i) {
    const o = e.options, r = o[n.name].max, s = o[n.name].maxPerElement, a = i.autoStart.maxInteractions;
    let l = 0, c = 0, u = 0;
    if (!(r && s && a))
      return false;
    for (const f of i.interactions.list) {
      const v = f.prepared.name;
      if (!!f.interacting()) {
        if (l++, l >= a)
          return false;
        if (f.interactable === e && (c += v === n.name ? 1 : 0, c >= r || f.element === t && (u++, v === n.name && u >= s)))
          return false;
      }
    }
    return a > 0;
  }
  function wi(e, t) {
    return g.number(e) ? (t.autoStart.maxInteractions = e, this) : t.autoStart.maxInteractions;
  }
  function Qe(e, t, n) {
    const {
      cursorElement: i
    } = n.autoStart;
    i && i !== e && (i.style.cursor = ""), e.ownerDocument.documentElement.style.cursor = t, e.style.cursor = t, n.autoStart.cursorElement = t ? e : null;
  }
  function Si(e, t) {
    const {
      interactable: n,
      element: i,
      prepared: o
    } = e;
    if (!(e.pointerType === "mouse" && n && n.options.styleCursor)) {
      t.autoStart.cursorElement && Qe(t.autoStart.cursorElement, "", t);
      return;
    }
    let r = "";
    if (o.name) {
      const s = n.options[o.name].cursorChecker;
      g.func(s) ? r = s(o, n, i, e._interacting) : r = t.actions.map[o.name].getCursor(o);
    }
    Qe(e.element, r || "", t);
  }
  const fr = {
    id: "auto-start/base",
    before: ["actions"],
    install: rr,
    listeners: {
      "interactions:down": sr,
      "interactions:move": (e, t) => {
        ar(e, t), lr(e, t);
      },
      "interactions:stop": cr
    },
    maxInteractions: wi,
    withinInteractionLimit: Me,
    validateAction: yi
  }, ln = fr;
  function dr({
    interaction: e,
    eventTarget: t,
    dx: n,
    dy: i
  }, o) {
    if (e.prepared.name !== "drag")
      return;
    const r = Math.abs(n), s = Math.abs(i), a = e.interactable.options.drag, l = a.startAxis, c = r > s ? "x" : r < s ? "y" : "xy";
    if (e.prepared.axis = a.lockAxis === "start" ? c[0] : a.lockAxis, c !== "xy" && l !== "xy" && l !== c) {
      e.prepared.name = null;
      let u = t;
      const f = function(v) {
        if (v === e.interactable)
          return;
        const y = e.interactable.options.drag;
        if (!y.manualStart && v.testIgnoreAllow(y, u, t)) {
          const x = v.getAction(e.downPointer, e.downEvent, e, u);
          if (x && x.name === "drag" && hr(c, v) && ln.validateAction(x, v, u, t, o))
            return v;
        }
      };
      for (; g.element(u); ) {
        const v = o.interactables.forEachMatch(u, f);
        if (v) {
          e.prepared.name = "drag", e.interactable = v, e.element = u;
          break;
        }
        u = Rt(u);
      }
    }
  }
  function hr(e, t) {
    if (!t)
      return false;
    const n = t.options.drag.startAxis;
    return e === "xy" || n === "xy" || n === e;
  }
  const pr = {
    id: "auto-start/dragAxis",
    listeners: {
      "autoStart:before-start": dr
    }
  };
  function gr(e) {
    const {
      defaults: t
    } = e;
    e.usePlugin(ln), t.perAction.hold = 0, t.perAction.delay = 0;
  }
  function $e(e) {
    const t = e.prepared && e.prepared.name;
    if (!t)
      return null;
    const n = e.interactable.options;
    return n[t].hold || n[t].delay;
  }
  const vr = {
    id: "auto-start/hold",
    install: gr,
    listeners: {
      "interactions:new": ({
        interaction: e
      }) => {
        e.autoStartHoldTimer = null;
      },
      "autoStart:prepared": ({
        interaction: e
      }) => {
        const t = $e(e);
        t > 0 && (e.autoStartHoldTimer = setTimeout(() => {
          e.start(e.prepared, e.interactable, e.element);
        }, t));
      },
      "interactions:move": ({
        interaction: e,
        duplicate: t
      }) => {
        e.autoStartHoldTimer && e.pointerWasMoved && !t && (clearTimeout(e.autoStartHoldTimer), e.autoStartHoldTimer = null);
      },
      "autoStart:before-start": ({
        interaction: e
      }) => {
        $e(e) > 0 && (e.prepared.name = null);
      }
    },
    getHoldDuration: $e
  }, mr = vr, yr = {
    id: "auto-start",
    install(e) {
      e.usePlugin(ln), e.usePlugin(mr), e.usePlugin(pr);
    }
  };
  _t.use(yr);
  function br(e) {
    const {
      defaults: t,
      actions: n
    } = e;
    e.autoScroll = P, P.now = () => e.now(), n.phaselessTypes.autoscroll = true, t.perAction.autoScroll = P.defaults;
  }
  const P = {
    defaults: {
      enabled: false,
      margin: 60,
      container: null,
      speed: 300
    },
    now: Date.now,
    interaction: null,
    i: 0,
    x: 0,
    y: 0,
    isScrolling: false,
    prevTime: 0,
    margin: 0,
    speed: 0,
    start(e) {
      P.isScrolling = true, Ut.cancel(P.i), e.autoScroll = P, P.interaction = e, P.prevTime = P.now(), P.i = Ut.request(P.scroll);
    },
    stop() {
      P.isScrolling = false, P.interaction && (P.interaction.autoScroll = null), Ut.cancel(P.i);
    },
    scroll() {
      const {
        interaction: e
      } = P, {
        interactable: t,
        element: n
      } = e, i = e.prepared.name, o = t.options[i].autoScroll, r = Cn(o.container, t, n), s = P.now(), a = (s - P.prevTime) / 1e3, l = o.speed * a;
      if (l >= 1) {
        const c = {
          x: P.x * l,
          y: P.y * l
        };
        if (c.x || c.y) {
          const u = Dn(r);
          g.window(r) ? r.scrollBy(c.x, c.y) : r && (r.scrollLeft += c.x, r.scrollTop += c.y);
          const f = Dn(r), v = {
            x: f.x - u.x,
            y: f.y - u.y
          };
          (v.x || v.y) && t.fire({
            type: "autoscroll",
            target: n,
            interactable: t,
            delta: v,
            interaction: e,
            container: r
          });
        }
        P.prevTime = s;
      }
      P.isScrolling && (Ut.cancel(P.i), P.i = Ut.request(P.scroll));
    },
    check(e, t) {
      var n;
      return (n = e.options[t].autoScroll) == null ? void 0 : n.enabled;
    },
    onInteractionMove({
      interaction: e,
      pointer: t
    }) {
      if (!(e.interacting() && P.check(e.interactable, e.prepared.name)))
        return;
      if (e.simulation) {
        P.x = P.y = 0;
        return;
      }
      let n, i, o, r;
      const {
        interactable: s,
        element: a
      } = e, l = e.prepared.name, c = s.options[l].autoScroll, u = Cn(c.container, s, a);
      if (g.window(u))
        r = t.clientX < P.margin, n = t.clientY < P.margin, i = t.clientX > u.innerWidth - P.margin, o = t.clientY > u.innerHeight - P.margin;
      else {
        const f = en(u);
        r = t.clientX < f.left + P.margin, n = t.clientY < f.top + P.margin, i = t.clientX > f.right - P.margin, o = t.clientY > f.bottom - P.margin;
      }
      P.x = i ? 1 : r ? -1 : 0, P.y = o ? 1 : n ? -1 : 0, P.isScrolling || (P.margin = c.margin, P.speed = c.speed, P.start(e));
    }
  };
  function Cn(e, t, n) {
    return (g.string(e) ? ai(e, t, n) : e) || Ft(n);
  }
  function Dn(e) {
    return g.window(e) && (e = window.document.body), {
      x: e.scrollLeft,
      y: e.scrollTop
    };
  }
  const xr = {
    id: "auto-scroll",
    install: br,
    listeners: {
      "interactions:new": ({
        interaction: e
      }) => {
        e.autoScroll = null;
      },
      "interactions:destroy": ({
        interaction: e
      }) => {
        e.autoScroll = null, P.stop(), P.interaction && (P.interaction = null);
      },
      "interactions:stop": P.stop,
      "interactions:action-move": (e) => P.onInteractionMove(e)
    }
  }, wr = xr;
  _t.use(wr);
  function Sr(e) {
    const {
      actions: t,
      Interactable: n,
      defaults: i
    } = e;
    n.prototype.draggable = ye.draggable, t.map.drag = ye, t.methodDict.drag = "draggable", i.actions.drag = ye.defaults;
  }
  function Be({
    interaction: e
  }) {
    if (e.prepared.name !== "drag")
      return;
    const t = e.prepared.axis;
    t === "x" ? (e.coords.cur.page.y = e.coords.start.page.y, e.coords.cur.client.y = e.coords.start.client.y, e.coords.velocity.client.y = 0, e.coords.velocity.page.y = 0) : t === "y" && (e.coords.cur.page.x = e.coords.start.page.x, e.coords.cur.client.x = e.coords.start.client.x, e.coords.velocity.client.x = 0, e.coords.velocity.page.x = 0);
  }
  function Pn({
    iEvent: e,
    interaction: t
  }) {
    if (t.prepared.name !== "drag")
      return;
    const n = t.prepared.axis;
    if (n === "x" || n === "y") {
      const i = n === "x" ? "y" : "x";
      e.page[i] = t.coords.start.page[i], e.client[i] = t.coords.start.client[i], e.delta[i] = 0;
    }
  }
  const Er = function(t) {
    return g.object(t) ? (this.options.drag.enabled = t.enabled !== false, this.setPerAction("drag", t), this.setOnEvents("drag", t), /^(xy|x|y|start)$/.test(t.lockAxis) && (this.options.drag.lockAxis = t.lockAxis), /^(xy|x|y)$/.test(t.startAxis) && (this.options.drag.startAxis = t.startAxis), this) : g.bool(t) ? (this.options.drag.enabled = t, this) : this.options.drag;
  }, ye = {
    id: "actions/drag",
    install: Sr,
    listeners: {
      "interactions:before-action-move": Be,
      "interactions:action-resume": Be,
      "interactions:action-move": Pn,
      "auto-start:check": (e) => {
        const {
          interaction: t,
          interactable: n,
          buttons: i
        } = e, o = n.options.drag;
        if (!(!(o && o.enabled) || t.pointerIsDown && /mouse|pointer/.test(t.pointerType) && (i & n.options.drag.mouseButtons) === 0))
          return e.action = {
            name: "drag",
            axis: o.lockAxis === "start" ? o.startAxis : o.lockAxis
          }, false;
      }
    },
    draggable: Er,
    beforeMove: Be,
    move: Pn,
    defaults: {
      startAxis: "xy",
      lockAxis: "xy"
    },
    getCursor() {
      return "move";
    }
  }, Ir = ye;
  _t.use(Ir);
  function zr(e) {
    const {
      actions: t,
      browser: n,
      Interactable: i,
      defaults: o
    } = e;
    Mt.cursors = Cr(n), Mt.defaultMargin = n.supportsTouch || n.supportsPointerEvent ? 20 : 10, i.prototype.resizable = function(r) {
      return Mr(this, r, e);
    }, t.map.resize = Mt, t.methodDict.resize = "resizable", o.actions.resize = Mt.defaults;
  }
  function Tr(e) {
    const {
      interaction: t,
      interactable: n,
      element: i,
      rect: o,
      buttons: r
    } = e;
    if (!o)
      return;
    const s = D({}, t.coords.cur.page), a = n.options.resize;
    if (!(!(a && a.enabled) || t.pointerIsDown && /mouse|pointer/.test(t.pointerType) && (r & a.mouseButtons) === 0)) {
      if (g.object(a.edges)) {
        const l = {
          left: false,
          right: false,
          top: false,
          bottom: false
        };
        for (const c in l)
          l[c] = _r(c, a.edges[c], s, t._latestPointer.eventTarget, i, o, a.margin || Mt.defaultMargin);
        l.left = l.left && !l.right, l.top = l.top && !l.bottom, (l.left || l.right || l.top || l.bottom) && (e.action = {
          name: "resize",
          edges: l
        });
      } else {
        const l = a.axis !== "y" && s.x > o.right - Mt.defaultMargin, c = a.axis !== "x" && s.y > o.bottom - Mt.defaultMargin;
        (l || c) && (e.action = {
          name: "resize",
          axes: (l ? "x" : "") + (c ? "y" : "")
        });
      }
      return e.action ? false : void 0;
    }
  }
  function Mr(e, t, n) {
    return g.object(t) ? (e.options.resize.enabled = t.enabled !== false, e.setPerAction("resize", t), e.setOnEvents("resize", t), g.string(t.axis) && /^x$|^y$|^xy$/.test(t.axis) ? e.options.resize.axis = t.axis : t.axis === null && (e.options.resize.axis = n.defaults.actions.resize.axis), g.bool(t.preserveAspectRatio) ? e.options.resize.preserveAspectRatio = t.preserveAspectRatio : g.bool(t.square) && (e.options.resize.square = t.square), e) : g.bool(t) ? (e.options.resize.enabled = t, e) : e.options.resize;
  }
  function _r(e, t, n, i, o, r, s) {
    if (!t)
      return false;
    if (t === true) {
      const a = g.number(r.width) ? r.width : r.right - r.left, l = g.number(r.height) ? r.height : r.bottom - r.top;
      if (s = Math.min(s, Math.abs((e === "left" || e === "right" ? a : l) / 2)), a < 0 && (e === "left" ? e = "right" : e === "right" && (e = "left")), l < 0 && (e === "top" ? e = "bottom" : e === "bottom" && (e = "top")), e === "left") {
        const c = a >= 0 ? r.left : r.right;
        return n.x < c + s;
      }
      if (e === "top") {
        const c = l >= 0 ? r.top : r.bottom;
        return n.y < c + s;
      }
      if (e === "right")
        return n.x > (a >= 0 ? r.right : r.left) - s;
      if (e === "bottom")
        return n.y > (l >= 0 ? r.bottom : r.top) - s;
    }
    return g.element(i) ? g.element(t) ? t === i : Ue(i, t, o) : false;
  }
  function Cr(e) {
    return e.isIe9 ? {
      x: "e-resize",
      y: "s-resize",
      xy: "se-resize",
      top: "n-resize",
      left: "w-resize",
      bottom: "s-resize",
      right: "e-resize",
      topleft: "se-resize",
      bottomright: "se-resize",
      topright: "ne-resize",
      bottomleft: "ne-resize"
    } : {
      x: "ew-resize",
      y: "ns-resize",
      xy: "nwse-resize",
      top: "ns-resize",
      left: "ew-resize",
      bottom: "ns-resize",
      right: "ew-resize",
      topleft: "nwse-resize",
      bottomright: "nwse-resize",
      topright: "nesw-resize",
      bottomleft: "nesw-resize"
    };
  }
  function Dr({
    iEvent: e,
    interaction: t
  }) {
    if (t.prepared.name !== "resize" || !t.prepared.edges)
      return;
    const n = e, i = t.rect;
    t._rects = {
      start: D({}, i),
      corrected: D({}, i),
      previous: D({}, i),
      delta: {
        left: 0,
        right: 0,
        width: 0,
        top: 0,
        bottom: 0,
        height: 0
      }
    }, n.edges = t.prepared.edges, n.rect = t._rects.corrected, n.deltaRect = t._rects.delta;
  }
  function Pr({
    iEvent: e,
    interaction: t
  }) {
    if (t.prepared.name !== "resize" || !t.prepared.edges)
      return;
    const n = e, o = t.interactable.options.resize.invert, r = o === "reposition" || o === "negate", s = t.rect, {
      start: a,
      corrected: l,
      delta: c,
      previous: u
    } = t._rects;
    if (D(u, l), r) {
      if (D(l, s), o === "reposition") {
        if (l.top > l.bottom) {
          const f = l.top;
          l.top = l.bottom, l.bottom = f;
        }
        if (l.left > l.right) {
          const f = l.left;
          l.left = l.right, l.right = f;
        }
      }
    } else
      l.top = Math.min(s.top, a.bottom), l.bottom = Math.max(s.bottom, a.top), l.left = Math.min(s.left, a.right), l.right = Math.max(s.right, a.left);
    l.width = l.right - l.left, l.height = l.bottom - l.top;
    for (const f in l)
      c[f] = l[f] - u[f];
    n.edges = t.prepared.edges, n.rect = l, n.deltaRect = c;
  }
  function kr({
    iEvent: e,
    interaction: t
  }) {
    if (t.prepared.name !== "resize" || !t.prepared.edges)
      return;
    const n = e;
    n.edges = t.prepared.edges, n.rect = t._rects.corrected, n.deltaRect = t._rects.delta;
  }
  function kn({
    iEvent: e,
    interaction: t
  }) {
    if (t.prepared.name !== "resize" || !t.resizeAxes)
      return;
    const n = t.interactable.options, i = e;
    n.resize.square ? (t.resizeAxes === "y" ? i.delta.x = i.delta.y : i.delta.y = i.delta.x, i.axes = "xy") : (i.axes = t.resizeAxes, t.resizeAxes === "x" ? i.delta.y = 0 : t.resizeAxes === "y" && (i.delta.x = 0));
  }
  const Mt = {
    id: "actions/resize",
    before: ["actions/drag"],
    install: zr,
    listeners: {
      "interactions:new": ({
        interaction: e
      }) => {
        e.resizeAxes = "xy";
      },
      "interactions:action-start": (e) => {
        Dr(e), kn(e);
      },
      "interactions:action-move": (e) => {
        Pr(e), kn(e);
      },
      "interactions:action-end": kr,
      "auto-start:check": Tr
    },
    defaults: {
      square: false,
      preserveAspectRatio: false,
      axis: "xy",
      margin: NaN,
      edges: null,
      invert: "none"
    },
    cursors: null,
    getCursor({
      edges: e,
      axis: t,
      name: n
    }) {
      const i = Mt.cursors;
      let o = null;
      if (t)
        o = i[n + t];
      else if (e) {
        let r = "";
        for (const s of ["top", "bottom", "left", "right"])
          e[s] && (r += s);
        o = i[r];
      }
      return o;
    },
    defaultMargin: null
  }, Ar = Mt;
  _t.use(Ar);
  const Or = () => {
  }, Rr = () => {
  }, Hr = (e) => {
    const t = [["x", "y"], ["left", "top"], ["right", "bottom"], ["width", "height"]].filter(([i, o]) => i in e || o in e), n = (i, o) => {
      const {
        range: r,
        limits: s = {
          left: -1 / 0,
          right: 1 / 0,
          top: -1 / 0,
          bottom: 1 / 0
        },
        offset: a = {
          x: 0,
          y: 0
        }
      } = e, l = {
        range: r,
        grid: e,
        x: null,
        y: null
      };
      for (const [c, u] of t) {
        const f = Math.round((i - a.x) / e[c]), v = Math.round((o - a.y) / e[u]);
        l[c] = Math.max(s.left, Math.min(s.right, f * e[c] + a.x)), l[u] = Math.max(s.top, Math.min(s.bottom, v * e[u] + a.y));
      }
      return l;
    };
    return n.grid = e, n.coordFields = t, n;
  }, $r = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
    __proto__: null,
    edgeTarget: Or,
    elements: Rr,
    grid: Hr
  }, Symbol.toStringTag, { value: "Module" })), Br = {
    id: "snappers",
    install(e) {
      const {
        interactStatic: t
      } = e;
      t.snappers = D(t.snappers || {}, $r), t.createSnapGrid = t.snappers.grid;
    }
  }, Wr = Br;
  class Ei {
    constructor(t) {
      p(this, "states", []);
      p(this, "startOffset", {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0
      });
      p(this, "startDelta");
      p(this, "result");
      p(this, "endResult");
      p(this, "edges");
      p(this, "interaction");
      this.interaction = t, this.result = ve();
    }
    start({
      phase: t
    }, n) {
      const {
        interaction: i
      } = this, o = Lr(i);
      this.prepareStates(o), this.edges = D({}, i.edges), this.startOffset = Fr(i.rect, n), this.startDelta = {
        x: 0,
        y: 0
      };
      const r = this.fillArg({
        phase: t,
        pageCoords: n,
        preEnd: false
      });
      return this.result = ve(), this.startAll(r), this.result = this.setAll(r);
    }
    fillArg(t) {
      const {
        interaction: n
      } = this;
      return t.interaction = n, t.interactable = n.interactable, t.element = n.element, t.rect = t.rect || n.rect, t.edges = this.edges, t.startOffset = this.startOffset, t;
    }
    startAll(t) {
      for (const n of this.states)
        n.methods.start && (t.state = n, n.methods.start(t));
    }
    setAll(t) {
      const {
        phase: n,
        preEnd: i,
        skipModifiers: o,
        rect: r
      } = t;
      t.coords = D({}, t.pageCoords), t.rect = D({}, r);
      const s = o ? this.states.slice(o) : this.states, a = ve(t.coords, t.rect);
      for (const f of s) {
        var l;
        const {
          options: v
        } = f, y = D({}, t.coords);
        let x = null;
        (l = f.methods) != null && l.set && this.shouldDo(v, i, n) && (t.state = f, x = f.methods.set(t), on(this.interaction.edges, t.rect, {
          x: t.coords.x - y.x,
          y: t.coords.y - y.y
        })), a.eventProps.push(x);
      }
      a.delta.x = t.coords.x - t.pageCoords.x, a.delta.y = t.coords.y - t.pageCoords.y, a.rectDelta.left = t.rect.left - r.left, a.rectDelta.right = t.rect.right - r.right, a.rectDelta.top = t.rect.top - r.top, a.rectDelta.bottom = t.rect.bottom - r.bottom;
      const c = this.result.coords, u = this.result.rect;
      if (c && u) {
        const f = a.rect.left !== u.left || a.rect.right !== u.right || a.rect.top !== u.top || a.rect.bottom !== u.bottom;
        a.changed = f || c.x !== a.coords.x || c.y !== a.coords.y;
      }
      return a;
    }
    applyToInteraction(t) {
      const {
        interaction: n
      } = this, {
        phase: i
      } = t, o = n.coords.cur, r = n.coords.start, {
        result: s,
        startDelta: a
      } = this, l = s.delta;
      i === "start" && D(this.startDelta, s.delta);
      for (const [f, v] of [[r, a], [o, l]])
        f.page.x += v.x, f.page.y += v.y, f.client.x += v.x, f.client.y += v.y;
      const {
        rectDelta: c
      } = this.result, u = t.rect || n.rect;
      u.left += c.left, u.right += c.right, u.top += c.top, u.bottom += c.bottom, u.width = u.right - u.left, u.height = u.bottom - u.top;
    }
    setAndApply(t) {
      const {
        interaction: n
      } = this, {
        phase: i,
        preEnd: o,
        skipModifiers: r
      } = t, s = this.setAll(this.fillArg({
        preEnd: o,
        phase: i,
        pageCoords: t.modifiedCoords || n.coords.cur.page
      }));
      if (this.result = s, !s.changed && (!r || r < this.states.length) && n.interacting())
        return false;
      if (t.modifiedCoords) {
        const {
          page: a
        } = n.coords.cur, l = {
          x: t.modifiedCoords.x - a.x,
          y: t.modifiedCoords.y - a.y
        };
        s.coords.x += l.x, s.coords.y += l.y, s.delta.x += l.x, s.delta.y += l.y;
      }
      this.applyToInteraction(t);
    }
    beforeEnd(t) {
      const {
        interaction: n,
        event: i
      } = t, o = this.states;
      if (!o || !o.length)
        return;
      let r = false;
      for (const s of o) {
        t.state = s;
        const {
          options: a,
          methods: l
        } = s, c = l.beforeEnd && l.beforeEnd(t);
        if (c)
          return this.endResult = c, false;
        r = r || !r && this.shouldDo(a, true, t.phase, true);
      }
      r && n.move({
        event: i,
        preEnd: true
      });
    }
    stop(t) {
      const {
        interaction: n
      } = t;
      if (!this.states || !this.states.length)
        return;
      const i = D({
        states: this.states,
        interactable: n.interactable,
        element: n.element,
        rect: null
      }, t);
      this.fillArg(i);
      for (const o of this.states)
        i.state = o, o.methods.stop && o.methods.stop(i);
      this.states = null, this.endResult = null;
    }
    prepareStates(t) {
      this.states = [];
      for (let n = 0; n < t.length; n++) {
        const {
          options: i,
          methods: o,
          name: r
        } = t[n];
        this.states.push({
          options: i,
          methods: o,
          index: n,
          name: r
        });
      }
      return this.states;
    }
    restoreInteractionCoords({
      interaction: {
        coords: t,
        rect: n,
        modification: i
      }
    }) {
      if (!i.result)
        return;
      const {
        startDelta: o
      } = i, {
        delta: r,
        rectDelta: s
      } = i.result, a = [[t.start, o], [t.cur, r]];
      for (const [l, c] of a)
        l.page.x -= c.x, l.page.y -= c.y, l.client.x -= c.x, l.client.y -= c.y;
      n.left -= s.left, n.right -= s.right, n.top -= s.top, n.bottom -= s.bottom;
    }
    shouldDo(t, n, i, o) {
      return !(!t || t.enabled === false || o && !t.endOnly || t.endOnly && !n || i === "start" && !t.setStart);
    }
    copyFrom(t) {
      this.startOffset = t.startOffset, this.startDelta = t.startDelta, this.edges = t.edges, this.states = t.states.map((n) => Jt(n)), this.result = ve(D({}, t.result.coords), D({}, t.result.rect));
    }
    destroy() {
      for (const t in this)
        this[t] = null;
    }
  }
  function ve(e, t) {
    return {
      rect: t,
      coords: e,
      delta: {
        x: 0,
        y: 0
      },
      rectDelta: {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0
      },
      eventProps: [],
      changed: true
    };
  }
  function Lr(e) {
    const t = e.interactable.options[e.prepared.name], n = t.modifiers;
    return n && n.length ? n : ["snap", "snapSize", "snapEdges", "restrict", "restrictEdges", "restrictSize"].map((i) => {
      const o = t[i];
      return o && o.enabled && {
        options: o,
        methods: o._methods
      };
    }).filter((i) => !!i);
  }
  function Fr(e, t) {
    return e ? {
      left: t.x - e.left,
      top: t.y - e.top,
      right: e.right - t.x,
      bottom: e.bottom - t.y
    } : {
      left: 0,
      top: 0,
      right: 0,
      bottom: 0
    };
  }
  function Ht(e, t) {
    const {
      defaults: n
    } = e, i = {
      start: e.start,
      set: e.set,
      beforeEnd: e.beforeEnd,
      stop: e.stop
    }, o = (r) => {
      const s = r || {};
      s.enabled = s.enabled !== false;
      for (const l in n)
        l in s || (s[l] = n[l]);
      const a = {
        options: s,
        methods: i,
        name: t,
        enable: () => (s.enabled = true, a),
        disable: () => (s.enabled = false, a)
      };
      return a;
    };
    return t && typeof t == "string" && (o._defaults = n, o._methods = i), o;
  }
  function We({
    iEvent: e,
    interaction: t
  }) {
    const n = t.modification.result;
    n && (e.modifiers = n.eventProps);
  }
  const Nr = {
    id: "modifiers/base",
    before: ["actions"],
    install: (e) => {
      e.defaults.perAction.modifiers = [];
    },
    listeners: {
      "interactions:new": ({
        interaction: e
      }) => {
        e.modification = new Ei(e);
      },
      "interactions:before-action-start": (e) => {
        const t = e.interaction.modification;
        t.start(e, e.interaction.coords.start.page), e.interaction.edges = t.edges, t.applyToInteraction(e);
      },
      "interactions:before-action-move": (e) => e.interaction.modification.setAndApply(e),
      "interactions:before-action-end": (e) => e.interaction.modification.beforeEnd(e),
      "interactions:action-start": We,
      "interactions:action-move": We,
      "interactions:action-end": We,
      "interactions:after-action-start": (e) => e.interaction.modification.restoreInteractionCoords(e),
      "interactions:after-action-move": (e) => e.interaction.modification.restoreInteractionCoords(e),
      "interactions:stop": (e) => e.interaction.modification.stop(e)
    }
  }, jr = Nr, Yr = {
    start(e) {
      const {
        state: t,
        rect: n,
        edges: i,
        pageCoords: o
      } = e;
      let {
        ratio: r
      } = t.options;
      const {
        equalDelta: s,
        modifiers: a
      } = t.options;
      r === "preserve" && (r = n.width / n.height), t.startCoords = D({}, o), t.startRect = D({}, n), t.ratio = r, t.equalDelta = s;
      const l = t.linkedEdges = {
        top: i.top || i.left && !i.bottom,
        left: i.left || i.top && !i.right,
        bottom: i.bottom || i.right && !i.top,
        right: i.right || i.bottom && !i.left
      };
      if (t.xIsPrimaryAxis = !!(i.left || i.right), t.equalDelta) {
        const u = (l.left ? 1 : -1) * (l.top ? 1 : -1);
        t.edgeSign = {
          x: u,
          y: u
        };
      } else
        t.edgeSign = {
          x: l.left ? -1 : 1,
          y: l.top ? -1 : 1
        };
      if (D(e.edges, l), !a || !a.length)
        return;
      const c = new Ei(e.interaction);
      c.copyFrom(e.interaction.modification), c.prepareStates(a), t.subModification = c, c.startAll({
        ...e
      });
    },
    set(e) {
      const {
        state: t,
        rect: n,
        coords: i
      } = e, o = D({}, i), r = t.equalDelta ? Xr : Gr;
      if (r(t, t.xIsPrimaryAxis, i, n), !t.subModification)
        return null;
      const s = D({}, n);
      on(t.linkedEdges, s, {
        x: i.x - o.x,
        y: i.y - o.y
      });
      const a = t.subModification.setAll({
        ...e,
        rect: s,
        edges: t.linkedEdges,
        pageCoords: i,
        prevCoords: i,
        prevRect: s
      }), {
        delta: l
      } = a;
      if (a.changed) {
        const c = Math.abs(l.x) > Math.abs(l.y);
        r(t, c, a.coords, a.rect), D(i, a.coords);
      }
      return a.eventProps;
    },
    defaults: {
      ratio: "preserve",
      equalDelta: false,
      modifiers: [],
      enabled: false
    }
  };
  function Xr({
    startCoords: e,
    edgeSign: t
  }, n, i) {
    n ? i.y = e.y + (i.x - e.x) * t.y : i.x = e.x + (i.y - e.y) * t.x;
  }
  function Gr({
    startRect: e,
    startCoords: t,
    ratio: n,
    edgeSign: i
  }, o, r, s) {
    if (o) {
      const a = s.width / n;
      r.y = t.y + (a - e.height) * i.y;
    } else {
      const a = s.height * n;
      r.x = t.x + (a - e.width) * i.x;
    }
  }
  const qr = Ht(Yr, "aspectRatio"), Ii = () => {
  };
  Ii._defaults = {};
  const me = Ii;
  function Ur({
    rect: e,
    startOffset: t,
    state: n,
    interaction: i,
    pageCoords: o
  }) {
    const {
      options: r
    } = n, {
      elementRect: s
    } = r, a = D({
      left: 0,
      top: 0,
      right: 0,
      bottom: 0
    }, r.offset || {});
    if (e && s) {
      const l = jt(r.restriction, i, o);
      if (l) {
        const c = l.right - l.left - e.width, u = l.bottom - l.top - e.height;
        c < 0 && (a.left += c, a.right += c), u < 0 && (a.top += u, a.bottom += u);
      }
      a.left += t.left - e.width * s.left, a.top += t.top - e.height * s.top, a.right += t.right - e.width * (1 - s.right), a.bottom += t.bottom - e.height * (1 - s.bottom);
    }
    n.offset = a;
  }
  function Vr({
    coords: e,
    interaction: t,
    state: n
  }) {
    const {
      options: i,
      offset: o
    } = n, r = jt(i.restriction, t, e);
    if (!r)
      return;
    const s = xo(r);
    e.x = Math.max(Math.min(s.right - o.right, e.x), s.left + o.left), e.y = Math.max(Math.min(s.bottom - o.bottom, e.y), s.top + o.top);
  }
  function jt(e, t, n) {
    return g.func(e) ? ce(e, t.interactable, t.element, [n.x, n.y, t]) : ce(e, t.interactable, t.element);
  }
  const Kr = {
    restriction: null,
    elementRect: null,
    offset: null,
    endOnly: false,
    enabled: false
  }, we = {
    start: Ur,
    set: Vr,
    defaults: Kr
  }, Jr = Ht(we, "restrict"), zi = {
    top: 1 / 0,
    left: 1 / 0,
    bottom: -1 / 0,
    right: -1 / 0
  }, Ti = {
    top: -1 / 0,
    left: -1 / 0,
    bottom: 1 / 0,
    right: 1 / 0
  };
  function Zr({
    interaction: e,
    startOffset: t,
    state: n
  }) {
    const {
      options: i
    } = n;
    let o;
    if (i) {
      const r = jt(i.offset, e, e.coords.start.page);
      o = ze(r);
    }
    o = o || {
      x: 0,
      y: 0
    }, n.offset = {
      top: o.y + t.top,
      left: o.x + t.left,
      bottom: o.y - t.bottom,
      right: o.x - t.right
    };
  }
  function Qr({
    coords: e,
    edges: t,
    interaction: n,
    state: i
  }) {
    const {
      offset: o,
      options: r
    } = i;
    if (!t)
      return;
    const s = D({}, e), a = jt(r.inner, n, s) || {}, l = jt(r.outer, n, s) || {};
    An(a, zi), An(l, Ti), t.top ? e.y = Math.min(Math.max(l.top + o.top, s.y), a.top + o.top) : t.bottom && (e.y = Math.max(Math.min(l.bottom + o.bottom, s.y), a.bottom + o.bottom)), t.left ? e.x = Math.min(Math.max(l.left + o.left, s.x), a.left + o.left) : t.right && (e.x = Math.max(Math.min(l.right + o.right, s.x), a.right + o.right));
  }
  function An(e, t) {
    for (const n of ["top", "left", "bottom", "right"])
      n in e || (e[n] = t[n]);
    return e;
  }
  const ts = {
    inner: null,
    outer: null,
    offset: null,
    endOnly: false,
    enabled: false
  }, le = {
    noInner: zi,
    noOuter: Ti,
    start: Zr,
    set: Qr,
    defaults: ts
  }, es = Ht(le, "restrictEdges"), ns = D({
    get elementRect() {
      return {
        top: 0,
        left: 0,
        bottom: 1,
        right: 1
      };
    },
    set elementRect(e) {
    }
  }, we.defaults), is = {
    start: we.start,
    set: we.set,
    defaults: ns
  }, os = Ht(is, "restrictRect"), rs = {
    width: -1 / 0,
    height: -1 / 0
  }, ss = {
    width: 1 / 0,
    height: 1 / 0
  };
  function as(e) {
    return le.start(e);
  }
  function ls(e) {
    const {
      interaction: t,
      state: n,
      rect: i,
      edges: o
    } = e, {
      options: r
    } = n;
    if (!o)
      return;
    const s = zn(jt(r.min, t, e.coords)) || rs, a = zn(jt(r.max, t, e.coords)) || ss;
    n.options = {
      endOnly: r.endOnly,
      inner: D({}, le.noInner),
      outer: D({}, le.noOuter)
    }, o.top ? (n.options.inner.top = i.bottom - s.height, n.options.outer.top = i.bottom - a.height) : o.bottom && (n.options.inner.bottom = i.top + s.height, n.options.outer.bottom = i.top + a.height), o.left ? (n.options.inner.left = i.right - s.width, n.options.outer.left = i.right - a.width) : o.right && (n.options.inner.right = i.left + s.width, n.options.outer.right = i.left + a.width), le.set(e), n.options = r;
  }
  const cs = {
    min: null,
    max: null,
    endOnly: false,
    enabled: false
  }, us = {
    start: as,
    set: ls,
    defaults: cs
  }, fs = Ht(us, "restrictSize");
  function ds(e) {
    const {
      interaction: t,
      interactable: n,
      element: i,
      rect: o,
      state: r,
      startOffset: s
    } = e, {
      options: a
    } = r, l = a.offsetWithOrigin ? ps(e) : {
      x: 0,
      y: 0
    };
    let c;
    if (a.offset === "startCoords")
      c = {
        x: t.coords.start.page.x,
        y: t.coords.start.page.y
      };
    else {
      const f = ce(a.offset, n, i, [t]);
      c = ze(f) || {
        x: 0,
        y: 0
      }, c.x += l.x, c.y += l.y;
    }
    const {
      relativePoints: u
    } = a;
    r.offsets = o && u && u.length ? u.map((f, v) => ({
      index: v,
      relativePoint: f,
      x: s.left - o.width * f.x + c.x,
      y: s.top - o.height * f.y + c.y
    })) : [{
      index: 0,
      relativePoint: null,
      x: c.x,
      y: c.y
    }];
  }
  function hs(e) {
    const {
      interaction: t,
      coords: n,
      state: i
    } = e, {
      options: o,
      offsets: r
    } = i, s = rn(t.interactable, t.element, t.prepared.name), a = D({}, n), l = [];
    o.offsetWithOrigin || (a.x -= s.x, a.y -= s.y);
    for (const u of r) {
      const f = a.x - u.x, v = a.y - u.y;
      for (let y = 0, x = o.targets.length; y < x; y++) {
        const S = o.targets[y];
        let z;
        g.func(S) ? z = S(f, v, t._proxy, u, y) : z = S, z && l.push({
          x: (g.number(z.x) ? z.x : f) + u.x,
          y: (g.number(z.y) ? z.y : v) + u.y,
          range: g.number(z.range) ? z.range : o.range,
          source: S,
          index: y,
          offset: u
        });
      }
    }
    const c = {
      target: null,
      inRange: false,
      distance: 0,
      range: 0,
      delta: {
        x: 0,
        y: 0
      }
    };
    for (const u of l) {
      const f = u.range, v = u.x - a.x, y = u.y - a.y, x = Te(v, y);
      let S = x <= f;
      f === 1 / 0 && c.inRange && c.range !== 1 / 0 && (S = false), (!c.target || (S ? c.inRange && f !== 1 / 0 ? x / f < c.distance / c.range : f === 1 / 0 && c.range !== 1 / 0 || x < c.distance : !c.inRange && x < c.distance)) && (c.target = u, c.distance = x, c.range = f, c.inRange = S, c.delta.x = v, c.delta.y = y);
    }
    return c.inRange && (n.x = c.target.x, n.y = c.target.y), i.closest = c, c;
  }
  function ps(e) {
    const {
      element: t
    } = e.interaction;
    return ze(ce(e.state.options.origin, null, null, [t])) || rn(e.interactable, t, e.interaction.prepared.name);
  }
  const gs = {
    range: 1 / 0,
    targets: null,
    offset: null,
    offsetWithOrigin: true,
    origin: null,
    relativePoints: null,
    endOnly: false,
    enabled: false
  }, cn = {
    start: ds,
    set: hs,
    defaults: gs
  }, vs = Ht(cn, "snap");
  function ms(e) {
    const {
      state: t,
      edges: n
    } = e, {
      options: i
    } = t;
    if (!n)
      return null;
    e.state = {
      options: {
        targets: null,
        relativePoints: [{
          x: n.left ? 0 : 1,
          y: n.top ? 0 : 1
        }],
        offset: i.offset || "self",
        origin: {
          x: 0,
          y: 0
        },
        range: i.range
      }
    }, t.targetFields = t.targetFields || [["width", "height"], ["x", "y"]], cn.start(e), t.offsets = e.state.offsets, e.state = t;
  }
  function ys(e) {
    const {
      interaction: t,
      state: n,
      coords: i
    } = e, {
      options: o,
      offsets: r
    } = n, s = {
      x: i.x - r[0].x,
      y: i.y - r[0].y
    };
    n.options = D({}, o), n.options.targets = [];
    for (const l of o.targets || []) {
      let c;
      if (g.func(l) ? c = l(s.x, s.y, t) : c = l, !!c) {
        for (const [u, f] of n.targetFields)
          if (u in c || f in c) {
            c.x = c[u], c.y = c[f];
            break;
          }
        n.options.targets.push(c);
      }
    }
    const a = cn.set(e);
    return n.options = o, a;
  }
  const bs = {
    range: 1 / 0,
    targets: null,
    offset: null,
    endOnly: false,
    enabled: false
  }, Se = {
    start: ms,
    set: ys,
    defaults: bs
  }, xs = Ht(Se, "snapSize");
  function ws(e) {
    const {
      edges: t
    } = e;
    return t ? (e.state.targetFields = e.state.targetFields || [[t.left ? "left" : "right", t.top ? "top" : "bottom"]], Se.start(e)) : null;
  }
  const Ss = {
    start: ws,
    set: Se.set,
    defaults: D(Jt(Se.defaults), {
      targets: null,
      range: null,
      offset: {
        x: 0,
        y: 0
      }
    })
  }, Es = Ht(Ss, "snapEdges"), Le = {
    aspectRatio: qr,
    restrictEdges: es,
    restrict: Jr,
    restrictRect: os,
    restrictSize: fs,
    snapEdges: Es,
    snap: vs,
    snapSize: xs,
    spring: me,
    avoid: me,
    transform: me,
    rubberband: me
  }, Is = {
    id: "modifiers",
    install(e) {
      const {
        interactStatic: t
      } = e;
      e.usePlugin(jr), e.usePlugin(Wr), t.modifiers = Le;
      for (const n in Le) {
        const {
          _defaults: i,
          _methods: o
        } = Le[n];
        i._methods = o, e.defaults.perAction[n] = i;
      }
    }
  }, zs = Is;
  _t.use(zs);
  const Ts = {};
  var Kt;
  (function(e) {
    e.touchAction = "touchAction", e.boxSizing = "boxSizing", e.noListeners = "noListeners";
  })(Kt || (Kt = {}));
  const On = "[interact.js] ", tn = {
    touchAction: "https://developer.mozilla.org/en-US/docs/Web/CSS/touch-action",
    boxSizing: "https://developer.mozilla.org/en-US/docs/Web/CSS/box-sizing"
  };
  function _s(e, {
    logger: t
  } = {}) {
    const {
      Interactable: n,
      defaults: i
    } = e;
    e.logger = t || console, i.base.devTools = {
      ignore: {}
    }, n.prototype.devTools = function(o) {
      return o ? (D(this.options.devTools, o), this) : this.options.devTools;
    }, e.usePlugin(Ts);
  }
  const Rn = [{
    name: Kt.touchAction,
    perform({
      element: e
    }) {
      return !Cs(e, "touchAction", /pan-|pinch|none/);
    },
    getInfo({
      element: e
    }) {
      return [e, tn.touchAction];
    },
    text: `Consider adding CSS "touch-action: none" to this element
`
  }, {
    name: Kt.boxSizing,
    perform(e) {
      const {
        element: t
      } = e;
      return e.prepared.name === "resize" && t instanceof ut.HTMLElement && !Mi(t, "boxSizing", /border-box/);
    },
    text: 'Consider adding CSS "box-sizing: border-box" to this resizable element',
    getInfo({
      element: e
    }) {
      return [e, tn.boxSizing];
    }
  }, {
    name: Kt.noListeners,
    perform(e) {
      const t = e.prepared.name;
      return !(e.interactable.events.types[`${t}move`] || []).length;
    },
    getInfo(e) {
      return [e.prepared.name, e.interactable];
    },
    text: "There are no listeners set for this action"
  }];
  function Mi(e, t, n) {
    const i = e.style[t] || Ot.getComputedStyle(e)[t];
    return n.test((i || "").toString());
  }
  function Cs(e, t, n) {
    let i = e;
    for (; g.element(i); ) {
      if (Mi(i, t, n))
        return true;
      i = Rt(i);
    }
    return false;
  }
  const Hn = "dev-tools", Ds = {
    id: Hn,
    install: _s,
    listeners: {
      "interactions:action-start": ({
        interaction: e
      }, t) => {
        for (const n of Rn) {
          const i = e.interactable && e.interactable.options;
          !(i && i.devTools && i.devTools.ignore[n.name]) && n.perform(e) && t.logger.warn(On + n.text, ...n.getInfo(e));
        }
      }
    },
    checks: Rn,
    CheckName: Kt,
    links: tn,
    prefix: On
  }, Ps = Ds;
  _t.use(Ps);
  function ks() {
    const { appContext: e, proxy: t } = vue.getCurrentInstance(), n = e.config.globalProperties;
    return {
      proxy: t,
      appContext: e,
      globalProperties: n
    };
  }
  const As = {
    name: "GridItem"
  }, _i = /* @__PURE__ */ vue.defineComponent({
    ...As,
    props: {
      isDraggable: { type: [Boolean, null], default: null },
      isResizable: { type: [Boolean, null], default: null },
      isBounded: { type: [Boolean, null], default: null },
      static: { type: Boolean, default: false },
      minH: { default: 1 },
      minW: { default: 1 },
      maxH: { default: 1 / 0 },
      maxW: { default: 1 / 0 },
      x: null,
      y: null,
      w: null,
      h: null,
      i: null,
      dragIgnoreFrom: { default: "a, button" },
      dragAllowFrom: { default: null },
      resizeIgnoreFrom: { default: "a, button" },
      preserveAspectRatio: { type: Boolean, default: false },
      dragOption: { default: () => ({}) },
      resizeOption: { default: () => ({}) }
    },
    emits: ["container-resized", "resize", "resized", "move", "moved"],
    setup(e, { expose: t, emit: n }) {
      const i = e, { proxy: o } = ks(), r = o == null ? void 0 : o.$parent, s = vue.inject("eventBus"), a = vue.ref({}), l = vue.ref(1), c = vue.ref(100), u = vue.ref(30), f = vue.ref([10, 10]), v = vue.ref(1 / 0), y = vue.ref(null), x = vue.ref(null), S = vue.ref(1), z = vue.ref(true), H = vue.ref(true), T = vue.ref(false), _ = vue.ref(null), m = vue.ref(false), d = vue.ref(null), R = vue.ref(NaN), w = vue.ref(NaN), N = vue.ref(NaN), K = vue.ref(NaN), A = vue.ref({}), J = vue.ref(false), b = vue.ref(false), C = vue.ref(false), B = vue.ref(null), Y = vue.ref(null), V = vue.ref(null), Z = vue.ref(null), M = vue.ref(i.x), Q = vue.ref(i.y), it = vue.ref(i.w), tt = vue.ref(i.h), st = vue.ref(null), G = vue.ref(null), fe = vue.computed(() => x.value && !i.static), _e = vue.computed(() => (y.value || x.value) && !i.static), Ce = vue.computed(() => navigator.userAgent.toLowerCase().indexOf("android") !== -1), ct = vue.computed(() => r != null && r.isMirrored ? !J.value : J.value), de = vue.computed(() => ({
        "vue-resizable": fe.value,
        static: i.static,
        resizing: m.value,
        "vue-draggable-dragging": T.value,
        cssTransforms: z.value,
        "render-rtl": ct.value,
        "disable-userselect": T.value,
        "no-touch": Ce.value && _e.value
      })), I = vue.computed(() => ct.value ? "vue-resizable-handle vue-rtl-resizable-handle" : "vue-resizable-handle");
      vue.watch(
        () => i.isDraggable,
        (h) => {
          y.value = h;
        }
      ), vue.watch(
        () => i.static,
        () => {
          pe(), lt();
        }
      ), vue.watch(y, () => {
        pe();
      }), vue.watch(
        () => i.isResizable,
        (h) => {
          x.value = h;
        }
      ), vue.watch(
        () => i.isBounded,
        (h) => {
          st.value = h;
        }
      ), vue.watch(x, () => {
        lt();
      }), vue.watch(u, () => {
        et(), dt();
      }), vue.watch(l, () => {
        lt(), et(), dt();
      }), vue.watch(c, () => {
        lt(), et();
      }), vue.watch(
        () => i.x,
        (h) => {
          M.value = h, et();
        }
      ), vue.watch(
        () => i.y,
        (h) => {
          Q.value = h, et();
        }
      ), vue.watch(
        () => i.h,
        (h) => {
          tt.value = h, et();
        }
      ), vue.watch(
        () => i.w,
        (h) => {
          it.value = h, et();
        }
      ), vue.watch(ct, () => {
        lt(), et();
      }), vue.watch(
        () => i.minH,
        () => {
          lt();
        }
      ), vue.watch(
        () => i.maxH,
        () => {
          lt();
        }
      ), vue.watch(
        () => i.minW,
        () => {
          lt();
        }
      ), vue.watch(
        () => i.maxW,
        () => {
          lt();
        }
      ), vue.watch(
        () => r == null ? void 0 : r.margin,
        (h) => {
          !h || h[0] == f.value[0] && h[1] == f.value[1] || (f.value = h.map((E) => Number(E)), et(), dt());
        }
      );
      function $(h) {
        Dt(h);
      }
      function q(h) {
        wt();
      }
      function ft(h) {
        i.isDraggable === null && (y.value = h);
      }
      function yt(h) {
        i.isResizable === null && (x.value = h);
      }
      function St(h) {
        i.isBounded === null && (st.value = h);
      }
      function Et(h) {
        S.value = h;
      }
      function rt(h) {
        u.value = h;
      }
      function W(h) {
        v.value = h;
      }
      function at() {
        J.value = bn() === "rtl", wt();
      }
      function bt(h) {
        const E = h.toString();
        l.value = parseInt(E);
      }
      s.on("updateWidth", $), s.on("compact", q), s.on("setDraggable", ft), s.on("setResizable", yt), s.on("setBounded", St), s.on("setTransformScale", Et), s.on("setRowHeight", rt), s.on("setMaxRows", W), s.on("directionchange", at), s.on("setColNum", bt), J.value = bn() === "rtl", vue.onBeforeUnmount(() => {
        s.off("updateWidth", $), s.off("compact", q), s.off("setDraggable", ft), s.off("setResizable", yt), s.off("setBounded", St), s.off("setTransformScale", Et), s.off("setRowHeight", rt), s.off("setMaxRows", W), s.off("directionchange", at), s.off("setColNum", bt), G.value && G.value.unset();
      }), vue.onMounted(() => {
        (r == null ? void 0 : r.responsive) && r.lastBreakpoint ? l.value = Ge(r.lastBreakpoint, r == null ? void 0 : r.cols) : l.value = r == null ? void 0 : r.colNum, u.value = r == null ? void 0 : r.rowHeight, c.value = (r == null ? void 0 : r.width) !== null ? r == null ? void 0 : r.width : 100, f.value = (r == null ? void 0 : r.margin) !== void 0 ? r.margin : [10, 10], v.value = r == null ? void 0 : r.maxRows, i.isDraggable === null ? y.value = r == null ? void 0 : r.isDraggable : y.value = i.isDraggable, i.isResizable === null ? x.value = r == null ? void 0 : r.isResizable : x.value = i.isResizable, i.isBounded === null ? st.value = r == null ? void 0 : r.isBounded : st.value = i.isBounded, S.value = r == null ? void 0 : r.transformScale, z.value = r == null ? void 0 : r.useCssTransforms, H.value = r == null ? void 0 : r.useStyleCursor, et();
      });
      function et() {
        var L, X, O, U, Bt;
        i.x + i.w > l.value ? (M.value = 0, it.value = i.w > l.value ? l.value : i.w) : (M.value = i.x, it.value = i.w);
        let h = xt(M.value, Q.value, it.value, tt.value);
        T.value && (h.top = (L = _.value) == null ? void 0 : L.top, ct.value ? h.right = (X = _.value) == null ? void 0 : X.left : h.left = (O = _.value) == null ? void 0 : O.left), m.value && (h.width = (U = d.value) == null ? void 0 : U.width, h.height = (Bt = d.value) == null ? void 0 : Bt.height);
        let E;
        z.value ? ct.value ? E = Ui(h.top, h.right, h.width, h.height) : E = qi(h.top, h.left, h.width, h.height) : ct.value ? E = Ki(h.top, h.right, h.width, h.height) : E = Vi(h.top, h.left, h.width, h.height), A.value = E;
      }
      function dt() {
        let h = {};
        for (let E of ["width", "height"]) {
          let X = A.value[E].match(/^(\d+)px$/);
          if (!X)
            return;
          h[E] = X[1];
        }
        n("container-resized", i.i, i.h, i.w, h.height, h.width);
      }
      function Ct(h) {
        var E, L, X;
        {
          if (i.static)
            return;
          const O = mn(h);
          if (O == null)
            return;
          const { x: U, y: Bt } = O, ot = { width: 0, height: 0 };
          let j;
          switch (h.type) {
            case "resizestart": {
              lt(), B.value = it.value, Y.value = tt.value, j = xt(M.value, Q.value, it.value, tt.value), ot.width = j.width, ot.height = j.height, d.value = ot, m.value = true;
              break;
            }
            case "resizemove": {
              const ht = yn(N.value, K.value, U, Bt);
              ct.value ? ot.width = Number((E = d.value) == null ? void 0 : E.width) - ht.deltaX / S.value : ot.width = Number((L = d.value) == null ? void 0 : L.width) + ht.deltaX / S.value, ot.height = Number((X = d.value) == null ? void 0 : X.height) + ht.deltaY / S.value, d.value = ot;
              break;
            }
            case "resizeend": {
              j = xt(M.value, Q.value, it.value, tt.value), ot.width = j.width, ot.height = j.height, d.value = null, m.value = false;
              break;
            }
          }
          j = pt(ot.height, ot.width), j.w < i.minW && (j.w = i.minW), j.w > i.maxW && (j.w = i.maxW), j.h < i.minH && (j.h = i.minH), j.h > i.maxH && (j.h = i.maxH), j.h < 1 && (j.h = 1), j.w < 1 && (j.w = 1), N.value = U, K.value = Bt, (it.value !== j.w || tt.value !== j.h) && n("resize", i.i, j.h, j.w, ot.height, ot.width), h.type === "resizeend" && (B.value !== it.value || Y.value !== tt.value) && n("resized", i.i, j.h, j.w, ot.height, ot.width);
          const ge = {
            eventType: h.type,
            i: i.i,
            x: M.value,
            y: Q.value,
            h: j.h,
            w: j.w
          };
          s.emit("resizeEvent", ge);
        }
      }
      function he(h) {
        var ot, j, ge;
        if (i.static || m.value)
          return;
        const E = mn(h);
        if (E === null)
          return;
        const { x: L, y: X } = E;
        let O = { top: 0, left: 0 };
        switch (h.type) {
          case "dragstart": {
            V.value = M.value, Z.value = Q.value;
            const ht = h.target;
            let Pt = ht.offsetParent.getBoundingClientRect(), It = ht.getBoundingClientRect();
            const ee = It.left / S.value, ne = Pt.left / S.value, De = It.right / S.value, Pe = Pt.right / S.value, ke = It.top / S.value, Ae = Pt.top / S.value;
            ct.value ? O.left = (De - Pe) * -1 : O.left = ee - ne, O.top = ke - Ae, _.value = O, T.value = true;
            break;
          }
          case "dragend": {
            if (!T.value)
              return;
            const ht = h.target;
            let Pt = ht.offsetParent.getBoundingClientRect(), It = ht.getBoundingClientRect();
            const ee = It.left / S.value, ne = Pt.left / S.value, De = It.right / S.value, Pe = Pt.right / S.value, ke = It.top / S.value, Ae = Pt.top / S.value;
            ct.value ? O.left = (De - Pe) * -1 : O.left = ee - ne, O.top = ke - Ae, _.value = null, T.value = false;
            break;
          }
          case "dragmove": {
            const ht = yn(R.value, w.value, L, X);
            if (ct.value ? O.left = Number((ot = _.value) == null ? void 0 : ot.left) - ht.deltaX / S.value : O.left = Number((j = _.value) == null ? void 0 : j.left) + ht.deltaX / S.value, O.top = Number((ge = _.value) == null ? void 0 : ge.top) + ht.deltaY / S.value, st.value) {
              const It = h.target.offsetParent.clientHeight - Zt(i.h, u.value, f.value[1]);
              O.top = nt(O.top, 0, It);
              const ee = $t(), ne = c.value - Zt(i.w, ee, f.value[0]);
              O.left = nt(O.left, 0, ne);
            }
            _.value = O;
            break;
          }
        }
        let U;
        ct.value, U = Yt(O.top, O.left), R.value = L, w.value = X, (M.value !== U.x || Q.value !== U.y) && n("move", i.i, U.x, U.y), h.type === "dragend" && (V.value !== M.value || Z.value !== Q.value) && n("moved", i.i, U.x, U.y);
        const Bt = {
          eventType: h.type,
          i: i.i,
          x: U.x,
          y: U.y,
          h: tt.value,
          w: it.value
        };
        s.emit("dragEvent", Bt);
      }
      function xt(h, E, L, X) {
        const O = $t();
        let U;
        return ct.value ? U = {
          right: Math.round(O * h + (h + 1) * f.value[0]),
          top: Math.round(u.value * E + (E + 1) * f.value[1]),
          width: L === 1 / 0 ? L : Math.round(O * L + Math.max(0, L - 1) * f.value[0]),
          height: X === 1 / 0 ? X : Math.round(u.value * X + Math.max(0, X - 1) * f.value[1])
        } : U = {
          left: Math.round(O * h + (h + 1) * f.value[0]),
          top: Math.round(u.value * E + (E + 1) * f.value[1]),
          width: L === 1 / 0 ? L : Math.round(O * L + Math.max(0, L - 1) * f.value[0]),
          height: X === 1 / 0 ? X : Math.round(u.value * X + Math.max(0, X - 1) * f.value[1])
        }, U;
      }
      function Yt(h, E) {
        const L = $t();
        let X = Math.round((E - f.value[0]) / (L + f.value[0])), O = Math.round((h - f.value[1]) / (u.value + f.value[1]));
        return X = Math.max(Math.min(X, l.value - it.value), 0), O = Math.max(Math.min(O, v.value - tt.value), 0), { x: X, y: O };
      }
      function $t() {
        return (c.value - f.value[0] * (l.value + 1)) / l.value;
      }
      function Zt(h, E, L) {
        return Number.isFinite(h) ? Math.round(E * h + Math.max(0, h - 1) * L) : h;
      }
      function nt(h, E, L) {
        return Math.max(Math.min(h, L), E);
      }
      function pt(h, E, L = false) {
        const X = $t();
        let O = Math.round((E + f.value[0]) / (X + f.value[0])), U = 0;
        return L ? U = Math.ceil((h + f.value[1]) / (u.value + f.value[1])) : U = Math.round((h + f.value[1]) / (u.value + f.value[1])), O = Math.max(Math.min(O, l.value - M.value), 0), U = Math.max(Math.min(U, v.value - Q.value), 0), { w: O, h: U };
      }
      function Dt(h, E) {
        c.value = h, E != null && (l.value = E);
      }
      function wt(h) {
        et();
      }
      function pe() {
        if ((G.value === null || G.value === void 0) && (G.value = _t(a.value), H.value || G.value.styleCursor(false)), y.value && !i.static) {
          const h = {
            ignoreFrom: i.dragIgnoreFrom,
            allowFrom: i.dragAllowFrom,
            ...i.dragOption
          };
          G.value.draggable(h), b.value || (b.value = true, G.value.on("dragstart dragmove dragend", function(E) {
            he(E);
          }));
        } else
          G.value.draggable({
            enabled: false
          });
      }
      function lt() {
        if ((G.value === null || G.value === void 0) && (G.value = _t(a.value), H.value || G.value.styleCursor(false)), x.value && !i.static) {
          let h = xt(0, 0, i.maxW, i.maxH), E = xt(0, 0, i.minW, i.minH);
          const L = {
            edges: {
              left: false,
              right: "." + I.value.trim().replace(" ", "."),
              bottom: "." + I.value.trim().replace(" ", "."),
              top: false
            },
            ignoreFrom: i.resizeIgnoreFrom,
            restrictSize: {
              min: {
                height: E.height * S.value,
                width: E.width * S.value
              },
              max: {
                height: h.height * S.value,
                width: h.width * S.value
              }
            },
            ...i.resizeOption
          };
          i.preserveAspectRatio && (L.modifiers = [
            _t.modifiers.aspectRatio({
              ratio: "preserve"
            })
          ]), G.value.resizable(L), C.value || (C.value = true, G.value.on("resizestart resizemove resizeend", function(X) {
            Ct(X);
          }));
        } else
          G.value.resizable({
            enabled: false
          });
      }
      const Qt = vue.useSlots();
      function te() {
        B.value = it.value, Y.value = tt.value;
        let h = Qt == null ? void 0 : Qt.default[0].elm.getBoundingClientRect(), E = pt(h.height, h.width, true);
        if (E.w < i.minW && (E.w = i.minW), E.w > i.maxW && (E.w = i.maxW), E.h < i.minH && (E.h = i.minH), E.h > i.maxH && (E.h = i.maxH), E.h < 1 && (E.h = 1), E.w < 1 && (E.w = 1), (it.value !== E.w || tt.value !== E.h) && n("resize", i.i, E.h, E.w, h.height, h.width), B.value !== E.w || Y.value !== E.h) {
          n("resized", i.i, E.h, E.w, h.height, h.width);
          const L = {
            eventType: "resizeend",
            i: i.i,
            x: M.value,
            y: Q.value,
            h: E.h,
            w: E.w
          };
          s.emit("resizeEvent", L);
        }
      }
      return t({
        autoSize: te,
        calcXY: Yt,
        dragging: _,
        ...i
      }), (h, E) => (vue.openBlock(), vue.createElementBlock("div", {
        ref_key: "this$refsItem",
        ref: a,
        class: vue.normalizeClass(["vue-grid-item", vue.unref(de)]),
        style: vue.normalizeStyle(A.value)
      }, [
        vue.renderSlot(h.$slots, "default", {
          style: vue.normalizeStyle(A.value)
        }),
        vue.unref(fe) ? (vue.openBlock(), vue.createElementBlock("span", {
          key: 0,
          ref: "handle",
          class: vue.normalizeClass(vue.unref(I))
        }, null, 2)) : vue.createCommentVNode("", true)
      ], 6));
    }
  });
  function Os(e) {
    return { all: e = e || /* @__PURE__ */ new Map(), on: function(t, n) {
      var i = e.get(t);
      i ? i.push(n) : e.set(t, [n]);
    }, off: function(t, n) {
      var i = e.get(t);
      i && (n ? i.splice(i.indexOf(n) >>> 0, 1) : e.set(t, []));
    }, emit: function(t, n) {
      var i = e.get(t);
      i && i.slice().map(function(o) {
        o(n);
      }), (i = e.get("*")) && i.slice().map(function(o) {
        o(t, n);
      });
    } };
  }
  var un = { exports: {} }, Rs = un.exports = {};
  Rs.forEach = function(e, t) {
    for (var n = 0; n < e.length; n++) {
      var i = t(e[n]);
      if (i)
        return i;
    }
  };
  var Hs = function(e) {
    var t = e.stateHandler.getState;
    function n(s) {
      var a = t(s);
      return a && !!a.isDetectable;
    }
    function i(s) {
      t(s).isDetectable = true;
    }
    function o(s) {
      return !!t(s).busy;
    }
    function r(s, a) {
      t(s).busy = !!a;
    }
    return {
      isDetectable: n,
      markAsDetectable: i,
      isBusy: o,
      markBusy: r
    };
  }, $s = function(e) {
    var t = {};
    function n(s) {
      var a = e.get(s);
      return a === void 0 ? [] : t[a] || [];
    }
    function i(s, a) {
      var l = e.get(s);
      t[l] || (t[l] = []), t[l].push(a);
    }
    function o(s, a) {
      for (var l = n(s), c = 0, u = l.length; c < u; ++c)
        if (l[c] === a) {
          l.splice(c, 1);
          break;
        }
    }
    function r(s) {
      var a = n(s);
      !a || (a.length = 0);
    }
    return {
      get: n,
      add: i,
      removeListener: o,
      removeAllListeners: r
    };
  }, Bs = function() {
    var e = 1;
    function t() {
      return e++;
    }
    return {
      generate: t
    };
  }, Ws = function(e) {
    var t = e.idGenerator, n = e.stateHandler.getState;
    function i(r) {
      var s = n(r);
      return s && s.id !== void 0 ? s.id : null;
    }
    function o(r) {
      var s = n(r);
      if (!s)
        throw new Error("setId required the element to have a resize detection state.");
      var a = t.generate();
      return s.id = a, a;
    }
    return {
      get: i,
      set: o
    };
  }, Ls = function(e) {
    function t() {
    }
    var n = {
      log: t,
      warn: t,
      error: t
    };
    if (!e && window.console) {
      var i = function(o, r) {
        o[r] = function() {
          var a = console[r];
          if (a.apply)
            a.apply(console, arguments);
          else
            for (var l = 0; l < arguments.length; l++)
              a(arguments[l]);
        };
      };
      i(n, "log"), i(n, "warn"), i(n, "error");
    }
    return n;
  }, fn = { exports: {} }, Ci = fn.exports = {};
  Ci.isIE = function(e) {
    function t() {
      var i = navigator.userAgent.toLowerCase();
      return i.indexOf("msie") !== -1 || i.indexOf("trident") !== -1 || i.indexOf(" edge/") !== -1;
    }
    if (!t())
      return false;
    if (!e)
      return true;
    var n = function() {
      var i, o = 3, r = document.createElement("div"), s = r.getElementsByTagName("i");
      do
        r.innerHTML = "<!--[if gt IE " + ++o + "]><i></i><![endif]-->";
      while (s[0]);
      return o > 4 ? o : i;
    }();
    return e === n;
  };
  Ci.isLegacyOpera = function() {
    return !!window.opera;
  };
  var Di = { exports: {} }, Fs = Di.exports = {};
  Fs.getOption = Ns;
  function Ns(e, t, n) {
    var i = e[t];
    return i == null && n !== void 0 ? n : i;
  }
  var $n = Di.exports, js = function(t) {
    t = t || {};
    var n = t.reporter, i = $n.getOption(t, "async", true), o = $n.getOption(t, "auto", true);
    o && !i && (n && n.warn("Invalid options combination. auto=true and async=false is invalid. Setting async=true."), i = true);
    var r = Bn(), s, a = false;
    function l(x, S) {
      !a && o && i && r.size() === 0 && f(), r.add(x, S);
    }
    function c() {
      for (a = true; r.size(); ) {
        var x = r;
        r = Bn(), x.process();
      }
      a = false;
    }
    function u(x) {
      a || (x === void 0 && (x = i), s && (v(s), s = null), x ? f() : c());
    }
    function f() {
      s = y(c);
    }
    function v(x) {
      var S = clearTimeout;
      return S(x);
    }
    function y(x) {
      var S = function(z) {
        return setTimeout(z, 0);
      };
      return S(x);
    }
    return {
      add: l,
      force: u
    };
  };
  function Bn() {
    var e = {}, t = 0, n = 0, i = 0;
    function o(a, l) {
      l || (l = a, a = 0), a > n ? n = a : a < i && (i = a), e[a] || (e[a] = []), e[a].push(l), t++;
    }
    function r() {
      for (var a = i; a <= n; a++)
        for (var l = e[a], c = 0; c < l.length; c++) {
          var u = l[c];
          u();
        }
    }
    function s() {
      return t;
    }
    return {
      add: o,
      process: r,
      size: s
    };
  }
  var dn = "_erd";
  function Ys(e) {
    return e[dn] = {}, Pi(e);
  }
  function Pi(e) {
    return e[dn];
  }
  function Xs(e) {
    delete e[dn];
  }
  var Gs = {
    initState: Ys,
    getState: Pi,
    cleanState: Xs
  }, re = fn.exports, qs = function(e) {
    e = e || {};
    var t = e.reporter, n = e.batchProcessor, i = e.stateHandler.getState;
    if (!t)
      throw new Error("Missing required dependency: reporter.");
    function o(c, u) {
      function f() {
        u(c);
      }
      if (re.isIE(8))
        i(c).object = {
          proxy: f
        }, c.attachEvent("onresize", f);
      else {
        var v = a(c);
        if (!v)
          throw new Error("Element is not detectable by this strategy.");
        v.contentDocument.defaultView.addEventListener("resize", f);
      }
    }
    function r(c) {
      var u = e.important ? " !important; " : "; ";
      return (c.join(u) + u).trim();
    }
    function s(c, u, f) {
      f || (f = u, u = c, c = null), c = c || {}, c.debug;
      function v(y, x) {
        var S = r(["display: block", "position: absolute", "top: 0", "left: 0", "width: 100%", "height: 100%", "border: none", "padding: 0", "margin: 0", "opacity: 0", "z-index: -1000", "pointer-events: none"]), z = false, H = window.getComputedStyle(y), T = y.offsetWidth, _ = y.offsetHeight;
        i(y).startSize = {
          width: T,
          height: _
        };
        function m() {
          function d() {
            if (H.position === "static") {
              y.style.setProperty("position", "relative", c.important ? "important" : "");
              var N = function(K, A, J, b) {
                function C(Y) {
                  return Y.replace(/[^-\d\.]/g, "");
                }
                var B = J[b];
                B !== "auto" && C(B) !== "0" && (K.warn("An element that is positioned static has style." + b + "=" + B + " which is ignored due to the static positioning. The element will need to be positioned relative, so the style." + b + " will be set to 0. Element: ", A), A.style.setProperty(b, "0", c.important ? "important" : ""));
              };
              N(t, y, H, "top"), N(t, y, H, "right"), N(t, y, H, "bottom"), N(t, y, H, "left");
            }
          }
          function R() {
            z || d();
            function N(A, J) {
              if (!A.contentDocument) {
                var b = i(A);
                b.checkForObjectDocumentTimeoutId && window.clearTimeout(b.checkForObjectDocumentTimeoutId), b.checkForObjectDocumentTimeoutId = setTimeout(function() {
                  b.checkForObjectDocumentTimeoutId = 0, N(A, J);
                }, 100);
                return;
              }
              J(A.contentDocument);
            }
            var K = this;
            N(K, function(J) {
              x(y);
            });
          }
          H.position !== "" && (d(), z = true);
          var w = document.createElement("object");
          w.style.cssText = S, w.tabIndex = -1, w.type = "text/html", w.setAttribute("aria-hidden", "true"), w.onload = R, re.isIE() || (w.data = "about:blank"), i(y) && (y.appendChild(w), i(y).object = w, re.isIE() && (w.data = "about:blank"));
        }
        n ? n.add(m) : m();
      }
      re.isIE(8) ? f(u) : v(u, f);
    }
    function a(c) {
      return i(c).object;
    }
    function l(c) {
      if (!!i(c)) {
        var u = a(c);
        !u || (re.isIE(8) ? c.detachEvent("onresize", u.proxy) : c.removeChild(u), i(c).checkForObjectDocumentTimeoutId && window.clearTimeout(i(c).checkForObjectDocumentTimeoutId), delete i(c).object);
      }
    }
    return {
      makeDetectable: s,
      addListener: o,
      uninstall: l
    };
  }, Us = un.exports.forEach, Vs = function(e) {
    e = e || {};
    var t = e.reporter, n = e.batchProcessor, i = e.stateHandler.getState;
    e.stateHandler.hasState;
    var o = e.idHandler;
    if (!n)
      throw new Error("Missing required dependency: batchProcessor");
    if (!t)
      throw new Error("Missing required dependency: reporter.");
    var r = u(), s = "erd_scroll_detection_scrollbar_style", a = "erd_scroll_detection_container";
    function l(m) {
      f(m, s, a);
    }
    l(window.document);
    function c(m) {
      var d = e.important ? " !important; " : "; ";
      return (m.join(d) + d).trim();
    }
    function u() {
      var m = 500, d = 500, R = document.createElement("div");
      R.style.cssText = c(["position: absolute", "width: " + m * 2 + "px", "height: " + d * 2 + "px", "visibility: hidden", "margin: 0", "padding: 0"]);
      var w = document.createElement("div");
      w.style.cssText = c(["position: absolute", "width: " + m + "px", "height: " + d + "px", "overflow: scroll", "visibility: none", "top: " + -m * 3 + "px", "left: " + -d * 3 + "px", "visibility: hidden", "margin: 0", "padding: 0"]), w.appendChild(R), document.body.insertBefore(w, document.body.firstChild);
      var N = m - w.clientWidth, K = d - w.clientHeight;
      return document.body.removeChild(w), {
        width: N,
        height: K
      };
    }
    function f(m, d, R) {
      function w(J, b) {
        b = b || function(B) {
          m.head.appendChild(B);
        };
        var C = m.createElement("style");
        return C.innerHTML = J, C.id = d, b(C), C;
      }
      if (!m.getElementById(d)) {
        var N = R + "_animation", K = R + "_animation_active", A = `/* Created by the element-resize-detector library. */
`;
        A += "." + R + " > div::-webkit-scrollbar { " + c(["display: none"]) + ` }

`, A += "." + K + " { " + c(["-webkit-animation-duration: 0.1s", "animation-duration: 0.1s", "-webkit-animation-name: " + N, "animation-name: " + N]) + ` }
`, A += "@-webkit-keyframes " + N + ` { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
`, A += "@keyframes " + N + " { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }", w(A);
      }
    }
    function v(m) {
      m.className += " " + a + "_animation_active";
    }
    function y(m, d, R) {
      if (m.addEventListener)
        m.addEventListener(d, R);
      else if (m.attachEvent)
        m.attachEvent("on" + d, R);
      else
        return t.error("[scroll] Don't know how to add event listeners.");
    }
    function x(m, d, R) {
      if (m.removeEventListener)
        m.removeEventListener(d, R);
      else if (m.detachEvent)
        m.detachEvent("on" + d, R);
      else
        return t.error("[scroll] Don't know how to remove event listeners.");
    }
    function S(m) {
      return i(m).container.childNodes[0].childNodes[0].childNodes[0];
    }
    function z(m) {
      return i(m).container.childNodes[0].childNodes[0].childNodes[1];
    }
    function H(m, d) {
      var R = i(m).listeners;
      if (!R.push)
        throw new Error("Cannot add listener to an element that is not detectable.");
      i(m).listeners.push(d);
    }
    function T(m, d, R) {
      R || (R = d, d = m, m = null), m = m || {};
      function w() {
        if (m.debug) {
          var I = Array.prototype.slice.call(arguments);
          if (I.unshift(o.get(d), "Scroll: "), t.log.apply)
            t.log.apply(null, I);
          else
            for (var $ = 0; $ < I.length; $++)
              t.log(I[$]);
        }
      }
      function N(I) {
        function $(q) {
          var ft = q.getRootNode && q.getRootNode().contains(q);
          return q === q.ownerDocument.body || q.ownerDocument.body.contains(q) || ft;
        }
        return !$(I) || window.getComputedStyle(I) === null;
      }
      function K(I) {
        var $ = i(I).container.childNodes[0], q = window.getComputedStyle($);
        return !q.width || q.width.indexOf("px") === -1;
      }
      function A() {
        var I = window.getComputedStyle(d), $ = {};
        return $.position = I.position, $.width = d.offsetWidth, $.height = d.offsetHeight, $.top = I.top, $.right = I.right, $.bottom = I.bottom, $.left = I.left, $.widthCSS = I.width, $.heightCSS = I.height, $;
      }
      function J() {
        var I = A();
        i(d).startSize = {
          width: I.width,
          height: I.height
        }, w("Element start size", i(d).startSize);
      }
      function b() {
        i(d).listeners = [];
      }
      function C() {
        if (w("storeStyle invoked."), !i(d)) {
          w("Aborting because element has been uninstalled");
          return;
        }
        var I = A();
        i(d).style = I;
      }
      function B(I, $, q) {
        i(I).lastWidth = $, i(I).lastHeight = q;
      }
      function Y(I) {
        return S(I).childNodes[0];
      }
      function V() {
        return 2 * r.width + 1;
      }
      function Z() {
        return 2 * r.height + 1;
      }
      function M(I) {
        return I + 10 + V();
      }
      function Q(I) {
        return I + 10 + Z();
      }
      function it(I) {
        return I * 2 + V();
      }
      function tt(I) {
        return I * 2 + Z();
      }
      function st(I, $, q) {
        var ft = S(I), yt = z(I), St = M($), Et = Q(q), rt = it($), W = tt(q);
        ft.scrollLeft = St, ft.scrollTop = Et, yt.scrollLeft = rt, yt.scrollTop = W;
      }
      function G() {
        var I = i(d).container;
        if (!I) {
          I = document.createElement("div"), I.className = a, I.style.cssText = c(["visibility: hidden", "display: inline", "width: 0px", "height: 0px", "z-index: -1", "overflow: hidden", "margin: 0", "padding: 0"]), i(d).container = I, v(I), d.appendChild(I);
          var $ = function() {
            i(d).onRendered && i(d).onRendered();
          };
          y(I, "animationstart", $), i(d).onAnimationStart = $;
        }
        return I;
      }
      function fe() {
        function I() {
          var nt = i(d).style;
          if (nt.position === "static") {
            d.style.setProperty("position", "relative", m.important ? "important" : "");
            var pt = function(Dt, wt, pe, lt) {
              function Qt(h) {
                return h.replace(/[^-\d\.]/g, "");
              }
              var te = pe[lt];
              te !== "auto" && Qt(te) !== "0" && (Dt.warn("An element that is positioned static has style." + lt + "=" + te + " which is ignored due to the static positioning. The element will need to be positioned relative, so the style." + lt + " will be set to 0. Element: ", wt), wt.style[lt] = 0);
            };
            pt(t, d, nt, "top"), pt(t, d, nt, "right"), pt(t, d, nt, "bottom"), pt(t, d, nt, "left");
          }
        }
        function $(nt, pt, Dt, wt) {
          return nt = nt ? nt + "px" : "0", pt = pt ? pt + "px" : "0", Dt = Dt ? Dt + "px" : "0", wt = wt ? wt + "px" : "0", ["left: " + nt, "top: " + pt, "right: " + wt, "bottom: " + Dt];
        }
        if (w("Injecting elements"), !i(d)) {
          w("Aborting because element has been uninstalled");
          return;
        }
        I();
        var q = i(d).container;
        q || (q = G());
        var ft = r.width, yt = r.height, St = c(["position: absolute", "flex: none", "overflow: hidden", "z-index: -1", "visibility: hidden", "width: 100%", "height: 100%", "left: 0px", "top: 0px"]), Et = c(["position: absolute", "flex: none", "overflow: hidden", "z-index: -1", "visibility: hidden"].concat($(-(1 + ft), -(1 + yt), -yt, -ft))), rt = c(["position: absolute", "flex: none", "overflow: scroll", "z-index: -1", "visibility: hidden", "width: 100%", "height: 100%"]), W = c(["position: absolute", "flex: none", "overflow: scroll", "z-index: -1", "visibility: hidden", "width: 100%", "height: 100%"]), at = c(["position: absolute", "left: 0", "top: 0"]), bt = c(["position: absolute", "width: 200%", "height: 200%"]), et = document.createElement("div"), dt = document.createElement("div"), Ct = document.createElement("div"), he = document.createElement("div"), xt = document.createElement("div"), Yt = document.createElement("div");
        et.dir = "ltr", et.style.cssText = St, et.className = a, dt.className = a, dt.style.cssText = Et, Ct.style.cssText = rt, he.style.cssText = at, xt.style.cssText = W, Yt.style.cssText = bt, Ct.appendChild(he), xt.appendChild(Yt), dt.appendChild(Ct), dt.appendChild(xt), et.appendChild(dt), q.appendChild(et);
        function $t() {
          var nt = i(d);
          nt && nt.onExpand ? nt.onExpand() : w("Aborting expand scroll handler: element has been uninstalled");
        }
        function Zt() {
          var nt = i(d);
          nt && nt.onShrink ? nt.onShrink() : w("Aborting shrink scroll handler: element has been uninstalled");
        }
        y(Ct, "scroll", $t), y(xt, "scroll", Zt), i(d).onExpandScroll = $t, i(d).onShrinkScroll = Zt;
      }
      function _e() {
        function I(rt, W, at) {
          var bt = Y(rt), et = M(W), dt = Q(at);
          bt.style.setProperty("width", et + "px", m.important ? "important" : ""), bt.style.setProperty("height", dt + "px", m.important ? "important" : "");
        }
        function $(rt) {
          var W = d.offsetWidth, at = d.offsetHeight, bt = W !== i(d).lastWidth || at !== i(d).lastHeight;
          w("Storing current size", W, at), B(d, W, at), n.add(0, function() {
            if (!!bt) {
              if (!i(d)) {
                w("Aborting because element has been uninstalled");
                return;
              }
              if (!q()) {
                w("Aborting because element container has not been initialized");
                return;
              }
              if (m.debug) {
                var dt = d.offsetWidth, Ct = d.offsetHeight;
                (dt !== W || Ct !== at) && t.warn(o.get(d), "Scroll: Size changed before updating detector elements.");
              }
              I(d, W, at);
            }
          }), n.add(1, function() {
            if (!i(d)) {
              w("Aborting because element has been uninstalled");
              return;
            }
            if (!q()) {
              w("Aborting because element container has not been initialized");
              return;
            }
            st(d, W, at);
          }), bt && rt && n.add(2, function() {
            if (!i(d)) {
              w("Aborting because element has been uninstalled");
              return;
            }
            if (!q()) {
              w("Aborting because element container has not been initialized");
              return;
            }
            rt();
          });
        }
        function q() {
          return !!i(d).container;
        }
        function ft() {
          function rt() {
            return i(d).lastNotifiedWidth === void 0;
          }
          w("notifyListenersIfNeeded invoked");
          var W = i(d);
          if (rt() && W.lastWidth === W.startSize.width && W.lastHeight === W.startSize.height)
            return w("Not notifying: Size is the same as the start size, and there has been no notification yet.");
          if (W.lastWidth === W.lastNotifiedWidth && W.lastHeight === W.lastNotifiedHeight)
            return w("Not notifying: Size already notified");
          w("Current size not notified, notifying..."), W.lastNotifiedWidth = W.lastWidth, W.lastNotifiedHeight = W.lastHeight, Us(i(d).listeners, function(at) {
            at(d);
          });
        }
        function yt() {
          if (w("startanimation triggered."), K(d)) {
            w("Ignoring since element is still unrendered...");
            return;
          }
          w("Element rendered.");
          var rt = S(d), W = z(d);
          (rt.scrollLeft === 0 || rt.scrollTop === 0 || W.scrollLeft === 0 || W.scrollTop === 0) && (w("Scrollbars out of sync. Updating detector elements..."), $(ft));
        }
        function St() {
          if (w("Scroll detected."), K(d)) {
            w("Scroll event fired while unrendered. Ignoring...");
            return;
          }
          $(ft);
        }
        if (w("registerListenersAndPositionElements invoked."), !i(d)) {
          w("Aborting because element has been uninstalled");
          return;
        }
        i(d).onRendered = yt, i(d).onExpand = St, i(d).onShrink = St;
        var Et = i(d).style;
        I(d, Et.width, Et.height);
      }
      function Ce() {
        if (w("finalizeDomMutation invoked."), !i(d)) {
          w("Aborting because element has been uninstalled");
          return;
        }
        var I = i(d).style;
        B(d, I.width, I.height), st(d, I.width, I.height);
      }
      function ct() {
        R(d);
      }
      function de() {
        w("Installing..."), b(), J(), n.add(0, C), n.add(1, fe), n.add(2, _e), n.add(3, Ce), n.add(4, ct);
      }
      w("Making detectable..."), N(d) ? (w("Element is detached"), G(), w("Waiting until element is attached..."), i(d).onRendered = function() {
        w("Element is now attached"), de();
      }) : de();
    }
    function _(m) {
      var d = i(m);
      !d || (d.onExpandScroll && x(S(m), "scroll", d.onExpandScroll), d.onShrinkScroll && x(z(m), "scroll", d.onShrinkScroll), d.onAnimationStart && x(d.container, "animationstart", d.onAnimationStart), d.container && m.removeChild(d.container));
    }
    return {
      makeDetectable: T,
      addListener: H,
      uninstall: _,
      initDocument: l
    };
  }, se = un.exports.forEach, Ks = Hs, Js = $s, Zs = Bs, Qs = Ws, ta = Ls, Wn = fn.exports, ea = js, kt = Gs, na = qs, ia = Vs;
  function Ln(e) {
    return Array.isArray(e) || e.length !== void 0;
  }
  function Fn(e) {
    if (Array.isArray(e))
      return e;
    var t = [];
    return se(e, function(n) {
      t.push(n);
    }), t;
  }
  function Nn(e) {
    return e && e.nodeType === 1;
  }
  var oa = function(e) {
    e = e || {};
    var t;
    if (e.idHandler)
      t = {
        get: function(T) {
          return e.idHandler.get(T, true);
        },
        set: e.idHandler.set
      };
    else {
      var n = Zs(), i = Qs({
        idGenerator: n,
        stateHandler: kt
      });
      t = i;
    }
    var o = e.reporter;
    if (!o) {
      var r = o === false;
      o = ta(r);
    }
    var s = At(e, "batchProcessor", ea({ reporter: o })), a = {};
    a.callOnAdd = !!At(e, "callOnAdd", true), a.debug = !!At(e, "debug", false);
    var l = Js(t), c = Ks({
      stateHandler: kt
    }), u, f = At(e, "strategy", "object"), v = At(e, "important", false), y = {
      reporter: o,
      batchProcessor: s,
      stateHandler: kt,
      idHandler: t,
      important: v
    };
    if (f === "scroll" && (Wn.isLegacyOpera() ? (o.warn("Scroll strategy is not supported on legacy Opera. Changing to object strategy."), f = "object") : Wn.isIE(9) && (o.warn("Scroll strategy is not supported on IE9. Changing to object strategy."), f = "object")), f === "scroll")
      u = ia(y);
    else if (f === "object")
      u = na(y);
    else
      throw new Error("Invalid strategy name: " + f);
    var x = {};
    function S(T, _, m) {
      function d(J) {
        var b = l.get(J);
        se(b, function(B) {
          B(J);
        });
      }
      function R(J, b, C) {
        l.add(b, C), J && C(b);
      }
      if (m || (m = _, _ = T, T = {}), !_)
        throw new Error("At least one element required.");
      if (!m)
        throw new Error("Listener required.");
      if (Nn(_))
        _ = [_];
      else if (Ln(_))
        _ = Fn(_);
      else
        return o.error("Invalid arguments. Must be a DOM element or a collection of DOM elements.");
      var w = 0, N = At(T, "callOnAdd", a.callOnAdd), K = At(T, "onReady", function() {
      }), A = At(T, "debug", a.debug);
      se(_, function(b) {
        kt.getState(b) || (kt.initState(b), t.set(b));
        var C = t.get(b);
        if (A && o.log("Attaching listener to element", C, b), !c.isDetectable(b)) {
          if (A && o.log(C, "Not detectable."), c.isBusy(b)) {
            A && o.log(C, "System busy making it detectable"), R(N, b, m), x[C] = x[C] || [], x[C].push(function() {
              w++, w === _.length && K();
            });
            return;
          }
          return A && o.log(C, "Making detectable..."), c.markBusy(b, true), u.makeDetectable({ debug: A, important: v }, b, function(Y) {
            if (A && o.log(C, "onElementDetectable"), kt.getState(Y)) {
              c.markAsDetectable(Y), c.markBusy(Y, false), u.addListener(Y, d), R(N, Y, m);
              var V = kt.getState(Y);
              if (V && V.startSize) {
                var Z = Y.offsetWidth, M = Y.offsetHeight;
                (V.startSize.width !== Z || V.startSize.height !== M) && d(Y);
              }
              x[C] && se(x[C], function(Q) {
                Q();
              });
            } else
              A && o.log(C, "Element uninstalled before being detectable.");
            delete x[C], w++, w === _.length && K();
          });
        }
        A && o.log(C, "Already detecable, adding listener."), R(N, b, m), w++;
      }), w === _.length && K();
    }
    function z(T) {
      if (!T)
        return o.error("At least one element is required.");
      if (Nn(T))
        T = [T];
      else if (Ln(T))
        T = Fn(T);
      else
        return o.error("Invalid arguments. Must be a DOM element or a collection of DOM elements.");
      se(T, function(_) {
        l.removeAllListeners(_), u.uninstall(_), kt.cleanState(_);
      });
    }
    function H(T) {
      u.initDocument && u.initDocument(T);
    }
    return {
      listenTo: S,
      removeListener: l.removeListener,
      removeAllListeners: l.removeAllListeners,
      uninstall: z,
      initDocument: H
    };
  };
  function At(e, t, n) {
    var i = e[t];
    return i == null && n !== void 0 ? n : i;
  }
  const ra = {
    name: "GridLayout"
  }, sa = /* @__PURE__ */ vue.defineComponent({
    ...ra,
    props: {
      autoSize: { type: Boolean, default: true },
      colNum: { default: 12 },
      rowHeight: { default: 100 },
      maxRows: { default: 1 / 0 },
      margin: { default: () => [10, 10] },
      isDraggable: { type: Boolean, default: true },
      isResizable: { type: Boolean, default: true },
      isMirrored: { type: Boolean, default: false },
      isBounded: { type: Boolean, default: false },
      useCssTransforms: { type: Boolean, default: true },
      verticalCompact: { type: Boolean, default: true },
      restoreOnDrag: { type: Boolean, default: false },
      layout: null,
      responsive: { type: Boolean, default: false },
      responsiveLayouts: { default: () => ({}) },
      transformScale: { default: 1 },
      breakpoints: { default: () => ({ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }) },
      cols: { default: () => ({ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }) },
      preventCollision: { type: Boolean, default: false },
      useStyleCursor: { type: Boolean, default: true }
    },
    emits: ["layout-created", "layout-before-mount", "layout-mounted", "layout-updated", "layout-ready", "update:layout", "breakpoint-changed"],
    setup(e, { expose: t, emit: n }) {
      const i = e, o = vue.ref(null), r = vue.ref({}), s = vue.ref(0), a = vue.ref(false), l = vue.ref({ x: 0, y: 0, w: 0, h: 0, i: -1 }), c = vue.ref({}), u = vue.ref(null), f = vue.ref(null), v = vue.ref(null), y = vue.ref(), x = vue.ref({}), S = vue.ref(), z = Os();
      vue.provide("eventBus", z);
      function H(b) {
        if (!b)
          N();
        else {
          const { eventType: C, i: B, x: Y, y: V, h: Z, w: M } = b;
          N(C, B, Y, V, Z, M);
        }
      }
      function T(b) {
        if (!b)
          w();
        else {
          const { eventType: C, i: B, x: Y, y: V, h: Z, w: M } = b;
          w(C, B, Y, V, Z, M);
        }
      }
      z.on("resizeEvent", H), z.on("dragEvent", T), n("layout-created", i.layout), vue.onBeforeUnmount(() => {
        z.off("resizeEvent", H), z.off("dragEvent", T), ro("resize", d), v.value && v.value.uninstall(x.value);
      }), vue.onBeforeMount(() => {
        n("layout-before-mount", i.layout);
      }), vue.onMounted(() => {
        n("layout-mounted", i.layout), vue.nextTick(function() {
          Ji(i.layout), f.value = i.layout, vue.nextTick(() => {
            A(), d(), oo("resize", d), qt(i.layout, i.verticalCompact), n("layout-updated", i.layout), m(), vue.nextTick(() => {
              v.value = oa({
                strategy: "scroll",
                callOnAdd: false
              }), v.value.listenTo(x.value, function() {
                d();
              });
            });
          });
        });
      }), vue.watch(o, (b, C) => {
        vue.nextTick(() => {
          z.emit("updateWidth", b), C === null && vue.nextTick(() => {
            n("layout-ready", i.layout);
          }), m();
        });
      }), vue.watch(
        () => i.layout,
        () => {
          _();
        }
      ), vue.watch(
        () => i.layout.length,
        () => {
          _();
        }
      ), vue.watch(
        () => i.colNum,
        (b) => {
          z.emit("setColNum", b);
        }
      ), vue.watch(
        () => i.rowHeight,
        (b) => {
          z.emit("setRowHeight", b);
        }
      ), vue.watch(
        () => i.isDraggable,
        (b) => {
          z.emit("setDraggable", b);
        }
      ), vue.watch(
        () => i.isResizable,
        (b) => {
          z.emit("setResizable", b);
        }
      ), vue.watch(
        () => i.isBounded,
        (b) => {
          z.emit("setBounded", b);
        }
      ), vue.watch(
        () => i.transformScale,
        (b) => {
          z.emit("setTransformScale", b);
        }
      ), vue.watch(
        () => i.responsive,
        (b) => {
          b || (n("update:layout", f.value || []), z.emit("setColNum", i.colNum)), d();
        }
      ), vue.watch(
        () => i.maxRows,
        (b) => {
          z.emit("setMaxRows", b);
        }
      ), vue.watch(
        () => i.margin,
        () => {
          m();
        }
      );
      function _() {
        if (i.layout !== void 0 && f.value !== null) {
          if (i.layout.length !== f.value.length) {
            let b = J(i.layout, f.value);
            b.length > 0 && (i.layout.length > f.value.length ? f.value = f.value.concat(b) : f.value = f.value.filter((C) => !b.some((B) => C.i === B.i))), s.value = i.layout.length, A();
          }
          qt(i.layout, i.verticalCompact), z.emit("updateWidth", o.value), m(), n("layout-updated", i.layout);
        }
      }
      function m() {
        r.value = {
          height: R()
        };
      }
      function d() {
        x.value !== null && x.value !== void 0 && (o.value = x.value.offsetWidth), z.emit("resizeEvent");
      }
      function R() {
        return i.autoSize ? ji(i.layout) * (i.rowHeight + i.margin[1]) + i.margin[1] + "px" : "";
      }
      function w(b, C, B, Y, V, Z) {
        let M = gn(i.layout, C);
        M == null && (M = { x: 0, y: 0 }), b === "dragstart" && !i.verticalCompact && (y.value = i.layout.reduce(
          (it, { i: tt, x: st, y: G }) => ({
            ...it,
            [tt]: { x: st, y: G }
          }),
          {}
        )), b === "dragmove" || b === "dragstart" ? (l.value.i = C, l.value.x = M.x, l.value.y = M.y, l.value.w = Z, l.value.h = V, vue.nextTick(function() {
          a.value = true;
        }), z.emit("updateWidth", o.value)) : vue.nextTick(function() {
          a.value = false;
        });
        const Q = Xe(i.layout, M, B, Y, true, i.preventCollision);
        n("update:layout", Q), i.restoreOnDrag ? (M.static = true, qt(i.layout, i.verticalCompact, y.value), M.static = false) : qt(i.layout, i.verticalCompact), z.emit("compact"), m(), b === "dragend" && (y.value = void 0, n("layout-updated", Q));
      }
      function N(b, C, B, Y, V, Z) {
        let M = gn(i.layout, C);
        M == null && (M = { h: 0, w: 0 }), Z = Number(Z), V = Number(V);
        let Q;
        if (i.preventCollision) {
          const it = Un(i.layout, { ...M, w: Z, h: V }).filter(
            (tt) => tt.i !== (M == null ? void 0 : M.i)
          );
          if (Q = it.length > 0, Q) {
            let tt = 1 / 0, st = 1 / 0;
            it.forEach((G) => {
              G.x > Number(M == null ? void 0 : M.x) && (tt = Math.min(tt, G.x)), G.y > Number(M == null ? void 0 : M.y) && (st = Math.min(st, G.y));
            }), Number.isFinite(tt) && (M.w = tt - M.x), Number.isFinite(st) && (M.h = st - M.y);
          }
        }
        Q || (M.w = Z, M.h = V), b === "resizestart" || b === "resizemove" ? (l.value.i = C, l.value.x = B, l.value.y = Y, l.value.w = M.w, l.value.h = M.h, vue.nextTick(function() {
          a.value = true;
        }), z.emit("updateWidth", o.value)) : vue.nextTick(function() {
          a.value = false;
        }), i.responsive && K(), qt(i.layout, i.verticalCompact), z.emit("compact"), m(), b === "resizeend" && n("layout-updated", i.layout);
      }
      function K() {
        let b = to(i.breakpoints, o.value), C = Ge(b, i.cols);
        u.value != null && !c.value[u.value] && (c.value[u.value] = Ye(i.layout));
        let B = eo(
          f.value,
          c.value,
          i.breakpoints,
          b,
          u.value,
          C,
          i.verticalCompact
        );
        c.value[b] = B, u.value !== b && n("breakpoint-changed", b, B), n("update:layout", B), u.value = b, z.emit("setColNum", Ge(b, i.cols));
      }
      function A() {
        c.value = Object.assign({}, i.responsiveLayouts);
      }
      function J(b, C) {
        let B = b.filter(function(V) {
          return !C.some(function(Z) {
            return V.i === Z.i;
          });
        }), Y = C.filter(function(V) {
          return !b.some(function(Z) {
            return V.i === Z.i;
          });
        });
        return B.concat(Y);
      }
      return t({
        ...i,
        width: o,
        mergeStyle: r,
        lastLayoutLength: s,
        isDragging: a,
        placeholder: l,
        layouts: c,
        lastBreakpoint: u,
        originalLayout: f,
        erd: v,
        defaultGridItem: S,
        dragEvent: w
      }), (b, C) => (vue.openBlock(), vue.createElementBlock("div", {
        ref_key: "this$refsLayout",
        ref: x,
        class: "vue-grid-layout",
        style: vue.normalizeStyle(r.value)
      }, [
        vue.renderSlot(b.$slots, "default"),
        vue.withDirectives(vue.createVNode(_i, {
          ref_key: "defaultGridItem",
          ref: S,
          class: "vue-grid-placeholder",
          x: l.value.x,
          y: l.value.y,
          w: l.value.w,
          h: l.value.h,
          i: l.value.i
        }, null, 8, ["x", "y", "w", "h", "i"]), [
          [vue.vShow, a.value]
        ])
      ], 4));
    }
  });
  var DomHandler = {
    innerWidth(el) {
      if (el) {
        let width = el.offsetWidth;
        let style2 = getComputedStyle(el);
        width += parseFloat(style2.paddingLeft) + parseFloat(style2.paddingRight);
        return width;
      }
      return 0;
    },
    width(el) {
      if (el) {
        let width = el.offsetWidth;
        let style2 = getComputedStyle(el);
        width -= parseFloat(style2.paddingLeft) + parseFloat(style2.paddingRight);
        return width;
      }
      return 0;
    },
    getWindowScrollTop() {
      let doc = document.documentElement;
      return (window.pageYOffset || doc.scrollTop) - (doc.clientTop || 0);
    },
    getWindowScrollLeft() {
      let doc = document.documentElement;
      return (window.pageXOffset || doc.scrollLeft) - (doc.clientLeft || 0);
    },
    getOuterWidth(el, margin) {
      if (el) {
        let width = el.offsetWidth;
        if (margin) {
          let style2 = getComputedStyle(el);
          width += parseFloat(style2.marginLeft) + parseFloat(style2.marginRight);
        }
        return width;
      }
      return 0;
    },
    getOuterHeight(el, margin) {
      if (el) {
        let height = el.offsetHeight;
        if (margin) {
          let style2 = getComputedStyle(el);
          height += parseFloat(style2.marginTop) + parseFloat(style2.marginBottom);
        }
        return height;
      }
      return 0;
    },
    getClientHeight(el, margin) {
      if (el) {
        let height = el.clientHeight;
        if (margin) {
          let style2 = getComputedStyle(el);
          height += parseFloat(style2.marginTop) + parseFloat(style2.marginBottom);
        }
        return height;
      }
      return 0;
    },
    getViewport() {
      let win2 = window, d = document, e = d.documentElement, g2 = d.getElementsByTagName("body")[0], w = win2.innerWidth || e.clientWidth || g2.clientWidth, h = win2.innerHeight || e.clientHeight || g2.clientHeight;
      return { width: w, height: h };
    },
    getOffset(el) {
      if (el) {
        let rect = el.getBoundingClientRect();
        return {
          top: rect.top + (window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0),
          left: rect.left + (window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0)
        };
      }
      return {
        top: "auto",
        left: "auto"
      };
    },
    index(element) {
      if (element) {
        let children = element.parentNode.childNodes;
        let num = 0;
        for (let i = 0; i < children.length; i++) {
          if (children[i] === element)
            return num;
          if (children[i].nodeType === 1)
            num++;
        }
      }
      return -1;
    },
    addMultipleClasses(element, className) {
      if (element && className) {
        if (element.classList) {
          let styles = className.split(" ");
          for (let i = 0; i < styles.length; i++) {
            element.classList.add(styles[i]);
          }
        } else {
          let styles = className.split(" ");
          for (let i = 0; i < styles.length; i++) {
            element.className += " " + styles[i];
          }
        }
      }
    },
    addClass(element, className) {
      if (element && className) {
        if (element.classList)
          element.classList.add(className);
        else
          element.className += " " + className;
      }
    },
    removeClass(element, className) {
      if (element && className) {
        if (element.classList)
          element.classList.remove(className);
        else
          element.className = element.className.replace(new RegExp("(^|\\b)" + className.split(" ").join("|") + "(\\b|$)", "gi"), " ");
      }
    },
    hasClass(element, className) {
      if (element) {
        if (element.classList)
          return element.classList.contains(className);
        else
          return new RegExp("(^| )" + className + "( |$)", "gi").test(element.className);
      }
      return false;
    },
    find(element, selector) {
      return this.isElement(element) ? element.querySelectorAll(selector) : [];
    },
    findSingle(element, selector) {
      return this.isElement(element) ? element.querySelector(selector) : null;
    },
    getHeight(el) {
      if (el) {
        let height = el.offsetHeight;
        let style2 = getComputedStyle(el);
        height -= parseFloat(style2.paddingTop) + parseFloat(style2.paddingBottom) + parseFloat(style2.borderTopWidth) + parseFloat(style2.borderBottomWidth);
        return height;
      }
      return 0;
    },
    getWidth(el) {
      if (el) {
        let width = el.offsetWidth;
        let style2 = getComputedStyle(el);
        width -= parseFloat(style2.paddingLeft) + parseFloat(style2.paddingRight) + parseFloat(style2.borderLeftWidth) + parseFloat(style2.borderRightWidth);
        return width;
      }
      return 0;
    },
    absolutePosition(element, target) {
      if (element) {
        let elementDimensions = element.offsetParent ? { width: element.offsetWidth, height: element.offsetHeight } : this.getHiddenElementDimensions(element);
        let elementOuterHeight = elementDimensions.height;
        let elementOuterWidth = elementDimensions.width;
        let targetOuterHeight = target.offsetHeight;
        let targetOuterWidth = target.offsetWidth;
        let targetOffset = target.getBoundingClientRect();
        let windowScrollTop = this.getWindowScrollTop();
        let windowScrollLeft = this.getWindowScrollLeft();
        let viewport = this.getViewport();
        let top, left;
        if (targetOffset.top + targetOuterHeight + elementOuterHeight > viewport.height) {
          top = targetOffset.top + windowScrollTop - elementOuterHeight;
          element.style.transformOrigin = "bottom";
          if (top < 0) {
            top = windowScrollTop;
          }
        } else {
          top = targetOuterHeight + targetOffset.top + windowScrollTop;
          element.style.transformOrigin = "top";
        }
        if (targetOffset.left + elementOuterWidth > viewport.width)
          left = Math.max(0, targetOffset.left + windowScrollLeft + targetOuterWidth - elementOuterWidth);
        else
          left = targetOffset.left + windowScrollLeft;
        element.style.top = top + "px";
        element.style.left = left + "px";
      }
    },
    relativePosition(element, target) {
      if (element) {
        let elementDimensions = element.offsetParent ? { width: element.offsetWidth, height: element.offsetHeight } : this.getHiddenElementDimensions(element);
        const targetHeight = target.offsetHeight;
        const targetOffset = target.getBoundingClientRect();
        const viewport = this.getViewport();
        let top, left;
        if (targetOffset.top + targetHeight + elementDimensions.height > viewport.height) {
          top = -1 * elementDimensions.height;
          element.style.transformOrigin = "bottom";
          if (targetOffset.top + top < 0) {
            top = -1 * targetOffset.top;
          }
        } else {
          top = targetHeight;
          element.style.transformOrigin = "top";
        }
        if (elementDimensions.width > viewport.width) {
          left = targetOffset.left * -1;
        } else if (targetOffset.left + elementDimensions.width > viewport.width) {
          left = (targetOffset.left + elementDimensions.width - viewport.width) * -1;
        } else {
          left = 0;
        }
        element.style.top = top + "px";
        element.style.left = left + "px";
      }
    },
    getParents(element, parents = []) {
      return element["parentNode"] === null ? parents : this.getParents(element.parentNode, parents.concat([element.parentNode]));
    },
    getScrollableParents(element) {
      let scrollableParents = [];
      if (element) {
        let parents = this.getParents(element);
        const overflowRegex = /(auto|scroll)/;
        const overflowCheck = (node) => {
          let styleDeclaration = window["getComputedStyle"](node, null);
          return overflowRegex.test(styleDeclaration.getPropertyValue("overflow")) || overflowRegex.test(styleDeclaration.getPropertyValue("overflowX")) || overflowRegex.test(styleDeclaration.getPropertyValue("overflowY"));
        };
        for (let parent of parents) {
          let scrollSelectors = parent.nodeType === 1 && parent.dataset["scrollselectors"];
          if (scrollSelectors) {
            let selectors = scrollSelectors.split(",");
            for (let selector of selectors) {
              let el = this.findSingle(parent, selector);
              if (el && overflowCheck(el)) {
                scrollableParents.push(el);
              }
            }
          }
          if (parent.nodeType !== 9 && overflowCheck(parent)) {
            scrollableParents.push(parent);
          }
        }
      }
      return scrollableParents;
    },
    getHiddenElementOuterHeight(element) {
      if (element) {
        element.style.visibility = "hidden";
        element.style.display = "block";
        let elementHeight = element.offsetHeight;
        element.style.display = "none";
        element.style.visibility = "visible";
        return elementHeight;
      }
      return 0;
    },
    getHiddenElementOuterWidth(element) {
      if (element) {
        element.style.visibility = "hidden";
        element.style.display = "block";
        let elementWidth = element.offsetWidth;
        element.style.display = "none";
        element.style.visibility = "visible";
        return elementWidth;
      }
      return 0;
    },
    getHiddenElementDimensions(element) {
      if (element) {
        let dimensions = {};
        element.style.visibility = "hidden";
        element.style.display = "block";
        dimensions.width = element.offsetWidth;
        dimensions.height = element.offsetHeight;
        element.style.display = "none";
        element.style.visibility = "visible";
        return dimensions;
      }
      return 0;
    },
    fadeIn(element, duration) {
      if (element) {
        element.style.opacity = 0;
        let last = +new Date();
        let opacity = 0;
        let tick = function() {
          opacity = +element.style.opacity + (new Date().getTime() - last) / duration;
          element.style.opacity = opacity;
          last = +new Date();
          if (+opacity < 1) {
            window.requestAnimationFrame && requestAnimationFrame(tick) || setTimeout(tick, 16);
          }
        };
        tick();
      }
    },
    fadeOut(element, ms2) {
      if (element) {
        let opacity = 1, interval = 50, duration = ms2, gap = interval / duration;
        let fading = setInterval(() => {
          opacity -= gap;
          if (opacity <= 0) {
            opacity = 0;
            clearInterval(fading);
          }
          element.style.opacity = opacity;
        }, interval);
      }
    },
    getUserAgent() {
      return navigator.userAgent;
    },
    appendChild(element, target) {
      if (this.isElement(target))
        target.appendChild(element);
      else if (target.el && target.elElement)
        target.elElement.appendChild(element);
      else
        throw new Error("Cannot append " + target + " to " + element);
    },
    isElement(obj) {
      return typeof HTMLElement === "object" ? obj instanceof HTMLElement : obj && typeof obj === "object" && obj !== null && obj.nodeType === 1 && typeof obj.nodeName === "string";
    },
    scrollInView(container, item) {
      let borderTopValue = getComputedStyle(container).getPropertyValue("borderTopWidth");
      let borderTop = borderTopValue ? parseFloat(borderTopValue) : 0;
      let paddingTopValue = getComputedStyle(container).getPropertyValue("paddingTop");
      let paddingTop = paddingTopValue ? parseFloat(paddingTopValue) : 0;
      let containerRect = container.getBoundingClientRect();
      let itemRect = item.getBoundingClientRect();
      let offset = itemRect.top + document.body.scrollTop - (containerRect.top + document.body.scrollTop) - borderTop - paddingTop;
      let scroll = container.scrollTop;
      let elementHeight = container.clientHeight;
      let itemHeight = this.getOuterHeight(item);
      if (offset < 0) {
        container.scrollTop = scroll + offset;
      } else if (offset + itemHeight > elementHeight) {
        container.scrollTop = scroll + offset - elementHeight + itemHeight;
      }
    },
    clearSelection() {
      if (window.getSelection) {
        if (window.getSelection().empty) {
          window.getSelection().empty();
        } else if (window.getSelection().removeAllRanges && window.getSelection().rangeCount > 0 && window.getSelection().getRangeAt(0).getClientRects().length > 0) {
          window.getSelection().removeAllRanges();
        }
      } else if (document["selection"] && document["selection"].empty) {
        try {
          document["selection"].empty();
        } catch (error) {
        }
      }
    },
    getSelection() {
      if (window.getSelection)
        return window.getSelection().toString();
      else if (document.getSelection)
        return document.getSelection().toString();
      else if (document["selection"])
        return document["selection"].createRange().text;
      return null;
    },
    calculateScrollbarWidth() {
      if (this.calculatedScrollbarWidth != null)
        return this.calculatedScrollbarWidth;
      let scrollDiv = document.createElement("div");
      scrollDiv.className = "p-scrollbar-measure";
      document.body.appendChild(scrollDiv);
      let scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth;
      document.body.removeChild(scrollDiv);
      this.calculatedScrollbarWidth = scrollbarWidth;
      return scrollbarWidth;
    },
    getBrowser() {
      if (!this.browser) {
        let matched = this.resolveUserAgent();
        this.browser = {};
        if (matched.browser) {
          this.browser[matched.browser] = true;
          this.browser["version"] = matched.version;
        }
        if (this.browser["chrome"]) {
          this.browser["webkit"] = true;
        } else if (this.browser["webkit"]) {
          this.browser["safari"] = true;
        }
      }
      return this.browser;
    },
    resolveUserAgent() {
      let ua = navigator.userAgent.toLowerCase();
      let match = /(chrome)[ ]([\w.]+)/.exec(ua) || /(webkit)[ ]([\w.]+)/.exec(ua) || /(opera)(?:.*version|)[ ]([\w.]+)/.exec(ua) || /(msie) ([\w.]+)/.exec(ua) || ua.indexOf("compatible") < 0 && /(mozilla)(?:.*? rv:([\w.]+)|)/.exec(ua) || [];
      return {
        browser: match[1] || "",
        version: match[2] || "0"
      };
    },
    isVisible(element) {
      return element && element.offsetParent != null;
    },
    invokeElementMethod(element, methodName, args) {
      element[methodName].apply(element, args);
    },
    isExist(element) {
      return !!(element !== null && typeof element !== "undefined" && element.nodeName && element.parentNode);
    },
    isClient() {
      return !!(typeof window !== "undefined" && window.document && window.document.createElement);
    },
    focus(el, options) {
      el && document.activeElement !== el && el.focus(options);
    },
    isFocusableElement(element, selector = "") {
      return this.isElement(element) ? element.matches(`button:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                [href][clientHeight][clientWidth]:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                input:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                select:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                textarea:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                [tabIndex]:not([tabIndex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                [contenteditable]:not([tabIndex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector}`) : false;
    },
    getFocusableElements(element, selector = "") {
      let focusableElements = this.find(
        element,
        `button:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                [href][clientHeight][clientWidth]:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                input:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                select:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                textarea:not([tabindex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                [tabIndex]:not([tabIndex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector},
                [contenteditable]:not([tabIndex = "-1"]):not([disabled]):not([style*="display:none"]):not([hidden])${selector}`
      );
      let visibleFocusableElements = [];
      for (let focusableElement of focusableElements) {
        if (getComputedStyle(focusableElement).display != "none" && getComputedStyle(focusableElement).visibility != "hidden")
          visibleFocusableElements.push(focusableElement);
      }
      return visibleFocusableElements;
    },
    getFirstFocusableElement(element, selector) {
      const focusableElements = this.getFocusableElements(element, selector);
      return focusableElements.length > 0 ? focusableElements[0] : null;
    },
    getLastFocusableElement(element, selector) {
      const focusableElements = this.getFocusableElements(element, selector);
      return focusableElements.length > 0 ? focusableElements[focusableElements.length - 1] : null;
    },
    getNextFocusableElement(container, element, selector) {
      const focusableElements = this.getFocusableElements(container, selector);
      const index = focusableElements.length > 0 ? focusableElements.findIndex((el) => el === element) : -1;
      const nextIndex = index > -1 && focusableElements.length >= index + 1 ? index + 1 : -1;
      return nextIndex > -1 ? focusableElements[nextIndex] : null;
    },
    isClickable(element) {
      const targetNode = element.nodeName;
      const parentNode = element.parentElement && element.parentElement.nodeName;
      return targetNode == "INPUT" || targetNode == "BUTTON" || targetNode == "A" || parentNode == "INPUT" || parentNode == "BUTTON" || parentNode == "A" || this.hasClass(element, "p-button") || this.hasClass(element.parentElement, "p-button") || this.hasClass(element.parentElement, "p-checkbox") || this.hasClass(element.parentElement, "p-radiobutton");
    },
    applyStyle(element, style2) {
      if (typeof style2 === "string") {
        element.style.cssText = style2;
      } else {
        for (let prop in style2) {
          element.style[prop] = style2[prop];
        }
      }
    },
    isIOS() {
      return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window["MSStream"];
    },
    isAndroid() {
      return /(android)/i.test(navigator.userAgent);
    },
    isTouchDevice() {
      return "ontouchstart" in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
    },
    exportCSV(csv, filename) {
      let blob = new Blob([csv], {
        type: "application/csv;charset=utf-8;"
      });
      if (window.navigator.msSaveOrOpenBlob) {
        navigator.msSaveOrOpenBlob(blob, filename + ".csv");
      } else {
        let link = document.createElement("a");
        if (link.download !== void 0) {
          link.setAttribute("href", URL.createObjectURL(blob));
          link.setAttribute("download", filename + ".csv");
          link.style.display = "none";
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        } else {
          csv = "data:text/csv;charset=utf-8," + csv;
          window.open(encodeURI(csv));
        }
      }
    }
  };
  var ObjectUtils = {
    equals(obj1, obj2, field) {
      if (field)
        return this.resolveFieldData(obj1, field) === this.resolveFieldData(obj2, field);
      else
        return this.deepEquals(obj1, obj2);
    },
    deepEquals(a, b) {
      if (a === b)
        return true;
      if (a && b && typeof a == "object" && typeof b == "object") {
        var arrA = Array.isArray(a), arrB = Array.isArray(b), i, length, key;
        if (arrA && arrB) {
          length = a.length;
          if (length != b.length)
            return false;
          for (i = length; i-- !== 0; )
            if (!this.deepEquals(a[i], b[i]))
              return false;
          return true;
        }
        if (arrA != arrB)
          return false;
        var dateA = a instanceof Date, dateB = b instanceof Date;
        if (dateA != dateB)
          return false;
        if (dateA && dateB)
          return a.getTime() == b.getTime();
        var regexpA = a instanceof RegExp, regexpB = b instanceof RegExp;
        if (regexpA != regexpB)
          return false;
        if (regexpA && regexpB)
          return a.toString() == b.toString();
        var keys = Object.keys(a);
        length = keys.length;
        if (length !== Object.keys(b).length)
          return false;
        for (i = length; i-- !== 0; )
          if (!Object.prototype.hasOwnProperty.call(b, keys[i]))
            return false;
        for (i = length; i-- !== 0; ) {
          key = keys[i];
          if (!this.deepEquals(a[key], b[key]))
            return false;
        }
        return true;
      }
      return a !== a && b !== b;
    },
    resolveFieldData(data, field) {
      if (data && Object.keys(data).length && field) {
        if (this.isFunction(field)) {
          return field(data);
        } else if (field.indexOf(".") === -1) {
          return data[field];
        } else {
          let fields = field.split(".");
          let value = data;
          for (var i = 0, len = fields.length; i < len; ++i) {
            if (value == null) {
              return null;
            }
            value = value[fields[i]];
          }
          return value;
        }
      } else {
        return null;
      }
    },
    isFunction(obj) {
      return !!(obj && obj.constructor && obj.call && obj.apply);
    },
    getItemValue(obj, ...params) {
      return this.isFunction(obj) ? obj(...params) : obj;
    },
    filter(value, fields, filterValue) {
      var filteredItems = [];
      if (value) {
        for (let item of value) {
          for (let field of fields) {
            if (String(this.resolveFieldData(item, field)).toLowerCase().indexOf(filterValue.toLowerCase()) > -1) {
              filteredItems.push(item);
              break;
            }
          }
        }
      }
      return filteredItems;
    },
    reorderArray(value, from, to2) {
      if (value && from !== to2) {
        if (to2 >= value.length) {
          to2 %= value.length;
          from %= value.length;
        }
        value.splice(to2, 0, value.splice(from, 1)[0]);
      }
    },
    findIndexInList(value, list) {
      let index = -1;
      if (list) {
        for (let i = 0; i < list.length; i++) {
          if (list[i] === value) {
            index = i;
            break;
          }
        }
      }
      return index;
    },
    contains(value, list) {
      if (value != null && list && list.length) {
        for (let val of list) {
          if (this.equals(value, val))
            return true;
        }
      }
      return false;
    },
    insertIntoOrderedArray(item, index, arr, sourceArr) {
      if (arr.length > 0) {
        let injected = false;
        for (let i = 0; i < arr.length; i++) {
          let currentItemIndex = this.findIndexInList(arr[i], sourceArr);
          if (currentItemIndex > index) {
            arr.splice(i, 0, item);
            injected = true;
            break;
          }
        }
        if (!injected) {
          arr.push(item);
        }
      } else {
        arr.push(item);
      }
    },
    removeAccents(str) {
      if (str && str.search(/[\xC0-\xFF]/g) > -1) {
        str = str.replace(/[\xC0-\xC5]/g, "A").replace(/[\xC6]/g, "AE").replace(/[\xC7]/g, "C").replace(/[\xC8-\xCB]/g, "E").replace(/[\xCC-\xCF]/g, "I").replace(/[\xD0]/g, "D").replace(/[\xD1]/g, "N").replace(/[\xD2-\xD6\xD8]/g, "O").replace(/[\xD9-\xDC]/g, "U").replace(/[\xDD]/g, "Y").replace(/[\xDE]/g, "P").replace(/[\xE0-\xE5]/g, "a").replace(/[\xE6]/g, "ae").replace(/[\xE7]/g, "c").replace(/[\xE8-\xEB]/g, "e").replace(/[\xEC-\xEF]/g, "i").replace(/[\xF1]/g, "n").replace(/[\xF2-\xF6\xF8]/g, "o").replace(/[\xF9-\xFC]/g, "u").replace(/[\xFE]/g, "p").replace(/[\xFD\xFF]/g, "y");
      }
      return str;
    },
    getVNodeProp(vnode, prop) {
      let props = vnode.props;
      if (props) {
        let kebapProp = prop.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();
        let propName = Object.prototype.hasOwnProperty.call(props, kebapProp) ? kebapProp : prop;
        return vnode.type.props[prop].type === Boolean && props[propName] === "" ? true : props[propName];
      }
      return null;
    },
    isEmpty(value) {
      return value === null || value === void 0 || value === "" || Array.isArray(value) && value.length === 0 || !(value instanceof Date) && typeof value === "object" && Object.keys(value).length === 0;
    },
    isNotEmpty(value) {
      return !this.isEmpty(value);
    },
    isPrintableCharacter(char = "") {
      return this.isNotEmpty(char) && char.length === 1 && char.match(/\S| /);
    },
    /**
     * Firefox-v103 does not currently support the "findLast" method. It is stated that this method will be supported with Firefox-v104.
     * https://caniuse.com/mdn-javascript_builtins_array_findlast
     */
    findLast(arr, callback) {
      let item;
      if (this.isNotEmpty(arr)) {
        try {
          item = arr.findLast(callback);
        } catch {
          item = [...arr].reverse().find(callback);
        }
      }
      return item;
    },
    /**
     * Firefox-v103 does not currently support the "findLastIndex" method. It is stated that this method will be supported with Firefox-v104.
     * https://caniuse.com/mdn-javascript_builtins_array_findlastindex
     */
    findLastIndex(arr, callback) {
      let index = -1;
      if (this.isNotEmpty(arr)) {
        try {
          index = arr.findLastIndex(callback);
        } catch {
          index = arr.lastIndexOf([...arr].reverse().find(callback));
        }
      }
      return index;
    }
  };
  var lastId = 0;
  function UniqueComponentId(prefix = "pv_id_") {
    lastId++;
    return `${prefix}${lastId}`;
  }
  function handler() {
    let zIndexes = [];
    const generateZIndex = (key, autoZIndex, baseZIndex = 999) => {
      const lastZIndex = getLastZIndex(key, autoZIndex, baseZIndex);
      const newZIndex = lastZIndex.value + (lastZIndex.key === key ? 0 : baseZIndex) + 1;
      zIndexes.push({ key, value: newZIndex });
      return newZIndex;
    };
    const revertZIndex = (zIndex) => {
      zIndexes = zIndexes.filter((obj) => obj.value !== zIndex);
    };
    const getCurrentZIndex = (key, autoZIndex) => {
      return getLastZIndex(key, autoZIndex).value;
    };
    const getLastZIndex = (key, autoZIndex, baseZIndex = 0) => {
      return [...zIndexes].reverse().find((obj) => autoZIndex ? true : obj.key === key) || { key, value: baseZIndex };
    };
    const getZIndex = (el) => {
      return el ? parseInt(el.style.zIndex, 10) || 0 : 0;
    };
    return {
      get: getZIndex,
      set: (key, el, baseZIndex) => {
        if (el) {
          el.style.zIndex = String(generateZIndex(key, true, baseZIndex));
        }
      },
      clear: (el) => {
        if (el) {
          revertZIndex(getZIndex(el));
          el.style.zIndex = "";
        }
      },
      getCurrent: (key) => getCurrentZIndex(key, true)
    };
  }
  var ZIndexUtils = handler();
  let timeout;
  function bindEvents(el) {
    el.addEventListener("mousedown", onMouseDown);
  }
  function unbindEvents(el) {
    el.removeEventListener("mousedown", onMouseDown);
  }
  function create(el) {
    let ink = document.createElement("span");
    ink.className = "p-ink";
    ink.setAttribute("role", "presentation");
    ink.setAttribute("aria-hidden", "true");
    el.appendChild(ink);
    ink.addEventListener("animationend", onAnimationEnd);
  }
  function remove(el) {
    let ink = getInk(el);
    if (ink) {
      unbindEvents(el);
      ink.removeEventListener("animationend", onAnimationEnd);
      ink.remove();
    }
  }
  function onMouseDown(event) {
    let target = event.currentTarget;
    let ink = getInk(target);
    if (!ink || getComputedStyle(ink, null).display === "none") {
      return;
    }
    DomHandler.removeClass(ink, "p-ink-active");
    if (!DomHandler.getHeight(ink) && !DomHandler.getWidth(ink)) {
      let d = Math.max(DomHandler.getOuterWidth(target), DomHandler.getOuterHeight(target));
      ink.style.height = d + "px";
      ink.style.width = d + "px";
    }
    let offset = DomHandler.getOffset(target);
    let x = event.pageX - offset.left + document.body.scrollTop - DomHandler.getWidth(ink) / 2;
    let y = event.pageY - offset.top + document.body.scrollLeft - DomHandler.getHeight(ink) / 2;
    ink.style.top = y + "px";
    ink.style.left = x + "px";
    DomHandler.addClass(ink, "p-ink-active");
    timeout = setTimeout(() => {
      if (ink) {
        DomHandler.removeClass(ink, "p-ink-active");
      }
    }, 401);
  }
  function onAnimationEnd(event) {
    if (timeout) {
      clearTimeout(timeout);
    }
    DomHandler.removeClass(event.currentTarget, "p-ink-active");
  }
  function getInk(el) {
    for (let i = 0; i < el.children.length; i++) {
      if (typeof el.children[i].className === "string" && el.children[i].className.indexOf("p-ink") !== -1) {
        return el.children[i];
      }
    }
    return null;
  }
  const Ripple = {
    mounted(el, binding) {
      if (binding.instance.$primevue && binding.instance.$primevue.config && binding.instance.$primevue.config.ripple) {
        create(el);
        bindEvents(el);
      }
    },
    unmounted(el) {
      remove(el);
    }
  };
  var script$4 = {
    name: "Accordion",
    emits: ["update:activeIndex", "tab-open", "tab-close", "tab-click"],
    props: {
      multiple: {
        type: Boolean,
        default: false
      },
      activeIndex: {
        type: [Number, Array],
        default: null
      },
      lazy: {
        type: Boolean,
        default: false
      },
      expandIcon: {
        type: String,
        default: "pi pi-chevron-right"
      },
      collapseIcon: {
        type: String,
        default: "pi pi-chevron-down"
      },
      tabindex: {
        type: Number,
        default: 0
      },
      selectOnFocus: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        id: this.$attrs.id,
        d_activeIndex: this.activeIndex
      };
    },
    watch: {
      "$attrs.id": function(newValue) {
        this.id = newValue || UniqueComponentId();
      },
      activeIndex(newValue) {
        this.d_activeIndex = newValue;
      }
    },
    mounted() {
      this.id = this.id || UniqueComponentId();
    },
    methods: {
      isAccordionTab(child) {
        return child.type.name === "AccordionTab";
      },
      isTabActive(index) {
        return this.multiple ? this.d_activeIndex && this.d_activeIndex.includes(index) : this.d_activeIndex === index;
      },
      getTabProp(tab, name) {
        return tab.props ? tab.props[name] : void 0;
      },
      getKey(tab, index) {
        return this.getTabProp(tab, "header") || index;
      },
      getTabHeaderActionId(index) {
        return `${this.id}_${index}_header_action`;
      },
      getTabContentId(index) {
        return `${this.id}_${index}_content`;
      },
      onTabClick(event, tab, index) {
        this.changeActiveIndex(event, tab, index);
        this.$emit("tab-click", { originalEvent: event, index });
      },
      onTabKeyDown(event, tab, index) {
        switch (event.code) {
          case "ArrowDown":
            this.onTabArrowDownKey(event);
            break;
          case "ArrowUp":
            this.onTabArrowUpKey(event);
            break;
          case "Home":
            this.onTabHomeKey(event);
            break;
          case "End":
            this.onTabEndKey(event);
            break;
          case "Enter":
          case "Space":
            this.onTabEnterKey(event, tab, index);
            break;
        }
      },
      onTabArrowDownKey(event) {
        const nextHeaderAction = this.findNextHeaderAction(event.target.parentElement.parentElement);
        nextHeaderAction ? this.changeFocusedTab(event, nextHeaderAction) : this.onTabHomeKey(event);
        event.preventDefault();
      },
      onTabArrowUpKey(event) {
        const prevHeaderAction = this.findPrevHeaderAction(event.target.parentElement.parentElement);
        prevHeaderAction ? this.changeFocusedTab(event, prevHeaderAction) : this.onTabEndKey(event);
        event.preventDefault();
      },
      onTabHomeKey(event) {
        const firstHeaderAction = this.findFirstHeaderAction();
        this.changeFocusedTab(event, firstHeaderAction);
        event.preventDefault();
      },
      onTabEndKey(event) {
        const lastHeaderAction = this.findLastHeaderAction();
        this.changeFocusedTab(event, lastHeaderAction);
        event.preventDefault();
      },
      onTabEnterKey(event, tab, index) {
        this.changeActiveIndex(event, tab, index);
        event.preventDefault();
      },
      findNextHeaderAction(tabElement, selfCheck = false) {
        const nextTabElement = selfCheck ? tabElement : tabElement.nextElementSibling;
        const headerElement = DomHandler.findSingle(nextTabElement, ".p-accordion-header");
        return headerElement ? DomHandler.hasClass(headerElement, "p-disabled") ? this.findNextHeaderAction(headerElement.parentElement) : DomHandler.findSingle(headerElement, ".p-accordion-header-action") : null;
      },
      findPrevHeaderAction(tabElement, selfCheck = false) {
        const prevTabElement = selfCheck ? tabElement : tabElement.previousElementSibling;
        const headerElement = DomHandler.findSingle(prevTabElement, ".p-accordion-header");
        return headerElement ? DomHandler.hasClass(headerElement, "p-disabled") ? this.findPrevHeaderAction(headerElement.parentElement) : DomHandler.findSingle(headerElement, ".p-accordion-header-action") : null;
      },
      findFirstHeaderAction() {
        return this.findNextHeaderAction(this.$el.firstElementChild, true);
      },
      findLastHeaderAction() {
        return this.findPrevHeaderAction(this.$el.lastElementChild, true);
      },
      changeActiveIndex(event, tab, index) {
        if (!this.getTabProp(tab, "disabled")) {
          const active = this.isTabActive(index);
          const eventName = active ? "tab-close" : "tab-open";
          if (this.multiple) {
            if (active) {
              this.d_activeIndex = this.d_activeIndex.filter((i) => i !== index);
            } else {
              if (this.d_activeIndex)
                this.d_activeIndex.push(index);
              else
                this.d_activeIndex = [index];
            }
          } else {
            this.d_activeIndex = this.d_activeIndex === index ? null : index;
          }
          this.$emit("update:activeIndex", this.d_activeIndex);
          this.$emit(eventName, { originalEvent: event, index });
        }
      },
      changeFocusedTab(event, element) {
        if (element) {
          DomHandler.focus(element);
          if (this.selectOnFocus) {
            const index = parseInt(element.parentElement.parentElement.dataset.index, 10);
            const tab = this.tabs[index];
            this.changeActiveIndex(event, tab, index);
          }
        }
      },
      getTabClass(i) {
        return [
          "p-accordion-tab",
          {
            "p-accordion-tab-active": this.isTabActive(i)
          }
        ];
      },
      getTabHeaderClass(tab, i) {
        return [
          "p-accordion-header",
          this.getTabProp(tab, "headerClass"),
          {
            "p-highlight": this.isTabActive(i),
            "p-disabled": this.getTabProp(tab, "disabled")
          }
        ];
      },
      getTabHeaderIconClass(i) {
        return ["p-accordion-toggle-icon", this.isTabActive(i) ? this.collapseIcon : this.expandIcon];
      },
      getTabContentClass(tab) {
        return ["p-toggleable-content", this.getTabProp(tab, "contentClass")];
      }
    },
    computed: {
      tabs() {
        return this.$slots.default().reduce((tabs, child) => {
          if (this.isAccordionTab(child)) {
            tabs.push(child);
          } else if (child.children && child.children instanceof Array) {
            child.children.forEach((nestedChild) => {
              if (this.isAccordionTab(nestedChild)) {
                tabs.push(nestedChild);
              }
            });
          }
          return tabs;
        }, []);
      }
    },
    directives: {
      ripple: Ripple
    }
  };
  const _hoisted_1$2 = { class: "p-accordion p-component" };
  const _hoisted_2$2 = ["data-index"];
  const _hoisted_3$2 = ["id", "tabindex", "aria-disabled", "aria-expanded", "aria-controls", "onClick", "onKeydown"];
  const _hoisted_4$2 = {
    key: 0,
    class: "p-accordion-header-text"
  };
  const _hoisted_5$2 = ["id", "aria-labelledby"];
  const _hoisted_6$2 = { class: "p-accordion-content" };
  function render$4(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.openBlock(), vue.createElementBlock("div", _hoisted_1$2, [
      (vue.openBlock(true), vue.createElementBlock(vue.Fragment, null, vue.renderList($options.tabs, (tab, i) => {
        return vue.openBlock(), vue.createElementBlock("div", {
          key: $options.getKey(tab, i),
          class: vue.normalizeClass($options.getTabClass(i)),
          "data-index": i
        }, [
          vue.createElementVNode("div", vue.mergeProps({
            style: $options.getTabProp(tab, "headerStyle"),
            class: $options.getTabHeaderClass(tab, i)
          }, $options.getTabProp(tab, "headerProps")), [
            vue.createElementVNode("a", vue.mergeProps({
              id: $options.getTabHeaderActionId(i),
              class: "p-accordion-header-link p-accordion-header-action",
              tabindex: $options.getTabProp(tab, "disabled") ? -1 : $props.tabindex,
              role: "button",
              "aria-disabled": $options.getTabProp(tab, "disabled"),
              "aria-expanded": $options.isTabActive(i),
              "aria-controls": $options.getTabContentId(i),
              onClick: ($event) => $options.onTabClick($event, tab, i),
              onKeydown: ($event) => $options.onTabKeyDown($event, tab, i)
            }, $options.getTabProp(tab, "headerActionProps")), [
              vue.createElementVNode("span", {
                class: vue.normalizeClass($options.getTabHeaderIconClass(i)),
                "aria-hidden": "true"
              }, null, 2),
              tab.props && tab.props.header ? (vue.openBlock(), vue.createElementBlock("span", _hoisted_4$2, vue.toDisplayString(tab.props.header), 1)) : vue.createCommentVNode("", true),
              tab.children && tab.children.header ? (vue.openBlock(), vue.createBlock(vue.resolveDynamicComponent(tab.children.header), { key: 1 })) : vue.createCommentVNode("", true)
            ], 16, _hoisted_3$2)
          ], 16),
          vue.createVNode(vue.Transition, { name: "p-toggleable-content" }, {
            default: vue.withCtx(() => [
              ($props.lazy ? $options.isTabActive(i) : true) ? vue.withDirectives((vue.openBlock(), vue.createElementBlock("div", vue.mergeProps({
                key: 0,
                id: $options.getTabContentId(i),
                style: $options.getTabProp(tab, "contentStyle"),
                class: $options.getTabContentClass(tab),
                role: "region",
                "aria-labelledby": $options.getTabHeaderActionId(i)
              }, $options.getTabProp(tab, "contentProps")), [
                vue.createElementVNode("div", _hoisted_6$2, [
                  (vue.openBlock(), vue.createBlock(vue.resolveDynamicComponent(tab)))
                ])
              ], 16, _hoisted_5$2)), [
                [vue.vShow, $props.lazy ? true : $options.isTabActive(i)]
              ]) : vue.createCommentVNode("", true)
            ]),
            _: 2
          }, 1024)
        ], 10, _hoisted_2$2);
      }), 128))
    ]);
  }
  function styleInject$1(css, ref) {
    if (ref === void 0)
      ref = {};
    var insertAt = ref.insertAt;
    if (!css || typeof document === "undefined") {
      return;
    }
    var head = document.head || document.getElementsByTagName("head")[0];
    var style2 = document.createElement("style");
    style2.type = "text/css";
    if (insertAt === "top") {
      if (head.firstChild) {
        head.insertBefore(style2, head.firstChild);
      } else {
        head.appendChild(style2);
      }
    } else {
      head.appendChild(style2);
    }
    if (style2.styleSheet) {
      style2.styleSheet.cssText = css;
    } else {
      style2.appendChild(document.createTextNode(css));
    }
  }
  var css_248z$1 = "\n.p-accordion-header-action {\n    cursor: pointer;\n    display: flex;\n    align-items: center;\n    user-select: none;\n    position: relative;\n    text-decoration: none;\n}\n.p-accordion-header-action:focus {\n    z-index: 1;\n}\n.p-accordion-header-text {\n    line-height: 1;\n}\n";
  styleInject$1(css_248z$1);
  script$4.render = render$4;
  var script$3 = {
    name: "AccordionTab",
    props: {
      header: null,
      headerStyle: null,
      headerClass: null,
      headerProps: null,
      headerActionProps: null,
      contentStyle: null,
      contentClass: null,
      contentProps: null,
      disabled: Boolean
    }
  };
  function render$3(_ctx, _cache, $props, $setup, $data, $options) {
    return vue.renderSlot(_ctx.$slots, "default");
  }
  script$3.render = render$3;
  var script$2 = {
    name: "Portal",
    props: {
      appendTo: {
        type: String,
        default: "body"
      },
      disabled: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        mounted: false
      };
    },
    mounted() {
      this.mounted = DomHandler.isClient();
    },
    computed: {
      inline() {
        return this.disabled || this.appendTo === "self";
      }
    }
  };
  function render$2(_ctx, _cache, $props, $setup, $data, $options) {
    return $options.inline ? vue.renderSlot(_ctx.$slots, "default", { key: 0 }) : $data.mounted ? (vue.openBlock(), vue.createBlock(vue.Teleport, {
      key: 1,
      to: $props.appendTo
    }, [
      vue.renderSlot(_ctx.$slots, "default")
    ], 8, ["to"])) : vue.createCommentVNode("", true);
  }
  script$2.render = render$2;
  var script$1 = {
    name: "ContextMenuSub",
    emits: ["item-click", "item-mouseenter"],
    props: {
      items: {
        type: Array,
        default: null
      },
      menuId: {
        type: String,
        default: null
      },
      focusedItemId: {
        type: String,
        default: null
      },
      root: {
        type: Boolean,
        default: false
      },
      visible: {
        type: Boolean,
        default: false
      },
      level: {
        type: Number,
        default: 0
      },
      template: {
        type: Function,
        default: null
      },
      exact: {
        type: Boolean,
        default: true
      },
      activeItemPath: {
        type: Object,
        default: null
      }
    },
    methods: {
      getItemId(processedItem) {
        return `${this.menuId}_${processedItem.key}`;
      },
      getItemKey(processedItem) {
        return this.getItemId(processedItem);
      },
      getItemProp(processedItem, name, params) {
        return processedItem && processedItem.item ? ObjectUtils.getItemValue(processedItem.item[name], params) : void 0;
      },
      getItemLabel(processedItem) {
        return this.getItemProp(processedItem, "label");
      },
      isItemActive(processedItem) {
        return this.activeItemPath.some((path) => path.key === processedItem.key);
      },
      isItemVisible(processedItem) {
        return this.getItemProp(processedItem, "visible") !== false;
      },
      isItemDisabled(processedItem) {
        return this.getItemProp(processedItem, "disabled");
      },
      isItemFocused(processedItem) {
        return this.focusedItemId === this.getItemId(processedItem);
      },
      isItemGroup(processedItem) {
        return ObjectUtils.isNotEmpty(processedItem.items);
      },
      onItemClick(event, processedItem) {
        this.getItemProp(processedItem, "command", { originalEvent: event, item: processedItem.item });
        this.$emit("item-click", { originalEvent: event, processedItem, isFocus: true });
      },
      onItemMouseEnter(event, processedItem) {
        this.$emit("item-mouseenter", { originalEvent: event, processedItem });
      },
      onItemActionClick(event, navigate) {
        navigate && navigate(event);
      },
      getAriaSetSize() {
        return this.items.filter((processedItem) => this.isItemVisible(processedItem) && !this.getItemProp(processedItem, "separator")).length;
      },
      getAriaPosInset(index) {
        return index - this.items.slice(0, index).filter((processedItem) => this.isItemVisible(processedItem) && this.getItemProp(processedItem, "separator")).length + 1;
      },
      onEnter() {
        this.position();
      },
      position() {
        const parentItem = this.$refs.container.parentElement;
        const containerOffset = DomHandler.getOffset(this.$refs.container.parentElement);
        const viewport = DomHandler.getViewport();
        const sublistWidth = this.$refs.container.offsetParent ? this.$refs.container.offsetWidth : DomHandler.getHiddenElementOuterWidth(this.$refs.container);
        const itemOuterWidth = DomHandler.getOuterWidth(parentItem.children[0]);
        this.$refs.container.style.top = "0px";
        if (parseInt(containerOffset.left, 10) + itemOuterWidth + sublistWidth > viewport.width - DomHandler.calculateScrollbarWidth()) {
          this.$refs.container.style.left = -1 * sublistWidth + "px";
        } else {
          this.$refs.container.style.left = itemOuterWidth + "px";
        }
      },
      getItemClass(processedItem) {
        return [
          "p-menuitem",
          this.getItemProp(processedItem, "class"),
          {
            "p-menuitem-active p-highlight": this.isItemActive(processedItem),
            "p-focus": this.isItemFocused(processedItem),
            "p-disabled": this.isItemDisabled(processedItem)
          }
        ];
      },
      getItemActionClass(processedItem, routerProps) {
        return [
          "p-menuitem-link",
          {
            "router-link-active": routerProps && routerProps.isActive,
            "router-link-active-exact": this.exact && routerProps && routerProps.isExactActive
          }
        ];
      },
      getItemIconClass(processedItem) {
        return ["p-menuitem-icon", this.getItemProp(processedItem, "icon")];
      },
      getSeparatorItemClass(processedItem) {
        return ["p-menuitem-separator", this.getItemProp(processedItem, "class")];
      }
    },
    directives: {
      ripple: Ripple
    }
  };
  const _hoisted_1$1 = {
    key: 0,
    ref: "container"
  };
  const _hoisted_2$1 = ["id", "aria-label", "aria-disabled", "aria-expanded", "aria-haspopup", "aria-level", "aria-setsize", "aria-posinset"];
  const _hoisted_3$1 = ["onClick", "onMouseenter"];
  const _hoisted_4$1 = ["href", "onClick"];
  const _hoisted_5$1 = { class: "p-menuitem-text" };
  const _hoisted_6$1 = ["href", "target"];
  const _hoisted_7$1 = { class: "p-menuitem-text" };
  const _hoisted_8$1 = {
    key: 1,
    class: "p-submenu-icon pi pi-angle-right"
  };
  const _hoisted_9$1 = ["id"];
  function render$1(_ctx, _cache, $props, $setup, $data, $options) {
    const _component_router_link = vue.resolveComponent("router-link");
    const _component_ContextMenuSub = vue.resolveComponent("ContextMenuSub", true);
    const _directive_ripple = vue.resolveDirective("ripple");
    return vue.openBlock(), vue.createBlock(vue.Transition, {
      name: "p-contextmenusub",
      onEnter: $options.onEnter
    }, {
      default: vue.withCtx(() => [
        ($props.root ? true : $props.visible) ? (vue.openBlock(), vue.createElementBlock("ul", _hoisted_1$1, [
          (vue.openBlock(true), vue.createElementBlock(vue.Fragment, null, vue.renderList($props.items, (processedItem, index) => {
            return vue.openBlock(), vue.createElementBlock(vue.Fragment, {
              key: $options.getItemKey(processedItem)
            }, [
              $options.isItemVisible(processedItem) && !$options.getItemProp(processedItem, "separator") ? (vue.openBlock(), vue.createElementBlock("li", {
                key: 0,
                id: $options.getItemId(processedItem),
                style: vue.normalizeStyle($options.getItemProp(processedItem, "style")),
                class: vue.normalizeClass($options.getItemClass(processedItem)),
                role: "menuitem",
                "aria-label": $options.getItemLabel(processedItem),
                "aria-disabled": $options.isItemDisabled(processedItem) || void 0,
                "aria-expanded": $options.isItemGroup(processedItem) ? $options.isItemActive(processedItem) : void 0,
                "aria-haspopup": $options.isItemGroup(processedItem) && !$options.getItemProp(processedItem, "to") ? "menu" : void 0,
                "aria-level": $props.level + 1,
                "aria-setsize": $options.getAriaSetSize(),
                "aria-posinset": $options.getAriaPosInset(index)
              }, [
                vue.createElementVNode("div", {
                  class: "p-menuitem-content",
                  onClick: ($event) => $options.onItemClick($event, processedItem),
                  onMouseenter: ($event) => $options.onItemMouseEnter($event, processedItem)
                }, [
                  !$props.template ? (vue.openBlock(), vue.createElementBlock(vue.Fragment, { key: 0 }, [
                    $options.getItemProp(processedItem, "to") && !$options.isItemDisabled(processedItem) ? (vue.openBlock(), vue.createBlock(_component_router_link, {
                      key: 0,
                      to: $options.getItemProp(processedItem, "to"),
                      custom: ""
                    }, {
                      default: vue.withCtx(({ navigate, href, isActive, isExactActive }) => [
                        vue.withDirectives((vue.openBlock(), vue.createElementBlock("a", {
                          href,
                          class: vue.normalizeClass($options.getItemActionClass(processedItem, { isActive, isExactActive })),
                          tabindex: "-1",
                          "aria-hidden": "true",
                          onClick: ($event) => $options.onItemActionClick($event, navigate)
                        }, [
                          $options.getItemProp(processedItem, "icon") ? (vue.openBlock(), vue.createElementBlock("span", {
                            key: 0,
                            class: vue.normalizeClass($options.getItemIconClass(processedItem))
                          }, null, 2)) : vue.createCommentVNode("", true),
                          vue.createElementVNode("span", _hoisted_5$1, vue.toDisplayString($options.getItemLabel(processedItem)), 1)
                        ], 10, _hoisted_4$1)), [
                          [_directive_ripple]
                        ])
                      ]),
                      _: 2
                    }, 1032, ["to"])) : vue.withDirectives((vue.openBlock(), vue.createElementBlock("a", {
                      key: 1,
                      href: $options.getItemProp(processedItem, "url"),
                      class: vue.normalizeClass($options.getItemActionClass(processedItem)),
                      target: $options.getItemProp(processedItem, "target"),
                      tabindex: "-1",
                      "aria-hidden": "true"
                    }, [
                      $options.getItemProp(processedItem, "icon") ? (vue.openBlock(), vue.createElementBlock("span", {
                        key: 0,
                        class: vue.normalizeClass($options.getItemIconClass(processedItem))
                      }, null, 2)) : vue.createCommentVNode("", true),
                      vue.createElementVNode("span", _hoisted_7$1, vue.toDisplayString($options.getItemLabel(processedItem)), 1),
                      $options.getItemProp(processedItem, "items") ? (vue.openBlock(), vue.createElementBlock("span", _hoisted_8$1)) : vue.createCommentVNode("", true)
                    ], 10, _hoisted_6$1)), [
                      [_directive_ripple]
                    ])
                  ], 64)) : (vue.openBlock(), vue.createBlock(vue.resolveDynamicComponent($props.template), {
                    key: 1,
                    item: processedItem.item
                  }, null, 8, ["item"]))
                ], 40, _hoisted_3$1),
                $options.isItemVisible(processedItem) && $options.isItemGroup(processedItem) ? (vue.openBlock(), vue.createBlock(_component_ContextMenuSub, {
                  key: 0,
                  id: $options.getItemId(processedItem) + "_list",
                  role: "menu",
                  class: "p-submenu-list",
                  menuId: $props.menuId,
                  focusedItemId: $props.focusedItemId,
                  items: processedItem.items,
                  template: $props.template,
                  activeItemPath: $props.activeItemPath,
                  exact: $props.exact,
                  level: $props.level + 1,
                  visible: $options.isItemActive(processedItem) && $options.isItemGroup(processedItem),
                  onItemClick: _cache[0] || (_cache[0] = ($event) => _ctx.$emit("item-click", $event)),
                  onItemMouseenter: _cache[1] || (_cache[1] = ($event) => _ctx.$emit("item-mouseenter", $event))
                }, null, 8, ["id", "menuId", "focusedItemId", "items", "template", "activeItemPath", "exact", "level", "visible"])) : vue.createCommentVNode("", true)
              ], 14, _hoisted_2$1)) : vue.createCommentVNode("", true),
              $options.isItemVisible(processedItem) && $options.getItemProp(processedItem, "separator") ? (vue.openBlock(), vue.createElementBlock("li", {
                key: 1,
                id: $options.getItemId(processedItem),
                style: vue.normalizeStyle($options.getItemProp(processedItem, "style")),
                class: vue.normalizeClass($options.getSeparatorItemClass(processedItem)),
                role: "separator"
              }, null, 14, _hoisted_9$1)) : vue.createCommentVNode("", true)
            ], 64);
          }), 128))
        ], 512)) : vue.createCommentVNode("", true)
      ]),
      _: 1
    }, 8, ["onEnter"]);
  }
  script$1.render = render$1;
  var script = {
    name: "ContextMenu",
    inheritAttrs: false,
    emits: ["focus", "blur", "show", "hide"],
    props: {
      model: {
        type: Array,
        default: null
      },
      appendTo: {
        type: String,
        default: "body"
      },
      autoZIndex: {
        type: Boolean,
        default: true
      },
      baseZIndex: {
        type: Number,
        default: 0
      },
      global: {
        type: Boolean,
        default: false
      },
      exact: {
        type: Boolean,
        default: true
      },
      tabindex: {
        type: Number,
        default: 0
      },
      "aria-labelledby": {
        type: String,
        default: null
      },
      "aria-label": {
        type: String,
        default: null
      }
    },
    target: null,
    outsideClickListener: null,
    resizeListener: null,
    documentContextMenuListener: null,
    pageX: null,
    pageY: null,
    container: null,
    list: null,
    data() {
      return {
        id: this.$attrs.id,
        focused: false,
        focusedItemInfo: { index: -1, level: 0, parentKey: "" },
        activeItemPath: [],
        visible: false,
        submenuVisible: false
      };
    },
    watch: {
      "$attrs.id": function(newValue) {
        this.id = newValue || UniqueComponentId();
      },
      activeItemPath(newPath) {
        if (ObjectUtils.isNotEmpty(newPath)) {
          this.bindOutsideClickListener();
          this.bindResizeListener();
          this.bindDocumentContextMenuListener();
        } else if (!this.visible) {
          this.unbindOutsideClickListener();
          this.unbindResizeListener();
          this.unbindDocumentContextMenuListener();
        }
      }
    },
    beforeUnmount() {
      this.unbindResizeListener();
      this.unbindOutsideClickListener();
      this.unbindDocumentContextMenuListener();
      if (this.container && this.autoZIndex) {
        ZIndexUtils.clear(this.container);
      }
      this.target = null;
      this.container = null;
    },
    mounted() {
      this.id = this.id || UniqueComponentId();
      if (this.global) {
        this.bindDocumentContextMenuListener();
      }
    },
    methods: {
      getItemProp(item, name) {
        return item ? ObjectUtils.getItemValue(item[name]) : void 0;
      },
      getItemLabel(item) {
        return this.getItemProp(item, "label");
      },
      isItemDisabled(item) {
        return this.getItemProp(item, "disabled");
      },
      isItemGroup(item) {
        return ObjectUtils.isNotEmpty(this.getItemProp(item, "items"));
      },
      isItemSeparator(item) {
        return this.getItemProp(item, "separator");
      },
      getProccessedItemLabel(processedItem) {
        return processedItem ? this.getItemLabel(processedItem.item) : void 0;
      },
      isProccessedItemGroup(processedItem) {
        return processedItem && ObjectUtils.isNotEmpty(processedItem.items);
      },
      toggle(event) {
        this.visible ? this.hide() : this.show(event);
      },
      show(event) {
        this.activeItemPath = [];
        this.focusedItemInfo = { index: -1, level: 0, parentKey: "" };
        DomHandler.focus(this.list);
        this.pageX = event.pageX;
        this.pageY = event.pageY;
        this.visible ? this.position() : this.visible = true;
        event.stopPropagation();
        event.preventDefault();
      },
      hide() {
        this.visible = false;
        this.activeItemPath = [];
        this.focusedItemInfo = { index: -1, level: 0, parentKey: "" };
      },
      onFocus(event) {
        this.focused = true;
        this.focusedItemInfo = this.focusedItemInfo.index !== -1 ? this.focusedItemInfo : { index: -1, level: 0, parentKey: "" };
        this.$emit("focus", event);
      },
      onBlur(event) {
        this.focused = false;
        this.focusedItemInfo = { index: -1, level: 0, parentKey: "" };
        this.searchValue = "";
        this.$emit("blur", event);
      },
      onKeyDown(event) {
        const metaKey = event.metaKey || event.ctrlKey;
        switch (event.code) {
          case "ArrowDown":
            this.onArrowDownKey(event);
            break;
          case "ArrowUp":
            this.onArrowUpKey(event);
            break;
          case "ArrowLeft":
            this.onArrowLeftKey(event);
            break;
          case "ArrowRight":
            this.onArrowRightKey(event);
            break;
          case "Home":
            this.onHomeKey(event);
            break;
          case "End":
            this.onEndKey(event);
            break;
          case "Space":
            this.onSpaceKey(event);
            break;
          case "Enter":
            this.onEnterKey(event);
            break;
          case "Escape":
            this.onEscapeKey(event);
            break;
          case "Tab":
            this.onTabKey(event);
            break;
          case "PageDown":
          case "PageUp":
          case "Backspace":
          case "ShiftLeft":
          case "ShiftRight":
            break;
          default:
            if (!metaKey && ObjectUtils.isPrintableCharacter(event.key)) {
              this.searchItems(event, event.key);
            }
            break;
        }
      },
      onItemChange(event) {
        const { processedItem, isFocus } = event;
        if (ObjectUtils.isEmpty(processedItem))
          return;
        const { index, key, level, parentKey, items } = processedItem;
        const grouped = ObjectUtils.isNotEmpty(items);
        const activeItemPath = this.activeItemPath.filter((p2) => p2.parentKey !== parentKey && p2.parentKey !== key);
        if (grouped) {
          activeItemPath.push(processedItem);
          this.submenuVisible = true;
        }
        this.focusedItemInfo = { index, level, parentKey };
        this.activeItemPath = activeItemPath;
        isFocus && DomHandler.focus(this.list);
      },
      onItemClick(event) {
        const { processedItem } = event;
        const grouped = this.isProccessedItemGroup(processedItem);
        const selected = this.isSelected(processedItem);
        if (selected) {
          const { index, key, level, parentKey } = processedItem;
          this.activeItemPath = this.activeItemPath.filter((p2) => key !== p2.key && key.startsWith(p2.key));
          this.focusedItemInfo = { index, level, parentKey };
          DomHandler.focus(this.list);
        } else {
          grouped ? this.onItemChange(event) : this.hide();
        }
      },
      onItemMouseEnter(event) {
        this.onItemChange(event);
      },
      onArrowDownKey(event) {
        const itemIndex = this.focusedItemInfo.index !== -1 ? this.findNextItemIndex(this.focusedItemInfo.index) : this.findFirstFocusedItemIndex();
        this.changeFocusedItemIndex(event, itemIndex);
        event.preventDefault();
      },
      onArrowUpKey(event) {
        if (event.altKey) {
          if (this.focusedItemInfo.index !== -1) {
            const processedItem = this.visibleItems[this.focusedItemInfo.index];
            const grouped = this.isProccessedItemGroup(processedItem);
            !grouped && this.onItemChange({ originalEvent: event, processedItem });
          }
          this.popup && this.hide();
          event.preventDefault();
        } else {
          const itemIndex = this.focusedItemInfo.index !== -1 ? this.findPrevItemIndex(this.focusedItemInfo.index) : this.findLastFocusedItemIndex();
          this.changeFocusedItemIndex(event, itemIndex);
          event.preventDefault();
        }
      },
      onArrowLeftKey(event) {
        const processedItem = this.visibleItems[this.focusedItemInfo.index];
        const parentItem = this.activeItemPath.find((p2) => p2.key === processedItem.parentKey);
        const root = ObjectUtils.isEmpty(processedItem.parent);
        if (!root) {
          this.focusedItemInfo = { index: -1, parentKey: parentItem ? parentItem.parentKey : "" };
          this.searchValue = "";
          this.onArrowDownKey(event);
        }
        this.activeItemPath = this.activeItemPath.filter((p2) => p2.parentKey !== this.focusedItemInfo.parentKey);
        event.preventDefault();
      },
      onArrowRightKey(event) {
        const processedItem = this.visibleItems[this.focusedItemInfo.index];
        const grouped = this.isProccessedItemGroup(processedItem);
        if (grouped) {
          this.onItemChange({ originalEvent: event, processedItem });
          this.focusedItemInfo = { index: -1, parentKey: processedItem.key };
          this.searchValue = "";
          this.onArrowDownKey(event);
        }
        event.preventDefault();
      },
      onHomeKey(event) {
        this.changeFocusedItemIndex(event, this.findFirstItemIndex());
        event.preventDefault();
      },
      onEndKey(event) {
        this.changeFocusedItemIndex(event, this.findLastItemIndex());
        event.preventDefault();
      },
      onEnterKey(event) {
        if (this.focusedItemInfo.index !== -1) {
          const element = DomHandler.findSingle(this.list, `li[id="${`${this.focusedItemId}`}"]`);
          const anchorElement = element && DomHandler.findSingle(element, ".p-menuitem-link");
          anchorElement ? anchorElement.click() : element && element.click();
          const processedItem = this.visibleItems[this.focusedItemInfo.index];
          const grouped = this.isProccessedItemGroup(processedItem);
          !grouped && (this.focusedItemInfo.index = this.findFirstFocusedItemIndex());
        }
        event.preventDefault();
      },
      onSpaceKey(event) {
        this.onEnterKey(event);
      },
      onEscapeKey(event) {
        this.hide();
        !this.popup && (this.focusedItemInfo.index = this.findFirstFocusedItemIndex());
        event.preventDefault();
      },
      onTabKey(event) {
        if (this.focusedItemInfo.index !== -1) {
          const processedItem = this.visibleItems[this.focusedItemInfo.index];
          const grouped = this.isProccessedItemGroup(processedItem);
          !grouped && this.onItemChange({ originalEvent: event, processedItem });
        }
        this.hide();
      },
      onEnter(el) {
        this.position();
        if (this.autoZIndex) {
          ZIndexUtils.set("menu", el, this.baseZIndex + this.$primevue.config.zIndex.menu);
        }
      },
      onAfterEnter() {
        this.bindOutsideClickListener();
        this.bindResizeListener();
        this.bindDocumentContextMenuListener();
        this.$emit("show");
        DomHandler.focus(this.list);
      },
      onLeave() {
        this.$emit("hide");
        this.container = null;
      },
      onAfterLeave(el) {
        if (this.autoZIndex) {
          ZIndexUtils.clear(el);
        }
        this.unbindOutsideClickListener();
        this.unbindResizeListener();
        this.unbindDocumentContextMenuListener();
      },
      position() {
        let left = this.pageX + 1;
        let top = this.pageY + 1;
        let width = this.container.offsetParent ? this.container.offsetWidth : DomHandler.getHiddenElementOuterWidth(this.container);
        let height = this.container.offsetParent ? this.container.offsetHeight : DomHandler.getHiddenElementOuterHeight(this.container);
        let viewport = DomHandler.getViewport();
        if (left + width - document.body.scrollLeft > viewport.width) {
          left -= width;
        }
        if (top + height - document.body.scrollTop > viewport.height) {
          top -= height;
        }
        if (left < document.body.scrollLeft) {
          left = document.body.scrollLeft;
        }
        if (top < document.body.scrollTop) {
          top = document.body.scrollTop;
        }
        this.container.style.left = left + "px";
        this.container.style.top = top + "px";
      },
      bindOutsideClickListener() {
        if (!this.outsideClickListener) {
          this.outsideClickListener = (event) => {
            const isOutsideContainer = this.container && !this.container.contains(event.target);
            const isOutsideTarget = this.visible ? !(this.target && (this.target === event.target || this.target.contains(event.target))) : true;
            if (isOutsideContainer && isOutsideTarget) {
              this.hide();
            }
          };
          document.addEventListener("click", this.outsideClickListener);
        }
      },
      unbindOutsideClickListener() {
        if (this.outsideClickListener) {
          document.removeEventListener("click", this.outsideClickListener);
          this.outsideClickListener = null;
        }
      },
      bindResizeListener() {
        if (!this.resizeListener) {
          this.resizeListener = () => {
            if (this.visible && !DomHandler.isTouchDevice()) {
              this.hide();
            }
          };
          window.addEventListener("resize", this.resizeListener);
        }
      },
      unbindResizeListener() {
        if (this.resizeListener) {
          window.removeEventListener("resize", this.resizeListener);
          this.resizeListener = null;
        }
      },
      bindDocumentContextMenuListener() {
        if (!this.documentContextMenuListener) {
          this.documentContextMenuListener = (event) => {
            event.button !== 2 ? this.show(event) : this.hide();
          };
          document.addEventListener("contextmenu", this.documentContextMenuListener);
        }
      },
      unbindDocumentContextMenuListener() {
        if (this.documentContextMenuListener) {
          document.removeEventListener("contextmenu", this.documentContextMenuListener);
          this.documentContextMenuListener = null;
        }
      },
      isItemMatched(processedItem) {
        return this.isValidItem(processedItem) && this.getProccessedItemLabel(processedItem).toLocaleLowerCase().startsWith(this.searchValue.toLocaleLowerCase());
      },
      isValidItem(processedItem) {
        return !!processedItem && !this.isItemDisabled(processedItem.item) && !this.isItemSeparator(processedItem.item);
      },
      isValidSelectedItem(processedItem) {
        return this.isValidItem(processedItem) && this.isSelected(processedItem);
      },
      isSelected(processedItem) {
        return this.activeItemPath.some((p2) => p2.key === processedItem.key);
      },
      findFirstItemIndex() {
        return this.visibleItems.findIndex((processedItem) => this.isValidItem(processedItem));
      },
      findLastItemIndex() {
        return ObjectUtils.findLastIndex(this.visibleItems, (processedItem) => this.isValidItem(processedItem));
      },
      findNextItemIndex(index) {
        const matchedItemIndex = index < this.visibleItems.length - 1 ? this.visibleItems.slice(index + 1).findIndex((processedItem) => this.isValidItem(processedItem)) : -1;
        return matchedItemIndex > -1 ? matchedItemIndex + index + 1 : index;
      },
      findPrevItemIndex(index) {
        const matchedItemIndex = index > 0 ? ObjectUtils.findLastIndex(this.visibleItems.slice(0, index), (processedItem) => this.isValidItem(processedItem)) : -1;
        return matchedItemIndex > -1 ? matchedItemIndex : index;
      },
      findSelectedItemIndex() {
        return this.visibleItems.findIndex((processedItem) => this.isValidSelectedItem(processedItem));
      },
      findFirstFocusedItemIndex() {
        const selectedIndex = this.findSelectedItemIndex();
        return selectedIndex < 0 ? this.findFirstItemIndex() : selectedIndex;
      },
      findLastFocusedItemIndex() {
        const selectedIndex = this.findSelectedItemIndex();
        return selectedIndex < 0 ? this.findLastItemIndex() : selectedIndex;
      },
      searchItems(event, char) {
        this.searchValue = (this.searchValue || "") + char;
        let itemIndex = -1;
        let matched = false;
        if (this.focusedItemInfo.index !== -1) {
          itemIndex = this.visibleItems.slice(this.focusedItemInfo.index).findIndex((processedItem) => this.isItemMatched(processedItem));
          itemIndex = itemIndex === -1 ? this.visibleItems.slice(0, this.focusedItemInfo.index).findIndex((processedItem) => this.isItemMatched(processedItem)) : itemIndex + this.focusedItemInfo.index;
        } else {
          itemIndex = this.visibleItems.findIndex((processedItem) => this.isItemMatched(processedItem));
        }
        if (itemIndex !== -1) {
          matched = true;
        }
        if (itemIndex === -1 && this.focusedItemInfo.index === -1) {
          itemIndex = this.findFirstFocusedItemIndex();
        }
        if (itemIndex !== -1) {
          this.changeFocusedItemIndex(event, itemIndex);
        }
        if (this.searchTimeout) {
          clearTimeout(this.searchTimeout);
        }
        this.searchTimeout = setTimeout(() => {
          this.searchValue = "";
          this.searchTimeout = null;
        }, 500);
        return matched;
      },
      changeFocusedItemIndex(event, index) {
        if (this.focusedItemInfo.index !== index) {
          this.focusedItemInfo.index = index;
          this.scrollInView();
        }
      },
      scrollInView(index = -1) {
        const id = index !== -1 ? `${this.id}_${index}` : this.focusedItemId;
        const element = DomHandler.findSingle(this.list, `li[id="${id}"]`);
        if (element) {
          element.scrollIntoView && element.scrollIntoView({ block: "nearest", inline: "start" });
        }
      },
      createProcessedItems(items, level = 0, parent = {}, parentKey = "") {
        const processedItems = [];
        items && items.forEach((item, index) => {
          const key = (parentKey !== "" ? parentKey + "_" : "") + index;
          const newItem = {
            item,
            index,
            level,
            key,
            parent,
            parentKey
          };
          newItem["items"] = this.createProcessedItems(item.items, level + 1, newItem, key);
          processedItems.push(newItem);
        });
        return processedItems;
      },
      containerRef(el) {
        this.container = el;
      },
      listRef(el) {
        this.list = el ? el.$el : void 0;
      }
    },
    computed: {
      containerClass() {
        return ["p-contextmenu p-component", { "p-input-filled": this.$primevue.config.inputStyle === "filled", "p-ripple-disabled": this.$primevue.config.ripple === false }];
      },
      processedItems() {
        return this.createProcessedItems(this.model || []);
      },
      visibleItems() {
        const processedItem = this.activeItemPath.find((p2) => p2.key === this.focusedItemInfo.parentKey);
        return processedItem ? processedItem.items : this.processedItems;
      },
      focusedItemId() {
        return this.focusedItemInfo.index !== -1 ? `${this.id}${ObjectUtils.isNotEmpty(this.focusedItemInfo.parentKey) ? "_" + this.focusedItemInfo.parentKey : ""}_${this.focusedItemInfo.index}` : null;
      }
    },
    components: {
      ContextMenuSub: script$1,
      Portal: script$2
    }
  };
  function render(_ctx, _cache, $props, $setup, $data, $options) {
    const _component_ContextMenuSub = vue.resolveComponent("ContextMenuSub");
    const _component_Portal = vue.resolveComponent("Portal");
    return vue.openBlock(), vue.createBlock(_component_Portal, { appendTo: $props.appendTo }, {
      default: vue.withCtx(() => [
        vue.createVNode(vue.Transition, {
          name: "p-contextmenu",
          onEnter: $options.onEnter,
          onAfterEnter: $options.onAfterEnter,
          onLeave: $options.onLeave,
          onAfterLeave: $options.onAfterLeave
        }, {
          default: vue.withCtx(() => [
            $data.visible ? (vue.openBlock(), vue.createElementBlock("div", vue.mergeProps({
              key: 0,
              ref: $options.containerRef,
              class: $options.containerClass
            }, _ctx.$attrs), [
              vue.createVNode(_component_ContextMenuSub, {
                ref: $options.listRef,
                id: $data.id + "_list",
                class: "p-contextmenu-root-list",
                role: "menubar",
                root: true,
                tabindex: $props.tabindex,
                "aria-orientation": "vertical",
                "aria-activedescendant": $data.focused ? $options.focusedItemId : void 0,
                menuId: $data.id,
                focusedItemId: $data.focused ? $options.focusedItemId : void 0,
                items: $options.processedItems,
                template: _ctx.$slots.item,
                activeItemPath: $data.activeItemPath,
                exact: $props.exact,
                "aria-labelledby": _ctx.ariaLabelledby,
                "aria-label": _ctx.ariaLabel,
                level: 0,
                visible: $data.submenuVisible,
                onFocus: $options.onFocus,
                onBlur: $options.onBlur,
                onKeydown: $options.onKeyDown,
                onItemClick: $options.onItemClick,
                onItemMouseenter: $options.onItemMouseEnter
              }, null, 8, ["id", "tabindex", "aria-activedescendant", "menuId", "focusedItemId", "items", "template", "activeItemPath", "exact", "aria-labelledby", "aria-label", "visible", "onFocus", "onBlur", "onKeydown", "onItemClick", "onItemMouseenter"])
            ], 16)) : vue.createCommentVNode("", true)
          ]),
          _: 1
        }, 8, ["onEnter", "onAfterEnter", "onLeave", "onAfterLeave"])
      ]),
      _: 1
    }, 8, ["appendTo"]);
  }
  function styleInject(css, ref) {
    if (ref === void 0)
      ref = {};
    var insertAt = ref.insertAt;
    if (!css || typeof document === "undefined") {
      return;
    }
    var head = document.head || document.getElementsByTagName("head")[0];
    var style2 = document.createElement("style");
    style2.type = "text/css";
    if (insertAt === "top") {
      if (head.firstChild) {
        head.insertBefore(style2, head.firstChild);
      } else {
        head.appendChild(style2);
      }
    } else {
      head.appendChild(style2);
    }
    if (style2.styleSheet) {
      style2.styleSheet.cssText = css;
    } else {
      style2.appendChild(document.createTextNode(css));
    }
  }
  var css_248z = "\n.p-contextmenu {\n    position: absolute;\n}\n.p-contextmenu ul {\n    margin: 0;\n    padding: 0;\n    list-style: none;\n}\n.p-contextmenu .p-submenu-list {\n    position: absolute;\n    min-width: 100%;\n    z-index: 1;\n}\n.p-contextmenu .p-menuitem-link {\n    cursor: pointer;\n    display: flex;\n    align-items: center;\n    text-decoration: none;\n    overflow: hidden;\n    position: relative;\n}\n.p-contextmenu .p-menuitem-text {\n    line-height: 1;\n}\n.p-contextmenu .p-menuitem {\n    position: relative;\n}\n.p-contextmenu .p-menuitem-link .p-submenu-icon {\n    margin-left: auto;\n}\n.p-contextmenu-enter-from {\n    opacity: 0;\n}\n.p-contextmenu-enter-active {\n    transition: opacity 250ms;\n}\n";
  styleInject(css_248z);
  script.render = render;
  const Cockpit_vue_vue_type_style_index_0_lang = "";
  const _hoisted_1 = { style: { "height": "100%", "display": "grid", "grid-auto-flow": "column", "grid-auto-columns": "auto minmax(0, 1fr)" } };
  const _hoisted_2 = { class: "cockpit-palette" };
  const _hoisted_3 = /* @__PURE__ */ vue.createElementVNode("div", null, "Palette", -1);
  const _hoisted_4 = { style: { "width": "100%" } };
  const _hoisted_5 = ["tile_category", "tile_class", "default_params"];
  const _hoisted_6 = { style: { "display": "flex", "justify-content": "space-evenly", "padding": "12px" } };
  const _hoisted_7 = ["innerHTML"];
  const _hoisted_8 = { class: "frame-overlay" };
  const _hoisted_9 = {
    key: 0,
    class: "title"
  };
  const _hoisted_10 = {
    key: 1,
    class: "remove"
  };
  const _hoisted_11 = ["onClick"];
  const _hoisted_12 = ["onClick"];
  const _hoisted_13 = ["innerHTML"];
  const _hoisted_14 = /* @__PURE__ */ vue.createElementVNode("ul", null, [
    /* @__PURE__ */ vue.createElementVNode("li", null, "Ajouter une tuile"),
    /* @__PURE__ */ vue.createElementVNode("li", null, "Supprimer une tuile"),
    /* @__PURE__ */ vue.createElementVNode("li", null, "Déplacer une tuile"),
    /* @__PURE__ */ vue.createElementVNode("li", null, "Changer la taille d'une tuile")
  ], -1);
  const _hoisted_15 = /* @__PURE__ */ vue.createElementVNode("p", null, [
    /* @__PURE__ */ vue.createElementVNode("b", null, "Note :"),
    /* @__PURE__ */ vue.createTextVNode(" Vous pouvez garder cette aide ouverte et continuer à travailler"),
    /* @__PURE__ */ vue.createElementVNode("br"),
    /* @__PURE__ */ vue.createTextVNode("(vous pouvez la déplacer en cliquant sur le titre) ")
  ], -1);
  const _hoisted_16 = /* @__PURE__ */ vue.createElementVNode("div", { class: "dialog-title" }, null, -1);
  const _hoisted_17 = { class: "dialog-form" };
  const _hoisted_18 = /* @__PURE__ */ vue.createElementVNode("legend", null, "Modification du Widget :", -1);
  const _hoisted_19 = /* @__PURE__ */ vue.createElementVNode("label", null, "Titre", -1);
  const _hoisted_20 = ["onUpdate:modelValue"];
  const _hoisted_21 = ["onUpdate:modelValue"];
  const _hoisted_22 = ["onUpdate:modelValue"];
  const _hoisted_23 = ["onUpdate:modelValue"];
  const _hoisted_24 = ["value"];
  const _hoisted_25 = ["onUpdate:modelValue"];
  const _hoisted_26 = { class: "form-buttons-box" };
  const _sfc_main = {
    __name: "Cockpit",
    props: {
      html_id: { type: String, required: true },
      grid_params: {
        type: Object,
        required: true
      },
      palette: { type: Object, required: true }
    },
    setup(__props) {
      const props = __props;
      const Button = primevue2.button;
      const Dialog = primevue2.dialog;
      const Tooltip = primevue2.tooltip;
      const InputText = primevue2.inputtext;
      const InputNumber = primevue2.inputnumber;
      const vTooltip = Tooltip;
      const currentInstance = vue.getCurrentInstance();
      const gridData = vue.reactive({ layout: props.grid_params.init_layout });
      const tileFormStructure = vue.ref([{ test1: "popo1" }]);
      const tileFormIsOpen = vue.ref(false);
      const editable = vue.ref(true);
      const gridLayout = vue.ref(null);
      const gridItemRefs = vue.ref([]);
      const showHelpDialog = vue.ref(false);
      const contextMenu = vue.ref();
      const contextMenuItems = vue.ref([
        {
          icon: "pi pi-pencil",
          label: "Modifier",
          visible: editable.value,
          command: () => {
            unlocked.value = true;
          }
        },
        {
          icon: "pi pi-sync",
          label: "Rafraîchir",
          command: () => {
            refresh_all();
          }
        }
      ]);
      const unlocked = vue.ref(false);
      const touched = vue.ref(false);
      let mouseXY = { x: null, y: null };
      let DragPos = { x: null, y: null, w: 1, h: 1, i: null, tile_class: null, tile_category: null };
      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
      const csrftoken = getCookie("csrftoken");
      vue.onBeforeMount(() => {
      });
      vue.onMounted(() => {
        document.addEventListener(
          "dragover",
          function(e) {
            mouseXY.x = e.clientX;
            mouseXY.y = e.clientY;
          },
          false
        );
      });
      function layoutUpdated() {
        console.log("layout updated");
      }
      function refresh_all() {
        const params = new URLSearchParams();
        let layout = [];
        params.append("widget_id", props.html_id);
        for (var i = 0; i < gridData.layout.length; i++) {
          let tile = gridData.layout[i];
          layout.push({
            i: tile.i,
            tile_class: tile.tile_class,
            w_params: tile.w_params
          });
        }
        params.append("layout", JSON.stringify(layout));
        axios2.get(".", { params }).then((response) => {
          console.log(response.data);
          for (var i2 = 0; i2 < gridData.layout.length; i2++) {
            let tile = gridData.layout[i2];
            if (response.data.tiles.hasOwnProperty(tile.i)) {
              console.log("i=", tile.i, "html=", response.data.tiles[tile.i].html);
              tile.content = response.data.tiles[tile.i].html;
            }
          }
        });
      }
      function layoutReady() {
        console.log("layout ready");
        refresh_all();
      }
      function editItem(i) {
        console.log("Editing tile properties...", i);
        let index = gridData.layout.findIndex((item) => item.i === i);
        let tileData = gridData.layout[index];
        let w_params = JSON.parse(tileData.w_params);
        let form = [{ id: "title", label: "Titre", type: "string", value: tileData.title }];
        for (const [prop_id, prop_value] of Object.entries(
          props.palette[tileData.tile_category].items[tileData.tile_class].properties
        )) {
          form.push({
            id: prop_id,
            label: prop_value.label,
            help_text: prop_value.help_text,
            type: prop_value.type,
            value: w_params[prop_id]
          });
        }
        tileData.editing = true;
        tileFormStructure.value = {
          i,
          index,
          form
        };
        tileFormIsOpen.value = true;
      }
      function editItemOk() {
        console.log("Saving !");
        let tileData = gridData.layout[tileFormStructure.value.index];
        let templateProperties = props.palette[tileData.tile_category].items[tileData.tile_class].properties;
        let w_params = {};
        for (var i = 0; i < tileFormStructure.value.form.length; i++) {
          let parameter = tileFormStructure.value.form[i];
          console.log("  Value:", parameter.label, parameter.value);
          if (parameter.id === "title") {
            tileData.title = parameter.value;
          } else if (templateProperties.hasOwnProperty(parameter.id)) {
            w_params[parameter.id] = parameter.value;
          }
        }
        tileData.w_params = JSON.stringify(w_params);
        tileData.editing = false;
        touched.value = true;
        tileFormIsOpen.value = false;
      }
      function editItemCancel() {
        let tileData = gridData.layout[tileFormStructure.value.index];
        tileData.editing = false;
        tileFormIsOpen.value = false;
      }
      function modifiedItem(event) {
        touched.value = true;
      }
      function openContextMenu(event) {
        contextMenu.value.show(event);
      }
      function openHelpDialog() {
        showHelpDialog.value = true;
      }
      function saveLayout() {
        unlocked.value = false;
        showHelpDialog.value = false;
        if (touched.value) {
          console.log("Storing layout...");
          const params = new URLSearchParams();
          params.append("widget_id", props.html_id);
          params.append("layout", JSON.stringify(gridData.layout));
          axios2.post(".", params, {
            headers: {
              "X-CSRFToken": csrftoken
            }
          }).then(function(response) {
            console.log(response);
          });
        }
        touched.value = false;
        refresh_all();
      }
      function removeItem(val) {
        const index = gridData.layout.map((item) => item.i).indexOf(val);
        gridData.layout.splice(index, 1);
      }
      function drag(e) {
        console.log(e);
        let parentRect = document.getElementById("grid-container").getBoundingClientRect();
        let mouseInGrid = false;
        if (mouseXY.x > parentRect.left && mouseXY.x < parentRect.right && mouseXY.y > parentRect.top && mouseXY.y < parentRect.bottom) {
          mouseInGrid = true;
        }
        if (mouseInGrid === true && gridData.layout.findIndex((item) => item.i === "__drop__") === -1) {
          gridData.layout.push({
            x: gridData.layout.length * 2 % (gridLayout.value.colNum || 12),
            y: gridData.layout.length + (gridLayout.value.colNum || 12),
            // puts it at the bottom
            w: 3,
            h: 1,
            i: "__drop__",
            title: "__dropped__"
          });
        }
        let index = gridData.layout.findIndex((item) => item.i === "__drop__");
        if (index !== -1) {
          let el = gridItemRefs.value[index];
          let new_pos = null;
          if (el !== void 0) {
            el.dragging = { top: mouseXY.y - parentRect.top, left: mouseXY.x - parentRect.left };
            el.$.attrs.style.display = "none";
            new_pos = el.calcXY(mouseXY.y - parentRect.top, mouseXY.x - parentRect.left);
          } else {
            new_pos = { x: 0, y: 0 };
          }
          if (mouseInGrid === true) {
            gridLayout.value.dragEvent("dragstart", "__drop__", new_pos.x, new_pos.y, 1, 3);
            let al = gridData.layout.map((a) => a.i);
            let next_id = index;
            while (al.includes(next_id)) {
              next_id++;
            }
            console.log(al, next_id);
            DragPos.i = next_id;
            DragPos.x = gridData.layout[index].x;
            DragPos.y = gridData.layout[index].y;
            DragPos.tile_category = e.target.attributes.tile_category.value;
            DragPos.tile_class = e.target.attributes.tile_class.value;
          }
          if (mouseInGrid === false) {
            gridLayout.value.dragEvent("dragend", "__drop__", new_pos.x, new_pos.y, 1, 3);
            gridData.layout = gridData.layout.filter((obj) => obj.i !== "__drop__");
          }
        }
      }
      function dragend(e) {
        var _a;
        touched.value = true;
        let parentRect = document.getElementById("grid-container").getBoundingClientRect();
        let mouseInGrid = false;
        if (mouseXY.x > parentRect.left && mouseXY.x < parentRect.right && mouseXY.y > parentRect.top && mouseXY.y < parentRect.bottom) {
          mouseInGrid = true;
        }
        if (mouseInGrid === true) {
          gridLayout.value.dragEvent("dragend", "__drop__", DragPos.x, DragPos.y, 1, 3);
          gridData.layout = gridData.layout.filter((obj) => obj.i !== "__drop__");
          let defaults = {};
          for (const [prop_id, prop_value] of Object.entries(
            props.palette[DragPos.tile_category].items[DragPos.tile_class].properties
          )) {
            defaults[prop_id] = prop_value.default;
          }
          gridData.layout[gridData.layout.length] = vue.reactive({
            x: DragPos.x,
            y: DragPos.y,
            w: 3,
            h: 2,
            i: DragPos.i,
            static: false,
            moved: false,
            title: "Dropped (" + DragPos.tile_class + ") !",
            tile_class: DragPos.tile_class,
            tile_category: DragPos.tile_category,
            w_params: JSON.stringify(defaults)
          });
          (_a = currentInstance == null ? void 0 : currentInstance.proxy) == null ? void 0 : _a.$forceUpdate();
          vue.nextTick(() => {
            gridLayout.value.dragEvent("dragend", DragPos.i, DragPos.x, DragPos.y, 1, 3);
            let index = gridData.layout.findIndex((item) => item.i === DragPos.i);
            gridItemRefs.value[index];
            editItem(DragPos.i);
          });
        }
      }
      return (_ctx, _cache) => {
        return vue.openBlock(), vue.createElementBlock("div", _hoisted_1, [
          vue.withDirectives(vue.createElementVNode("div", _hoisted_2, [
            _hoisted_3,
            vue.createVNode(vue.unref(script$4), { activeIndex: 0 }, {
              default: vue.withCtx(() => [
                (vue.openBlock(true), vue.createElementBlock(vue.Fragment, null, vue.renderList(__props.palette, (category, category_id) => {
                  return vue.openBlock(), vue.createBlock(vue.unref(script$3), null, {
                    header: vue.withCtx(() => [
                      vue.withDirectives((vue.openBlock(), vue.createElementBlock("div", _hoisted_4, [
                        vue.createTextVNode(vue.toDisplayString(category.label), 1)
                      ])), [
                        [vue.unref(vTooltip), category.help_text]
                      ])
                    ]),
                    default: vue.withCtx(() => [
                      (vue.openBlock(true), vue.createElementBlock(vue.Fragment, null, vue.renderList(category.items, (item, tmpl_name) => {
                        return vue.withDirectives((vue.openBlock(), vue.createElementBlock("div", {
                          onDrag: drag,
                          onDragend: dragend,
                          class: "droppable-element palette-item",
                          draggable: "true",
                          unselectable: "on",
                          tile_category: category_id,
                          tile_class: tmpl_name,
                          default_params: item.default_params
                        }, [
                          vue.createElementVNode("div", null, vue.toDisplayString(item.label), 1)
                        ], 40, _hoisted_5)), [
                          [vue.unref(vTooltip), item.help_text]
                        ]);
                      }), 256))
                    ]),
                    _: 2
                  }, 1024);
                }), 256))
              ]),
              _: 1
            }),
            vue.createElementVNode("div", _hoisted_6, [
              vue.createVNode(vue.unref(Button), {
                icon: "pi pi-question",
                class: "p-button-raised p-button-rounded p-button-lg",
                onClick: openHelpDialog
              }),
              vue.createVNode(vue.unref(Button), {
                icon: "pi pi-times",
                class: "p-button-raised p-button-rounded p-button-lg"
              }),
              vue.createVNode(vue.unref(Button), {
                icon: "pi pi-check",
                class: "p-button-raised p-button-rounded p-button-lg",
                onClick: saveLayout
              })
            ])
          ], 512), [
            [vue.vShow, unlocked.value]
          ]),
          vue.createElementVNode("div", {
            id: "grid-container",
            class: "grid-container",
            onClick: _cache[6] || (_cache[6] = (...args) => _ctx.layoutClick && _ctx.layoutClick(...args))
          }, [
            vue.createVNode(vue.unref(sa), {
              ref_key: "gridLayout",
              ref: gridLayout,
              layout: gridData.layout,
              "onUpdate:layout": _cache[0] || (_cache[0] = ($event) => gridData.layout = $event),
              "col-num": __props.grid_params.columns,
              "row-height": __props.grid_params.rows,
              "is-draggable": unlocked.value,
              "is-resizable": unlocked.value,
              "is-mirrored": false,
              "restore-on-drag": true,
              "prevent-collision": true,
              "vertical-compact": false,
              margin: [__props.grid_params.h_spacing, __props.grid_params.v_spacing],
              "use-css-transforms": true,
              onLayoutUpdated: layoutUpdated,
              onLayoutReady: layoutReady,
              onContextmenu: openContextMenu
            }, {
              default: vue.withCtx(() => [
                (vue.openBlock(true), vue.createElementBlock(vue.Fragment, null, vue.renderList(gridData.layout, (item, index) => {
                  return vue.openBlock(), vue.createBlock(vue.unref(_i), {
                    ref_for: true,
                    ref_key: "gridItemRefs",
                    ref: gridItemRefs,
                    x: item.x,
                    y: item.y,
                    w: item.w,
                    h: item.h,
                    i: item.i,
                    tile_class: item.tile_class,
                    w_params: item.w_params,
                    "drag-allow-from": ".title",
                    key: item.i,
                    class: vue.normalizeClass({ "add-border": item.title, editing: item.editing }),
                    style: { display: "block" },
                    onMoved: modifiedItem,
                    onResized: modifiedItem
                  }, {
                    default: vue.withCtx(() => [
                      vue.createElementVNode("div", {
                        class: vue.normalizeClass(["frame", {
                          "with-title": item.title.length,
                          unlocked: unlocked.value,
                          "without-title": !item.title.length
                        }])
                      }, [
                        !item.title.length ? (vue.openBlock(), vue.createElementBlock("div", {
                          key: 0,
                          class: vue.normalizeClass(["content", { "with-title": item.title.length }]),
                          innerHTML: item.content
                        }, null, 10, _hoisted_7)) : vue.createCommentVNode("", true),
                        vue.createElementVNode("div", _hoisted_8, [
                          item.title.length | unlocked.value ? (vue.openBlock(), vue.createElementBlock("div", _hoisted_9, vue.toDisplayString(item.title), 1)) : vue.createCommentVNode("", true),
                          unlocked.value ? (vue.openBlock(), vue.createElementBlock("div", _hoisted_10, [
                            vue.createElementVNode("i", {
                              class: "pi pi-pencil",
                              onClick: ($event) => editItem(item.i)
                            }, null, 8, _hoisted_11),
                            vue.createElementVNode("i", {
                              class: "pi pi-trash",
                              onClick: ($event) => removeItem(item.i)
                            }, null, 8, _hoisted_12)
                          ])) : vue.createCommentVNode("", true),
                          item.title.length ? (vue.openBlock(), vue.createElementBlock("div", {
                            key: 2,
                            class: "window",
                            innerHTML: item.content
                          }, null, 8, _hoisted_13)) : vue.createCommentVNode("", true)
                        ])
                      ], 2)
                    ]),
                    _: 2
                  }, 1032, ["x", "y", "w", "h", "i", "tile_class", "w_params", "drag-allow-from", "class"]);
                }), 128)),
                vue.createVNode(vue.unref(script), {
                  ref_key: "contextMenu",
                  ref: contextMenu,
                  model: contextMenuItems.value
                }, null, 8, ["model"])
              ]),
              _: 1
            }, 8, ["layout", "col-num", "row-height", "is-draggable", "is-resizable", "margin"]),
            vue.createVNode(vue.unref(Dialog), {
              ref: "helpDialog",
              header: "Utilisation de l'éditeur de cockpit",
              footer: "",
              visible: showHelpDialog.value,
              "onUpdate:visible": _cache[1] || (_cache[1] = ($event) => showHelpDialog.value = $event)
            }, {
              default: vue.withCtx(() => [
                vue.createTextVNode(" Hello ! "),
                _hoisted_14,
                _hoisted_15
              ]),
              _: 1
            }, 8, ["visible"]),
            vue.createVNode(vue.unref(Dialog), {
              ref: "tileForm",
              visible: tileFormIsOpen.value,
              "onUpdate:visible": _cache[2] || (_cache[2] = ($event) => tileFormIsOpen.value = $event),
              header: "Propriétés",
              modal: true,
              onAfterHide: editItemCancel
            }, {
              default: vue.withCtx(() => [
                (vue.openBlock(true), vue.createElementBlock(vue.Fragment, null, vue.renderList(tileFormStructure.value.form, (formItem) => {
                  return vue.openBlock(), vue.createElementBlock("div", null, [
                    vue.createElementVNode("label", null, vue.toDisplayString(formItem.label), 1),
                    formItem.type == "string" ? (vue.openBlock(), vue.createBlock(vue.unref(InputText), {
                      key: 0,
                      type: "text",
                      modelValue: formItem.value,
                      "onUpdate:modelValue": ($event) => formItem.value = $event
                    }, null, 8, ["modelValue", "onUpdate:modelValue"])) : vue.createCommentVNode("", true),
                    formItem.type == "integer" ? (vue.openBlock(), vue.createBlock(vue.unref(InputNumber), {
                      key: 1,
                      modelValue: formItem.value,
                      "onUpdate:modelValue": ($event) => formItem.value = $event
                    }, null, 8, ["modelValue", "onUpdate:modelValue"])) : vue.createCommentVNode("", true)
                  ]);
                }), 256)),
                vue.createElementVNode("div", null, [
                  vue.createVNode(vue.unref(Button), {
                    icon: "pi pi-times",
                    class: "p-button-raised p-button-rounded p-button-lg",
                    onClick: editItemCancel
                  }),
                  vue.createVNode(vue.unref(Button), {
                    icon: "pi pi-check",
                    class: "p-button-raised p-button-rounded p-button-lg",
                    onClick: editItemOk
                  })
                ])
              ]),
              _: 1
            }, 8, ["visible"]),
            vue.createVNode(vue.unref(Dialog), null, {
              default: vue.withCtx(() => [
                _hoisted_16,
                vue.createElementVNode("form", _hoisted_17, [
                  vue.createElementVNode("fieldset", null, [
                    _hoisted_18,
                    _hoisted_19,
                    vue.withDirectives(vue.createElementVNode("input", {
                      "onUpdate:modelValue": _cache[3] || (_cache[3] = ($event) => _ctx.edit_widget_title = $event)
                    }, null, 512), [
                      [vue.vModelText, _ctx.edit_widget_title]
                    ]),
                    (vue.openBlock(true), vue.createElementBlock(vue.Fragment, null, vue.renderList(_ctx.form, (entry) => {
                      return vue.openBlock(), vue.createElementBlock(vue.Fragment, null, [
                        vue.createElementVNode("label", null, vue.toDisplayString(entry.label), 1),
                        entry.type == "int" ? vue.withDirectives((vue.openBlock(), vue.createElementBlock("input", {
                          key: 0,
                          "onUpdate:modelValue": ($event) => entry.value = $event,
                          type: "number"
                        }, null, 8, _hoisted_20)), [
                          [
                            vue.vModelText,
                            entry.value,
                            void 0,
                            { lazy: true }
                          ]
                        ]) : entry.type == "boolean" ? vue.withDirectives((vue.openBlock(), vue.createElementBlock("input", {
                          key: 1,
                          "onUpdate:modelValue": ($event) => entry.value = $event,
                          type: "checkbox"
                        }, null, 8, _hoisted_21)), [
                          [
                            vue.vModelCheckbox,
                            entry.value,
                            void 0,
                            { lazy: true }
                          ]
                        ]) : entry.type == "color" ? vue.withDirectives((vue.openBlock(), vue.createElementBlock("input", {
                          key: 2,
                          "onUpdate:modelValue": ($event) => entry.value = $event,
                          type: "color"
                        }, null, 8, _hoisted_22)), [
                          [
                            vue.vModelText,
                            entry.value,
                            void 0,
                            { lazy: true }
                          ]
                        ]) : entry.type == "choice" ? vue.withDirectives((vue.openBlock(), vue.createElementBlock("select", {
                          key: 3,
                          "onUpdate:modelValue": ($event) => entry.value = $event
                        }, [
                          (vue.openBlock(true), vue.createElementBlock(vue.Fragment, null, vue.renderList(entry.choices, (choice) => {
                            return vue.openBlock(), vue.createElementBlock("option", {
                              value: choice[0]
                            }, vue.toDisplayString(choice[1]), 9, _hoisted_24);
                          }), 256))
                        ], 8, _hoisted_23)), [
                          [
                            vue.vModelSelect,
                            entry.value,
                            void 0,
                            { lazy: true }
                          ]
                        ]) : vue.withDirectives((vue.openBlock(), vue.createElementBlock("input", {
                          key: 4,
                          "onUpdate:modelValue": ($event) => entry.value = $event
                        }, null, 8, _hoisted_25)), [
                          [
                            vue.vModelText,
                            entry.value,
                            void 0,
                            { lazy: true }
                          ]
                        ])
                      ], 64);
                    }), 256))
                  ])
                ]),
                vue.createElementVNode("div", _hoisted_26, [
                  vue.createElementVNode("button", {
                    class: "dialog-button",
                    onClick: _cache[4] || (_cache[4] = ($event) => _ctx.itemEditOk(_ctx.edit_item))
                  }, "Ok"),
                  vue.createElementVNode("button", {
                    class: "dialog-button",
                    onClick: _cache[5] || (_cache[5] = ($event) => _ctx.itemEditCancel(_ctx.edit_item))
                  }, "Annuler")
                ])
              ]),
              _: 1
            })
          ])
        ]);
      };
    }
  };
  win.cockpit = _sfc_main;
})(window, Vue, axios, primevue);
