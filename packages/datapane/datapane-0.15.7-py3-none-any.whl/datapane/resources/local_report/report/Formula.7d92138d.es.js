import { defineComponent as s, openBlock as a, createElementBlock as m, Fragment as i, createElementVNode as n } from "../vue.esm-browser.prod.js";
import f from "https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.mjs";
const u = /* @__PURE__ */ n("link", {
  rel: "stylesheet",
  href: "https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css",
  integrity: "sha384-Xi8rHCmBmhbuyyhbI88391ZKP2dmfnOl4rT9ZfRI7mLTdk1wblIUnrIq35nqwEvC",
  crossorigin: "anonymous"
}, null, -1), p = /* @__PURE__ */ s({
  __name: "Formula",
  props: {
    content: null
  },
  setup(t) {
    const o = t, l = (e) => {
      try {
        f.render(o.content, e);
      } catch (r) {
        console.error(`Error rendering formula: ${r}`);
      }
    }, c = (e) => {
      e && l(e);
    };
    return (e, r) => (a(), m(i, null, [
      u,
      n("div", {
        "data-cy": "block-formula",
        className: "w-full overflow-y-hidden bg-white flex justify-center",
        ref: c
      })
    ], 64));
  }
});
export {
  p as default
};
