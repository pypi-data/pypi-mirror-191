// 硬核

// 周控制变量
// 0 当前周
// -1 上周
var CURRENT_WEEK = 0;

// true 修改了
// false 没修改
var EDITED_LOCK = false;

// function set_editable_writing(editable) {
//     editable.nextElementSibling.children[0].style.display = 'block';
//     editable.nextElementSibling.children[1].style.display = 'none';
// }

// function set_editable_uploading(editable) {
//     editable.nextElementSibling.children[0].style.display = 'none';
//     editable.nextElementSibling.children[1].style.display = 'block';
// }

// function set_editable_none(editable) {
//     editable.nextElementSibling.children[0].style.display = 'none';
//     editable.nextElementSibling.children[1].style.display = 'none';
// }

function bind_listener(editor) {
    editor.subscribe('focus', function(event, editable) {
        // Do some work
        console.log('focus', editable);
        // set_editable_writing(editable);
        // EDITED_LOCK = true
    });

    editor.subscribe('editableInput', function(event, editable) {
        // Do some work
        console.log('editableInput', editable);
        // EDITED_LOCK = true
    });

    editor.subscribe('editableBlur', function(event, editable) {
        // if (EDITED_LOCK == false) {
        //     return
        // }
        // set_editable_uploading(editable);
        // EDITED_LOCK = false
        // Do some work
        // update sql
        console.log('editableBlur', editable.parentNode)
        let id = editable.parentNode.dataset.id
        let html = editable.parentNode.childNodes[3].innerHTML.trim();
        let text = editable.parentNode.childNodes[3].innerText.trim();
        let tag = Commonexp.tag(text);
        // UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
        let sql = '{"sql":"UPDATE DONE SET HTML\= \'' + html.toHtmlEntities() + '\', CLASS\= \'' + tag.toHtmlEntities() + '\' WHERE ID\=\'' + id + '\';"}'
        $.post("/dcl", sql, function(result) {
            console.log(result);
            // set_editable_none(editable);
            // callback()
        });
    });

    // $('.editortest').mediumInsert({
    //     editor: editor,
    //     addons: {
    //         images: {
    //             fileUploadOptions: {
    //                 url: 'http://localhost:8888/file-upload'
    //             }
    //         }
    //     }
    // });
}


/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

function addrecord(element) {
    // TODO: 这里的情况应该分为
    let target = element.parentNode.previousElementSibling
    let date = moment(target.parentNode.firstElementChild.firstElementChild.children[2].innerHTML).utc().format();
    if ($(target).hasClass('ld-harness-list-header')) {
        console.log('这日期没写过')
        let id = moment(moment()).valueOf();
        if (moment(date).format('YYYY/MM/DD') == moment().format('YYYY/MM/DD')) {
            date = getDatetime()
        }
        // let date = getDatetime();
        $.post("/dcl", '{"sql":"INSERT INTO DONE(ID,DATETIME) VALUES(\'' + id + '\',\'' + date + '\');"}', function(result) {
            console.log(result);
            htmlrecord(id, date, element);
            // callback()
        });
    } else if ($(target).hasClass('ld-harness-list-item')) {
        console.log('这日期写过，追加');
        let id = moment(moment()).valueOf();
        // let date = moment(target.parentNode.firstElementChild.firstElementChild.children[2].innerHTML).utc().format();
        if (moment(date).format('YYYY/MM/DD') == moment().format('YYYY/MM/DD')) {
            date = getDatetime()
        }
        if (target.children[1].innerText.trim() == "") {
            alert("芽衣姐，上一个还是全空啊")
            return
        }
        $.post("/dcl", '{"sql":"INSERT INTO DONE(ID,DATETIME) VALUES(\'' + id + '\',\'' + date + '\');"}', function(result) {
            console.log(result);
            htmlrecord(id, date, element);
            // callback()
        });
    } else {
        console.log('bug')
        debugger
    }

}

// TODO 两个应该合在一起
function htmlrecord(id, date, element) {
    console.log(element)
    console.log(element.parentNode)
    var target = element.parentNode
    var root = element.parentNode.parentNode
    var source = htmlToElement('<div class="ld-harness-list-item list-group-item" aria-current="true" data-id="' + id + '" data-date="' + date + '">\
        <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">\
            <small class="text-muted">' + moment(date).format('ah:mm') + '</small>\
            <small>\
            </small>\
        </div>\
        <div class="ld-harness-list-item-text">\
        </div>\
    </div>')
    root.insertBefore(source, target)
    var source_editor = new MediumEditor(source.childNodes[3], {
        buttonLabels: 'fontawesome'
    });

    bind_listener(source_editor)

}

