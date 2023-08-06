var app = (function () {
    'use strict';

    function noop() { }
    function add_location(element, file, line, column, char) {
        element.__svelte_meta = {
            loc: { file, line, column, char }
        };
    }
    function run(fn) {
        return fn();
    }
    function blank_object() {
        return Object.create(null);
    }
    function run_all(fns) {
        fns.forEach(run);
    }
    function is_function(thing) {
        return typeof thing === 'function';
    }
    function safe_not_equal(a, b) {
        return a != a ? b == b : a !== b || ((a && typeof a === 'object') || typeof a === 'function');
    }
    let src_url_equal_anchor;
    function src_url_equal(element_src, url) {
        if (!src_url_equal_anchor) {
            src_url_equal_anchor = document.createElement('a');
        }
        src_url_equal_anchor.href = url;
        return element_src === src_url_equal_anchor.href;
    }
    function is_empty(obj) {
        return Object.keys(obj).length === 0;
    }
    function append(target, node) {
        target.appendChild(node);
    }
    function insert(target, node, anchor) {
        target.insertBefore(node, anchor || null);
    }
    function detach(node) {
        if (node.parentNode) {
            node.parentNode.removeChild(node);
        }
    }
    function destroy_each(iterations, detaching) {
        for (let i = 0; i < iterations.length; i += 1) {
            if (iterations[i])
                iterations[i].d(detaching);
        }
    }
    function element(name) {
        return document.createElement(name);
    }
    function text(data) {
        return document.createTextNode(data);
    }
    function listen(node, event, handler, options) {
        node.addEventListener(event, handler, options);
        return () => node.removeEventListener(event, handler, options);
    }
    function prevent_default(fn) {
        return function (event) {
            event.preventDefault();
            // @ts-ignore
            return fn.call(this, event);
        };
    }
    function attr(node, attribute, value) {
        if (value == null)
            node.removeAttribute(attribute);
        else if (node.getAttribute(attribute) !== value)
            node.setAttribute(attribute, value);
    }
    function children(element) {
        return Array.from(element.childNodes);
    }
    function set_input_value(input, value) {
        input.value = value == null ? '' : value;
    }
    function custom_event(type, detail, { bubbles = false, cancelable = false } = {}) {
        const e = document.createEvent('CustomEvent');
        e.initCustomEvent(type, bubbles, cancelable, detail);
        return e;
    }

    let current_component;
    function set_current_component(component) {
        current_component = component;
    }
    function get_current_component() {
        if (!current_component)
            throw new Error('Function called outside component initialization');
        return current_component;
    }
    /**
     * The `onMount` function schedules a callback to run as soon as the component has been mounted to the DOM.
     * It must be called during the component's initialisation (but doesn't need to live *inside* the component;
     * it can be called from an external module).
     *
     * `onMount` does not run inside a [server-side component](/docs#run-time-server-side-component-api).
     *
     * https://svelte.dev/docs#run-time-svelte-onmount
     */
    function onMount(fn) {
        get_current_component().$$.on_mount.push(fn);
    }

    const dirty_components = [];
    const binding_callbacks = [];
    const render_callbacks = [];
    const flush_callbacks = [];
    const resolved_promise = Promise.resolve();
    let update_scheduled = false;
    function schedule_update() {
        if (!update_scheduled) {
            update_scheduled = true;
            resolved_promise.then(flush);
        }
    }
    function add_render_callback(fn) {
        render_callbacks.push(fn);
    }
    // flush() calls callbacks in this order:
    // 1. All beforeUpdate callbacks, in order: parents before children
    // 2. All bind:this callbacks, in reverse order: children before parents.
    // 3. All afterUpdate callbacks, in order: parents before children. EXCEPT
    //    for afterUpdates called during the initial onMount, which are called in
    //    reverse order: children before parents.
    // Since callbacks might update component values, which could trigger another
    // call to flush(), the following steps guard against this:
    // 1. During beforeUpdate, any updated components will be added to the
    //    dirty_components array and will cause a reentrant call to flush(). Because
    //    the flush index is kept outside the function, the reentrant call will pick
    //    up where the earlier call left off and go through all dirty components. The
    //    current_component value is saved and restored so that the reentrant call will
    //    not interfere with the "parent" flush() call.
    // 2. bind:this callbacks cannot trigger new flush() calls.
    // 3. During afterUpdate, any updated components will NOT have their afterUpdate
    //    callback called a second time; the seen_callbacks set, outside the flush()
    //    function, guarantees this behavior.
    const seen_callbacks = new Set();
    let flushidx = 0; // Do *not* move this inside the flush() function
    function flush() {
        // Do not reenter flush while dirty components are updated, as this can
        // result in an infinite loop. Instead, let the inner flush handle it.
        // Reentrancy is ok afterwards for bindings etc.
        if (flushidx !== 0) {
            return;
        }
        const saved_component = current_component;
        do {
            // first, call beforeUpdate functions
            // and update components
            try {
                while (flushidx < dirty_components.length) {
                    const component = dirty_components[flushidx];
                    flushidx++;
                    set_current_component(component);
                    update(component.$$);
                }
            }
            catch (e) {
                // reset dirty state to not end up in a deadlocked state and then rethrow
                dirty_components.length = 0;
                flushidx = 0;
                throw e;
            }
            set_current_component(null);
            dirty_components.length = 0;
            flushidx = 0;
            while (binding_callbacks.length)
                binding_callbacks.pop()();
            // then, once components are updated, call
            // afterUpdate functions. This may cause
            // subsequent updates...
            for (let i = 0; i < render_callbacks.length; i += 1) {
                const callback = render_callbacks[i];
                if (!seen_callbacks.has(callback)) {
                    // ...so guard against infinite loops
                    seen_callbacks.add(callback);
                    callback();
                }
            }
            render_callbacks.length = 0;
        } while (dirty_components.length);
        while (flush_callbacks.length) {
            flush_callbacks.pop()();
        }
        update_scheduled = false;
        seen_callbacks.clear();
        set_current_component(saved_component);
    }
    function update($$) {
        if ($$.fragment !== null) {
            $$.update();
            run_all($$.before_update);
            const dirty = $$.dirty;
            $$.dirty = [-1];
            $$.fragment && $$.fragment.p($$.ctx, dirty);
            $$.after_update.forEach(add_render_callback);
        }
    }
    const outroing = new Set();
    let outros;
    function group_outros() {
        outros = {
            r: 0,
            c: [],
            p: outros // parent group
        };
    }
    function check_outros() {
        if (!outros.r) {
            run_all(outros.c);
        }
        outros = outros.p;
    }
    function transition_in(block, local) {
        if (block && block.i) {
            outroing.delete(block);
            block.i(local);
        }
    }
    function transition_out(block, local, detach, callback) {
        if (block && block.o) {
            if (outroing.has(block))
                return;
            outroing.add(block);
            outros.c.push(() => {
                outroing.delete(block);
                if (callback) {
                    if (detach)
                        block.d(1);
                    callback();
                }
            });
            block.o(local);
        }
        else if (callback) {
            callback();
        }
    }

    const globals = (typeof window !== 'undefined'
        ? window
        : typeof globalThis !== 'undefined'
            ? globalThis
            : global);
    function create_component(block) {
        block && block.c();
    }
    function mount_component(component, target, anchor, customElement) {
        const { fragment, after_update } = component.$$;
        fragment && fragment.m(target, anchor);
        if (!customElement) {
            // onMount happens before the initial afterUpdate
            add_render_callback(() => {
                const new_on_destroy = component.$$.on_mount.map(run).filter(is_function);
                // if the component was destroyed immediately
                // it will update the `$$.on_destroy` reference to `null`.
                // the destructured on_destroy may still reference to the old array
                if (component.$$.on_destroy) {
                    component.$$.on_destroy.push(...new_on_destroy);
                }
                else {
                    // Edge case - component was destroyed immediately,
                    // most likely as a result of a binding initialising
                    run_all(new_on_destroy);
                }
                component.$$.on_mount = [];
            });
        }
        after_update.forEach(add_render_callback);
    }
    function destroy_component(component, detaching) {
        const $$ = component.$$;
        if ($$.fragment !== null) {
            run_all($$.on_destroy);
            $$.fragment && $$.fragment.d(detaching);
            // TODO null out other refs, including component.$$ (but need to
            // preserve final state?)
            $$.on_destroy = $$.fragment = null;
            $$.ctx = [];
        }
    }
    function make_dirty(component, i) {
        if (component.$$.dirty[0] === -1) {
            dirty_components.push(component);
            schedule_update();
            component.$$.dirty.fill(0);
        }
        component.$$.dirty[(i / 31) | 0] |= (1 << (i % 31));
    }
    function init(component, options, instance, create_fragment, not_equal, props, append_styles, dirty = [-1]) {
        const parent_component = current_component;
        set_current_component(component);
        const $$ = component.$$ = {
            fragment: null,
            ctx: [],
            // state
            props,
            update: noop,
            not_equal,
            bound: blank_object(),
            // lifecycle
            on_mount: [],
            on_destroy: [],
            on_disconnect: [],
            before_update: [],
            after_update: [],
            context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
            // everything else
            callbacks: blank_object(),
            dirty,
            skip_bound: false,
            root: options.target || parent_component.$$.root
        };
        append_styles && append_styles($$.root);
        let ready = false;
        $$.ctx = instance
            ? instance(component, options.props || {}, (i, ret, ...rest) => {
                const value = rest.length ? rest[0] : ret;
                if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
                    if (!$$.skip_bound && $$.bound[i])
                        $$.bound[i](value);
                    if (ready)
                        make_dirty(component, i);
                }
                return ret;
            })
            : [];
        $$.update();
        ready = true;
        run_all($$.before_update);
        // `false` as a special case of no DOM component
        $$.fragment = create_fragment ? create_fragment($$.ctx) : false;
        if (options.target) {
            if (options.hydrate) {
                const nodes = children(options.target);
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                $$.fragment && $$.fragment.l(nodes);
                nodes.forEach(detach);
            }
            else {
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                $$.fragment && $$.fragment.c();
            }
            if (options.intro)
                transition_in(component.$$.fragment);
            mount_component(component, options.target, options.anchor, options.customElement);
            flush();
        }
        set_current_component(parent_component);
    }
    /**
     * Base class for Svelte components. Used when dev=false.
     */
    class SvelteComponent {
        $destroy() {
            destroy_component(this, 1);
            this.$destroy = noop;
        }
        $on(type, callback) {
            if (!is_function(callback)) {
                return noop;
            }
            const callbacks = (this.$$.callbacks[type] || (this.$$.callbacks[type] = []));
            callbacks.push(callback);
            return () => {
                const index = callbacks.indexOf(callback);
                if (index !== -1)
                    callbacks.splice(index, 1);
            };
        }
        $set($$props) {
            if (this.$$set && !is_empty($$props)) {
                this.$$.skip_bound = true;
                this.$$set($$props);
                this.$$.skip_bound = false;
            }
        }
    }

    function dispatch_dev(type, detail) {
        document.dispatchEvent(custom_event(type, Object.assign({ version: '3.55.1' }, detail), { bubbles: true }));
    }
    function append_dev(target, node) {
        dispatch_dev('SvelteDOMInsert', { target, node });
        append(target, node);
    }
    function insert_dev(target, node, anchor) {
        dispatch_dev('SvelteDOMInsert', { target, node, anchor });
        insert(target, node, anchor);
    }
    function detach_dev(node) {
        dispatch_dev('SvelteDOMRemove', { node });
        detach(node);
    }
    function listen_dev(node, event, handler, options, has_prevent_default, has_stop_propagation) {
        const modifiers = options === true ? ['capture'] : options ? Array.from(Object.keys(options)) : [];
        if (has_prevent_default)
            modifiers.push('preventDefault');
        if (has_stop_propagation)
            modifiers.push('stopPropagation');
        dispatch_dev('SvelteDOMAddEventListener', { node, event, handler, modifiers });
        const dispose = listen(node, event, handler, options);
        return () => {
            dispatch_dev('SvelteDOMRemoveEventListener', { node, event, handler, modifiers });
            dispose();
        };
    }
    function attr_dev(node, attribute, value) {
        attr(node, attribute, value);
        if (value == null)
            dispatch_dev('SvelteDOMRemoveAttribute', { node, attribute });
        else
            dispatch_dev('SvelteDOMSetAttribute', { node, attribute, value });
    }
    function set_data_dev(text, data) {
        data = '' + data;
        if (text.wholeText === data)
            return;
        dispatch_dev('SvelteDOMSetData', { node: text, data });
        text.data = data;
    }
    function validate_each_argument(arg) {
        if (typeof arg !== 'string' && !(arg && typeof arg === 'object' && 'length' in arg)) {
            let msg = '{#each} only iterates over array-like objects.';
            if (typeof Symbol === 'function' && arg && Symbol.iterator in arg) {
                msg += ' You can use a spread to convert this iterable into an array.';
            }
            throw new Error(msg);
        }
    }
    function validate_slots(name, slot, keys) {
        for (const slot_key of Object.keys(slot)) {
            if (!~keys.indexOf(slot_key)) {
                console.warn(`<${name}> received an unexpected slot "${slot_key}".`);
            }
        }
    }
    /**
     * Base class for Svelte components with some minor dev-enhancements. Used when dev=true.
     */
    class SvelteComponentDev extends SvelteComponent {
        constructor(options) {
            if (!options || (!options.target && !options.$$inline)) {
                throw new Error("'target' is a required option");
            }
            super();
        }
        $destroy() {
            super.$destroy();
            this.$destroy = () => {
                console.warn('Component was already destroyed'); // eslint-disable-line no-console
            };
        }
        $capture_state() { }
        $inject_state() { }
    }

    /*
    NoComment --- Comment any resource on the web!
    Copyright © 2023 Bioneland

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    */

    function isSuccess(response) {
      return verifiesCondition(response, (r) => r.status >= 200 && r.status <= 299)
    }

    function verifiesCondition(response, checkResponse) {
      if (checkResponse(response)) {
        return response
      } else {
        throw Error(response.statusText)
      }
    }

    /* src/js/components/Message.svelte generated by Svelte v3.55.1 */

    const file$3 = "src/js/components/Message.svelte";

    function create_fragment$4(ctx) {
    	let p;
    	let t;
    	let p_class_value;

    	const block = {
    		c: function create() {
    			p = element("p");
    			t = text(/*text*/ ctx[0]);
    			attr_dev(p, "class", p_class_value = "notification is-light className " + /*className*/ ctx[1] + " svelte-1xnji6g");
    			add_location(p, file$3, 31, 0, 951);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, p, anchor);
    			append_dev(p, t);
    		},
    		p: function update(ctx, [dirty]) {
    			if (dirty & /*text*/ 1) set_data_dev(t, /*text*/ ctx[0]);

    			if (dirty & /*className*/ 2 && p_class_value !== (p_class_value = "notification is-light className " + /*className*/ ctx[1] + " svelte-1xnji6g")) {
    				attr_dev(p, "class", p_class_value);
    			}
    		},
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(p);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$4.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$4($$self, $$props, $$invalidate) {
    	let className;
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('Message', slots, []);
    	let { text } = $$props;
    	let { category } = $$props;

    	const alertClasses = {
    		success: "is-success",
    		error: "is-danger",
    		info: "is-info",
    		warning: "is-warning"
    	};

    	$$self.$$.on_mount.push(function () {
    		if (text === undefined && !('text' in $$props || $$self.$$.bound[$$self.$$.props['text']])) {
    			console.warn("<Message> was created without expected prop 'text'");
    		}

    		if (category === undefined && !('category' in $$props || $$self.$$.bound[$$self.$$.props['category']])) {
    			console.warn("<Message> was created without expected prop 'category'");
    		}
    	});

    	const writable_props = ['text', 'category'];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Message> was created with unknown prop '${key}'`);
    	});

    	$$self.$$set = $$props => {
    		if ('text' in $$props) $$invalidate(0, text = $$props.text);
    		if ('category' in $$props) $$invalidate(2, category = $$props.category);
    	};

    	$$self.$capture_state = () => ({ text, category, alertClasses, className });

    	$$self.$inject_state = $$props => {
    		if ('text' in $$props) $$invalidate(0, text = $$props.text);
    		if ('category' in $$props) $$invalidate(2, category = $$props.category);
    		if ('className' in $$props) $$invalidate(1, className = $$props.className);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	$$self.$$.update = () => {
    		if ($$self.$$.dirty & /*category*/ 4) {
    			$$invalidate(1, className = alertClasses[category] || "");
    		}
    	};

    	return [text, className, category];
    }

    class Message extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$4, create_fragment$4, safe_not_equal, { text: 0, category: 2 });

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "Message",
    			options,
    			id: create_fragment$4.name
    		});
    	}

    	get text() {
    		throw new Error("<Message>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set text(value) {
    		throw new Error("<Message>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get category() {
    		throw new Error("<Message>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set category(value) {
    		throw new Error("<Message>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}
    }

    /* src/js/components/AddCommentForm.svelte generated by Svelte v3.55.1 */

    const { console: console_1$2 } = globals;
    const file$2 = "src/js/components/AddCommentForm.svelte";

    // (51:284) {:else}
    function create_else_block(ctx) {
    	let input;
    	let mounted;
    	let dispose;

    	const block = {
    		c: function create() {
    			input = element("input");
    			attr_dev(input, "type", "hidden");
    			attr_dev(input, "name", "url");
    			add_location(input, file$2, 50, 291, 1732);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, input, anchor);
    			set_input_value(input, /*url*/ ctx[1]);

    			if (!mounted) {
    				dispose = listen_dev(input, "input", /*input_input_handler_1*/ ctx[8]);
    				mounted = true;
    			}
    		},
    		p: function update(ctx, dirty) {
    			if (dirty & /*url*/ 2) {
    				set_input_value(input, /*url*/ ctx[1]);
    			}
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(input);
    			mounted = false;
    			dispose();
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_else_block.name,
    		type: "else",
    		source: "(51:284) {:else}",
    		ctx
    	});

    	return block;
    }

    // (51:46) {#if targetUrl === ''}
    function create_if_block_1(ctx) {
    	let div1;
    	let label;
    	let div0;
    	let input;
    	let mounted;
    	let dispose;

    	const block = {
    		c: function create() {
    			div1 = element("div");
    			label = element("label");
    			label.textContent = "URL";
    			div0 = element("div");
    			input = element("input");
    			attr_dev(label, "class", "label");
    			attr_dev(label, "for", "url");
    			add_location(label, file$2, 50, 87, 1528);
    			attr_dev(input, "class", "input");
    			attr_dev(input, "id", "url");
    			attr_dev(input, "type", "url");
    			attr_dev(input, "name", "url");
    			attr_dev(input, "placeholder", "The URL of the resource to comment");
    			add_location(input, file$2, 50, 150, 1591);
    			attr_dev(div0, "class", "control");
    			add_location(div0, file$2, 50, 129, 1570);
    			attr_dev(div1, "class", "field");
    			add_location(div1, file$2, 50, 68, 1509);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div1, anchor);
    			append_dev(div1, label);
    			append_dev(div1, div0);
    			append_dev(div0, input);
    			set_input_value(input, /*url*/ ctx[1]);

    			if (!mounted) {
    				dispose = listen_dev(input, "input", /*input_input_handler*/ ctx[7]);
    				mounted = true;
    			}
    		},
    		p: function update(ctx, dirty) {
    			if (dirty & /*url*/ 2) {
    				set_input_value(input, /*url*/ ctx[1]);
    			}
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div1);
    			mounted = false;
    			dispose();
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_if_block_1.name,
    		type: "if",
    		source: "(51:46) {#if targetUrl === ''}",
    		ctx
    	});

    	return block;
    }

    // (51:643) {#if message}
    function create_if_block$1(ctx) {
    	let div;
    	let message_1;
    	let current;

    	message_1 = new Message({
    			props: {
    				text: /*message*/ ctx[3],
    				category: /*category*/ ctx[4]
    			},
    			$$inline: true
    		});

    	const block = {
    		c: function create() {
    			div = element("div");
    			create_component(message_1.$$.fragment);
    			attr_dev(div, "class", "control is-expended");
    			add_location(div, file$2, 50, 656, 2097);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div, anchor);
    			mount_component(message_1, div, null);
    			current = true;
    		},
    		p: function update(ctx, dirty) {
    			const message_1_changes = {};
    			if (dirty & /*message*/ 8) message_1_changes.text = /*message*/ ctx[3];
    			if (dirty & /*category*/ 16) message_1_changes.category = /*category*/ ctx[4];
    			message_1.$set(message_1_changes);
    		},
    		i: function intro(local) {
    			if (current) return;
    			transition_in(message_1.$$.fragment, local);
    			current = true;
    		},
    		o: function outro(local) {
    			transition_out(message_1.$$.fragment, local);
    			current = false;
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div);
    			destroy_component(message_1);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_if_block$1.name,
    		type: "if",
    		source: "(51:643) {#if message}",
    		ctx
    	});

    	return block;
    }

    function create_fragment$3(ctx) {
    	let form;
    	let div1;
    	let label;
    	let div0;
    	let textarea;
    	let div3;
    	let div2;
    	let button;
    	let current;
    	let mounted;
    	let dispose;

    	function select_block_type(ctx, dirty) {
    		if (/*targetUrl*/ ctx[0] === '') return create_if_block_1;
    		return create_else_block;
    	}

    	let current_block_type = select_block_type(ctx);
    	let if_block0 = current_block_type(ctx);
    	let if_block1 = /*message*/ ctx[3] && create_if_block$1(ctx);

    	const block = {
    		c: function create() {
    			form = element("form");
    			if_block0.c();
    			div1 = element("div");
    			label = element("label");
    			label.textContent = "Text";
    			div0 = element("div");
    			textarea = element("textarea");
    			div3 = element("div");
    			div2 = element("div");
    			button = element("button");
    			button.textContent = "Comment";
    			if (if_block1) if_block1.c();
    			attr_dev(label, "class", "label");
    			attr_dev(label, "for", "text");
    			add_location(label, file$2, 50, 368, 1809);
    			attr_dev(textarea, "class", "textarea");
    			attr_dev(textarea, "id", "text");
    			attr_dev(textarea, "type", "text");
    			attr_dev(textarea, "name", "text");
    			add_location(textarea, file$2, 50, 433, 1874);
    			attr_dev(div0, "class", "control");
    			add_location(div0, file$2, 50, 412, 1853);
    			attr_dev(div1, "class", "field");
    			add_location(div1, file$2, 50, 349, 1790);
    			attr_dev(button, "class", "button is-link");
    			add_location(button, file$2, 50, 590, 2031);
    			attr_dev(div2, "class", "control");
    			add_location(div2, file$2, 50, 569, 2010);
    			attr_dev(div3, "class", "field is-grouped");
    			add_location(div3, file$2, 50, 539, 1980);
    			add_location(form, file$2, 50, 0, 1441);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, form, anchor);
    			if_block0.m(form, null);
    			append_dev(form, div1);
    			append_dev(div1, label);
    			append_dev(div1, div0);
    			append_dev(div0, textarea);
    			set_input_value(textarea, /*text*/ ctx[2]);
    			append_dev(form, div3);
    			append_dev(div3, div2);
    			append_dev(div2, button);
    			if (if_block1) if_block1.m(div3, null);
    			current = true;

    			if (!mounted) {
    				dispose = [
    					listen_dev(textarea, "input", /*textarea_input_handler*/ ctx[9]),
    					listen_dev(form, "submit", prevent_default(/*onSubmit*/ ctx[5]), false, true, false)
    				];

    				mounted = true;
    			}
    		},
    		p: function update(ctx, [dirty]) {
    			if (current_block_type === (current_block_type = select_block_type(ctx)) && if_block0) {
    				if_block0.p(ctx, dirty);
    			} else {
    				if_block0.d(1);
    				if_block0 = current_block_type(ctx);

    				if (if_block0) {
    					if_block0.c();
    					if_block0.m(form, div1);
    				}
    			}

    			if (dirty & /*text*/ 4) {
    				set_input_value(textarea, /*text*/ ctx[2]);
    			}

    			if (/*message*/ ctx[3]) {
    				if (if_block1) {
    					if_block1.p(ctx, dirty);

    					if (dirty & /*message*/ 8) {
    						transition_in(if_block1, 1);
    					}
    				} else {
    					if_block1 = create_if_block$1(ctx);
    					if_block1.c();
    					transition_in(if_block1, 1);
    					if_block1.m(div3, null);
    				}
    			} else if (if_block1) {
    				group_outros();

    				transition_out(if_block1, 1, 1, () => {
    					if_block1 = null;
    				});

    				check_outros();
    			}
    		},
    		i: function intro(local) {
    			if (current) return;
    			transition_in(if_block1);
    			current = true;
    		},
    		o: function outro(local) {
    			transition_out(if_block1);
    			current = false;
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(form);
    			if_block0.d();
    			if (if_block1) if_block1.d();
    			mounted = false;
    			run_all(dispose);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$3.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$3($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('AddCommentForm', slots, []);
    	let { addComment = (data, onSuccess, onError) => console.error("Not Implemented!") } = $$props;
    	let { targetUrl = "" } = $$props;
    	let url = "";
    	let text = "";
    	let message = "";
    	let category = "";

    	const onSuccess = () => {
    		$$invalidate(3, message = "Comment added!");
    		$$invalidate(4, category = "success");

    		if (targetUrl === "") {
    			// Do not reset `url` if an URL as been provided on mount
    			$$invalidate(1, url = "");
    		}

    		$$invalidate(2, text = "");
    	};

    	const onError = () => {
    		$$invalidate(3, message = "Something unexpected happened!?");
    		$$invalidate(4, category = "error");
    	};

    	const onSubmit = () => addComment({ url, text }, onSuccess, onError);

    	onMount(async () => {
    		$$invalidate(1, url = targetUrl);
    	});

    	const writable_props = ['addComment', 'targetUrl'];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1$2.warn(`<AddCommentForm> was created with unknown prop '${key}'`);
    	});

    	function input_input_handler() {
    		url = this.value;
    		$$invalidate(1, url);
    	}

    	function input_input_handler_1() {
    		url = this.value;
    		$$invalidate(1, url);
    	}

    	function textarea_input_handler() {
    		text = this.value;
    		$$invalidate(2, text);
    	}

    	$$self.$$set = $$props => {
    		if ('addComment' in $$props) $$invalidate(6, addComment = $$props.addComment);
    		if ('targetUrl' in $$props) $$invalidate(0, targetUrl = $$props.targetUrl);
    	};

    	$$self.$capture_state = () => ({
    		onMount,
    		Message,
    		addComment,
    		targetUrl,
    		url,
    		text,
    		message,
    		category,
    		onSuccess,
    		onError,
    		onSubmit
    	});

    	$$self.$inject_state = $$props => {
    		if ('addComment' in $$props) $$invalidate(6, addComment = $$props.addComment);
    		if ('targetUrl' in $$props) $$invalidate(0, targetUrl = $$props.targetUrl);
    		if ('url' in $$props) $$invalidate(1, url = $$props.url);
    		if ('text' in $$props) $$invalidate(2, text = $$props.text);
    		if ('message' in $$props) $$invalidate(3, message = $$props.message);
    		if ('category' in $$props) $$invalidate(4, category = $$props.category);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	return [
    		targetUrl,
    		url,
    		text,
    		message,
    		category,
    		onSubmit,
    		addComment,
    		input_input_handler,
    		input_input_handler_1,
    		textarea_input_handler
    	];
    }

    class AddCommentForm extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$3, create_fragment$3, safe_not_equal, { addComment: 6, targetUrl: 0 });

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "AddCommentForm",
    			options,
    			id: create_fragment$3.name
    		});
    	}

    	get addComment() {
    		throw new Error("<AddCommentForm>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set addComment(value) {
    		throw new Error("<AddCommentForm>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get targetUrl() {
    		throw new Error("<AddCommentForm>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set targetUrl(value) {
    		throw new Error("<AddCommentForm>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}
    }

    /* src/js/components/Comment.svelte generated by Svelte v3.55.1 */

    const file$1 = "src/js/components/Comment.svelte";

    function create_fragment$2(ctx) {
    	let div;
    	let pre;
    	let t0;
    	let p;
    	let a;
    	let t1;

    	const block = {
    		c: function create() {
    			div = element("div");
    			pre = element("pre");
    			t0 = text(/*text*/ ctx[0]);
    			p = element("p");
    			a = element("a");
    			t1 = text(/*url*/ ctx[1]);
    			attr_dev(pre, "class", "text");
    			add_location(pre, file$1, 23, 40, 832);
    			attr_dev(a, "class", "url");
    			attr_dev(a, "href", /*url*/ ctx[1]);
    			add_location(a, file$1, 23, 73, 865);
    			add_location(p, file$1, 23, 70, 862);
    			attr_dev(div, "class", "comment");
    			attr_dev(div, "date", /*created*/ ctx[2]);
    			add_location(div, file$1, 23, 0, 792);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div, anchor);
    			append_dev(div, pre);
    			append_dev(pre, t0);
    			append_dev(div, p);
    			append_dev(p, a);
    			append_dev(a, t1);
    		},
    		p: function update(ctx, [dirty]) {
    			if (dirty & /*text*/ 1) set_data_dev(t0, /*text*/ ctx[0]);
    			if (dirty & /*url*/ 2) set_data_dev(t1, /*url*/ ctx[1]);

    			if (dirty & /*url*/ 2) {
    				attr_dev(a, "href", /*url*/ ctx[1]);
    			}

    			if (dirty & /*created*/ 4) {
    				attr_dev(div, "date", /*created*/ ctx[2]);
    			}
    		},
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$2.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$2($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('Comment', slots, []);
    	let { text } = $$props;
    	let { url } = $$props;
    	let { created } = $$props;

    	$$self.$$.on_mount.push(function () {
    		if (text === undefined && !('text' in $$props || $$self.$$.bound[$$self.$$.props['text']])) {
    			console.warn("<Comment> was created without expected prop 'text'");
    		}

    		if (url === undefined && !('url' in $$props || $$self.$$.bound[$$self.$$.props['url']])) {
    			console.warn("<Comment> was created without expected prop 'url'");
    		}

    		if (created === undefined && !('created' in $$props || $$self.$$.bound[$$self.$$.props['created']])) {
    			console.warn("<Comment> was created without expected prop 'created'");
    		}
    	});

    	const writable_props = ['text', 'url', 'created'];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Comment> was created with unknown prop '${key}'`);
    	});

    	$$self.$$set = $$props => {
    		if ('text' in $$props) $$invalidate(0, text = $$props.text);
    		if ('url' in $$props) $$invalidate(1, url = $$props.url);
    		if ('created' in $$props) $$invalidate(2, created = $$props.created);
    	};

    	$$self.$capture_state = () => ({ text, url, created });

    	$$self.$inject_state = $$props => {
    		if ('text' in $$props) $$invalidate(0, text = $$props.text);
    		if ('url' in $$props) $$invalidate(1, url = $$props.url);
    		if ('created' in $$props) $$invalidate(2, created = $$props.created);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	return [text, url, created];
    }

    class Comment extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance$2, create_fragment$2, safe_not_equal, { text: 0, url: 1, created: 2 });

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "Comment",
    			options,
    			id: create_fragment$2.name
    		});
    	}

    	get text() {
    		throw new Error("<Comment>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set text(value) {
    		throw new Error("<Comment>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get url() {
    		throw new Error("<Comment>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set url(value) {
    		throw new Error("<Comment>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get created() {
    		throw new Error("<Comment>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set created(value) {
    		throw new Error("<Comment>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}
    }

    /* src/js/components/Page.svelte generated by Svelte v3.55.1 */

    const { console: console_1$1 } = globals;
    const file = "src/js/components/Page.svelte";

    function get_each_context(ctx, list, i) {
    	const child_ctx = ctx.slice();
    	child_ctx[6] = list[i];
    	return child_ctx;
    }

    // (30:528) {#if comments && comments.length > 0}
    function create_if_block(ctx) {
    	let div;
    	let current;
    	let each_value = /*comments*/ ctx[1];
    	validate_each_argument(each_value);
    	let each_blocks = [];

    	for (let i = 0; i < each_value.length; i += 1) {
    		each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
    	}

    	const out = i => transition_out(each_blocks[i], 1, 1, () => {
    		each_blocks[i] = null;
    	});

    	const block = {
    		c: function create() {
    			div = element("div");

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				each_blocks[i].c();
    			}

    			attr_dev(div, "class", "comments");
    			add_location(div, file, 29, 565, 1622);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div, anchor);

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				each_blocks[i].m(div, null);
    			}

    			current = true;
    		},
    		p: function update(ctx, dirty) {
    			if (dirty & /*comments*/ 2) {
    				each_value = /*comments*/ ctx[1];
    				validate_each_argument(each_value);
    				let i;

    				for (i = 0; i < each_value.length; i += 1) {
    					const child_ctx = get_each_context(ctx, each_value, i);

    					if (each_blocks[i]) {
    						each_blocks[i].p(child_ctx, dirty);
    						transition_in(each_blocks[i], 1);
    					} else {
    						each_blocks[i] = create_each_block(child_ctx);
    						each_blocks[i].c();
    						transition_in(each_blocks[i], 1);
    						each_blocks[i].m(div, null);
    					}
    				}

    				group_outros();

    				for (i = each_value.length; i < each_blocks.length; i += 1) {
    					out(i);
    				}

    				check_outros();
    			}
    		},
    		i: function intro(local) {
    			if (current) return;

    			for (let i = 0; i < each_value.length; i += 1) {
    				transition_in(each_blocks[i]);
    			}

    			current = true;
    		},
    		o: function outro(local) {
    			each_blocks = each_blocks.filter(Boolean);

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				transition_out(each_blocks[i]);
    			}

    			current = false;
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div);
    			destroy_each(each_blocks, detaching);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_if_block.name,
    		type: "if",
    		source: "(30:528) {#if comments && comments.length > 0}",
    		ctx
    	});

    	return block;
    }

    // (30:587) {#each comments as c}
    function create_each_block(ctx) {
    	let comment;
    	let current;

    	comment = new Comment({
    			props: {
    				text: /*c*/ ctx[6].text,
    				url: /*c*/ ctx[6].url,
    				created: /*c*/ ctx[6].created
    			},
    			$$inline: true
    		});

    	const block = {
    		c: function create() {
    			create_component(comment.$$.fragment);
    		},
    		m: function mount(target, anchor) {
    			mount_component(comment, target, anchor);
    			current = true;
    		},
    		p: function update(ctx, dirty) {
    			const comment_changes = {};
    			if (dirty & /*comments*/ 2) comment_changes.text = /*c*/ ctx[6].text;
    			if (dirty & /*comments*/ 2) comment_changes.url = /*c*/ ctx[6].url;
    			if (dirty & /*comments*/ 2) comment_changes.created = /*c*/ ctx[6].created;
    			comment.$set(comment_changes);
    		},
    		i: function intro(local) {
    			if (current) return;
    			transition_in(comment.$$.fragment, local);
    			current = true;
    		},
    		o: function outro(local) {
    			transition_out(comment.$$.fragment, local);
    			current = false;
    		},
    		d: function destroy(detaching) {
    			destroy_component(comment, detaching);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_each_block.name,
    		type: "each",
    		source: "(30:587) {#each comments as c}",
    		ctx
    	});

    	return block;
    }

    function create_fragment$1(ctx) {
    	let div3;
    	let section0;
    	let div0;
    	let figure;
    	let a;
    	let img;
    	let img_src_value;
    	let h1;
    	let t0;
    	let section1;
    	let div1;
    	let h20;
    	let addcommentform;
    	let section2;
    	let div2;
    	let h21;
    	let current;

    	addcommentform = new AddCommentForm({
    			props: {
    				addComment: /*addComment*/ ctx[5],
    				targetUrl: /*targetUrl*/ ctx[2]
    			},
    			$$inline: true
    		});

    	let if_block = /*comments*/ ctx[1] && /*comments*/ ctx[1].length > 0 && create_if_block(ctx);

    	const block = {
    		c: function create() {
    			div3 = element("div");
    			section0 = element("section");
    			div0 = element("div");
    			figure = element("figure");
    			a = element("a");
    			img = element("img");
    			h1 = element("h1");
    			t0 = text(/*name*/ ctx[0]);
    			section1 = element("section");
    			div1 = element("div");
    			h20 = element("h2");
    			h20.textContent = "Add a comment on…";
    			create_component(addcommentform.$$.fragment);
    			section2 = element("section");
    			div2 = element("div");
    			h21 = element("h2");
    			h21.textContent = "Past comments";
    			if (if_block) if_block.c();
    			attr_dev(img, "width", "32");
    			if (!src_url_equal(img.src, img_src_value = /*feedIconUrl*/ ctx[4])) attr_dev(img, "src", img_src_value);
    			attr_dev(img, "alt", "Feed");
    			add_location(img, file, 29, 133, 1190);
    			attr_dev(a, "href", /*feedUrl*/ ctx[3]);
    			add_location(a, file, 29, 113, 1170);
    			attr_dev(figure, "class", "image is-32x32 is-pulled-right");
    			add_location(figure, file, 29, 66, 1123);
    			attr_dev(h1, "class", "title is-1");
    			add_location(h1, file, 29, 193, 1250);
    			attr_dev(div0, "class", "container");
    			add_location(div0, file, 29, 43, 1100);
    			attr_dev(section0, "class", "section svelte-k9gotj");
    			add_location(section0, file, 29, 18, 1075);
    			attr_dev(h20, "class", "title is-3");
    			add_location(h20, file, 29, 291, 1348);
    			attr_dev(div1, "class", "container");
    			add_location(div1, file, 29, 268, 1325);
    			attr_dev(section1, "class", "section svelte-k9gotj");
    			add_location(section1, file, 29, 243, 1300);
    			attr_dev(h21, "class", "title is-3");
    			add_location(h21, file, 29, 487, 1544);
    			attr_dev(div2, "class", "container");
    			add_location(div2, file, 29, 464, 1521);
    			attr_dev(section2, "class", "section svelte-k9gotj");
    			add_location(section2, file, 29, 439, 1496);
    			attr_dev(div3, "class", "page");
    			add_location(div3, file, 29, 0, 1057);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div3, anchor);
    			append_dev(div3, section0);
    			append_dev(section0, div0);
    			append_dev(div0, figure);
    			append_dev(figure, a);
    			append_dev(a, img);
    			append_dev(div0, h1);
    			append_dev(h1, t0);
    			append_dev(div3, section1);
    			append_dev(section1, div1);
    			append_dev(div1, h20);
    			mount_component(addcommentform, div1, null);
    			append_dev(div3, section2);
    			append_dev(section2, div2);
    			append_dev(div2, h21);
    			if (if_block) if_block.m(div2, null);
    			current = true;
    		},
    		p: function update(ctx, [dirty]) {
    			if (!current || dirty & /*feedIconUrl*/ 16 && !src_url_equal(img.src, img_src_value = /*feedIconUrl*/ ctx[4])) {
    				attr_dev(img, "src", img_src_value);
    			}

    			if (!current || dirty & /*feedUrl*/ 8) {
    				attr_dev(a, "href", /*feedUrl*/ ctx[3]);
    			}

    			if (!current || dirty & /*name*/ 1) set_data_dev(t0, /*name*/ ctx[0]);
    			const addcommentform_changes = {};
    			if (dirty & /*addComment*/ 32) addcommentform_changes.addComment = /*addComment*/ ctx[5];
    			if (dirty & /*targetUrl*/ 4) addcommentform_changes.targetUrl = /*targetUrl*/ ctx[2];
    			addcommentform.$set(addcommentform_changes);

    			if (/*comments*/ ctx[1] && /*comments*/ ctx[1].length > 0) {
    				if (if_block) {
    					if_block.p(ctx, dirty);

    					if (dirty & /*comments*/ 2) {
    						transition_in(if_block, 1);
    					}
    				} else {
    					if_block = create_if_block(ctx);
    					if_block.c();
    					transition_in(if_block, 1);
    					if_block.m(div2, null);
    				}
    			} else if (if_block) {
    				group_outros();

    				transition_out(if_block, 1, 1, () => {
    					if_block = null;
    				});

    				check_outros();
    			}
    		},
    		i: function intro(local) {
    			if (current) return;
    			transition_in(addcommentform.$$.fragment, local);
    			transition_in(if_block);
    			current = true;
    		},
    		o: function outro(local) {
    			transition_out(addcommentform.$$.fragment, local);
    			transition_out(if_block);
    			current = false;
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div3);
    			destroy_component(addcommentform);
    			if (if_block) if_block.d();
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment$1.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance$1($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('Page', slots, []);
    	let { name = "" } = $$props;
    	let { comments = [] } = $$props;
    	let { targetUrl = "" } = $$props;
    	let { feedUrl = "" } = $$props;
    	let { feedIconUrl = "" } = $$props;
    	let { addComment = (data, onSuccess, onError) => console.error("Not Implemented!") } = $$props;
    	const writable_props = ['name', 'comments', 'targetUrl', 'feedUrl', 'feedIconUrl', 'addComment'];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1$1.warn(`<Page> was created with unknown prop '${key}'`);
    	});

    	$$self.$$set = $$props => {
    		if ('name' in $$props) $$invalidate(0, name = $$props.name);
    		if ('comments' in $$props) $$invalidate(1, comments = $$props.comments);
    		if ('targetUrl' in $$props) $$invalidate(2, targetUrl = $$props.targetUrl);
    		if ('feedUrl' in $$props) $$invalidate(3, feedUrl = $$props.feedUrl);
    		if ('feedIconUrl' in $$props) $$invalidate(4, feedIconUrl = $$props.feedIconUrl);
    		if ('addComment' in $$props) $$invalidate(5, addComment = $$props.addComment);
    	};

    	$$self.$capture_state = () => ({
    		AddCommentForm,
    		Comment,
    		name,
    		comments,
    		targetUrl,
    		feedUrl,
    		feedIconUrl,
    		addComment
    	});

    	$$self.$inject_state = $$props => {
    		if ('name' in $$props) $$invalidate(0, name = $$props.name);
    		if ('comments' in $$props) $$invalidate(1, comments = $$props.comments);
    		if ('targetUrl' in $$props) $$invalidate(2, targetUrl = $$props.targetUrl);
    		if ('feedUrl' in $$props) $$invalidate(3, feedUrl = $$props.feedUrl);
    		if ('feedIconUrl' in $$props) $$invalidate(4, feedIconUrl = $$props.feedIconUrl);
    		if ('addComment' in $$props) $$invalidate(5, addComment = $$props.addComment);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	return [name, comments, targetUrl, feedUrl, feedIconUrl, addComment];
    }

    class Page extends SvelteComponentDev {
    	constructor(options) {
    		super(options);

    		init(this, options, instance$1, create_fragment$1, safe_not_equal, {
    			name: 0,
    			comments: 1,
    			targetUrl: 2,
    			feedUrl: 3,
    			feedIconUrl: 4,
    			addComment: 5
    		});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "Page",
    			options,
    			id: create_fragment$1.name
    		});
    	}

    	get name() {
    		throw new Error("<Page>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set name(value) {
    		throw new Error("<Page>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get comments() {
    		throw new Error("<Page>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set comments(value) {
    		throw new Error("<Page>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get targetUrl() {
    		throw new Error("<Page>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set targetUrl(value) {
    		throw new Error("<Page>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get feedUrl() {
    		throw new Error("<Page>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set feedUrl(value) {
    		throw new Error("<Page>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get feedIconUrl() {
    		throw new Error("<Page>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set feedIconUrl(value) {
    		throw new Error("<Page>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get addComment() {
    		throw new Error("<Page>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set addComment(value) {
    		throw new Error("<Page>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}
    }

    /* src/js/containers/App.svelte generated by Svelte v3.55.1 */

    const { console: console_1 } = globals;

    function create_fragment(ctx) {
    	let page;
    	let current;

    	page = new Page({
    			props: {
    				name: /*name*/ ctx[4],
    				comments: /*comments*/ ctx[3],
    				targetUrl: /*targetUrl*/ ctx[0],
    				feedUrl: /*feedUrl*/ ctx[1],
    				feedIconUrl: /*feedIconUrl*/ ctx[2],
    				addComment: /*addComment*/ ctx[5]
    			},
    			$$inline: true
    		});

    	const block = {
    		c: function create() {
    			create_component(page.$$.fragment);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			mount_component(page, target, anchor);
    			current = true;
    		},
    		p: function update(ctx, [dirty]) {
    			const page_changes = {};
    			if (dirty & /*comments*/ 8) page_changes.comments = /*comments*/ ctx[3];
    			if (dirty & /*targetUrl*/ 1) page_changes.targetUrl = /*targetUrl*/ ctx[0];
    			if (dirty & /*feedUrl*/ 2) page_changes.feedUrl = /*feedUrl*/ ctx[1];
    			if (dirty & /*feedIconUrl*/ 4) page_changes.feedIconUrl = /*feedIconUrl*/ ctx[2];
    			page.$set(page_changes);
    		},
    		i: function intro(local) {
    			if (current) return;
    			transition_in(page.$$.fragment, local);
    			current = true;
    		},
    		o: function outro(local) {
    			transition_out(page.$$.fragment, local);
    			current = false;
    		},
    		d: function destroy(detaching) {
    			destroy_component(page, detaching);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function compareTimestamps(a, b) {
    	if (a.created < b.created) {
    		return 1;
    	}

    	if (a.created > b.created) {
    		return -1;
    	}

    	return 0;
    }

    function instance($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots('App', slots, []);
    	let { streamApiUrl } = $$props;
    	let { targetUrl = "" } = $$props;
    	let { feedUrl = "" } = $$props;
    	let { feedIconUrl = "" } = $$props;
    	let name = "A stream";
    	let comments = [];

    	function addComment(data, onSuccess, onError) {
    		const options = {
    			method: "POST",
    			headers: { "Content-Type": "application/json" },
    			body: JSON.stringify({ url: data.url, text: data.text })
    		};

    		fetch(streamApiUrl, options).then(isSuccess).then(() => {
    			$$invalidate(3, comments = [data, ...comments]);
    			onSuccess();
    		}).catch(() => onError("Something weird happened!"));
    	}

    	function dataToComments(data) {
    		$$invalidate(3, comments = [...data]);
    		comments.sort(compareTimestamps);
    		return comments;
    	}

    	async function loadComments() {
    		let url = streamApiUrl;

    		if (targetUrl !== "") {
    			url = url + "?url=" + targetUrl;
    		}

    		fetch(url).then(isSuccess).then(response => response.json()).then(data => {
    			$$invalidate(3, comments = dataToComments(data));
    		}).catch(error => console.error(error));
    	}

    	onMount(async () => {
    		loadComments();
    	});

    	$$self.$$.on_mount.push(function () {
    		if (streamApiUrl === undefined && !('streamApiUrl' in $$props || $$self.$$.bound[$$self.$$.props['streamApiUrl']])) {
    			console_1.warn("<App> was created without expected prop 'streamApiUrl'");
    		}
    	});

    	const writable_props = ['streamApiUrl', 'targetUrl', 'feedUrl', 'feedIconUrl'];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1.warn(`<App> was created with unknown prop '${key}'`);
    	});

    	$$self.$$set = $$props => {
    		if ('streamApiUrl' in $$props) $$invalidate(6, streamApiUrl = $$props.streamApiUrl);
    		if ('targetUrl' in $$props) $$invalidate(0, targetUrl = $$props.targetUrl);
    		if ('feedUrl' in $$props) $$invalidate(1, feedUrl = $$props.feedUrl);
    		if ('feedIconUrl' in $$props) $$invalidate(2, feedIconUrl = $$props.feedIconUrl);
    	};

    	$$self.$capture_state = () => ({
    		onMount,
    		isSuccess,
    		Page,
    		streamApiUrl,
    		targetUrl,
    		feedUrl,
    		feedIconUrl,
    		name,
    		comments,
    		addComment,
    		dataToComments,
    		compareTimestamps,
    		loadComments
    	});

    	$$self.$inject_state = $$props => {
    		if ('streamApiUrl' in $$props) $$invalidate(6, streamApiUrl = $$props.streamApiUrl);
    		if ('targetUrl' in $$props) $$invalidate(0, targetUrl = $$props.targetUrl);
    		if ('feedUrl' in $$props) $$invalidate(1, feedUrl = $$props.feedUrl);
    		if ('feedIconUrl' in $$props) $$invalidate(2, feedIconUrl = $$props.feedIconUrl);
    		if ('name' in $$props) $$invalidate(4, name = $$props.name);
    		if ('comments' in $$props) $$invalidate(3, comments = $$props.comments);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	return [targetUrl, feedUrl, feedIconUrl, comments, name, addComment, streamApiUrl];
    }

    class App extends SvelteComponentDev {
    	constructor(options) {
    		super(options);

    		init(this, options, instance, create_fragment, safe_not_equal, {
    			streamApiUrl: 6,
    			targetUrl: 0,
    			feedUrl: 1,
    			feedIconUrl: 2
    		});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "App",
    			options,
    			id: create_fragment.name
    		});
    	}

    	get streamApiUrl() {
    		throw new Error("<App>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set streamApiUrl(value) {
    		throw new Error("<App>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get targetUrl() {
    		throw new Error("<App>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set targetUrl(value) {
    		throw new Error("<App>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get feedUrl() {
    		throw new Error("<App>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set feedUrl(value) {
    		throw new Error("<App>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	get feedIconUrl() {
    		throw new Error("<App>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}

    	set feedIconUrl(value) {
    		throw new Error("<App>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
    	}
    }

    /*
    NoComment --- Comment any resource on the web!
    Copyright © 2023 Bioneland

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
    */

    const href = new URL(window.location.href);
    const url = href.searchParams.get("url") || "";

    const app = new App({
      target: document.body,
      props: {
        streamApiUrl: document.body.dataset.streamApiUrl,
        targetUrl: url,
        feedUrl: document.body.dataset.feedUrl,
        feedIconUrl: document.body.dataset.feedIconUrl,
      }
    });

    return app;

})();
//# sourceMappingURL=no-comment.js.map
