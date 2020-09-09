$( document ).ready(function() {
    // the language-menu
    var $langContainer = $("#portal-languageselector");
    $langContainer.append("<li class='arrow glyphicon glyphicon-chevron-down'></li>");

    var toggleMenu = function(closeIt) {
        var open = $langContainer.hasClass("open");
        if(!open && closeIt) {
            return;
        }
        $("arrow", $langContainer).toggleClass("glyphicon-chevron-up").toggleClass("glyphicon-chevron-down");
        $langContainer.toggleClass("open");
        $("li:not(.currentLanguage):not(.arrow)", $langContainer).toggle();
    };

    $(".currentLanguage", $langContainer).click(function(e) {
        e.stopPropagation();
        toggleMenu(false);
    });
    $(document).click(function() {
        toggleMenu(true);
    });


    ////////
    // normal navigation doubletab for touchscreens
    var $menu = $('#portal-globalnav-collapse');
    function toggleDoubleTab() {
        var opts = {};
        if (!window.matchMedia("(min-width: 768px)").matches) {
            opts = "destroy";
        }
        $menu.doubleTapToGo(opts);
    }
    toggleDoubleTab();
    window.onresize = toggleDoubleTab;


    ////////
    // mobile navigation
    var $ploneNav = $("ul.plone-nav");
    $ploneNav.find("li button").click(function() {
        var $this = $(this);
        var $submenu = $this.parent().children("ul");

        var closeComplete = {
            complete: function() {
                $(this).css("display", "")
                  .removeClass("open");
            }
        };
        var openComplete = {
            complete: function() {
                $(this).css("display", "")
                  .addClass("open");
            }
        };

        if($this.hasClass("icon-down")) {
            $ploneNav.find("ul").slideUp(closeComplete)
                .siblings("button").addClass("icon-down").removeClass("icon-up");
            $submenu.slideDown(openComplete);
        } else {
            $submenu.slideUp(closeComplete);
        }
        $this.toggleClass("icon-down icon-up");
    });


    // Wrap accordion panels in panel groups
    var tempClass = "currentAccordionGroup";
    var count = 1;
    var accordionCount = 1;
    $("div.panel").each(function(){
        var $this = $(this);

        $(".panel-heading", $this).attr("id", "heading"+count);
        $(".panel-title a", $this).attr("href", "#collapse"+count).attr("aria-controls", "collapse"+count).attr("data-parent", "#accordion"+accordionCount);
        $(".panel-collapse", $this).attr("aria-labelledby", "heading"+count).attr("id", "collapse"+count);

        $this.addClass(tempClass);
        if($this.next("div.panel").length === 0) {
            $("."+tempClass).removeClass(tempClass).wrapAll('<div class="panel-group" id="accordion'+accordionCount+'" role="tablist" aria-multiselectable="true"></div>');
            accordionCount++;
        }

        count++;
    });

    ////////
    // privacy statement handling
    var Cookies = (function ($) {
        "use strict";

        /**
         * Set the cookie with name, value and lifetime in miliseconds
         * @param {string} cname
         * @param {*}      cvalue
         * @param {number} extime
         */
        var set = function (cname, cvalue, extime) {
            try {
                var d = new Date();
                d.setTime(d.getTime() + extime);
                var expires     = "expires=" + d.toUTCString();
                document.cookie = cname + "=" + cvalue + "; path=/;" + expires;
            } catch (err) {
                // User blocked cookies
            }
        };

        /**
         * Return the cookie value by name
         *
         * @param {string} cname
         * @returns {*}
         */
        var get = function (cname) {
            try {
                var name = cname + "=";
                var ca   = document.cookie.split(';');
                for (var i = 0; i < ca.length; i++) {
                    var c = ca[i];
                    while (c.charAt(0) == ' ') c = c.substring(1);
                    if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
                }
                return "";
            } catch (err) {
                return null;
            }
        };

        return {
            "get": get,
            "set": set
        };

    })(jQuery);

    var $privacybar = $("#privacy-statement");

    var COOKIE_NAME = "privacyStatementAcked";
    var COOKIE_LIFETIME = 24 * 60 * 60 * 14; // 2 weeks

    // Test if localStorage is supported;
    // Modernizr test method
    function localStorageSupported() {
        var mod = 'llaLS';
        try {
            localStorage.setItem(mod, mod);
            localStorage.removeItem(mod);
            return true;
        } catch(e) {
            return false;
        }
    }

    (function($) {
        // Cases were we don't want to show the privacyStatement
        if (
            $privacybar.length === 0 ||
            // Browser doesn't support localStorage and Cookies
            (!localStorageSupported() && Cookies.get(COOKIE_NAME) === null) ||
            // Privacy statement previously acknowledged
            (localStorageSupported() && localStorage.getItem(COOKIE_NAME) === "yes") ||
            (Cookies.get(COOKIE_NAME) === "yes")
        ) {
            return false;
        }

        $privacybar.fadeIn();

        $(".close", $privacybar).click(function(event) {
            event.preventDefault();
            event.stopPropagation();
            if (localStorageSupported()) {
                localStorage.setItem(COOKIE_NAME, "yes");
            } else {
                Cookies.set(COOKIE_NAME, "yes", COOKIE_LIFETIME);
            }

            $privacybar.fadeOut();
        });
    })(jQuery);

});
