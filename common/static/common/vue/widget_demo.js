(function(win, vue) {
  "use strict";
  var __vite_style__ = document.createElement("style");
  __vite_style__.textContent = "\nh1[data-v-283afba5] {\n  font-weight: 500;\n  font-size: 2.6rem;\n  top: -10px;\n}\nh3[data-v-283afba5] {\n  font-size: 1.2rem;\n}\n.greetings h1[data-v-283afba5],\n.greetings h3[data-v-283afba5] {\n  text-align: center;\n}\n@media (min-width: 1024px) {\n.greetings h1[data-v-283afba5],\n  .greetings h3[data-v-283afba5] {\n    text-align: center;\n}\n}\n.p-button[data-v-283afba5] {\n  margin-right: 0.5rem;\n  text-align: center;\n}\n.p-buttonset .p-button[data-v-283afba5] {\n  margin-right: 0;\n}\n.sizes .button[data-v-283afba5] {\n  margin-bottom: 0.5rem;\n  display: block;\n}\n.template .p-button i[data-v-283afba5] {\n  line-height: 2.25rem;\n}\n";
  document.head.appendChild(__vite_style__);
  var DomHandler = {
    innerWidth(el) {
      if (el) {
        let width = el.offsetWidth;
        let style = getComputedStyle(el);
        width += parseFloat(style.paddingLeft) + parseFloat(style.paddingRight);
        return width;
      }
      return 0;
    },
    width(el) {
      if (el) {
        let width = el.offsetWidth;
        let style = getComputedStyle(el);
        width -= parseFloat(style.paddingLeft) + parseFloat(style.paddingRight);
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
          let style = getComputedStyle(el);
          width += parseFloat(style.marginLeft) + parseFloat(style.marginRight);
        }
        return width;
      }
      return 0;
    },
    getOuterHeight(el, margin) {
      if (el) {
        let height = el.offsetHeight;
        if (margin) {
          let style = getComputedStyle(el);
          height += parseFloat(style.marginTop) + parseFloat(style.marginBottom);
        }
        return height;
      }
      return 0;
    },
    getClientHeight(el, margin) {
      if (el) {
        let height = el.clientHeight;
        if (margin) {
          let style = getComputedStyle(el);
          height += parseFloat(style.marginTop) + parseFloat(style.marginBottom);
        }
        return height;
      }
      return 0;
    },
    getViewport() {
      let win2 = window, d = document, e = d.documentElement, g = d.getElementsByTagName("body")[0], w = win2.innerWidth || e.clientWidth || g.clientWidth, h = win2.innerHeight || e.clientHeight || g.clientHeight;
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
        let style = getComputedStyle(el);
        height -= parseFloat(style.paddingTop) + parseFloat(style.paddingBottom) + parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth);
        return height;
      }
      return 0;
    },
    getWidth(el) {
      if (el) {
        let width = el.offsetWidth;
        let style = getComputedStyle(el);
        width -= parseFloat(style.paddingLeft) + parseFloat(style.paddingRight) + parseFloat(style.borderLeftWidth) + parseFloat(style.borderRightWidth);
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
    fadeOut(element, ms) {
      if (element) {
        let opacity = 1, interval = 50, duration = ms, gap = interval / duration;
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
    applyStyle(element, style) {
      if (typeof style === "string") {
        element.style.cssText = style;
      } else {
        for (let prop in style) {
          element.style[prop] = style[prop];
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
  var script = {
    name: "Button",
    props: {
      label: {
        type: String,
        default: null
      },
      icon: {
        type: String,
        default: null
      },
      iconPos: {
        type: String,
        default: "left"
      },
      iconClass: {
        type: String,
        default: null
      },
      badge: {
        type: String,
        default: null
      },
      badgeClass: {
        type: String,
        default: null
      },
      loading: {
        type: Boolean,
        default: false
      },
      loadingIcon: {
        type: String,
        default: "pi pi-spinner pi-spin"
      }
    },
    computed: {
      buttonClass() {
        return {
          "p-button p-component": true,
          "p-button-icon-only": this.icon && !this.label,
          "p-button-vertical": (this.iconPos === "top" || this.iconPos === "bottom") && this.label,
          "p-disabled": this.$attrs.disabled || this.loading,
          "p-button-loading": this.loading,
          "p-button-loading-label-only": this.loading && !this.icon && this.label
        };
      },
      iconStyleClass() {
        return [
          this.loading ? "p-button-loading-icon " + this.loadingIcon : this.icon,
          "p-button-icon",
          this.iconClass,
          {
            "p-button-icon-left": this.iconPos === "left" && this.label,
            "p-button-icon-right": this.iconPos === "right" && this.label,
            "p-button-icon-top": this.iconPos === "top" && this.label,
            "p-button-icon-bottom": this.iconPos === "bottom" && this.label
          }
        ];
      },
      badgeStyleClass() {
        return [
          "p-badge p-component",
          this.badgeClass,
          {
            "p-badge-no-gutter": this.badge && String(this.badge).length === 1
          }
        ];
      },
      disabled() {
        return this.$attrs.disabled || this.loading;
      },
      defaultAriaLabel() {
        return this.label ? this.label + (this.badge ? " " + this.badge : "") : this.$attrs["aria-label"];
      }
    },
    directives: {
      ripple: Ripple
    }
  };
  const _hoisted_1$1 = ["aria-label", "disabled"];
  const _hoisted_2$1 = { class: "p-button-label" };
  function render(_ctx, _cache, $props, $setup, $data, $options) {
    const _directive_ripple = vue.resolveDirective("ripple");
    return vue.withDirectives((vue.openBlock(), vue.createElementBlock("button", {
      class: vue.normalizeClass($options.buttonClass),
      type: "button",
      "aria-label": $options.defaultAriaLabel,
      disabled: $options.disabled
    }, [
      vue.renderSlot(_ctx.$slots, "default", {}, () => [
        $props.loading && !$props.icon ? (vue.openBlock(), vue.createElementBlock("span", {
          key: 0,
          class: vue.normalizeClass($options.iconStyleClass)
        }, null, 2)) : vue.createCommentVNode("", true),
        $props.icon ? (vue.openBlock(), vue.createElementBlock("span", {
          key: 1,
          class: vue.normalizeClass($options.iconStyleClass)
        }, null, 2)) : vue.createCommentVNode("", true),
        vue.createElementVNode("span", _hoisted_2$1, vue.toDisplayString($props.label || " "), 1),
        $props.badge ? (vue.openBlock(), vue.createElementBlock("span", {
          key: 2,
          class: vue.normalizeClass($options.badgeStyleClass)
        }, vue.toDisplayString($props.badge), 3)) : vue.createCommentVNode("", true)
      ])
    ], 10, _hoisted_1$1)), [
      [_directive_ripple]
    ]);
  }
  script.render = render;
  const DemoWidget_vue_vue_type_style_index_0_scoped_283afba5_lang = "";
  const _export_sfc = (sfc, props) => {
    const target = sfc.__vccOpts || sfc;
    for (const [key, val] of props) {
      target[key] = val;
    }
    return target;
  };
  const _withScopeId = (n) => (vue.pushScopeId("data-v-283afba5"), n = n(), vue.popScopeId(), n);
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
      return (_ctx, _cache) => {
        return vue.openBlock(), vue.createElementBlock("div", _hoisted_1, [
          vue.createElementVNode("h1", _hoisted_2, vue.toDisplayString(__props.msg), 1),
          _hoisted_3,
          vue.createVNode(vue.unref(script), {
            label: __props.msg,
            icon: "pi pi-check",
            iconPos: "right"
          }, null, 8, ["label"])
        ]);
      };
    }
  };
  const dw = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-283afba5"]]);
  win.demo_widget = dw;
})(window, Vue);
