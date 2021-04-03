/**这个是最终要发给服务器的数据 */
var msg = {
    /**
     * 发送消息标记
     */
    send_flag: true,
    /**
     * 用户名,用于对应用户和log
     */
    username: "",
    /**
     * 开始创建时间
     * 单位ms
     */
    start_timestamp: 0,
    /**
     * 结束浏览时间
     * 单位ms
     */
    end_timestamp: 0,
    /**
     * 浏览总时间
     * 单位ms
     */
    dwell_time: 0,
    /**
     * 一个pageTimestamp的数组
     * 记录了每一次查看页面的进入和离开时间点
     */
    page_timestamps: new Array(),
    /**
     * 页面类型
     * "SERP": 搜索页面
     * "general": 非搜索页面
     */
    type: "",
    /**
     * SERP页面源
     * "baidu/sogou/360": 搜索页面
     * "": 非搜索页面
     */
    origin: "",
    /**
     * 网页链接
     */
    url: "",
    /**
    *  网页title
    */
    title: "",
    /**
     * 直接来源网址
     */
    referrer: "",
    /**
     * 在SERP上的来源网址
     * SERP自己的来源是空的
     */
    serp_link: "",

    /**
     * 搜索查询词
     */
    query: "",
    /**
     * 搜索页面序号
     */
    page_id: 0,
    /**
     * 保留页面整体的HTML用于以后使用
     */
    html: "",
    /**
     * 一个mouseMove的数组
     * 记录了鼠标此过程中的所有移动信息
     * 以及滑轮的信息
     */
    mouse_moves: "",
    /**
     * 为一个结果数组
     * 所有点击结果的信息
     */
    clicked_results: "",

    initialize: function () {
        msg.send_flag = true;
        msg.start_timestamp = 0;
        msg.end_timestamp = 0;
        msg.dwell_time = 0;
        msg.page_timestamps = new Array();
        msg.type = "";
        msg.origin = "";
        msg.url = "";
        msg.referrer = "";
        msg.serp_link = "";
        msg.query = "none SERP origin";
        msg.page_id = 0;
        msg.html = "";
        msg.mouse_moves = "";
        msg.clicked_results = "";
        msg.username = "";
    }
};

/**
 * 构造一个时间戳类，表示一次进入和离开页面的时间戳
 * @param {number} inT 进入时间
 * @param {number} outT 离开时间
 */
var pageTimestamp = function (inT, outT) {
    this.inT = inT;
    this.outT = outT;
    /**
     * 返回此次进入和离开的持续时间
     */
    this.getDwell = function () {
        return this.outT - this.inT;
    };
};

/**
 * 页面级别时间的管理
 * 所有关于该页面的时间戳事件由viewState改变pageManager状态
 */
var pageManager = {
    /**
     * 开始创建时间
     * 单位ms
     */
    start_timestamp: 0,
    /**
     * 结束浏览时间
     * 单位ms
     */
    end_timestamp: 0,
    /**
     * 浏览总时间
     * 单位ms
     */
    dwell_time: 0,
    /**
     * 一个pageTimestamp的数组
     * 记录了每一次查看页面的进入和离开时间点
     */
    page_timestamps: new Array(),
    /**
     * 上次进入这个页面查看的时间
     */
    lastViewTime: 0,

    /**
     * 开启一个页面
     */
    initialize: function () {
        pageManager.start_timestamp = (new Date()).getTime();
        pageManager.end_timestamp = pageManager.start_timestamp;
        pageManager.dwell_time = 0;
        pageManager.page_timestamps = new Array();
        pageManager.lastViewTime = pageManager.start_timestamp;
        if (debug) console.log("pageManager initialize");
    },
    /**
     * 用户开始查看这个页面
     */
    getIn: function () {
        pageManager.lastViewTime = (new Date()).getTime();
    },

    /**
     * 用户不再查看当前页面
     */
    getOut: function () {//切出页面
        pageManager.end_timestamp = (new Date()).getTime();
        pageManager.page_timestamps.push(new pageTimestamp(pageManager.lastViewTime, pageManager.end_timestamp));
        pageManager.dwell_time += pageManager.end_timestamp - pageManager.lastViewTime;
        pageManager.lastViewTime = pageManager.end_timestamp;
    }
};

