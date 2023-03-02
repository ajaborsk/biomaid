(function(win, vue) {
  "use strict";
  var __vite_style__ = document.createElement("style");
  __vite_style__.textContent = "\nh1[data-v-f34a3253] {\n  font-weight: 500;\n  font-size: 2.6rem;\n  top: -10px;\n}\nh3[data-v-f34a3253] {\n  font-size: 1.2rem;\n}\n.greetings h1[data-v-f34a3253],\n.greetings h3[data-v-f34a3253] {\n  text-align: center;\n}\n@media (min-width: 1024px) {\n.greetings h1[data-v-f34a3253],\n  .greetings h3[data-v-f34a3253] {\n    text-align: center;\n}\n}\n.p-button[data-v-f34a3253] {\n  margin-right: 0.5rem;\n  text-align: center;\n}\n.p-buttonset .p-button[data-v-f34a3253] {\n  margin-right: 0;\n}\n.sizes .button[data-v-f34a3253] {\n  margin-bottom: 0.5rem;\n  display: block;\n}\n.template .p-button i[data-v-f34a3253] {\n  line-height: 2.25rem;\n}\n";
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
    reorderArray(value, from, to) {
      if (value && from !== to) {
        if (to >= value.length) {
          to %= value.length;
          from %= value.length;
        }
        value.splice(to, 0, value.splice(from, 1)[0]);
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
  var script$2 = {
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
  const _hoisted_1$2 = ["aria-label", "disabled"];
  const _hoisted_2$2 = { class: "p-button-label" };
  function render$2(_ctx, _cache, $props, $setup, $data, $options) {
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
        vue.createElementVNode("span", _hoisted_2$2, vue.toDisplayString($props.label || " "), 1),
        $props.badge ? (vue.openBlock(), vue.createElementBlock("span", {
          key: 2,
          class: vue.normalizeClass($options.badgeStyleClass)
        }, vue.toDisplayString($props.badge), 3)) : vue.createCommentVNode("", true)
      ])
    ], 10, _hoisted_1$2)), [
      [_directive_ripple]
    ]);
  }
  script$2.render = render$2;
  function bind(el, binding) {
    const { onFocusIn, onFocusOut } = binding.value || {};
    el.$_pfocustrap_mutationobserver = new MutationObserver((mutationList) => {
      mutationList.forEach((mutation) => {
        if (mutation.type === "childList" && !el.contains(document.activeElement)) {
          const findNextFocusableElement = (el2) => {
            const focusableElement = DomHandler.isFocusableElement(el2) ? el2 : DomHandler.getFirstFocusableElement(el2);
            return ObjectUtils.isNotEmpty(focusableElement) ? focusableElement : findNextFocusableElement(el2.nextSibling);
          };
          DomHandler.focus(findNextFocusableElement(mutation.nextSibling));
        }
      });
    });
    el.$_pfocustrap_mutationobserver.disconnect();
    el.$_pfocustrap_mutationobserver.observe(el, {
      childList: true
    });
    el.$_pfocustrap_focusinlistener = (event) => onFocusIn && onFocusIn(event);
    el.$_pfocustrap_focusoutlistener = (event) => onFocusOut && onFocusOut(event);
    el.addEventListener("focusin", el.$_pfocustrap_focusinlistener);
    el.addEventListener("focusout", el.$_pfocustrap_focusoutlistener);
  }
  function unbind(el) {
    el.$_pfocustrap_mutationobserver && el.$_pfocustrap_mutationobserver.disconnect();
    el.$_pfocustrap_focusinlistener && el.removeEventListener("focusin", el.$_pfocustrap_focusinlistener) && (el.$_pfocustrap_focusinlistener = null);
    el.$_pfocustrap_focusoutlistener && el.removeEventListener("focusout", el.$_pfocustrap_focusoutlistener) && (el.$_pfocustrap_focusoutlistener = null);
  }
  function autoFocus(el, binding) {
    const { autoFocusSelector = "", firstFocusableSelector = "", autoFocus: autoFocus2 = false } = binding.value || {};
    let focusableElement = DomHandler.getFirstFocusableElement(el, `[autofocus]:not(.p-hidden-focusable)${autoFocusSelector}`);
    autoFocus2 && !focusableElement && (focusableElement = DomHandler.getFirstFocusableElement(el, `:not(.p-hidden-focusable)${firstFocusableSelector}`));
    DomHandler.focus(focusableElement);
  }
  function onFirstHiddenElementFocus(event) {
    const { currentTarget, relatedTarget } = event;
    const focusableElement = relatedTarget === currentTarget.$_pfocustrap_lasthiddenfocusableelement ? DomHandler.getFirstFocusableElement(currentTarget.parentElement, `:not(.p-hidden-focusable)${currentTarget.$_pfocustrap_focusableselector}`) : currentTarget.$_pfocustrap_lasthiddenfocusableelement;
    DomHandler.focus(focusableElement);
  }
  function onLastHiddenElementFocus(event) {
    const { currentTarget, relatedTarget } = event;
    const focusableElement = relatedTarget === currentTarget.$_pfocustrap_firsthiddenfocusableelement ? DomHandler.getLastFocusableElement(currentTarget.parentElement, `:not(.p-hidden-focusable)${currentTarget.$_pfocustrap_focusableselector}`) : currentTarget.$_pfocustrap_firsthiddenfocusableelement;
    DomHandler.focus(focusableElement);
  }
  function createHiddenFocusableElements(el, binding) {
    const { tabIndex = 0, firstFocusableSelector = "", lastFocusableSelector = "" } = binding.value || {};
    const createFocusableElement = (onFocus) => {
      const element = document.createElement("span");
      element.classList = "p-hidden-accessible p-hidden-focusable";
      element.tabIndex = tabIndex;
      element.setAttribute("aria-hidden", "true");
      element.setAttribute("role", "presentation");
      element.addEventListener("focus", onFocus);
      return element;
    };
    const firstFocusableElement = createFocusableElement(onFirstHiddenElementFocus);
    const lastFocusableElement = createFocusableElement(onLastHiddenElementFocus);
    firstFocusableElement.$_pfocustrap_lasthiddenfocusableelement = lastFocusableElement;
    firstFocusableElement.$_pfocustrap_focusableselector = firstFocusableSelector;
    lastFocusableElement.$_pfocustrap_firsthiddenfocusableelement = firstFocusableElement;
    lastFocusableElement.$_pfocustrap_focusableselector = lastFocusableSelector;
    el.prepend(firstFocusableElement);
    el.append(lastFocusableElement);
  }
  const FocusTrap = {
    mounted(el, binding) {
      const { disabled } = binding.value || {};
      if (!disabled) {
        createHiddenFocusableElements(el, binding);
        bind(el, binding);
        autoFocus(el, binding);
      }
    },
    updated(el, binding) {
      const { disabled } = binding.value || {};
      disabled && unbind(el);
    },
    unmounted(el) {
      unbind(el);
    }
  };
  var script$1 = {
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
  function render$1(_ctx, _cache, $props, $setup, $data, $options) {
    return $options.inline ? vue.renderSlot(_ctx.$slots, "default", { key: 0 }) : $data.mounted ? (vue.openBlock(), vue.createBlock(vue.Teleport, {
      key: 1,
      to: $props.appendTo
    }, [
      vue.renderSlot(_ctx.$slots, "default")
    ], 8, ["to"])) : vue.createCommentVNode("", true);
  }
  script$1.render = render$1;
  var script = {
    name: "Dialog",
    inheritAttrs: false,
    emits: ["update:visible", "show", "hide", "after-hide", "maximize", "unmaximize", "dragend"],
    props: {
      header: {
        type: null,
        default: null
      },
      footer: {
        type: null,
        default: null
      },
      visible: {
        type: Boolean,
        default: false
      },
      modal: {
        type: Boolean,
        default: null
      },
      contentStyle: {
        type: null,
        default: null
      },
      contentClass: {
        type: String,
        default: null
      },
      contentProps: {
        type: null,
        default: null
      },
      rtl: {
        type: Boolean,
        default: null
      },
      maximizable: {
        type: Boolean,
        default: false
      },
      dismissableMask: {
        type: Boolean,
        default: false
      },
      closable: {
        type: Boolean,
        default: true
      },
      closeOnEscape: {
        type: Boolean,
        default: true
      },
      showHeader: {
        type: Boolean,
        default: true
      },
      baseZIndex: {
        type: Number,
        default: 0
      },
      autoZIndex: {
        type: Boolean,
        default: true
      },
      position: {
        type: String,
        default: "center"
      },
      breakpoints: {
        type: Object,
        default: null
      },
      draggable: {
        type: Boolean,
        default: true
      },
      keepInViewport: {
        type: Boolean,
        default: true
      },
      minX: {
        type: Number,
        default: 0
      },
      minY: {
        type: Number,
        default: 0
      },
      appendTo: {
        type: String,
        default: "body"
      },
      closeIcon: {
        type: String,
        default: "pi pi-times"
      },
      maximizeIcon: {
        type: String,
        default: "pi pi-window-maximize"
      },
      minimizeIcon: {
        type: String,
        default: "pi pi-window-minimize"
      },
      closeButtonProps: {
        type: null,
        default: null
      },
      _instance: null
    },
    provide() {
      return {
        dialogRef: vue.computed(() => this._instance)
      };
    },
    data() {
      return {
        containerVisible: this.visible,
        maximized: false,
        focusable: false
      };
    },
    documentKeydownListener: null,
    container: null,
    mask: null,
    content: null,
    headerContainer: null,
    footerContainer: null,
    maximizableButton: null,
    closeButton: null,
    styleElement: null,
    dragging: null,
    documentDragListener: null,
    documentDragEndListener: null,
    lastPageX: null,
    lastPageY: null,
    updated() {
      if (this.visible) {
        this.containerVisible = this.visible;
      }
    },
    beforeUnmount() {
      this.unbindDocumentState();
      this.unbindGlobalListeners();
      this.destroyStyle();
      if (this.mask && this.autoZIndex) {
        ZIndexUtils.clear(this.mask);
      }
      this.container = null;
      this.mask = null;
    },
    mounted() {
      if (this.breakpoints) {
        this.createStyle();
      }
    },
    methods: {
      close() {
        this.$emit("update:visible", false);
      },
      onBeforeEnter(el) {
        el.setAttribute(this.attributeSelector, "");
      },
      onEnter() {
        this.$emit("show");
        this.focus();
        this.enableDocumentSettings();
        this.bindGlobalListeners();
        if (this.autoZIndex) {
          ZIndexUtils.set("modal", this.mask, this.baseZIndex + this.$primevue.config.zIndex.modal);
        }
      },
      onBeforeLeave() {
        if (this.modal) {
          DomHandler.addClass(this.mask, "p-component-overlay-leave");
        }
      },
      onLeave() {
        this.$emit("hide");
        this.focusable = false;
      },
      onAfterLeave() {
        if (this.autoZIndex) {
          ZIndexUtils.clear(this.mask);
        }
        this.containerVisible = false;
        this.unbindDocumentState();
        this.unbindGlobalListeners();
        this.$emit("after-hide");
      },
      onMaskClick(event) {
        if (this.dismissableMask && this.modal && this.mask === event.target) {
          this.close();
        }
      },
      focus() {
        const findFocusableElement = (container) => {
          return container.querySelector("[autofocus]");
        };
        let focusTarget = this.$slots.footer && findFocusableElement(this.footerContainer);
        if (!focusTarget) {
          focusTarget = this.$slots.header && findFocusableElement(this.headerContainer);
          if (!focusTarget) {
            focusTarget = this.$slots.default && findFocusableElement(this.content);
            if (!focusTarget) {
              focusTarget = findFocusableElement(this.container);
            }
          }
        }
        if (focusTarget) {
          this.focusable = true;
          focusTarget.focus();
        }
      },
      maximize(event) {
        if (this.maximized) {
          this.maximized = false;
          this.$emit("unmaximize", event);
        } else {
          this.maximized = true;
          this.$emit("maximize", event);
        }
        if (!this.modal) {
          if (this.maximized)
            DomHandler.addClass(document.body, "p-overflow-hidden");
          else
            DomHandler.removeClass(document.body, "p-overflow-hidden");
        }
      },
      enableDocumentSettings() {
        if (this.modal || this.maximizable && this.maximized) {
          DomHandler.addClass(document.body, "p-overflow-hidden");
        }
      },
      unbindDocumentState() {
        if (this.modal || this.maximizable && this.maximized) {
          DomHandler.removeClass(document.body, "p-overflow-hidden");
        }
      },
      onKeyDown(event) {
        if (event.code === "Escape" && this.closeOnEscape) {
          this.close();
        }
      },
      bindDocumentKeyDownListener() {
        if (!this.documentKeydownListener) {
          this.documentKeydownListener = this.onKeyDown.bind(this);
          window.document.addEventListener("keydown", this.documentKeydownListener);
        }
      },
      unbindDocumentKeyDownListener() {
        if (this.documentKeydownListener) {
          window.document.removeEventListener("keydown", this.documentKeydownListener);
          this.documentKeydownListener = null;
        }
      },
      getPositionClass() {
        const positions = ["left", "right", "top", "topleft", "topright", "bottom", "bottomleft", "bottomright"];
        const pos = positions.find((item) => item === this.position);
        return pos ? `p-dialog-${pos}` : "";
      },
      containerRef(el) {
        this.container = el;
      },
      maskRef(el) {
        this.mask = el;
      },
      contentRef(el) {
        this.content = el;
      },
      headerContainerRef(el) {
        this.headerContainer = el;
      },
      footerContainerRef(el) {
        this.footerContainer = el;
      },
      maximizableRef(el) {
        this.maximizableButton = el;
      },
      closeButtonRef(el) {
        this.closeButton = el;
      },
      createStyle() {
        if (!this.styleElement) {
          this.styleElement = document.createElement("style");
          this.styleElement.type = "text/css";
          document.head.appendChild(this.styleElement);
          let innerHTML = "";
          for (let breakpoint in this.breakpoints) {
            innerHTML += `
                        @media screen and (max-width: ${breakpoint}) {
                            .p-dialog[${this.attributeSelector}] {
                                width: ${this.breakpoints[breakpoint]} !important;
                            }
                        }
                    `;
          }
          this.styleElement.innerHTML = innerHTML;
        }
      },
      destroyStyle() {
        if (this.styleElement) {
          document.head.removeChild(this.styleElement);
          this.styleElement = null;
        }
      },
      initDrag(event) {
        if (DomHandler.hasClass(event.target, "p-dialog-header-icon") || DomHandler.hasClass(event.target.parentElement, "p-dialog-header-icon")) {
          return;
        }
        if (this.draggable) {
          this.dragging = true;
          this.lastPageX = event.pageX;
          this.lastPageY = event.pageY;
          this.container.style.margin = "0";
          DomHandler.addClass(document.body, "p-unselectable-text");
        }
      },
      bindGlobalListeners() {
        if (this.draggable) {
          this.bindDocumentDragListener();
          this.bindDocumentDragEndListener();
        }
        if (this.closeOnEscape && this.closable) {
          this.bindDocumentKeyDownListener();
        }
      },
      unbindGlobalListeners() {
        this.unbindDocumentDragListener();
        this.unbindDocumentDragEndListener();
        this.unbindDocumentKeyDownListener();
      },
      bindDocumentDragListener() {
        this.documentDragListener = (event) => {
          if (this.dragging) {
            let width = DomHandler.getOuterWidth(this.container);
            let height = DomHandler.getOuterHeight(this.container);
            let deltaX = event.pageX - this.lastPageX;
            let deltaY = event.pageY - this.lastPageY;
            let offset = this.container.getBoundingClientRect();
            let leftPos = offset.left + deltaX;
            let topPos = offset.top + deltaY;
            let viewport = DomHandler.getViewport();
            this.container.style.position = "fixed";
            if (this.keepInViewport) {
              if (leftPos >= this.minX && leftPos + width < viewport.width) {
                this.lastPageX = event.pageX;
                this.container.style.left = leftPos + "px";
              }
              if (topPos >= this.minY && topPos + height < viewport.height) {
                this.lastPageY = event.pageY;
                this.container.style.top = topPos + "px";
              }
            } else {
              this.lastPageX = event.pageX;
              this.container.style.left = leftPos + "px";
              this.lastPageY = event.pageY;
              this.container.style.top = topPos + "px";
            }
          }
        };
        window.document.addEventListener("mousemove", this.documentDragListener);
      },
      unbindDocumentDragListener() {
        if (this.documentDragListener) {
          window.document.removeEventListener("mousemove", this.documentDragListener);
          this.documentDragListener = null;
        }
      },
      bindDocumentDragEndListener() {
        this.documentDragEndListener = (event) => {
          if (this.dragging) {
            this.dragging = false;
            DomHandler.removeClass(document.body, "p-unselectable-text");
            this.$emit("dragend", event);
          }
        };
        window.document.addEventListener("mouseup", this.documentDragEndListener);
      },
      unbindDocumentDragEndListener() {
        if (this.documentDragEndListener) {
          window.document.removeEventListener("mouseup", this.documentDragEndListener);
          this.documentDragEndListener = null;
        }
      }
    },
    computed: {
      maskClass() {
        return ["p-dialog-mask", { "p-component-overlay p-component-overlay-enter": this.modal }, this.getPositionClass()];
      },
      dialogClass() {
        return [
          "p-dialog p-component",
          {
            "p-dialog-rtl": this.rtl,
            "p-dialog-maximized": this.maximizable && this.maximized,
            "p-input-filled": this.$primevue.config.inputStyle === "filled",
            "p-ripple-disabled": this.$primevue.config.ripple === false
          }
        ];
      },
      maximizeIconClass() {
        return [
          "p-dialog-header-maximize-icon",
          {
            [this.maximizeIcon]: !this.maximized,
            [this.minimizeIcon]: this.maximized
          }
        ];
      },
      ariaId() {
        return UniqueComponentId();
      },
      ariaLabelledById() {
        return this.header != null || this.$attrs["aria-labelledby"] !== null ? this.ariaId + "_header" : null;
      },
      closeAriaLabel() {
        return this.$primevue.config.locale.aria ? this.$primevue.config.locale.aria.close : void 0;
      },
      attributeSelector() {
        return UniqueComponentId();
      },
      contentStyleClass() {
        return ["p-dialog-content", this.contentClass];
      }
    },
    directives: {
      ripple: Ripple,
      focustrap: FocusTrap
    },
    components: {
      Portal: script$1
    }
  };
  const _hoisted_1$1 = ["aria-labelledby", "aria-modal"];
  const _hoisted_2$1 = ["id"];
  const _hoisted_3$1 = { class: "p-dialog-header-icons" };
  const _hoisted_4 = ["autofocus", "tabindex"];
  const _hoisted_5 = ["autofocus", "aria-label"];
  function render(_ctx, _cache, $props, $setup, $data, $options) {
    const _component_Portal = vue.resolveComponent("Portal");
    const _directive_ripple = vue.resolveDirective("ripple");
    const _directive_focustrap = vue.resolveDirective("focustrap");
    return vue.openBlock(), vue.createBlock(_component_Portal, { appendTo: $props.appendTo }, {
      default: vue.withCtx(() => [
        $data.containerVisible ? (vue.openBlock(), vue.createElementBlock("div", {
          key: 0,
          ref: $options.maskRef,
          class: vue.normalizeClass($options.maskClass),
          onClick: _cache[3] || (_cache[3] = (...args) => $options.onMaskClick && $options.onMaskClick(...args))
        }, [
          vue.createVNode(vue.Transition, {
            name: "p-dialog",
            onBeforeEnter: $options.onBeforeEnter,
            onEnter: $options.onEnter,
            onBeforeLeave: $options.onBeforeLeave,
            onLeave: $options.onLeave,
            onAfterLeave: $options.onAfterLeave,
            appear: ""
          }, {
            default: vue.withCtx(() => [
              $props.visible ? vue.withDirectives((vue.openBlock(), vue.createElementBlock("div", vue.mergeProps({
                key: 0,
                ref: $options.containerRef,
                class: $options.dialogClass,
                role: "dialog",
                "aria-labelledby": $options.ariaLabelledById,
                "aria-modal": $props.modal
              }, _ctx.$attrs), [
                $props.showHeader ? (vue.openBlock(), vue.createElementBlock("div", {
                  key: 0,
                  ref: $options.headerContainerRef,
                  class: "p-dialog-header",
                  onMousedown: _cache[2] || (_cache[2] = (...args) => $options.initDrag && $options.initDrag(...args))
                }, [
                  vue.renderSlot(_ctx.$slots, "header", {}, () => [
                    $props.header ? (vue.openBlock(), vue.createElementBlock("span", {
                      key: 0,
                      id: $options.ariaLabelledById,
                      class: "p-dialog-title"
                    }, vue.toDisplayString($props.header), 9, _hoisted_2$1)) : vue.createCommentVNode("", true)
                  ]),
                  vue.createElementVNode("div", _hoisted_3$1, [
                    $props.maximizable ? vue.withDirectives((vue.openBlock(), vue.createElementBlock("button", {
                      key: 0,
                      ref: $options.maximizableRef,
                      autofocus: $data.focusable,
                      class: "p-dialog-header-icon p-dialog-header-maximize p-link",
                      onClick: _cache[0] || (_cache[0] = (...args) => $options.maximize && $options.maximize(...args)),
                      type: "button",
                      tabindex: $props.maximizable ? "0" : "-1"
                    }, [
                      vue.createElementVNode("span", {
                        class: vue.normalizeClass($options.maximizeIconClass)
                      }, null, 2)
                    ], 8, _hoisted_4)), [
                      [_directive_ripple]
                    ]) : vue.createCommentVNode("", true),
                    $props.closable ? vue.withDirectives((vue.openBlock(), vue.createElementBlock("button", vue.mergeProps({
                      key: 1,
                      ref: $options.closeButtonRef,
                      autofocus: $data.focusable,
                      class: "p-dialog-header-icon p-dialog-header-close p-link",
                      onClick: _cache[1] || (_cache[1] = (...args) => $options.close && $options.close(...args)),
                      "aria-label": $options.closeAriaLabel,
                      type: "button"
                    }, $props.closeButtonProps), [
                      vue.createElementVNode("span", {
                        class: vue.normalizeClass(["p-dialog-header-close-icon", $props.closeIcon])
                      }, null, 2)
                    ], 16, _hoisted_5)), [
                      [_directive_ripple]
                    ]) : vue.createCommentVNode("", true)
                  ])
                ], 544)) : vue.createCommentVNode("", true),
                vue.createElementVNode("div", vue.mergeProps({
                  ref: $options.contentRef,
                  class: $options.contentStyleClass,
                  style: $props.contentStyle
                }, $props.contentProps), [
                  vue.renderSlot(_ctx.$slots, "default")
                ], 16),
                $props.footer || _ctx.$slots.footer ? (vue.openBlock(), vue.createElementBlock("div", {
                  key: 1,
                  ref: $options.footerContainerRef,
                  class: "p-dialog-footer"
                }, [
                  vue.renderSlot(_ctx.$slots, "footer", {}, () => [
                    vue.createTextVNode(vue.toDisplayString($props.footer), 1)
                  ])
                ], 512)) : vue.createCommentVNode("", true)
              ], 16, _hoisted_1$1)), [
                [_directive_focustrap, { disabled: !$props.modal }]
              ]) : vue.createCommentVNode("", true)
            ]),
            _: 3
          }, 8, ["onBeforeEnter", "onEnter", "onBeforeLeave", "onLeave", "onAfterLeave"])
        ], 2)) : vue.createCommentVNode("", true)
      ]),
      _: 3
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
    var style = document.createElement("style");
    style.type = "text/css";
    if (insertAt === "top") {
      if (head.firstChild) {
        head.insertBefore(style, head.firstChild);
      } else {
        head.appendChild(style);
      }
    } else {
      head.appendChild(style);
    }
    if (style.styleSheet) {
      style.styleSheet.cssText = css;
    } else {
      style.appendChild(document.createTextNode(css));
    }
  }
  var css_248z = "\n.p-dialog-mask {\n    position: fixed;\n    top: 0;\n    left: 0;\n    width: 100%;\n    height: 100%;\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    pointer-events: none;\n}\n.p-dialog-mask.p-component-overlay {\n    pointer-events: auto;\n}\n.p-dialog {\n    display: flex;\n    flex-direction: column;\n    pointer-events: auto;\n    max-height: 90%;\n    transform: scale(1);\n}\n.p-dialog-content {\n    overflow-y: auto;\n}\n.p-dialog-header {\n    display: flex;\n    align-items: center;\n    justify-content: space-between;\n    flex-shrink: 0;\n}\n.p-dialog-footer {\n    flex-shrink: 0;\n}\n.p-dialog .p-dialog-header-icons {\n    display: flex;\n    align-items: center;\n}\n.p-dialog .p-dialog-header-icon {\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    overflow: hidden;\n    position: relative;\n}\n\n/* Fluid */\n.p-fluid .p-dialog-footer .p-button {\n    width: auto;\n}\n\n/* Animation */\n/* Center */\n.p-dialog-enter-active {\n    transition: all 150ms cubic-bezier(0, 0, 0.2, 1);\n}\n.p-dialog-leave-active {\n    transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);\n}\n.p-dialog-enter-from,\n.p-dialog-leave-to {\n    opacity: 0;\n    transform: scale(0.7);\n}\n\n/* Top, Bottom, Left, Right, Top* and Bottom* */\n.p-dialog-top .p-dialog,\n.p-dialog-bottom .p-dialog,\n.p-dialog-left .p-dialog,\n.p-dialog-right .p-dialog,\n.p-dialog-topleft .p-dialog,\n.p-dialog-topright .p-dialog,\n.p-dialog-bottomleft .p-dialog,\n.p-dialog-bottomright .p-dialog {\n    margin: 0.75rem;\n    transform: translate3d(0px, 0px, 0px);\n}\n.p-dialog-top .p-dialog-enter-active,\n.p-dialog-top .p-dialog-leave-active,\n.p-dialog-bottom .p-dialog-enter-active,\n.p-dialog-bottom .p-dialog-leave-active,\n.p-dialog-left .p-dialog-enter-active,\n.p-dialog-left .p-dialog-leave-active,\n.p-dialog-right .p-dialog-enter-active,\n.p-dialog-right .p-dialog-leave-active,\n.p-dialog-topleft .p-dialog-enter-active,\n.p-dialog-topleft .p-dialog-leave-active,\n.p-dialog-topright .p-dialog-enter-active,\n.p-dialog-topright .p-dialog-leave-active,\n.p-dialog-bottomleft .p-dialog-enter-active,\n.p-dialog-bottomleft .p-dialog-leave-active,\n.p-dialog-bottomright .p-dialog-enter-active,\n.p-dialog-bottomright .p-dialog-leave-active {\n    transition: all 0.3s ease-out;\n}\n.p-dialog-top .p-dialog-enter-from,\n.p-dialog-top .p-dialog-leave-to {\n    transform: translate3d(0px, -100%, 0px);\n}\n.p-dialog-bottom .p-dialog-enter-from,\n.p-dialog-bottom .p-dialog-leave-to {\n    transform: translate3d(0px, 100%, 0px);\n}\n.p-dialog-left .p-dialog-enter-from,\n.p-dialog-left .p-dialog-leave-to,\n.p-dialog-topleft .p-dialog-enter-from,\n.p-dialog-topleft .p-dialog-leave-to,\n.p-dialog-bottomleft .p-dialog-enter-from,\n.p-dialog-bottomleft .p-dialog-leave-to {\n    transform: translate3d(-100%, 0px, 0px);\n}\n.p-dialog-right .p-dialog-enter-from,\n.p-dialog-right .p-dialog-leave-to,\n.p-dialog-topright .p-dialog-enter-from,\n.p-dialog-topright .p-dialog-leave-to,\n.p-dialog-bottomright .p-dialog-enter-from,\n.p-dialog-bottomright .p-dialog-leave-to {\n    transform: translate3d(100%, 0px, 0px);\n}\n\n/* Maximize */\n.p-dialog-maximized {\n    -webkit-transition: none;\n    transition: none;\n    transform: none;\n    width: 100vw !important;\n    height: 100vh !important;\n    top: 0px !important;\n    left: 0px !important;\n    max-height: 100%;\n    height: 100%;\n}\n.p-dialog-maximized .p-dialog-content {\n    flex-grow: 1;\n}\n\n/* Position */\n.p-dialog-left {\n    justify-content: flex-start;\n}\n.p-dialog-right {\n    justify-content: flex-end;\n}\n.p-dialog-top {\n    align-items: flex-start;\n}\n.p-dialog-topleft {\n    justify-content: flex-start;\n    align-items: flex-start;\n}\n.p-dialog-topright {\n    justify-content: flex-end;\n    align-items: flex-start;\n}\n.p-dialog-bottom {\n    align-items: flex-end;\n}\n.p-dialog-bottomleft {\n    justify-content: flex-start;\n    align-items: flex-end;\n}\n.p-dialog-bottomright {\n    justify-content: flex-end;\n    align-items: flex-end;\n}\n.p-confirm-dialog .p-dialog-content {\n    display: flex;\n    align-items: center;\n}\n";
  styleInject(css_248z);
  script.render = render;
  const DemoWidget_vue_vue_type_style_index_0_scoped_f34a3253_lang = "";
  const _export_sfc = (sfc, props) => {
    const target = sfc.__vccOpts || sfc;
    for (const [key, val] of props) {
      target[key] = val;
    }
    return target;
  };
  const _withScopeId = (n) => (vue.pushScopeId("data-v-f34a3253"), n = n(), vue.popScopeId(), n);
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
      var displayModal = vue.ref(false);
      function openModal(ev) {
        displayModal.value = true;
      }
      return (_ctx, _cache) => {
        return vue.openBlock(), vue.createElementBlock("div", _hoisted_1, [
          vue.createElementVNode("h1", _hoisted_2, vue.toDisplayString(__props.msg), 1),
          _hoisted_3,
          vue.createVNode(vue.unref(script$2), {
            label: __props.msg,
            icon: "pi pi-check",
            iconPos: "right",
            onClick: openModal
          }, null, 8, ["label"]),
          vue.createVNode(vue.unref(script), {
            header: "Confirmation",
            visible: vue.unref(displayModal),
            "onUpdate:visible": _cache[0] || (_cache[0] = ($event) => vue.isRef(displayModal) ? displayModal.value = $event : displayModal = $event),
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
  const demo_widget = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-f34a3253"]]);
  win.demo_widget = demo_widget;
})(window, Vue);
