import { openBlock as o, createBlock as c, withKeys as f, withModifiers as r, renderSlot as h, createVNode as a, withDirectives as w, Fragment as D, renderList as T, toDisplayString as g, vShow as O, createCommentVNode as y, Transition as A, withCtx as H, createTextVNode as L, defineComponent as G, ref as z, computed as k, createElementBlock as S, createElementVNode as B, normalizeClass as E, unref as V } from "../vue.esm-browser.prod.js";
function P(e) {
  return e === 0 ? !1 : Array.isArray(e) && e.length === 0 ? !0 : !e;
}
function R(e) {
  return (...t) => !e(...t);
}
function j(e, t) {
  return e === void 0 && (e = "undefined"), e === null && (e = "null"), e === !1 && (e = "false"), e.toString().toLowerCase().indexOf(t.trim()) !== -1;
}
function N(e, t, i, l) {
  return t ? e.filter((u) => j(l(u, i), t)).sort((u, n) => l(u, i).length - l(n, i).length) : e;
}
function q(e) {
  return e.filter((t) => !t.$isLabel);
}
function M(e, t) {
  return (i) => i.reduce((l, u) => u[e] && u[e].length ? (l.push({
    $groupLabel: u[t],
    $isLabel: !0
  }), l.concat(u[e])) : l, []);
}
function I(e, t, i, l, u) {
  return (n) => n.map((s) => {
    if (!s[i])
      return console.warn("Options passed to vue-multiselect do not contain groups, despite the config."), [];
    const d = N(s[i], e, t, u);
    return d.length ? {
      [l]: s[l],
      [i]: d
    } : [];
  });
}
const C = (...e) => (t) => e.reduce((i, l) => l(i), t);
var U = {
  data() {
    return {
      search: "",
      isOpen: !1,
      preferredOpenDirection: "below",
      optimizedHeight: this.maxHeight
    };
  },
  props: {
    internalSearch: {
      type: Boolean,
      default: !0
    },
    options: {
      type: Array,
      required: !0
    },
    multiple: {
      type: Boolean,
      default: !1
    },
    trackBy: {
      type: String
    },
    label: {
      type: String
    },
    searchable: {
      type: Boolean,
      default: !0
    },
    clearOnSelect: {
      type: Boolean,
      default: !0
    },
    hideSelected: {
      type: Boolean,
      default: !1
    },
    placeholder: {
      type: String,
      default: "Select option"
    },
    allowEmpty: {
      type: Boolean,
      default: !0
    },
    resetAfter: {
      type: Boolean,
      default: !1
    },
    closeOnSelect: {
      type: Boolean,
      default: !0
    },
    customLabel: {
      type: Function,
      default(e, t) {
        return P(e) ? "" : t ? e[t] : e;
      }
    },
    taggable: {
      type: Boolean,
      default: !1
    },
    tagPlaceholder: {
      type: String,
      default: "Press enter to create a tag"
    },
    tagPosition: {
      type: String,
      default: "top"
    },
    max: {
      type: [Number, Boolean],
      default: !1
    },
    id: {
      default: null
    },
    optionsLimit: {
      type: Number,
      default: 1e3
    },
    groupValues: {
      type: String
    },
    groupLabel: {
      type: String
    },
    groupSelect: {
      type: Boolean,
      default: !1
    },
    blockKeys: {
      type: Array,
      default() {
        return [];
      }
    },
    preserveSearch: {
      type: Boolean,
      default: !1
    },
    preselectFirst: {
      type: Boolean,
      default: !1
    }
  },
  mounted() {
    !this.multiple && this.max && console.warn("[Vue-Multiselect warn]: Max prop should not be used when prop Multiple equals false."), this.preselectFirst && !this.internalValue.length && this.options.length && this.select(this.filteredOptions[0]);
  },
  computed: {
    internalValue() {
      return this.modelValue || this.modelValue === 0 ? Array.isArray(this.modelValue) ? this.modelValue : [this.modelValue] : [];
    },
    filteredOptions() {
      const e = this.search || "", t = e.toLowerCase().trim();
      let i = this.options.concat();
      return this.internalSearch ? i = this.groupValues ? this.filterAndFlat(i, t, this.label) : N(i, t, this.label, this.customLabel) : i = this.groupValues ? M(this.groupValues, this.groupLabel)(i) : i, i = this.hideSelected ? i.filter(R(this.isSelected)) : i, this.taggable && t.length && !this.isExistingOption(t) && (this.tagPosition === "bottom" ? i.push({ isTag: !0, label: e }) : i.unshift({ isTag: !0, label: e })), i.slice(0, this.optionsLimit);
    },
    valueKeys() {
      return this.trackBy ? this.internalValue.map((e) => e[this.trackBy]) : this.internalValue;
    },
    optionKeys() {
      return (this.groupValues ? this.flatAndStrip(this.options) : this.options).map((t) => this.customLabel(t, this.label).toString().toLowerCase());
    },
    currentOptionLabel() {
      return this.multiple ? this.searchable ? "" : this.placeholder : this.internalValue.length ? this.getOptionLabel(this.internalValue[0]) : this.searchable ? "" : this.placeholder;
    }
  },
  watch: {
    internalValue() {
      this.resetAfter && this.internalValue.length && (this.search = "", this.$emit("update:modelValue", this.multiple ? [] : null));
    },
    search() {
      this.$emit("search-change", this.search);
    }
  },
  emits: ["open", "search-change", "close", "select", "update:modelValue", "remove", "tag"],
  methods: {
    getValue() {
      return this.multiple ? this.internalValue : this.internalValue.length === 0 ? null : this.internalValue[0];
    },
    filterAndFlat(e, t, i) {
      return C(
        I(t, i, this.groupValues, this.groupLabel, this.customLabel),
        M(this.groupValues, this.groupLabel)
      )(e);
    },
    flatAndStrip(e) {
      return C(
        M(this.groupValues, this.groupLabel),
        q
      )(e);
    },
    updateSearch(e) {
      this.search = e;
    },
    isExistingOption(e) {
      return this.options ? this.optionKeys.indexOf(e) > -1 : !1;
    },
    isSelected(e) {
      const t = this.trackBy ? e[this.trackBy] : e;
      return this.valueKeys.indexOf(t) > -1;
    },
    isOptionDisabled(e) {
      return !!e.$isDisabled;
    },
    getOptionLabel(e) {
      if (P(e))
        return "";
      if (e.isTag)
        return e.label;
      if (e.$isLabel)
        return e.$groupLabel;
      const t = this.customLabel(e, this.label);
      return P(t) ? "" : t;
    },
    select(e, t) {
      if (e.$isLabel && this.groupSelect) {
        this.selectGroup(e);
        return;
      }
      if (!(this.blockKeys.indexOf(t) !== -1 || this.disabled || e.$isDisabled || e.$isLabel) && !(this.max && this.multiple && this.internalValue.length === this.max) && !(t === "Tab" && !this.pointerDirty)) {
        if (e.isTag)
          this.$emit("tag", e.label, this.id), this.search = "", this.closeOnSelect && !this.multiple && this.deactivate();
        else {
          if (this.isSelected(e)) {
            t !== "Tab" && this.removeElement(e);
            return;
          }
          this.$emit("select", e, this.id), this.multiple ? this.$emit("update:modelValue", this.internalValue.concat([e])) : this.$emit("update:modelValue", e), this.clearOnSelect && (this.search = "");
        }
        this.closeOnSelect && this.deactivate();
      }
    },
    selectGroup(e) {
      const t = this.options.find((i) => i[this.groupLabel] === e.$groupLabel);
      if (!!t) {
        if (this.wholeGroupSelected(t)) {
          this.$emit("remove", t[this.groupValues], this.id);
          const i = this.internalValue.filter(
            (l) => t[this.groupValues].indexOf(l) === -1
          );
          this.$emit("update:modelValue", i);
        } else {
          const i = t[this.groupValues].filter(
            (l) => !(this.isOptionDisabled(l) || this.isSelected(l))
          );
          this.$emit("select", i, this.id), this.$emit(
            "update:modelValue",
            this.internalValue.concat(i)
          );
        }
        this.closeOnSelect && this.deactivate();
      }
    },
    wholeGroupSelected(e) {
      return e[this.groupValues].every(
        (t) => this.isSelected(t) || this.isOptionDisabled(t)
      );
    },
    wholeGroupDisabled(e) {
      return e[this.groupValues].every(this.isOptionDisabled);
    },
    removeElement(e, t = !0) {
      if (this.disabled || e.$isDisabled)
        return;
      if (!this.allowEmpty && this.internalValue.length <= 1) {
        this.deactivate();
        return;
      }
      const i = typeof e == "object" ? this.valueKeys.indexOf(e[this.trackBy]) : this.valueKeys.indexOf(e);
      if (this.$emit("remove", e, this.id), this.multiple) {
        const l = this.internalValue.slice(0, i).concat(this.internalValue.slice(i + 1));
        this.$emit("update:modelValue", l);
      } else
        this.$emit("update:modelValue", null);
      this.closeOnSelect && t && this.deactivate();
    },
    removeLastElement() {
      this.blockKeys.indexOf("Delete") === -1 && this.search.length === 0 && Array.isArray(this.internalValue) && this.internalValue.length && this.removeElement(this.internalValue[this.internalValue.length - 1], !1);
    },
    activate() {
      this.isOpen || this.disabled || (this.adjustPosition(), this.groupValues && this.pointer === 0 && this.filteredOptions.length && (this.pointer = 1), this.isOpen = !0, this.searchable ? (this.preserveSearch || (this.search = ""), this.$nextTick(() => this.$refs.search && this.$refs.search.focus())) : this.$el.focus(), this.$emit("open", this.id));
    },
    deactivate() {
      !this.isOpen || (this.isOpen = !1, this.searchable ? this.$refs.search && this.$refs.search.blur() : this.$el.blur(), this.preserveSearch || (this.search = ""), this.$emit("close", this.getValue(), this.id));
    },
    toggle() {
      this.isOpen ? this.deactivate() : this.activate();
    },
    adjustPosition() {
      if (typeof window > "u")
        return;
      const e = this.$el.getBoundingClientRect().top, t = window.innerHeight - this.$el.getBoundingClientRect().bottom;
      t > this.maxHeight || t > e || this.openDirection === "below" || this.openDirection === "bottom" ? (this.preferredOpenDirection = "below", this.optimizedHeight = Math.min(t - 40, this.maxHeight)) : (this.preferredOpenDirection = "above", this.optimizedHeight = Math.min(e - 40, this.maxHeight));
    }
  }
}, J = {
  data() {
    return {
      pointer: 0,
      pointerDirty: !1
    };
  },
  props: {
    showPointer: {
      type: Boolean,
      default: !0
    },
    optionHeight: {
      type: Number,
      default: 40
    }
  },
  computed: {
    pointerPosition() {
      return this.pointer * this.optionHeight;
    },
    visibleElements() {
      return this.optimizedHeight / this.optionHeight;
    }
  },
  watch: {
    filteredOptions() {
      this.pointerAdjust();
    },
    isOpen() {
      this.pointerDirty = !1;
    },
    pointer() {
      this.$refs.search && this.$refs.search.setAttribute("aria-activedescendant", this.id + "-" + this.pointer.toString());
    }
  },
  methods: {
    optionHighlight(e, t) {
      return {
        "multiselect__option--highlight": e === this.pointer && this.showPointer,
        "multiselect__option--selected": this.isSelected(t)
      };
    },
    groupHighlight(e, t) {
      if (!this.groupSelect)
        return [
          "multiselect__option--disabled",
          { "multiselect__option--group": t.$isLabel }
        ];
      const i = this.options.find((l) => l[this.groupLabel] === t.$groupLabel);
      return i && !this.wholeGroupDisabled(i) ? [
        "multiselect__option--group",
        { "multiselect__option--highlight": e === this.pointer && this.showPointer },
        { "multiselect__option--group-selected": this.wholeGroupSelected(i) }
      ] : "multiselect__option--disabled";
    },
    addPointerElement({ key: e } = "Enter") {
      this.filteredOptions.length > 0 && this.select(this.filteredOptions[this.pointer], e), this.pointerReset();
    },
    pointerForward() {
      this.pointer < this.filteredOptions.length - 1 && (this.pointer++, this.$refs.list.scrollTop <= this.pointerPosition - (this.visibleElements - 1) * this.optionHeight && (this.$refs.list.scrollTop = this.pointerPosition - (this.visibleElements - 1) * this.optionHeight), this.filteredOptions[this.pointer] && this.filteredOptions[this.pointer].$isLabel && !this.groupSelect && this.pointerForward()), this.pointerDirty = !0;
    },
    pointerBackward() {
      this.pointer > 0 ? (this.pointer--, this.$refs.list.scrollTop >= this.pointerPosition && (this.$refs.list.scrollTop = this.pointerPosition), this.filteredOptions[this.pointer] && this.filteredOptions[this.pointer].$isLabel && !this.groupSelect && this.pointerBackward()) : this.filteredOptions[this.pointer] && this.filteredOptions[0].$isLabel && !this.groupSelect && this.pointerForward(), this.pointerDirty = !0;
    },
    pointerReset() {
      !this.closeOnSelect || (this.pointer = 0, this.$refs.list && (this.$refs.list.scrollTop = 0));
    },
    pointerAdjust() {
      this.pointer >= this.filteredOptions.length - 1 && (this.pointer = this.filteredOptions.length ? this.filteredOptions.length - 1 : 0), this.filteredOptions.length > 0 && this.filteredOptions[this.pointer].$isLabel && !this.groupSelect && this.pointerForward();
    },
    pointerSet(e) {
      this.pointer = e, this.pointerDirty = !0;
    }
  }
}, F = {
  name: "vue-multiselect",
  mixins: [U, J],
  props: {
    name: {
      type: String,
      default: ""
    },
    modelValue: {
      type: null,
      default() {
        return [];
      }
    },
    selectLabel: {
      type: String,
      default: "Press enter to select"
    },
    selectGroupLabel: {
      type: String,
      default: "Press enter to select group"
    },
    selectedLabel: {
      type: String,
      default: "Selected"
    },
    deselectLabel: {
      type: String,
      default: "Press enter to remove"
    },
    deselectGroupLabel: {
      type: String,
      default: "Press enter to deselect group"
    },
    showLabels: {
      type: Boolean,
      default: !0
    },
    limit: {
      type: Number,
      default: 99999
    },
    maxHeight: {
      type: Number,
      default: 300
    },
    limitText: {
      type: Function,
      default: (e) => `and ${e} more`
    },
    loading: {
      type: Boolean,
      default: !1
    },
    disabled: {
      type: Boolean,
      default: !1
    },
    openDirection: {
      type: String,
      default: ""
    },
    showNoOptions: {
      type: Boolean,
      default: !0
    },
    showNoResults: {
      type: Boolean,
      default: !0
    },
    tabindex: {
      type: Number,
      default: 0
    }
  },
  computed: {
    isSingleLabelVisible() {
      return (this.singleValue || this.singleValue === 0) && (!this.isOpen || !this.searchable) && !this.visibleValues.length;
    },
    isPlaceholderVisible() {
      return !this.internalValue.length && (!this.searchable || !this.isOpen);
    },
    visibleValues() {
      return this.multiple ? this.internalValue.slice(0, this.limit) : [];
    },
    singleValue() {
      return this.internalValue[0];
    },
    deselectLabelText() {
      return this.showLabels ? this.deselectLabel : "";
    },
    deselectGroupLabelText() {
      return this.showLabels ? this.deselectGroupLabel : "";
    },
    selectLabelText() {
      return this.showLabels ? this.selectLabel : "";
    },
    selectGroupLabelText() {
      return this.showLabels ? this.selectGroupLabel : "";
    },
    selectedLabelText() {
      return this.showLabels ? this.selectedLabel : "";
    },
    inputStyle() {
      return this.searchable || this.multiple && this.modelValue && this.modelValue.length ? this.isOpen ? { width: "100%" } : { width: "0", position: "absolute", padding: "0" } : "";
    },
    contentStyle() {
      return this.options.length ? { display: "inline-block" } : { display: "block" };
    },
    isAbove() {
      return this.openDirection === "above" || this.openDirection === "top" ? !0 : this.openDirection === "below" || this.openDirection === "bottom" ? !1 : this.preferredOpenDirection === "above";
    },
    showSearchInput() {
      return this.searchable && (this.hasSingleSelectedSlot && (this.visibleSingleValue || this.visibleSingleValue === 0) ? this.isOpen : !0);
    }
  }
};
const Q = {
  ref: "tags",
  class: "multiselect__tags"
}, W = { class: "multiselect__tags-wrap" }, X = { class: "multiselect__spinner" }, Y = { key: 0 }, Z = { class: "multiselect__option" }, x = { class: "multiselect__option" }, _ = /* @__PURE__ */ L("No elements found. Consider changing the search query."), ee = { class: "multiselect__option" }, te = /* @__PURE__ */ L("List is empty.");
function ie(e, t, i, l, u, n) {
  return o(), c("div", {
    tabindex: e.searchable ? -1 : i.tabindex,
    class: [{ "multiselect--active": e.isOpen, "multiselect--disabled": i.disabled, "multiselect--above": n.isAbove }, "multiselect"],
    onFocus: t[14] || (t[14] = (s) => e.activate()),
    onBlur: t[15] || (t[15] = (s) => e.searchable ? !1 : e.deactivate()),
    onKeydown: [
      t[16] || (t[16] = f(r((s) => e.pointerForward(), ["self", "prevent"]), ["down"])),
      t[17] || (t[17] = f(r((s) => e.pointerBackward(), ["self", "prevent"]), ["up"]))
    ],
    onKeypress: t[18] || (t[18] = f(r((s) => e.addPointerElement(s), ["stop", "self"]), ["enter", "tab"])),
    onKeyup: t[19] || (t[19] = f((s) => e.deactivate(), ["esc"])),
    role: "combobox",
    "aria-owns": "listbox-" + e.id
  }, [
    h(e.$slots, "caret", { toggle: e.toggle }, () => [
      a("div", {
        onMousedown: t[1] || (t[1] = r((s) => e.toggle(), ["prevent", "stop"])),
        class: "multiselect__select"
      }, null, 32)
    ]),
    h(e.$slots, "clear", { search: e.search }),
    a("div", Q, [
      h(e.$slots, "selection", {
        search: e.search,
        remove: e.removeElement,
        values: n.visibleValues,
        isOpen: e.isOpen
      }, () => [
        w(a("div", W, [
          (o(!0), c(D, null, T(n.visibleValues, (s, d) => h(e.$slots, "tag", {
            option: s,
            search: e.search,
            remove: e.removeElement
          }, () => [
            (o(), c("span", {
              class: "multiselect__tag",
              key: d
            }, [
              a("span", {
                textContent: g(e.getOptionLabel(s))
              }, null, 8, ["textContent"]),
              a("i", {
                tabindex: "1",
                onKeypress: f(r((b) => e.removeElement(s), ["prevent"]), ["enter"]),
                onMousedown: r((b) => e.removeElement(s), ["prevent"]),
                class: "multiselect__tag-icon"
              }, null, 40, ["onKeypress", "onMousedown"])
            ]))
          ])), 256))
        ], 512), [
          [O, n.visibleValues.length > 0]
        ]),
        e.internalValue && e.internalValue.length > i.limit ? h(e.$slots, "limit", { key: 0 }, () => [
          a("strong", {
            class: "multiselect__strong",
            textContent: g(i.limitText(e.internalValue.length - i.limit))
          }, null, 8, ["textContent"])
        ]) : y("v-if", !0)
      ]),
      a(A, { name: "multiselect__loading" }, {
        default: H(() => [
          h(e.$slots, "loading", {}, () => [
            w(a("div", X, null, 512), [
              [O, i.loading]
            ])
          ])
        ]),
        _: 3
      }),
      e.searchable ? (o(), c("input", {
        key: 0,
        ref: "search",
        name: i.name,
        id: e.id,
        type: "text",
        autocomplete: "off",
        spellcheck: "false",
        placeholder: e.placeholder,
        style: n.inputStyle,
        value: e.search,
        disabled: i.disabled,
        tabindex: i.tabindex,
        onInput: t[2] || (t[2] = (s) => e.updateSearch(s.target.value)),
        onFocus: t[3] || (t[3] = r((s) => e.activate(), ["prevent"])),
        onBlur: t[4] || (t[4] = r((s) => e.deactivate(), ["prevent"])),
        onKeyup: t[5] || (t[5] = f((s) => e.deactivate(), ["esc"])),
        onKeydown: [
          t[6] || (t[6] = f(r((s) => e.pointerForward(), ["prevent"]), ["down"])),
          t[7] || (t[7] = f(r((s) => e.pointerBackward(), ["prevent"]), ["up"])),
          t[9] || (t[9] = f(r((s) => e.removeLastElement(), ["stop"]), ["delete"]))
        ],
        onKeypress: t[8] || (t[8] = f(r((s) => e.addPointerElement(s), ["prevent", "stop", "self"]), ["enter"])),
        class: "multiselect__input",
        "aria-controls": "listbox-" + e.id
      }, null, 44, ["name", "id", "placeholder", "value", "disabled", "tabindex", "aria-controls"])) : y("v-if", !0),
      n.isSingleLabelVisible ? (o(), c("span", {
        key: 1,
        class: "multiselect__single",
        onMousedown: t[10] || (t[10] = r((...s) => e.toggle && e.toggle(...s), ["prevent"]))
      }, [
        h(e.$slots, "singleLabel", { option: n.singleValue }, () => [
          L(g(e.currentOptionLabel), 1)
        ])
      ], 32)) : y("v-if", !0),
      n.isPlaceholderVisible ? (o(), c("span", {
        key: 2,
        class: "multiselect__placeholder",
        onMousedown: t[11] || (t[11] = r((...s) => e.toggle && e.toggle(...s), ["prevent"]))
      }, [
        h(e.$slots, "placeholder", {}, () => [
          L(g(e.placeholder), 1)
        ])
      ], 32)) : y("v-if", !0)
    ], 512),
    a(A, { name: "multiselect" }, {
      default: H(() => [
        w(a("div", {
          class: "multiselect__content-wrapper",
          onFocus: t[12] || (t[12] = (...s) => e.activate && e.activate(...s)),
          tabindex: "-1",
          onMousedown: t[13] || (t[13] = r(() => {
          }, ["prevent"])),
          style: { maxHeight: e.optimizedHeight + "px" },
          ref: "list"
        }, [
          a("ul", {
            class: "multiselect__content",
            style: n.contentStyle,
            role: "listbox",
            id: "listbox-" + e.id
          }, [
            h(e.$slots, "beforeList"),
            e.multiple && e.max === e.internalValue.length ? (o(), c("li", Y, [
              a("span", Z, [
                h(e.$slots, "maxElements", {}, () => [
                  L("Maximum of " + g(e.max) + " options selected. First remove a selected option to select another.", 1)
                ])
              ])
            ])) : y("v-if", !0),
            !e.max || e.internalValue.length < e.max ? (o(!0), c(D, { key: 1 }, T(e.filteredOptions, (s, d) => (o(), c("li", {
              class: "multiselect__element",
              key: d,
              id: e.id + "-" + d,
              role: s && (s.$isLabel || s.$isDisabled) ? null : "option"
            }, [
              s && (s.$isLabel || s.$isDisabled) ? y("v-if", !0) : (o(), c("span", {
                key: 0,
                class: [e.optionHighlight(d, s), "multiselect__option"],
                onClick: r((b) => e.select(s), ["stop"]),
                onMouseenter: r((b) => e.pointerSet(d), ["self"]),
                "data-select": s && s.isTag ? e.tagPlaceholder : n.selectLabelText,
                "data-selected": n.selectedLabelText,
                "data-deselect": n.deselectLabelText
              }, [
                h(e.$slots, "option", {
                  option: s,
                  search: e.search,
                  index: d
                }, () => [
                  a("span", null, g(e.getOptionLabel(s)), 1)
                ])
              ], 42, ["onClick", "onMouseenter", "data-select", "data-selected", "data-deselect"])),
              s && (s.$isLabel || s.$isDisabled) ? (o(), c("span", {
                key: 1,
                "data-select": e.groupSelect && n.selectGroupLabelText,
                "data-deselect": e.groupSelect && n.deselectGroupLabelText,
                class: [e.groupHighlight(d, s), "multiselect__option"],
                onMouseenter: r((b) => e.groupSelect && e.pointerSet(d), ["self"]),
                onMousedown: r((b) => e.selectGroup(s), ["prevent"])
              }, [
                h(e.$slots, "option", {
                  option: s,
                  search: e.search,
                  index: d
                }, () => [
                  a("span", null, g(e.getOptionLabel(s)), 1)
                ])
              ], 42, ["data-select", "data-deselect", "onMouseenter", "onMousedown"])) : y("v-if", !0)
            ], 8, ["id", "role"]))), 128)) : y("v-if", !0),
            w(a("li", null, [
              a("span", x, [
                h(e.$slots, "noResult", { search: e.search }, () => [
                  _
                ])
              ])
            ], 512), [
              [O, i.showNoResults && e.filteredOptions.length === 0 && e.search && !i.loading]
            ]),
            w(a("li", null, [
              a("span", ee, [
                h(e.$slots, "noOptions", {}, () => [
                  te
                ])
              ])
            ], 512), [
              [O, i.showNoOptions && e.options.length === 0 && !e.search && !i.loading]
            ]),
            h(e.$slots, "afterList")
          ], 12, ["id"])
        ], 36), [
          [O, e.isOpen]
        ])
      ]),
      _: 3
    })
  ], 42, ["tabindex", "aria-owns"]);
}
F.render = ie;
const se = F;
const le = {
  class: "w-full",
  "data-cy": "section-tabs"
}, ne = ["value"], re = ["value"], ae = { class: "flex space-x-4 mb-2" }, oe = ["data-cy", "onClick"], he = /* @__PURE__ */ G({
  __name: "Select",
  props: {
    select: null
  },
  setup(e) {
    const t = e, i = z(0), l = k(() => {
      const { type: p, children: v } = t.select;
      return p || (v.length < 5 ? "tabs" : "dropdown");
    }), u = k(
      () => t.select.children.map(
        (p, v) => p.label || `Section ${v + 1}`
      )
    ), n = k(
      () => u.value.map((p, v) => v)
    ), s = k(() => t.select.children[i.value]), d = (p) => u.value[p], b = (p) => i.value = p, K = (p) => void b(+p.target.value);
    return (p, v) => (o(), S("div", le, [
      B("div", {
        class: E(["w-full mb-2", { "sm:hidden": V(l) === "tabs" }])
      }, [
        t.select.children.length < 10 ? (o(), S("select", {
          key: 0,
          id: "tabs",
          name: "tabs",
          class: "block mb-1 w-auto focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md",
          value: i.value,
          onChange: K
        }, [
          (o(!0), S(D, null, T(V(u), ($, m) => (o(), S("option", {
            key: m,
            value: m
          }, g($), 9, re))), 128))
        ], 40, ne)) : (o(), c(V(se), {
          key: 1,
          modelValue: i.value,
          "onUpdate:modelValue": v[0] || (v[0] = ($) => i.value = $),
          options: V(n),
          "preselect-first": !0,
          "clear-on-select": !1,
          "allow-empty": !1,
          "custom-label": d
        }, null, 8, ["modelValue", "options"]))
      ], 2),
      B("div", {
        class: E(["hidden", { "sm:block": V(l) === "tabs" }])
      }, [
        B("nav", ae, [
          (o(!0), S(D, null, T(t.select.children, ($, m) => (o(), S("a", {
            role: "button",
            key: m,
            "data-cy": `tab-${m}`,
            class: E([
              "px-3 py-2 font-medium text-sm rounded-md",
              {
                "text-dp-accent bg-dp-accent-light": i.value === m,
                "text-dp-light-gray hover:text-dp-dark-gray": i.value !== m
              }
            ]),
            onClick: () => b(m)
          }, g(V(u)[m]), 11, oe))), 128))
        ])
      ], 2),
      B("div", null, [
        h(p.$slots, "default", { tree: V(s) })
      ])
    ]));
  }
});
export {
  he as default
};
