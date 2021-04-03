if (debug) console.log("Sogou Main Page is Loaded!");

mPage.initialize = function () {
    mPage.query = $("#upquery").val();
    mPage.page_id = parseInt($("#pagebar_container span").text());
    mPage.html = document.documentElement.outerHTML;
};

setTimeout(mPage.initialize, 1500);

mPage.update = function () {
    $("ul.searchnav").find("a").each(function (id, element) {
        if ($(element).attr("bindClick") == undefined) {
            $(element).attr("bindClick", true);
            $(element).click(function () {
                mPage.click($(this).get(0), "tab", 0);
            });
        }
    });
    $("div.results").children("div").each(function (id, element) {
        $(element).find("a").each(function (child_id, child_element) {
            if ($(child_element).attr("bindClick") == undefined) {
                $(child_element).attr("bindClick", true);
                $(child_element).click(function () {
                    mPage.click($(this).get(0), "content", id+1);
                });
            }
        });
    });
};