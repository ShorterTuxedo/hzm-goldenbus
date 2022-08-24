! function(e, t) {
    var n = 1e4,
        g_moduleConfig = {
            uabModule: {
                grey: ["AWSC/uab/1.140.0/collina.js"],
                stable: ["AWSC/uab/1.140.0/collina.js"],
                greyBr: ["AWSC-br/uab/1.140.0/collina.js"],
                stableBr: ["AWSC-br/uab/1.140.0/collina.js"],
                ratio: 10000,
                greyConfig: {},
                stableConfig: {}
            },
            fyModule: {
                grey: ["AWSC/fireyejs/1.223.1/fireyejs.js"],
                stable: ["AWSC/fireyejs/1.222.3/fireyejs.js"],
                greyBr: ["AWSC-br/fireyejs/1.223.1/fireyejs.js"],
                stableBr: ["AWSC-br/fireyejs/1.222.3/fireyejs.js"],
                ratio: 2,
                greyConfig: {},
                stableConfig: {}
            },
            nsModule: {
                grey: ["js/nc/60.js"],
                stable: ["js/nc/60.js"],
                ratio: 1e4,
                greyConfig: {},
                stableConfig: {}
            },
            umidPCModule: {
                grey: ["AWSC/WebUMID/1.90.2/um.js"],
                stable: ["AWSC/WebUMID/1.90.2/um.js"],
                greyBr: ["AWSC-br/WebUMID/1.90.2/um.js"],
                stableBr: ["AWSC-br/WebUMID/1.90.2/um.js"],
                ratio: 10000,
                greyConfig: {},
                stableConfig: {}
            },
            etModule: {
                grey: ["AWSC/et/1.62.0/et_f.js", "AWSC/et/1.62.1/et_n.js"],
                stable: ["AWSC/et/1.62.0/et_f.js", "AWSC/et/1.62.1/et_n.js"],
                greyBr: ["AWSC-br/et/1.62.0/et_f.js", "AWSC-br/et/1.62.1/et_n.js"],
                stableBr: ["AWSC-br/et/1.62.0/et_f.js", "AWSC-br/et/1.62.1/et_n.js"],
                ratio: 10000,
                greyConfig: {
                    "whitelist": ["login.taobao.com/member/login.jhtml", "passport.alibaba.com/mini_login.htm", "login.taobao.com/member/loginByIm.do", "login.taobao.com/member/login_by_safe.htm", "login.taobao.com/member/vst.htm", "login.taobao.com/member/facebookLogin.do", "login.m.taobao.com/login.htm", "login.m.taobao.com/sendMsg.do", "login.m.taobao.com/msg_login.htm", "login.m.taobao.com/login_oversea.htm", "login.m.taobao.com/login_oversea_phone.htm", "login.m.taobao.com/newlogin/login.do", "login.m.taobao.com/newlogin/account/check.do", "login.m.taobao.com/newlogin/sms/send.do", "login.m.taobao.com/newlogin/sms/login.do", "buy.taobao.com/auction/buy_now.jhtml", "buy.taobao.com/auction/order/confirm_order.html", "buy.tmall.com/order/confirm_order.html", "buyertrade.taobao.com/trade/itemlist/list_bought_items.htm", "member1.taobao.com/member/fresh/account_security.htm", "member1.taobao.com/member/fresh/account_management.htm", "member1.taobao.com/member/fresh/weibo_bind_management.htm", "member1.taobao.com/member/fresh/deliver_address.htm", "h5.m.taobao.com/mlapp/olist.html", "h5.m.taobao.com/mlapp/odetail.html", "main.m.taobao.com/olist/index.html", "main.m.taobao.com/odetail/index.html", "h5.m.taobao.com/app/hongbao/www/detail/index.html", "market.m.taobao.com/app/dinamic/h5-tb-olist/index.html", "market.m.taobao.com/app/dinamic/h5-tb-odetail/index.html", "market.m.taobao.com/app/mtb/evaluation-list/pages/index2", "h5.m.taobao.com/qn/mobile/delivery.html", "h5.m.taobao.com/mlapp/odetail.html", "main.m.taobao.com/order/index.html", "buy.m.tmall.com/order/confirmOrderWap.htm", "h5.m.taobao.com/cart/order.html", "h5.m.tmall.hk/cart/order.html"]
                },
                stableConfig: {
                    "whitelist": ["login.taobao.com/member/login.jhtml", "passport.alibaba.com/mini_login.htm", "login.taobao.com/member/loginByIm.do", "login.taobao.com/member/login_by_safe.htm", "login.taobao.com/member/vst.htm", "login.taobao.com/member/facebookLogin.do", "login.m.taobao.com/login.htm", "login.m.taobao.com/sendMsg.do", "login.m.taobao.com/msg_login.htm", "login.m.taobao.com/login_oversea.htm", "login.m.taobao.com/login_oversea_phone.htm", "login.m.taobao.com/newlogin/login.do", "login.m.taobao.com/newlogin/account/check.do", "login.m.taobao.com/newlogin/sms/send.do", "login.m.taobao.com/newlogin/sms/login.do", "buy.taobao.com/auction/buy_now.jhtml", "buy.taobao.com/auction/order/confirm_order.html", "buy.tmall.com/order/confirm_order.html", "buyertrade.taobao.com/trade/itemlist/list_bought_items.htm", "member1.taobao.com/member/fresh/account_security.htm", "member1.taobao.com/member/fresh/account_management.htm", "member1.taobao.com/member/fresh/weibo_bind_management.htm", "member1.taobao.com/member/fresh/deliver_address.htm", "h5.m.taobao.com/mlapp/olist.html", "h5.m.taobao.com/mlapp/odetail.html", "main.m.taobao.com/olist/index.html", "main.m.taobao.com/odetail/index.html", "h5.m.taobao.com/app/hongbao/www/detail/index.html", "market.m.taobao.com/app/dinamic/h5-tb-olist/index.html", "market.m.taobao.com/app/dinamic/h5-tb-odetail/index.html", "market.m.taobao.com/app/mtb/evaluation-list/pages/index2", "h5.m.taobao.com/qn/mobile/delivery.html", "h5.m.taobao.com/mlapp/odetail.html", "main.m.taobao.com/order/index.html", "buy.m.tmall.com/order/confirmOrderWap.htm", "h5.m.taobao.com/cart/order.html", "h5.m.tmall.hk/cart/order.html"]
                }
            },
            ncModule: {
                grey: ["nc.js"],
                stable: ["nc.js"],
                ratio: 10000,
                greyConfig: {},
                stableConfig: {}
            }
        },
        o = [{
            name: "umidPCModule",
            features: ["umpc", "um", "umh5"],
            depends: [],
            sync: !1
        }, {
            name: "uabModule",
            features: ["uab"],
            depends: [],
            sync: !1
        }, {
            name: "fyModule",
            features: ["fy"],
            depends: [],
            sync: !1
        }, {
            name: "nsModule",
            features: ["ns"],
            depends: [],
            sync: !1
        }, {
            name: "etModule",
            features: ["et"],
            depends: [],
            sync: !1
        }, {
            name: "ncModule",
            features: ["nc", "nvc", "ic"],
            depends: ["fy"],
            sync: !1
        }],
        a = navigator.userAgent,
        r = a.match(/Chrome\/(\d*)/);
    r && (r = +r[1]);
    var i = a.match(/Edge\/([\d]*)/),
        s = a.match(/Safari\/([\d]*)/),
        l = a.match(/Firefox\/([\d]*)/),
        c = a.match(/MSIE|Trident/);

    function u() {
        var e = "function%20javaEnabled%28%29%20%7B%20%5Bnative%20code%5D%20%7D";
        return "WebkitAppearance" in document.documentElement.style && escape(navigator.javaEnabled.toString()) === e ? !0 : !1
    }

    function d(t, o) {
        var a = "AWSC_SPECIFY_" + t.toUpperCase() + "_ADDRESSES";
        if (e[a]) return e[a];
        var d = {
            normalAddresses: [],
            brAddresses: []
        };
        for (var f in g_moduleConfig)
            if (g_moduleConfig.hasOwnProperty(f) && f === t) {
                var m = g_moduleConfig[f],
                    b = Math.ceil(Math.random() * n) <= m.ratio;
                d.normalAddresses = b ? m.grey.slice() : m.stable.slice(), m.stableBr && m.greyBr && (d.brAddresses = b ? m.greyBr.slice() : m.stableBr.slice()), "etModule" === t && (i ? (d.normalAddresses.pop(), d.brAddresses.pop()) : r ? (d.normalAddresses.pop(), d.brAddresses.pop()) : s || l || c ? (d.normalAddresses.shift(), d.brAddresses.shift()) : u() ? (d.normalAddresses.pop(), d.brAddresses.pop()) : (d.normalAddresses.shift(), d.brAddresses.shift()));
                for (var g = 0; g < d.normalAddresses.length; g++) {
                    var p = o ? "https://" + o + "/" : A;
                    "https://assets.alicdn.com/" === p && (p += "g/"), d.normalAddresses[g] = p + d.normalAddresses[g], d.brAddresses[g] && (d.brAddresses[g] = p + d.brAddresses[g])
                }
                return d
            }
    }
    var f = [],
        m = "loading",
        b = "loaded",
        g = "timeout",
        p = "unexpected",
        h = "no such feature",
        y = new RegExp("^([\\w\\d+.-]+:)?(?://(?:([^/?#@]*)@)?([\\w\\d\\-\\u0100-\\uffff.+%]*|\\[[^\\]]+\\])(?::([0-9]+))?)?([^?#]+)?(\\?[^#]*)?(#.*)?$"),
        A = v(C());

    function v(e) {
        var t = "https://g.alicdn.com/";
        if (!e) return t;
        if (/aliexpress/.test(location.href)) return "https://aeis.alicdn.com/";
        var n = y.exec(e);
        return n ? "https://" + n[3] + (n[4] ? ":" + n[4] : "") + "/" : t
    }

    function C() {
        for (var e = document.getElementsByTagName("script"), t = 0; t < e.length; t++) {
            var n = e[t],
                o = n.hasAttribute ? n.src : n.getAttribute("src", 4);
            if (/\/awsc\.js/.test(o)) return o
        }
    }

    function _(e) {
        for (var t = void 0, n = 0; n < o.length; n++) {
            for (var a = o[n], r = 0; r < a.features.length; r++)
                if (a.features[r] === e) {
                    t = a;
                    break
                } if (t) break
        }
        return t
    }

    function j(e) {
        for (var t = 0; t < f.length; t++) {
            var n = f[t];
            if (n.name === e) return n
        }
    }

    function S(e) {
        for (var t = void 0, n = 0; n < o.length; n++) {
            var a = o[n];
            if (a.name === e) {
                t = a;
                break
            }
            if (t) break
        }
        return t
    }

    function W(e, n, o) {
        if (o)
            for (var a = 0; a < e.normalAddresses.length; a++) {
                var r = e.normalAddresses[a];
                t.write("<script src=" + r + "></script>")
            } else {
                function i(e, o, a) {
                    for (var r = 0; r < e.length; r++) {
                        var i = e[r],
                            s = t.createElement("script");
                        i = i.split("/")
                        i = i[i.length - 1];
                        console.log(i);
                        s.async = !1, s.src = i, s.id = n, s.onerror = o || function() {}, s.onload = a || function() {};
                        var l = t.getElementsByTagName("script")[0];
                        l && l.parentNode ? l.parentNode.insertBefore(s, l) : (l = t.body || t.head, l && l.appendChild(s))
                        
                    }
                }
                i(e.normalAddresses)
            }
    }

    function T(t, n, o) {
        var a = "https://acjs.aliyun.com/error?v=" + t + "&e=" + encodeURIComponent(n) + "&stack=" + encodeURIComponent(o),
            r = new Image,
            i = "_awsc_img_" + Math.floor(1e6 * Math.random());
        e[i] = r, r.onload = r.onerror = function() {
            try {
                delete e[i]
            } catch (t) {
                e[i] = null
            }
        }, r.src = a
    }

    function w(e, t) {
        Math.random() < 1e-4 && T("awsc_state", "feature=" + e.name + "&state=" + e.state + "&href=" + encodeURIComponent(location.href));
        for (var n = void 0; n = e.callbacks.shift();) try {
            if ("function" == typeof n) n(e.state, e.exportObj);
            else if ("object" == typeof n) {
                var o = e.exportObj;
                o && "function" == typeof o.init && o.init(n)
            }
        } catch (a) {
            if (t) throw a;
            T(e.name, a.message, a.stack)
        }
    }

    function k(e, t, n, o) {
        var a = _(e);
        if (!a) return "function" == typeof t && t(h), void 0;
        var r = n && n.cdn,
            i = n && n.sync,
            s = n && n.timeout || 5e3;
        if (0 !== a.depends.length)
            for (var l = 0; l < a.depends.length; l++) {
                var c = a.depends[l];
                n && (delete n.sync, delete n.timeout, delete n.cdn), M(c, void 0, n)
            }
        var u = o || {};
        u.module = a, u.name = e, u.state = m, u.callbacks = u.callbacks || [], u.options = n, t && u.callbacks.push(t), u.timeoutTimer = setTimeout(function() {
            u.state = g, w(u, n && n.throwExceptionInCallback)
        }, s), o || f.push(u);
        var b = a.sync;
        i && (b = i);
        var p = d(a.name, r);
        W(p, "AWSC_" + a.name, b)
    }

    function M(e, t, n) {
        var o = j(e);
        if (o)
            if (o.state === g) k(e, t, n, o);
            else if (o.state === b) {
            if ("function" == typeof t) t(o.state, o.exportObj);
            else if ("object" == typeof t) {
                var a = o.exportObj;
                a && "function" == typeof a.init && a.init(t)
            }
        } else o.state === m ? t && o.callbacks.push(t) : void 0;
        else k(e, t, n)
    }

    function B(e, t, n) {
        var o = !1;
        try {
            var a = S(e);
            a || void 0, a.moduleLoadStatus = b;
            for (var r = void 0, i = 0; i < f.length; i++) {
                var s = f[i];
                s.module === a && s.name === t && (o = s.options && s.options.throwExceptionInCallback, r = s, clearTimeout(r.timeoutTimer), delete r.timeoutTimer, r.exportObj = n, s.state === m || s.state === g ? (r.state = b, setTimeout(function() {
                    w(r, o)
                }, 0)) : void 0)
            }
            r || (r = {}, r.module = a, r.name = t, r.state = b, r.exportObj = n, r.callbacks = [], f.push(r))
        } catch (l) {
            if (o) throw l;
            T("awsc_error", l.message, l.stack)
        }
    }

    function U(e) {
        e.AWSCFY = function() {}, e.AWSC.configFY = function(e, n, o, a) {
            return t(e, n, o, a)
        }, e.AWSC.configFYSync = function(e, n) {
            return t(null, e, n)
        };

        function t(t, n, o, a) {
            var r = location.protocol + "//" + location.host + location.pathname,
                i = new e.AWSCFY;
            e._umopt_npfp = 0;
            var s = !1;
            i.umidToken = "defaultToken1_um_not_loaded@@" + r + "@@" + (new Date).getTime(), e.AWSC.use("um", function(e, t) {
                "loaded" === e ? (i.umidToken = "defaultToken3_init_callback_not_called@@" + r + "@@" + (new Date).getTime(), t.init(n, function(e, t) {
                    "success" === e ? i.umidToken = t.tn : i.umidToken = "defaultToken4_init_failed with " + e + "@@" + r + "@@" + (new Date).getTime(), s = !0, u()
                })) : (i.umidToken = "defaultToken2_load_failed with " + e + "@@" + r + "@@" + (new Date).getTime(), s = !0, u())
            });
            var l = !1;
            if (i.getUA = function() {
                    return "defaultUA1_uab_not_loaded@@" + r + "@@" + (new Date).getTime()
                }, e.AWSC.use("uab", function(e, t) {
                    l = !0, "loaded" === e ? (i.uabModule = t, i.uabConfig = o, i.getUA = function() {
                        return this.uabModule.getUA(this.uabConfig)
                    }) : i.getUA = function() {
                        return "defaultUA2_load_failed with " + e + "@@" + r + "@@" + (new Date).getTime()
                    }, u()
                }), null != t) var c = e.setTimeout(function() {
                u(!0)
            }, a ? a : 2e3);

            function u(n) {
                null != t && (l && s || n) && (t(i), e.clearTimeout(c))
            }
            return null == t ? i : void 0
        }
    }

    function D(e) {
        var t = function() {};
        e.AWSC.configFYEx = function(e, t, o) {
            return n(e, t, o)
        }, e.AWSC.configFYSyncEx = function(e) {
            return n(null, e)
        };

        function n(n, o, a) {
            var r = (location.protocol + "//" + location.host + location.pathname).substr(0, 128),
                i = new t;
            if (a = a || 2e3, "function" == typeof n) var s = e.setTimeout(function() {
                l()
            }, a);

            function l() {
                "function" == typeof n && (n(i), e.clearTimeout(s))
            }
            return i.getFYToken = i.getUidToken = function() {
                return "defaultFY1_fyjs_not_loaded@@" + r + "@@" + (new Date).getTime()
            }, e.fyglobalopt = o, e.AWSC.use("fy", function(e, t) {
                "loaded" === e ? (i.getFYToken = i.getUidToken = function() {
                    return "defaultFY3_fyjs_not_initialized@@" + r + "@@" + (new Date).getTime()
                }, i.fyObj = t, t.init(o, function(e) {
                    i.getFYToken = function() {
                        return this.fyObj.getFYToken(o)
                    }, i.getUidToken = function() {
                        return this.fyObj.getUidToken(o)
                    }, l()
                })) : (i.getFYToken = i.getUidToken = function() {
                    return "defaultFY2_load_failed with " + e + "@@" + r + "@@" + (new Date).getTime()
                }, l())
            }), "function" == typeof n ? void 0 : i
        }
    }

    function E(e) {
        var t = g_moduleConfig.etModule,
            o = Math.ceil(Math.random() * n) <= t.ratio,
            a = o ? t.greyConfig.whitelist : t.stableConfig.whitelist,
            r = new RegExp(("^" + a.join("$|^") + "$").replace(/\*/g, ".*"));
        r.test(location.host + location.pathname) && (window.etrprtrt = .01, e.AWSC.use("et"))
    }

    function x(e) {
        e.AWSC || (e.AWSC = {}, e.AWSC.use = M, e.AWSCInner = {}, e.AWSCInner.register = B, U(e), D(e), E(e))
    }
    x(e)
}(window, document);