function random(items) {
    var item = items[Math.floor(Math.random() * items.length)];
    return item
}

function html_lender_image_box(time, url) {
    let html = function() {
        /*
        <a href="/html/{0}" target="_blank">
            <img src="/html/{0}"/>
            <div class="mdui-grid-tile-actions mdui-grid-tile-actions-gradient">
                <div class="mdui-grid-tile-text">
                    <!--div class="mdui-grid-tile-title"></div-->
                    <!--div class="mdui-grid-tile-subtitle"><i class="mdui-icon material-icons">grid_on</i>Ellie Goulding</div-->
                    <div class="mdui-grid-tile-text"><div class="mdui-grid-tile-title">{1}</div></div>
                </div>
                <!--div class="mdui-grid-tile-buttons">
                    <a class="mdui-btn mdui-btn-icon"><i class="mdui-icon material-icons">star_border</i></a>
                </div-->
            </div>
        </a>
        */
    }
    return '<div class="mdui-grid-tile">' + html.getMultiLine().format(url, moment(time).format('Y-MM-DD')) + '</div>'
}

function html_badges(badges) {
    console.log(badges)
    var items = ['badge bg-primary', 'badge bg-secondary', 'badge bg-success', 'badge bg-danger', 'badge bg-warning text-dark', 'badge bg-info text-dark', 'badge bg-light text-dark', 'badge bg-dark'];
    let badge = ''
    String.fromHtmlEntities(badges).split(",").forEach(function(t) {
        badge += '<span class="' + random(items) + '">' + t + '</span>\n'
    })
    return badge
}

function html_lender_list_box(time, obj) {
    let header = '\
    <li class="ld-harness-list-header list-group-item list-group-item-secondary mdui-color-theme-50">\
        <div class="row">\
            <div class="col-md-2">' + moment(time).format("dddd") + '</div>\
            <div class="col-md-8"></div>\
            <div class="col-md-2">' + time + '</div>\
        </div>\
    </li>'

    let items = ''
    for (let index = 0; index < obj.length; index++) {
        const element = obj[index];
        let badge = html_badges(element[4])

        let html = function() {
            /*
            <div href="#" class="ld-harness-list-item list-group-item" aria-current="true" data-id="{0}" data-date="{1}">
                <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">
                    <div class="text-muted" style="margin: auto 0;">
                        <small>{2}</small>
                    </div>
                    <div>
                        <button type="button" class="btn btn-sm mdui-btn mdui-btn-icon mdui-ripple" onclick="clipCard(this)" mdui-tooltip="{content: '复制', position: 'bottom'}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard-check" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
                            </svg></button>
                        <button type="button" class="btn btn-sm mdui-btn mdui-btn-icon mdui-ripple" onclick="deleteCard(this)" mdui-tooltip="{content: '删除', position: 'bottom'}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                        </svg></button>
                            
                    </div>
                </div>
                <div class="ld-harness-list-item-text">
                    {3}
                </div>
                <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">
                    <small class="writing text-muted">Writing
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                            <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"/>
                            </svg></small>
                    <small class="uploading text-muted">Uploading
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-upload" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
                            <path fill-rule="evenodd" d="M7.646 4.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V14.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3z"/>
                            </svg></small>
                    <small>{4}</small>
                </div>
            </div>
            */
        };

        // items += html.getMultiLine().format(moment(element[1]).format('LT'), badge, element[2]);
        items += html.getMultiLine().format(element[0], moment(element[1]), moment(element[1]).format('ah:mm'), String.fromHtmlEntities(element[2]), badge);
    }

    let add = '\
    <div class="ld-harness-list-add list-group-item" aria-current="true">\
        <div class=" d-grid gap-2 col-6 mx-auto" onclick="addrecord(this)">\
            <button type="button" class="btn btn-outline-light"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">\
                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>\
            </svg></button>\
        </div>\
    </div>'

    return '<div class="list-group">' + header + items + add + '</div>'
}

// 输出UTC
// 按中国时区的UTC时间，所以输出的应该是一个八点到八点的时间
function getWeekRangeUTC(offset = 0) {
    let weekOfday = moment().format('E'); //计算今天是这周第几天
    let monday = moment(moment().format('YYYY-MM-DD')).subtract(weekOfday - 1, 'days');
    monday = monday.add(offset, 'weeks');
    let sunday = moment(monday).add(7, 'days');
    return [monday.utc().format(), sunday.utc().format()]
}

