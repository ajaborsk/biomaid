(function(win, vue, primevue2) {
  "use strict";
  var __vite_style__ = document.createElement("style");
  __vite_style__.textContent = "\nh1[data-v-f14ffa1a] {\n  font-weight: 500;\n  font-size: 2.6rem;\n  top: -10px;\n}\nh3[data-v-f14ffa1a] {\n  font-size: 1.2rem;\n}\n.greetings h1[data-v-f14ffa1a],\n.greetings h3[data-v-f14ffa1a] {\n  text-align: center;\n}\n@media (min-width: 1024px) {\n.greetings h1[data-v-f14ffa1a],\n  .greetings h3[data-v-f14ffa1a] {\n    text-align: center;\n}\n}\n.p-button[data-v-f14ffa1a] {\n  margin-right: 0.5rem;\n  text-align: center;\n}\n.p-buttonset .p-button[data-v-f14ffa1a] {\n  margin-right: 0;\n}\n.sizes .button[data-v-f14ffa1a] {\n  margin-bottom: 0.5rem;\n  display: block;\n}\n.template .p-button i[data-v-f14ffa1a] {\n  line-height: 2.25rem;\n}\n";
  document.head.appendChild(__vite_style__);
  const DemoWidget_vue_vue_type_style_index_0_scoped_f14ffa1a_lang = "";
  const _export_sfc = (sfc, props) => {
    const target = sfc.__vccOpts || sfc;
    for (const [key, val] of props) {
      target[key] = val;
    }
    return target;
  };
  const _withScopeId = (n) => (vue.pushScopeId("data-v-f14ffa1a"), n = n(), vue.popScopeId(), n);
  const _hoisted_1 = { class: "greetings" };
  const _hoisted_2 = { class: "green" };
  const _hoisted_3 = /* @__PURE__ */ _withScopeId(() => /* @__PURE__ */ vue.createElementVNode("h3", null, [
    /* @__PURE__ */ vue.createTextVNode(" You’ve successfully created a widget with "),
    /* @__PURE__ */ vue.createElementVNode("a", {
      href: "https://vitejs.dev/",
      target: "_blank",
      rel: "noopener"
    }, "Vite"),
    /* @__PURE__ */ vue.createTextVNode(" + "),
    /* @__PURE__ */ vue.createElementVNode("a", {
      href: "https://vuejs.org/",
      target: "_blank",
      rel: "noopener"
    }, "Vue 3"),
    /* @__PURE__ */ vue.createTextVNode(". ")
  ], -1));
  const _sfc_main = {
    __name: "DemoWidget",
    props: {
      msg: {
        type: String,
        required: true
      }
    },
    setup(__props) {
      const Button = primevue2.button;
      const Dialog = primevue2.dialog;
      const displayModal = vue.ref(false);
      function openModal(ev) {
        displayModal.value = true;
      }
      return (_ctx, _cache) => {
        return vue.openBlock(), vue.createElementBlock("div", _hoisted_1, [
          vue.createElementVNode("h1", _hoisted_2, vue.toDisplayString(__props.msg), 1),
          _hoisted_3,
          vue.createVNode(vue.unref(Button), {
            label: __props.msg,
            icon: "pi pi-check",
            iconPos: "right",
            onClick: openModal
          }, null, 8, ["label"]),
          vue.createVNode(vue.unref(Dialog), {
            header: "Confirmation",
            visible: displayModal.value,
            "onUpdate:visible": _cache[0] || (_cache[0] = ($event) => displayModal.value = $event),
            style: { width: "350px" },
            modal: true
          }, {
            default: vue.withCtx(() => [
              vue.createTextVNode(vue.toDisplayString(__props.msg), 1)
            ]),
            _: 1
          }, 8, ["visible"])
        ]);
      };
    }
  };
  const demo_widget = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-f14ffa1a"]]);
  win.demo_widget = demo_widget;
})(window, Vue, primevue);