/**当前页面可见性 */
var viewState = {
    /**
     * 当前状态
     * true 用户正在查看页面
     * false 用户切出页面以外
     */
    show: true,
    /**
     * 上次操作时间
     */
    lastOp: 0,
    /**
     * 超时时长
     * 如果用户超过这个时间没有任何动作，
     * 我们认为用户离开。
     * 当前时限：10s
     */
    timeLimit: 10000,
    /**
     * 检查是否超时
     */
    check: function () {
        if (debug) console.log("check state");
        if ((new Date()).getTime() - viewState.lastOp >= viewState.timeLimit && viewState.show == true)
            viewState.toggleState();
        else if (viewState.show == true)
            setTimeout(viewState.check, viewState.timeLimit);
    },
    /**
     * 切换当前可见状态
     */
    toggleState: function () {
        if (debug) console.log("View State Changed from " + viewState.show + " to " + !viewState.show);
        if (viewState.show == false) {
            viewState.show = true;
            viewState.check();
            pageManager.getIn();
        } else {
            viewState.show = false;
            pageManager.getOut();
            mRec.pause();
        }
    },

    /**
     * 进入页面
     */
    getIn: function () {
        viewState.lastOp = (new Date()).getTime();
        if (viewState.show == false) {
            viewState.toggleState();
        }
    },
    /**
     * 离开页面
     */
    getOut: function () {
        if (viewState.show == true) {
            viewState.toggleState();
        }
    },
    /**
     * 标签栏切入页面响应的函数
     */
    tabEnter: function () {
        viewState.getIn();
    },
    /**
     * 标签栏切出页面响应的函数
     * 在页面关闭时也会响应
     * 会在 onbeforeunload 之后响应
     * 切入后台(alt+tab)不会响应，
     * 只有标签页切换才会响应
     */
    tabLeave: function () {
        viewState.getOut();
    },
    /**
     * 获得焦点
     * 如果同时触发tabEnter,会在tabEnter之后调用
     */
    focus: function () {
        if (debug) console.log("focus");
        viewState.getIn();
    },
    /**
     * 失去焦点
     * 比如鼠标点击地址栏或切入后台
     */
    blur: function () {
        if (debug) console.log("blur");
        viewState.getOut();
    },
    /**
     * 鼠标在当前页面内移动了一下
     * @param {鼠标位置信息} e
     */
    mMove: function (e) {
        viewState.getIn();
        mRec.move(e);

        //if (debug) console.log(msg);
    },
    /**
     *  鼠标滚轮滚动
     */
    mScroll: function () {
        viewState.getIn();
        mRec.scroll();
    },
    /**
     * 页面内容改变
     */
    update: function () {
        //if (debug) console.log("update");
        mPage.update();
        //viewState.getIn();
    },
    /**
     * 页面关闭
     */
    close: function () {
        viewState.sendMessage();
    },
    /**
     * 页面初始化
     */
    initialize: function () {
        document.addEventListener("visibilitychange", function (event) {
            var hidden = event.target.webkitHidden;
            if (hidden) viewState.tabLeave();
            else viewState.tabEnter();
        }, false);
        window.onbeforeunload = viewState.close;
        $(window).focus(viewState.focus);
        $(window).blur(viewState.blur);
        viewState.show = true;
        viewState.lastOp = (new Date()).getTime();

        var origin = "???";
        var temp = window.location.href.match(/www\.(baidu)?(sogou)?(so)?\.com\/(s|web)/g);
        if (temp != null) { //SERP页面
            switch (temp[0]) {
                case "www.sogou.com/web":
                    origin = "sogou";
                    break;

                case "www.baidu.com/s":
                    origin = "baidu";
                    break;

                case "www.so.com/s":
                    origin = "360";
                    break;

                default:
                    break;
            }
        }
        if (debug) {
            /*console.log("origin=" + origin);
            console.log(viewState);
            console.log(pageManager);
            console.log(mPage);
            console.log(mRec);*/
        }

        if (origin != "???") { //SERP页面
            if (debug) console.log("extension is working on SERP");
            /**
             * SERP页面才会记录鼠标移动和点击信息
             * 现在非SERP也可以了
             */
            $(window).bind('mousemove', viewState.mMove);
            $(window).bind('scroll', viewState.mScroll);
            //$(window).mousemove(viewState.mMove);
            //$(window).scroll(viewState.mScroll);
            /**
             * 执行相应搜索引擎的页面脚本
             */
            chrome.runtime.sendMessage({file: origin + ".js"}, function (response) {
                if (response.scriptFinish == true) {
                    if (debug) console.log("execute script done");
                    pageManager.initialize();
                    mPage.initialize();
                    mRec.initialize();
                    viewState.check();
                }
            });
        }
        else { //非SERP页面
            if (debug) console.log("extension is working on general page");
            $(window).bind('mousemove', viewState.mMove);
            $(window).bind('scroll', viewState.mScroll);
            pageManager.initialize();
            mPage.initialize();
            mRec.initialize();
            viewState.check();
        }

    },
    /**
     * 保存信息
     */
    sendMessage: function () {
        if (debug) console.log("send Message");
        pageManager.getOut();
        mRec.end();
        var origin = "???";
        var temp = current_url.match(/www\.(baidu)?(sogou)?(so)?\.com\/(s|web)/g);
        if (temp != null) { //SERP页面
            switch (temp[0]) {
                case "www.sogou.com/web":
                    origin = "sogou";
                    break;

                case "www.baidu.com/s":
                    origin = "baidu";
                    break;

                case "www.so.com/s":
                    origin = "360";
                    break;

                default:
                    break;
            }
        }

        msg.start_timestamp = pageManager.start_timestamp;
        msg.end_timestamp = pageManager.end_timestamp;
        msg.dwell_time = pageManager.dwell_time;
        msg.page_timestamps = JSON.stringify(pageManager.page_timestamps);
        msg.url = current_url;
        msg.title = document.title;
        console.log(msg.title);
        msg.referrer = current_referrer;
        msg.serp_link = current_serp_link;

        //msg.html = pako.deflate(mPage.getHtml(), {to: 'string'});
        msg.html = mPage.getHtml();
        //msg.mouse_moves = pako.deflate(JSON.stringify(mRec.getData()), {to: 'string'});
        msg.mouse_moves = JSON.stringify(mRec.getData());
        //msg.clicked_results = pako.deflate(JSON.stringify(mPage.getClickedResults()), {to: 'string'});
        msg.clicked_results = JSON.stringify(mPage.getClickedResults());

        if (origin != "???") {
            msg.type = "SERP";
            msg.origin = origin;
            msg.query = mPage.getQuery();//不应该实时取,应该读取当前保存的,否则监测到url变化但页面没刷新的情况就会出错.值的更新应该在initialize时完成
            msg.page_id = mPage.getPageId();//同上
        }
        else {
            msg.type = "general";
        }

        chrome.runtime.sendMessage(msg);
        msg.initialize();
    }
};