// offset: 0, current week
// offset: -1, last week
function getWeekdate(offset = 0, sort = 'asc', format = 'YYYY/MM/DD') {
    console.log(offset, format)
    let weekOfday = moment().format('E'); //计算今天是这周第几天
    let monday = moment().subtract(weekOfday, 'days');
    monday = monday.add(offset, 'weeks');
    let dates = []
    if (sort == 'asc') {
        for (let index = 1; index < 8; index++) {
            const element = index;
            let someday = moment(monday).add(index, 'days');
            if (someday <= moment()) {
                dates.push(someday.format(format))
            }
        }
    } else if (sort == 'desc') {
        for (let index = 7; index > 0; index--) {
            const element = index;
            let someday = moment(monday).add(index, 'days');
            if (someday <= moment()) {
                dates.push(someday.format(format))
            }
        }
    } else {

    }

    return dates
}
// 按日期重新组织数据
// 这里应该按日期，有的往里加，而不是简单构建map
// 输入UTC
// 输出locale
function list2daily(list) {
    let result = {};
    let weekdates = getWeekdate(CURRENT_WEEK, 'desc');
    for (let index = 0; index < weekdates.length; index++) {
        const element = weekdates[index];
        result[element] = []
    }

    console.log(list);
    for (let index = 0; index < list.length; index++) {
        const element = list[index];
        let day = locDatetime(element[1], 'L')
        if (day in result) {
            result[day].push(element)
        }
    }
    return result
}

// 输入UTC
// 输出locale
function list2dailyImage(list) {
    let week = {};
    let weekdates = getWeekdate(CURRENT_WEEK, 'desc');
    for (let index = 0; index < weekdates.length; index++) {
        const element = weekdates[index];
        week[element] = []
    }

    console.log(list);
    let results = []
    for (let index = 0; index < list.length; index++) {
        const element = list[index];
        let day = locDatetime(element.created_time * 1000, 'L');
        if (day in week) {
            results.push(element);
        }
    }
    return results
}

function lender_list_init(callback) {
    let weekdate = getWeekRangeUTC(CURRENT_WEEK);
    // 传入between的只能是单引号
    // 分号不要忘记了
    // $.post("/dql", '{"sql":"SELECT * FROM DONE WHERE DATETIME BETWEEN \'2020-06-12\' AND \'2022-06-18\'; "}', function(result) {
    $.post("/dql", '{"sql":"SELECT * FROM DONE WHERE DATETIME between \'' + weekdate[0] + '\' and \'' + weekdate[1] + '\'; "}', function(result) {
        var data = JSON.parse(result)
        data = list2daily(data)
        console.log(data)
        $(".ld-harness").empty()
        for (const key in data) {
            if (Object.hasOwnProperty.call(data, key)) {
                const element = data[key];
                console.log(element)
                $(".ld-harness").append(html_lender_list_box(key, element));
            }
        }
        callback()
    });
}

function lender_image_init(callback) {
    $.get("/userdata", function(result) {
        var data = JSON.parse(result)
        data = list2dailyImage(data)
        console.log(data)
        $(".ld-images").empty();

        for (let index = 0; index < data.length; index++) {
            const element = data[index];
            console.log(element);
            $(".ld-images").append(html_lender_image_box(element.created_time * 1000, element.url));
        }

        if (typeof callback === "function") {
            callback()
        }
    });
}

function initDatetime() {
    moment.locale('zh-cn');
}

function getDatetime() {
    return moment.utc().format();
}

function locDatetime(utcstring, type = 'LLLL') {
    return moment(utcstring).format(type); // 2022年5月3日星期二下午5点17分

    // moment.locale();         // zh-cn
    // moment().format('LT');   // 17:19
    // moment().format('LTS');  // 17:19:50
    // moment().format('L');    // 2022/05/03
    // moment().format('l');    // 2022/5/3
    // moment().format('LL');   // 2022年5月3日
    // moment().format('ll');   // 2022年5月3日
    // moment().format('LLL');  // 2022年5月3日下午5点19分
    // moment().format('lll');  // 2022年5月3日 17:19
    // moment().format('LLLL'); // 2022年5月3日星期二下午5点19分
    // moment().format('llll'); // 2022年5月3日星期二 17:19
}

function harness_editable() {
    // (Firefox 插入<br>、IE/Opera将使用<p>、 Chrome/Safari 将使用 <div>）
    var editor = new MediumEditor('.ld-harness-list-item-text', {
        buttonLabels: 'fontawesome'
    });
    bind_listener(editor)
}

