/**管理页面信息的接口 */
var mPage = {
    /**
     * 返回值
     */
    click_results: new Array(),
    query: "",
    page_id: 0,
    html: null,
    /**
     * 获得当前搜索查询词
     */
    getQuery: function () {
        return mPage.query;
    },
    getTitle: function () {
      return document.title;
    },
    /**
     * 获得当前搜索页面序号
     */
    getPageId: function () {
        return mPage.page_id;
    },
    /**
     * 获得当前搜索原始网页
     */
    getHtml: function () {
        return mPage.html;
    },

    /**
     * 返回当前页面所有点击结果信息
     */
    getClickedResults: function () {
        return mPage.click_results;
    },
    /**
     * 点击事件的处理
     */
    click: function (link_obj, type, id) {
        var new_click = {
            href: $(link_obj).attr("href"),
            type: type,
            id: id
        };
        mPage.click_results.push(new_click);
        console.log("mPage update");
    },
    lastUpdate: 0,
    /**
     * 更新页面的click绑定
     * 在页面DOM树更新的时候触发
     */
    update: function () {
        if (debug) console.log("mPage update");
    },

    /**
     * 页面信息初始化,不同搜索引擎页面初始化的格式不一样
     */
    initialize: function () {
        mPage.click_results = new Array();
        mPage.html = document.documentElement.outerHTML;
        if (debug) console.log("mPage initialize");
    }
};

var debug = true;
if (debug) console.log("page.js is loaded");
mPage.initialize();
