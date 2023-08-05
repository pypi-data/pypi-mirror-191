var c = [], ie = function() {
  return c.some(function(e) {
    return e.activeTargets.length > 0;
  });
}, ne = function() {
  return c.some(function(e) {
    return e.skippedTargets.length > 0;
  });
}, M = "ResizeObserver loop completed with undelivered notifications.", oe = function() {
  var e;
  typeof ErrorEvent == "function" ? e = new ErrorEvent("error", {
    message: M
  }) : (e = document.createEvent("Event"), e.initEvent("error", !1, !1), e.message = M), window.dispatchEvent(e);
}, p;
(function(e) {
  e.BORDER_BOX = "border-box", e.CONTENT_BOX = "content-box", e.DEVICE_PIXEL_CONTENT_BOX = "device-pixel-content-box";
})(p || (p = {}));
var X = function() {
  function e(t, r, i, n) {
    return this.x = t, this.y = r, this.width = i, this.height = n, this.top = this.y, this.left = this.x, this.bottom = this.top + this.height, this.right = this.left + this.width, Object.freeze(this);
  }
  return e.prototype.toJSON = function() {
    var t = this, r = t.x, i = t.y, n = t.top, s = t.right, o = t.bottom, u = t.left, h = t.width, v = t.height;
    return { x: r, y: i, top: n, right: s, bottom: o, left: u, width: h, height: v };
  }, e.fromRect = function(t) {
    return new e(t.x, t.y, t.width, t.height);
  }, e;
}(), S = function(e) {
  return e instanceof SVGElement && "getBBox" in e;
}, q = function(e) {
  if (S(e)) {
    var t = e.getBBox(), r = t.width, i = t.height;
    return !r && !i;
  }
  var n = e, s = n.offsetWidth, o = n.offsetHeight;
  return !(s || o || e.getClientRects().length);
}, P = function(e) {
  var t, r, i = (r = (t = e) === null || t === void 0 ? void 0 : t.ownerDocument) === null || r === void 0 ? void 0 : r.defaultView;
  return !!(i && e instanceof i.Element);
}, se = function(e) {
  switch (e.tagName) {
    case "INPUT":
      if (e.type !== "image")
        break;
    case "VIDEO":
    case "AUDIO":
    case "EMBED":
    case "OBJECT":
    case "CANVAS":
    case "IFRAME":
    case "IMG":
      return !0;
  }
  return !1;
}, l = typeof window < "u" ? window : {}, x = /* @__PURE__ */ new WeakMap(), _ = /auto|scroll/, ae = /^tb|vertical/, ve = /msie|trident/i.test(l.navigator && l.navigator.userAgent), a = function(e) {
  return parseFloat(e || "0");
}, d = function(e, t, r) {
  return e === void 0 && (e = 0), t === void 0 && (t = 0), r === void 0 && (r = !1), Object.freeze({
    inlineSize: (r ? t : e) || 0,
    blockSize: (r ? e : t) || 0
  });
}, I = Object.freeze({
  devicePixelContentBoxSize: d(),
  borderBoxSize: d(),
  contentBoxSize: d(),
  contentRect: new X(0, 0, 0, 0)
}), G = function(e, t) {
  if (t === void 0 && (t = !1), x.has(e) && !t)
    return x.get(e);
  if (q(e))
    return x.set(e, I), I;
  var r = getComputedStyle(e), i = S(e) && e.ownerSVGElement && e.getBBox(), n = !ve && r.boxSizing === "border-box", s = ae.test(r.writingMode || ""), o = !i && _.test(r.overflowY || ""), u = !i && _.test(r.overflowX || ""), h = i ? 0 : a(r.paddingTop), v = i ? 0 : a(r.paddingRight), w = i ? 0 : a(r.paddingBottom), f = i ? 0 : a(r.paddingLeft), Y = i ? 0 : a(r.borderTopWidth), K = i ? 0 : a(r.borderRightWidth), Q = i ? 0 : a(r.borderBottomWidth), Z = i ? 0 : a(r.borderLeftWidth), C = f + v, D = h + w, y = Z + K, T = Y + Q, k = u ? e.offsetHeight - T - e.clientHeight : 0, N = o ? e.offsetWidth - y - e.clientWidth : 0, $ = n ? C + y : 0, ee = n ? D + T : 0, b = i ? i.width : a(r.width) - $ - N, g = i ? i.height : a(r.height) - ee - k, te = b + C + N + y, re = g + D + k + T, A = Object.freeze({
    devicePixelContentBoxSize: d(Math.round(b * devicePixelRatio), Math.round(g * devicePixelRatio), s),
    borderBoxSize: d(te, re, s),
    contentBoxSize: d(b, g, s),
    contentRect: new X(f, h, b, g)
  });
  return x.set(e, A), A;
}, j = function(e, t, r) {
  var i = G(e, r), n = i.borderBoxSize, s = i.contentBoxSize, o = i.devicePixelContentBoxSize;
  switch (t) {
    case p.DEVICE_PIXEL_CONTENT_BOX:
      return o;
    case p.BORDER_BOX:
      return n;
    default:
      return s;
  }
}, ce = function() {
  function e(t) {
    var r = G(t);
    this.target = t, this.contentRect = r.contentRect, this.borderBoxSize = [r.borderBoxSize], this.contentBoxSize = [r.contentBoxSize], this.devicePixelContentBoxSize = [r.devicePixelContentBoxSize];
  }
  return e;
}(), J = function(e) {
  if (q(e))
    return 1 / 0;
  for (var t = 0, r = e.parentNode; r; )
    t += 1, r = r.parentNode;
  return t;
}, ue = function() {
  var e = 1 / 0, t = [];
  c.forEach(function(o) {
    if (o.activeTargets.length !== 0) {
      var u = [];
      o.activeTargets.forEach(function(v) {
        var w = new ce(v.target), f = J(v.target);
        u.push(w), v.lastReportedSize = j(v.target, v.observedBox), f < e && (e = f);
      }), t.push(function() {
        o.callback.call(o.observer, u, o.observer);
      }), o.activeTargets.splice(0, o.activeTargets.length);
    }
  });
  for (var r = 0, i = t; r < i.length; r++) {
    var n = i[r];
    n();
  }
  return e;
}, W = function(e) {
  c.forEach(function(r) {
    r.activeTargets.splice(0, r.activeTargets.length), r.skippedTargets.splice(0, r.skippedTargets.length), r.observationTargets.forEach(function(n) {
      n.isActive() && (J(n.target) > e ? r.activeTargets.push(n) : r.skippedTargets.push(n));
    });
  });
}, he = function() {
  var e = 0;
  for (W(e); ie(); )
    e = ue(), W(e);
  return ne() && oe(), e > 0;
}, R, U = [], de = function() {
  return U.splice(0).forEach(function(e) {
    return e();
  });
}, fe = function(e) {
  if (!R) {
    var t = 0, r = document.createTextNode(""), i = { characterData: !0 };
    new MutationObserver(function() {
      return de();
    }).observe(r, i), R = function() {
      r.textContent = "" + (t ? t-- : t++);
    };
  }
  U.push(e), R();
}, le = function(e) {
  fe(function() {
    requestAnimationFrame(e);
  });
}, E = 0, pe = function() {
  return !!E;
}, be = 250, ge = { attributes: !0, characterData: !0, childList: !0, subtree: !0 }, L = [
  "resize",
  "load",
  "transitionend",
  "animationend",
  "animationstart",
  "animationiteration",
  "keyup",
  "keydown",
  "mouseup",
  "mousedown",
  "mouseover",
  "mouseout",
  "blur",
  "focus"
], F = function(e) {
  return e === void 0 && (e = 0), Date.now() + e;
}, m = !1, xe = function() {
  function e() {
    var t = this;
    this.stopped = !0, this.listener = function() {
      return t.schedule();
    };
  }
  return e.prototype.run = function(t) {
    var r = this;
    if (t === void 0 && (t = be), !m) {
      m = !0;
      var i = F(t);
      le(function() {
        var n = !1;
        try {
          n = he();
        } finally {
          if (m = !1, t = i - F(), !pe())
            return;
          n ? r.run(1e3) : t > 0 ? r.run(t) : r.start();
        }
      });
    }
  }, e.prototype.schedule = function() {
    this.stop(), this.run();
  }, e.prototype.observe = function() {
    var t = this, r = function() {
      return t.observer && t.observer.observe(document.body, ge);
    };
    document.body ? r() : l.addEventListener("DOMContentLoaded", r);
  }, e.prototype.start = function() {
    var t = this;
    this.stopped && (this.stopped = !1, this.observer = new MutationObserver(this.listener), this.observe(), L.forEach(function(r) {
      return l.addEventListener(r, t.listener, !0);
    }));
  }, e.prototype.stop = function() {
    var t = this;
    this.stopped || (this.observer && this.observer.disconnect(), L.forEach(function(r) {
      return l.removeEventListener(r, t.listener, !0);
    }), this.stopped = !0);
  }, e;
}(), B = new xe(), H = function(e) {
  !E && e > 0 && B.start(), E += e, !E && B.stop();
}, ze = function(e) {
  return !S(e) && !se(e) && getComputedStyle(e).display === "inline";
}, Oe = function() {
  function e(t, r) {
    this.target = t, this.observedBox = r || p.CONTENT_BOX, this.lastReportedSize = {
      inlineSize: 0,
      blockSize: 0
    };
  }
  return e.prototype.isActive = function() {
    var t = j(this.target, this.observedBox, !0);
    return ze(this.target) && (this.lastReportedSize = t), this.lastReportedSize.inlineSize !== t.inlineSize || this.lastReportedSize.blockSize !== t.blockSize;
  }, e;
}(), Ee = function() {
  function e(t, r) {
    this.activeTargets = [], this.skippedTargets = [], this.observationTargets = [], this.observer = t, this.callback = r;
  }
  return e;
}(), z = /* @__PURE__ */ new WeakMap(), V = function(e, t) {
  for (var r = 0; r < e.length; r += 1)
    if (e[r].target === t)
      return r;
  return -1;
}, O = function() {
  function e() {
  }
  return e.connect = function(t, r) {
    var i = new Ee(t, r);
    z.set(t, i);
  }, e.observe = function(t, r, i) {
    var n = z.get(t), s = n.observationTargets.length === 0;
    V(n.observationTargets, r) < 0 && (s && c.push(n), n.observationTargets.push(new Oe(r, i && i.box)), H(1), B.schedule());
  }, e.unobserve = function(t, r) {
    var i = z.get(t), n = V(i.observationTargets, r), s = i.observationTargets.length === 1;
    n >= 0 && (s && c.splice(c.indexOf(i), 1), i.observationTargets.splice(n, 1), H(-1));
  }, e.disconnect = function(t) {
    var r = this, i = z.get(t);
    i.observationTargets.slice().forEach(function(n) {
      return r.unobserve(t, n.target);
    }), i.activeTargets.splice(0, i.activeTargets.length);
  }, e;
}(), we = function() {
  function e(t) {
    if (arguments.length === 0)
      throw new TypeError("Failed to construct 'ResizeObserver': 1 argument required, but only 0 present.");
    if (typeof t != "function")
      throw new TypeError("Failed to construct 'ResizeObserver': The callback provided as parameter 1 is not a function.");
    O.connect(this, t);
  }
  return e.prototype.observe = function(t, r) {
    if (arguments.length === 0)
      throw new TypeError("Failed to execute 'observe' on 'ResizeObserver': 1 argument required, but only 0 present.");
    if (!P(t))
      throw new TypeError("Failed to execute 'observe' on 'ResizeObserver': parameter 1 is not of type 'Element");
    O.observe(this, t, r);
  }, e.prototype.unobserve = function(t) {
    if (arguments.length === 0)
      throw new TypeError("Failed to execute 'unobserve' on 'ResizeObserver': 1 argument required, but only 0 present.");
    if (!P(t))
      throw new TypeError("Failed to execute 'unobserve' on 'ResizeObserver': parameter 1 is not of type 'Element");
    O.unobserve(this, t);
  }, e.prototype.disconnect = function() {
    O.disconnect(this);
  }, e.toString = function() {
    return "function ResizeObserver () { [polyfill code] }";
  }, e;
}();
export {
  we as ResizeObserver,
  ce as ResizeObserverEntry
};