function clipCard(aux) {
    let targets = aux.parentNode.parentNode.nextElementSibling.children;
    let textContent = ''
    for (const iterator of targets) {
        textContent += iterator.textContent + "\n"
    }
    // navigator.clipboard.writeText(target.textContent).then(function() {
    //     /* clipboard successfully set */
    // }, function() {
    //     /* clipboard write failed */
    // });
    // return
    let tmpele = document.createElement("textarea"); //创建input节点
    aux.appendChild(tmpele); //将节点添加到body
    tmpele.value = textContent; //将需要复制的字符串赋值到input的value中
    tmpele.select(); //选中文本(关键一步)
    document.execCommand("copy"); //执行浏览器复制功能(关键一步)
    aux.removeChild(tmpele); //复制完成后删除节点

    // console.log(target.textContent);
    // target.setAttribute("value", target.textContent);
    // target.select();
    // document.execCommand('copy', false, target.textContent);

    // let that = this
    // let txa = document.createElement('textarea')
    // let txval = 'SN:' + that.sn1 + '\n' + 'MAC:' + that.mac1 + '\n' + 'IMEI:' + that.imei1 + '\n' + 'PORT:' + that.port1;
    // // console.log('copy val:', txval)
    // txa.value = txval
    // document.body.appendChild(txa)
    // txa.select()
    // let res = document.execCommand('copy')
    // document.body.removeChild(txa)
    // console.log('copy success')
}

function deleteCard(aux) {
    console.log()
    let card = aux.parentNode.parentNode.parentNode
    let cardid = card.dataset.id;
    let sql = '{"sql":"UPDATE DONE SET STATUS\= \'1\' WHERE ID\=\'' + cardid + '\';"}'
    let timer_is_on = 0;

    card.style.display = 'none';
    mdui.snackbar({
        message: '[Lender] Deleting',
        buttonText: 'undo',
        onClick: function() {
            // mdui.alert('点击了 Sanckbar');
        },
        onButtonClick: function() {
            // mdui.alert('点击了按钮');
            timer_is_on = 1;
        },
        onClose: function() {
            // mdui.alert('关闭了');
            if (timer_is_on == 0) {
                $.post("/dcl", sql, function(result) {
                    console.log(result);
                    card.remove();
                });
            } else {
                card.style.display = 'block';
            }
        }
    });

}


function prevWeek() {
    InitWeek(-1)
    CURRENT_WEEK -= 1
    console.log('CURRENT_WEEK', CURRENT_WEEK)
    lender_list_init(harness_editable);
    $('.fc-toolbar-title')[0].innerHTML = moment().add(CURRENT_WEEK, 'weeks').format('Y年 第Wo')
}

function nextWeek() {
    CURRENT_WEEK += 1
    console.log('CURRENT_WEEK', CURRENT_WEEK)
    lender_list_init(harness_editable);
    $('.fc-toolbar-title')[0].innerHTML = moment().add(CURRENT_WEEK, 'weeks').format('Y年 第Wo')
}

function thisWeek() {
    CURRENT_WEEK = 0
    console.log('CURRENT_WEEK', CURRENT_WEEK)
    lender_list_init(harness_editable);
    $('.fc-toolbar-title')[0].innerHTML = moment().add(CURRENT_WEEK, 'weeks').format('Y年 第Wo')
    lender_image_init(null);
}

function InitWeek(week_offset = 0) {
    if (week_offset == 0) {
        CURRENT_WEEK = 0;
    }
    CURRENT_WEEK += week_offset
    console.log('CURRENT_WEEK', CURRENT_WEEK)
    lender_list_init(harness_editable);
    $('.fc-toolbar-title')[0].innerHTML = moment().add(CURRENT_WEEK, 'weeks').format('Y年 第Wo')
    lender_image_init(null);
}

var toastTrigger = document.getElementById('liveToastBtn')
var toastLiveExample = document.getElementById('liveToast')
if (toastTrigger) {
    toastTrigger.addEventListener('click', function() {
        var toast = new bootstrap.Toast(toastLiveExample)

        toast.show()
    })
}

initDatetime();
InitWeek(0);


