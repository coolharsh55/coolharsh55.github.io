/**
 * Cookie Notice JS
 * @author Alessandro Benoit
 */
;
(function () {

    "use strict";

    /**
     * Store current instance
     */
    var instance;
    /**
     * Initialize cookie notice on DOMContentLoaded
     * if not already initialized with alt params
     */
    document.addEventListener('DOMContentLoaded', function () {
        if (!instance) {
            new cookieNoticeJS();
        }
    });

    /**
     * Constructor
     * @constructor
     */
    window.cookieNoticeJS = function () {

        // If an instance is already set stop here
        if (instance !== undefined) {
            return;
        }
        // document.cookie = 'harshpTestCookie=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        // Set current instance
        instance = this;

        if (document.cookie.indexOf('harshpCookieConsent') != -1) {
            return;
        }

        // Create notice
        var notice = document.createElement('div'),
            noticeStyle = notice.style;

        notice.innerHTML = "I use cookies, for <a class='link' href='https://harshp.com/privacy-policy'><span class='light-blue'>good reasons</span></a>, promise!";
        notice.setAttribute('id', 'cookieNotice');

        noticeStyle.position = 'fixed';
        noticeStyle.bottom = 0;
        noticeStyle.left = 0;
        noticeStyle.right = 0;
        noticeStyle.background = "#111111";
        noticeStyle.color = "#EEEEEE";
        noticeStyle["z-index"] = '999';
        noticeStyle.padding = '10px 5px';
        noticeStyle["text-align"] = 'center';
        noticeStyle["font-size"] = "12px";
        noticeStyle["line-height"] = "28px";
        noticeStyle.fontFamily = 'Helvetica neue, Helvetica, sans-serif';

        var dismissButton = document.createElement('a'),
            dismissButtonStyle = dismissButton.style;

        // Dismiss button
        dismissButton.href = '#';
        dismissButton.innerHTML = "Yeah, Ok";

        // Dismiss button style
        dismissButtonStyle.background = "#EE5555";
        dismissButtonStyle.color = "#111111";
        dismissButtonStyle['text-decoration'] = 'none';
        dismissButtonStyle.display = 'inline-block';
        dismissButtonStyle.padding = '0 15px';
        dismissButtonStyle.margin = '0 0 0 10px';

        // Dismiss button click event
        dismissButton.addEventListener('click', function (e) {
            e.preventDefault();
            var now = new Date(),
            cookieExpire = new Date();
            cookieExpire.setTime(now.getTime() + 30 * 60 * 1000 * 60 * 24);
            document.cookie = "harshpCookieConsent=1; expires=" + cookieExpire.toUTCString() + ";domain=.harshp.com;path=/;";

            notice.style.opacity = 1;
            (function fade() {
                (notice.style.opacity -= .1) < 0.01 ? document.body.removeChild(notice) : setTimeout(fade, 40)
            })();
        });

        // Append notice to the DOM
        document.body.appendChild(notice).appendChild(dismissButton);

    };

    /* test-code */
    cookieNoticeJS.clearInstance = function () {
        instance = undefined;
    };
    /* end-test-code */

}());