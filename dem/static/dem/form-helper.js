/*

  Rules inputs are fields values. Each should have a 'id' attribute
  A rule is triggered each time one is changed by the user.

    Rule function returns a list of actions, each is a object with
  at least one attribute : 'action'

  Possible actions :
   - 'value' : Change (other) elements values
     * 'selector' : the field id/class
     * 'value' : the value to put in
   - 'classes' : change elements classes
     * 'selector' : the objects which classes will be changed
     * 'has' : classes to add
     * 'has_not' : classes to remove
   - 'help' : Add/remove a (colored) help item in a (dedicaced) window
     * 'text'
     * 'level'
     * 'selector' : the objects where help item will be added
   - 'links-lock' : Lock all links in the page a throw a alert box with a message
     * 'text' : alert message text

   Loop avoidance : None for now.
*/

class FormHelper {
    constructor(form, rules, options) {
        this.rules = rules;
        this.form = form;
        this.options = Object.assign(options, {
            'debug':false,
            'help_container_id':'help',
        });
        var self = this;

        if (typeof(form) == 'string') {
            form = document.querySelector(form);
        }

        var rules_keys = Object.keys(rules);
        for (var i = 0 ; i < rules_keys.length ; i++) {
            var rule = rules[rules_keys[i]];
            rule.id = rules_keys[i];

            var elements = this.get_elements(form, rule.input_selectors);
            if (options.debug)
                console.debug('inputs:', elements);

            // Apply the rule once (at launch)
            if (elements.length > 0) {
                this.helper_cb(form, rule, elements, options, true, null);
            }

            for (var k = 0 ; k < elements.length; k++) {
                if (options.debug)
                    console.debug(elements[k]);

                function handler(form, rule, elements, options) {
                    return function(event) {
                        self.helper_cb(form, rule, elements, options, false, event);
                    }
                }
                elements[k].addEventListener('change', handler(form, rule, elements, options));
            }
        }
    }

    /*
     * Méthode qui est appelée à chaque modification. Elle collecte les
     *   valeurs des champs, appelle la fonction de la règle et
     *   répercute le résultat de la règle sur la page (via le DOM)
     */
    helper_cb(form, rule, elements, options, init_call, event) {
        if (options.debug)
            console.debug(rule.func, elements, event);
        var my_vars = {};
        for (var i = 0 ; i < elements.length ; i++) {
            var element = elements[i];
            if (element.type == 'checkbox') {
                my_vars[element.id] = element.checked;
            } else {
                // Get input value
                my_vars[element.id] = element.value;
            }
        }

        var responses = rule.func(my_vars, rule, init_call);
        if (options.debug) {
            console.debug("Results from rule " + rule.id);
            console.debug(responses);
        }

        var altered_nodes = [];

        // Remove previous messages from this rule
        var items = document.querySelectorAll(".help-msg");
        for (var i = 0 ; i < items.length ; i++) {
            if (items[i].getAttribute("data-rule") == rule.id) {
                altered_nodes.push(items[i].parentNode);
                items[i].parentNode.removeChild(items[i]);
            }
        }

        // Apply rules response to the DOM
        for (var i = 0 ; i < responses.length ; i++) {
            var response = responses[i];

            // Change value
            if (response.action == 'value') {
                var node_list = form.querySelectorAll(response.selector);
                for (var j = 0 ; j < node_list.length ; j++) {
                    var node = node_list[j];
                    node.value = response.value;
                }
            }
            // Locks every links on the page
            else if (response.action == 'links-lock') {
                $("a").off("click");
                $('a').on('click', response, function(e) {
                    if (e.target.onclick === null) {
                        // Ne s'applique que pour les liens "normaux" (sans onclick défini)
                        e.preventDefault();
                        alert(e.data.text);
                    }
                });
            }
            // Change classes
            else if (response.action == 'classes') {
                var node_list = form.querySelectorAll(response.selector);
                for (var j = 0 ; j < node_list.length ; j++) {
                    var classes = node_list[j].classList;

                    if (typeof(response.has_not) == 'string')
                        var has_not = [response.has_not];
                    else
                        var has_not = response.has_not;

                    if (has_not)
                        for (var k = 0 ; k < has_not.length ; k++)
                            classes.remove(has_not[k]);

                    if (typeof(response.has) == 'string')
                        var has = [response.has];
                    else
                        var has = response.has;
                    if (has)
                        for (var k = 0 ; k < has.length ; k++)
                            classes.add(has[k]);
                }
            }
            // Add/replace help messages
            else if (response.action == 'help') {
                var parents = document.querySelectorAll(response.selector);
                if (options.debug)
                    console.debug("parents:",parents);
                if (parents.length < 1)
                    console.warn("Rule "+rule.id+" returns a help message (selector = '"+response.selector+"' which do not match !");
                for (var j = 0 ; j < parents.length ; j++) {
                    var parent = parents[j];
                    //console.debug("parent", parent);
                    var item = document.createElement("div");
                    item.setAttribute("data-rule", rule.id);
                    item.classList.add("help-msg");
                    item.classList.add("help-"+response.level);
                    item.textContent = response.text;
                    //TODO: insert at the right place to keep messages sorted by level
                    parent.appendChild(item);
                    altered_nodes.push(parent);
                }
            }
            // Trigger a rule (last action !!)
            else if (response.action == 'rule-trigger') {
                var rule = rules[response.rule_id];
                //console.debug("trigering rule", rule);
                var elements = this.get_elements(form, rule.input_selectors);
                this.helper_cb(form, rule, elements, options, false, null);
            } else {
                console.warn("Rule " + response.rule_id + " returns unknown action: " + response.action);
            }
        }

        // Compute highest level
        for (i=0;i<altered_nodes.length;i++) {
            var highest_level = 0;
            var parent = altered_nodes[i];
            // console.log("altered node (bubble)", parent);

            for (k=0;k<parent.children.length;k++) {
                var child = parent.children[k];
                if (child.classList.contains('help-error')) {
                    highest_level = 3;
                } else if (child.classList.contains('help-warning') && (highest_level <= 2)) {
                    highest_level = 2;
                } else if (child.classList.contains('help-info') && (highest_level <= 1)) {
                    highest_level = 1;
                }
            }
            // console.log("level", highest_level);

            var grandparent = parent.parentElement;
            // console.debug("gparent", grandparent.classList);
            if (highest_level >= 3)
                grandparent.classList.add("error");
            else if (highest_level >= 2) {
                grandparent.classList.remove("error");
                grandparent.classList.add("warning");
            } else if (highest_level >= 1) {
                grandparent.classList.remove("error");
                grandparent.classList.remove("warning");
                grandparent.classList.add("info");
            } else {
                grandparent.classList.remove("error");
                grandparent.classList.remove("warning");
                grandparent.classList.remove("info");
            }
        }
    }

// Method that get elements from a selector _or_ a list of selectors
    get_elements(form, selectors) {
        var isels;
        if (typeof(selectors) == 'string') {
            isels = [selectors];
        } else {
            isels = selectors;
        }
        var elements = [];
        for (var j = 0 ; j < isels.length ; j++) {
            var node_list = form.querySelectorAll(isels[j]);
            for (var k = 0 ; k < node_list.length ; k++) {
                elements.push(node_list[k]);
            }
        }
        return elements;
    }
}