function html_search_list_box(time, obj) {
    let header = '\
    <li class="ld-harness-list-header list-group-item list-group-item-secondary mdui-color-theme-50">\
        <div class="row">\
            <div class="col-md-2">' + moment(time).format("dddd") + '</div>\
            <div class="col-md-8"></div>\
            <div class="col-md-2">' + time + '</div>\
        </div>\
    </li>'

    let items = ''
    for (let index = 0; index < obj.length; index++) {
        const element = obj[index];
        let badge = html_badges(element[4])

        let html = function() {
            /*
            <div href="#" class="ld-harness-list-item list-group-item" aria-current="true" data-id="{0}" data-date="{1}">
                <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">
                    <div class="text-muted" style="margin: auto 0;">
                        <small>{2}</small>
                    </div>
                    <div>
                        <button type="button" class="btn btn-sm mdui-btn mdui-btn-icon mdui-ripple" onclick="clipCard(this)" mdui-tooltip="{content: '复制', position: 'bottom'}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard-check" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M10.854 7.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708 0z"/>
                            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
                            </svg></button>
                        <button type="button" class="btn btn-sm mdui-btn mdui-btn-icon mdui-ripple" onclick="deleteCard(this)" mdui-tooltip="{content: '删除', position: 'bottom'}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                        </svg></button>
                            
                    </div>
                </div>
                <div class="ld-harness-list-item-text">
                    {3}
                </div>
                <div class="ld-harness-list-item-info d-flex w-100 justify-content-between">
                    <small class="writing text-muted">Writing
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pen" viewBox="0 0 16 16">
                            <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001zm-.644.766a.5.5 0 0 0-.707 0L1.95 11.756l-.764 3.057 3.057-.764L14.44 3.854a.5.5 0 0 0 0-.708l-1.585-1.585z"/>
                            </svg></small>
                    <small class="uploading text-muted">Uploading
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-upload" viewBox="0 0 16 16">
                            <path fill-rule="evenodd" d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
                            <path fill-rule="evenodd" d="M7.646 4.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V14.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708l3-3z"/>
                            </svg></small>
                    <small>{4}</small>
                </div>
            </div>
            */
        };

        // items += html.getMultiLine().format(moment(element[1]).format('LT'), badge, element[2]);
        items += html.getMultiLine().format(element[0], moment(element[1]), locDatetime(element[1], 'L') + " " + moment(element[1]).format('ah:mm'), String.fromHtmlEntities(element[2]), badge);
    }

    let add = '\
    <div class="ld-harness-list-add list-group-item" aria-current="true">\
        <div class=" d-grid gap-2 col-6 mx-auto" onclick="addrecord(this)">\
            <button type="button" class="btn btn-outline-light"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">\
                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>\
            </svg></button>\
        </div>\
    </div>'

    return '<div class="list-group">' + items + '</div>'
}

function search_input(obj){
    console.log(obj.value)
    if (obj.value == "") {
        return
    }
    console.log(obj.value.toHtmlEntities())
    $.post("/dql", '{"sql":"SELECT * FROM DONE WHERE CLASS like \'%' + obj.value.toHtmlEntities() + '%\' or HTML like \'%' + obj.value.toHtmlEntities() + '%\'; "}', function(result) {
        var datas = JSON.parse(result)
        console.log(datas)
        // data = list2daily(data)
        $("#search-result").empty()
        $("#search-result").append(html_search_list_box(1, datas));
        harness_editable()
        $("#search-result").show()
});
}

function search_close(obj){
    console.log(obj)
    $("#search-result").hide()
    // $.post("/dql", '{"sql":"SELECT * FROM DONE WHERE tag like \'%' + html.toHtmlEntities() + '%\' or text \'' + html.toHtmlEntities() + '\'; "}', function(result) {
    //     var data = JSON.parse(result)
    //     data = list2daily(data)
    //     console.log(data)
    //     $("#search-result").empty()
    //     for (const key in data) {
    //         if (Object.hasOwnProperty.call(data, key)) {
    //             const element = data[key];
    //             console.log(element)
    //             $("#search-result").append(html_lender_list_box(key, element));
    //         }
    //     }
    //     callback()
    // });
}
// $(function() {
//     document.getElementById("changetheme").onchange = function (obj) {
//         console.log(obj.text)
//         document.body.classList = ['mdui-theme-primary-' + theme]
//     };
// });

function changetheme(theme) {
    console.log(theme)
    document.body.classList = ['mdui-theme-primary-' + theme]
}
// $(window).load(function() {});

function getDateDura(date) {
    let m2 = moment(); //当下时间
    // let m2=moment('2019-12-18 10:10:00');
    let m1 = moment(date);
    let du = moment.duration(m2 - m1, 'ms'); //做差
    let days = du.get('days');
    let hours = du.get('hours');
    let mins = du.get('minutes');
    let ss = du.get('seconds');
    console.log(days, hours, mins, ss);
    //  输出结果为   01天08时09分40秒
    if (days > 0) {
        date = moment(date).format("YYYY年MM月DD日");
        return date
    } else if (hours > 0) {
        return hours + '小时之前'
    } else {
        return mins + '分钟之前'
    }
}