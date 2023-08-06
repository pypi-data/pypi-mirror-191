/**
 * 
 * string format print, meaning Sprintf() in c++
 * 
 * Return string
 * 
 * Ex.
 * "h{0}t{1}m{2}l".format(4,5,6)
 *  
 * */
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length > 0) {
        if (arguments.length == 1 && typeof(args) == "object") {
            for (var key in args) {
                if (args[key] != undefined) {
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
        } else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] != undefined) {
                    //var reg = new RegExp("({[" + i + "]})", "g");//这个在索引大于9时会有问题，谢谢何以笙箫的指出
                    var reg = new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
}

String.format = function() {
    if (arguments.length == 0)
        return null;

    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
}

/**
 * 
 * isPhonenumberAvailable from commet
 * 
 * Return string
 * 
 * Ex.
 * "html".isPhonenumberAvailable()
 *  
 * */
String.prototype.isPhonenumberAvailable = function() {
    var result = this;
    var myreg = /^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$/;
    if (!myreg.test(result)) {
        return false;
    } else {
        return true;
    }
}

/**
 * 
 * getMultiLine from commet
 * 
 * Return string
 * 
 * Ex.
 * "html".getMultiLine()
 *  
 * */
Function.prototype.getMultiLine = function() {
    var lines = new String(this);
    lines = lines.substring(lines.indexOf("/*") + 3, lines.lastIndexOf("*/"));
    return lines;
}



// var str = "Dummy Test´†®¥¨©˙∫ø…ˆƒ∆÷∑™ƒ∆æøπ£¨ ƒ™en tést".toHtmlEntities();
// console.log("Entities:", str);
// console.log("String:", String.fromHtmlEntities(str));
// "Entities:"
// "Test&#180;&#8224;&#174;&#165;&#168;&#169;&#729;&#8747;&#248;&#8230;&#710;&#402;&#8710;&#247;&#8721;&#8482;&#402;&#8710;&#230;&#248;&#960;&#163;&#168; &#402;&#8482;en t&#233;st"
// "String:"
// "Dummy Test´†®¥¨©˙∫ø…ˆƒ∆÷∑™ƒ∆æøπ£¨ ƒ™en tést"

// 对应的python3 解码方式
// import html
// html.unescape(str)

/**
 * Conversion of string to HTML entities
 */
String.prototype.toHtmlEntities = function() {
    return this.replace(/./gm, function(s) {
        // return "&#" + s.charCodeAt(0) + ";";
        return (s.match(/[a-z0-9\s]+/i)) ? s : "&#" + s.charCodeAt(0) + ";";
    });
};

/**
 * Creation of string from HTML entities
 */
String.fromHtmlEntities = function(string) {
    return (string + "").replace(/&#\d+;/gm, function(s) {
        return String.fromCharCode(s.match(/\d+/gm)[0]);
    })
};