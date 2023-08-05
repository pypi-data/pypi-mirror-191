/*!
 * Font Awesome Free 6.2.0 by @fontawesome - https://fontawesome.com
 * License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License)
 * Copyright 2022 Fonticons, Inc.
 */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global['fontawesome-free-shims'] = factory());
}(this, (function () { 'use strict';

  var _WINDOW = {};
  var _DOCUMENT = {};

  try {
    if (typeof window !== 'undefined') _WINDOW = window;
    if (typeof document !== 'undefined') _DOCUMENT = document;
  } catch (e) {}

  var _ref = _WINDOW.navigator || {},
      _ref$userAgent = _ref.userAgent,
      userAgent = _ref$userAgent === void 0 ? '' : _ref$userAgent;
  var WINDOW = _WINDOW;
  var DOCUMENT = _DOCUMENT;
  var IS_BROWSER = !!WINDOW.document;
  var IS_DOM = !!DOCUMENT.documentElement && !!DOCUMENT.head && typeof DOCUMENT.addEventListener === 'function' && typeof DOCUMENT.createElement === 'function';
  var IS_IE = ~userAgent.indexOf('MSIE') || ~userAgent.indexOf('Trident/');

  function _defineProperty(obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }

    return obj;
  }

  function _toConsumableArray(arr) {
    return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread();
  }

  function _arrayWithoutHoles(arr) {
    if (Array.isArray(arr)) return _arrayLikeToArray(arr);
  }

  function _iterableToArray(iter) {
    if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter);
  }

  function _unsupportedIterableToArray(o, minLen) {
    if (!o) return;
    if (typeof o === "string") return _arrayLikeToArray(o, minLen);
    var n = Object.prototype.toString.call(o).slice(8, -1);
    if (n === "Object" && o.constructor) n = o.constructor.name;
    if (n === "Map" || n === "Set") return Array.from(o);
    if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen);
  }

  function _arrayLikeToArray(arr, len) {
    if (len == null || len > arr.length) len = arr.length;

    for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i];

    return arr2;
  }

  function _nonIterableSpread() {
    throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
  }

  var _familyProxy, _familyProxy2, _familyProxy3, _familyProxy4, _familyProxy5;

  var NAMESPACE_IDENTIFIER = '___FONT_AWESOME___';
  var PRODUCTION = function () {
    try {
      return process.env.NODE_ENV === 'production';
    } catch (e) {
      return false;
    }
  }();
  var FAMILY_CLASSIC = 'classic';
  var FAMILY_SHARP = 'sharp';
  var FAMILIES = [FAMILY_CLASSIC, FAMILY_SHARP];

  function familyProxy(obj) {
    // Defaults to the classic family if family is not available
    return new Proxy(obj, {
      get: function get(target, prop) {
        return prop in target ? target[prop] : target[FAMILY_CLASSIC];
      }
    });
  }
  var PREFIX_TO_STYLE = familyProxy((_familyProxy = {}, _defineProperty(_familyProxy, FAMILY_CLASSIC, {
    'fa': 'solid',
    'fas': 'solid',
    'fa-solid': 'solid',
    'far': 'regular',
    'fa-regular': 'regular',
    'fal': 'light',
    'fa-light': 'light',
    'fat': 'thin',
    'fa-thin': 'thin',
    'fad': 'duotone',
    'fa-duotone': 'duotone',
    'fab': 'brands',
    'fa-brands': 'brands',
    'fak': 'kit',
    'fa-kit': 'kit'
  }), _defineProperty(_familyProxy, FAMILY_SHARP, {
    'fa': 'solid',
    'fass': 'solid',
    'fa-solid': 'solid'
  }), _familyProxy));
  var STYLE_TO_PREFIX = familyProxy((_familyProxy2 = {}, _defineProperty(_familyProxy2, FAMILY_CLASSIC, {
    'solid': 'fas',
    'regular': 'far',
    'light': 'fal',
    'thin': 'fat',
    'duotone': 'fad',
    'brands': 'fab',
    'kit': 'fak'
  }), _defineProperty(_familyProxy2, FAMILY_SHARP, {
    'solid': 'fass'
  }), _familyProxy2));
  var PREFIX_TO_LONG_STYLE = familyProxy((_familyProxy3 = {}, _defineProperty(_familyProxy3, FAMILY_CLASSIC, {
    'fab': 'fa-brands',
    'fad': 'fa-duotone',
    'fak': 'fa-kit',
    'fal': 'fa-light',
    'far': 'fa-regular',
    'fas': 'fa-solid',
    'fat': 'fa-thin'
  }), _defineProperty(_familyProxy3, FAMILY_SHARP, {
    'fass': 'fa-solid'
  }), _familyProxy3));
  var LONG_STYLE_TO_PREFIX = familyProxy((_familyProxy4 = {}, _defineProperty(_familyProxy4, FAMILY_CLASSIC, {
    'fa-brands': 'fab',
    'fa-duotone': 'fad',
    'fa-kit': 'fak',
    'fa-light': 'fal',
    'fa-regular': 'far',
    'fa-solid': 'fas',
    'fa-thin': 'fat'
  }), _defineProperty(_familyProxy4, FAMILY_SHARP, {
    'fa-solid': 'fass'
  }), _familyProxy4));
  // TODO: do we need to handle font-weight for kit SVG pseudo-elements?

  var FONT_WEIGHT_TO_PREFIX = familyProxy((_familyProxy5 = {}, _defineProperty(_familyProxy5, FAMILY_CLASSIC, {
    '900': 'fas',
    '400': 'far',
    'normal': 'far',
    '300': 'fal',
    '100': 'fat'
  }), _defineProperty(_familyProxy5, FAMILY_SHARP, {
    '900': 'fass'
  }), _familyProxy5));
  var oneToTen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  var oneToTwenty = oneToTen.concat([11, 12, 13, 14, 15, 16, 17, 18, 19, 20]);
  var DUOTONE_CLASSES = {
    GROUP: 'duotone-group',
    SWAP_OPACITY: 'swap-opacity',
    PRIMARY: 'primary',
    SECONDARY: 'secondary'
  };
  var prefixes = new Set();
  Object.keys(STYLE_TO_PREFIX[FAMILY_CLASSIC]).map(prefixes.add.bind(prefixes));
  Object.keys(STYLE_TO_PREFIX[FAMILY_SHARP]).map(prefixes.add.bind(prefixes));
  var RESERVED_CLASSES = [].concat(FAMILIES, _toConsumableArray(prefixes), ['2xs', 'xs', 'sm', 'lg', 'xl', '2xl', 'beat', 'border', 'fade', 'beat-fade', 'bounce', 'flip-both', 'flip-horizontal', 'flip-vertical', 'flip', 'fw', 'inverse', 'layers-counter', 'layers-text', 'layers', 'li', 'pull-left', 'pull-right', 'pulse', 'rotate-180', 'rotate-270', 'rotate-90', 'rotate-by', 'shake', 'spin-pulse', 'spin-reverse', 'spin', 'stack-1x', 'stack-2x', 'stack', 'ul', DUOTONE_CLASSES.GROUP, DUOTONE_CLASSES.SWAP_OPACITY, DUOTONE_CLASSES.PRIMARY, DUOTONE_CLASSES.SECONDARY]).concat(oneToTen.map(function (n) {
    return "".concat(n, "x");
  })).concat(oneToTwenty.map(function (n) {
    return "w-".concat(n);
  }));

  function bunker(fn) {
    try {
      for (var _len = arguments.length, args = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
        args[_key - 1] = arguments[_key];
      }

      fn.apply(void 0, args);
    } catch (e) {
      if (!PRODUCTION) {
        throw e;
      }
    }
  }

  var w = WINDOW || {};
  if (!w[NAMESPACE_IDENTIFIER]) w[NAMESPACE_IDENTIFIER] = {};
  if (!w[NAMESPACE_IDENTIFIER].styles) w[NAMESPACE_IDENTIFIER].styles = {};
  if (!w[NAMESPACE_IDENTIFIER].hooks) w[NAMESPACE_IDENTIFIER].hooks = {};
  if (!w[NAMESPACE_IDENTIFIER].shims) w[NAMESPACE_IDENTIFIER].shims = [];
  var namespace = w[NAMESPACE_IDENTIFIER];

  var shims = [["glass", null, "martini-glass-empty"], ["envelope-o", "far", "envelope"], ["star-o", "far", "star"], ["remove", null, "xmark"], ["close", null, "xmark"], ["gear", null, "gear"], ["trash-o", "far", "trash-can"], ["home", null, "house"], ["file-o", "far", "file"], ["clock-o", "far", "clock"], ["arrow-circle-o-down", "far", "circle-down"], ["arrow-circle-o-up", "far", "circle-up"], ["play-circle-o", "far", "circle-play"], ["repeat", null, "arrow-rotate-right"], ["rotate-right", null, "arrow-rotate-right"], ["refresh", null, "arrows-rotate"], ["list-alt", "far", "rectangle-list"], ["dedent", null, "outdent"], ["video-camera", null, "video"], ["picture-o", "far", "image"], ["photo", "far", "image"], ["image", "far", "image"], ["map-marker", null, "location-dot"], ["pencil-square-o", "far", "pen-to-square"], ["edit", "far", "pen-to-square"], ["share-square-o", null, "share-from-square"], ["check-square-o", "far", "square-check"], ["arrows", null, "up-down-left-right"], ["times-circle-o", "far", "circle-xmark"], ["check-circle-o", "far", "circle-check"], ["mail-forward", null, "share"], ["expand", null, "up-right-and-down-left-from-center"], ["compress", null, "down-left-and-up-right-to-center"], ["eye", "far", null], ["eye-slash", "far", null], ["warning", null, "triangle-exclamation"], ["calendar", null, "calendar-days"], ["arrows-v", null, "up-down"], ["arrows-h", null, "left-right"], ["bar-chart", null, "chart-column"], ["bar-chart-o", null, "chart-column"], ["twitter-square", "fab", "square-twitter"], ["facebook-square", "fab", "square-facebook"], ["gears", null, "gears"], ["thumbs-o-up", "far", "thumbs-up"], ["thumbs-o-down", "far", "thumbs-down"], ["heart-o", "far", "heart"], ["sign-out", null, "right-from-bracket"], ["linkedin-square", "fab", "linkedin"], ["thumb-tack", null, "thumbtack"], ["external-link", null, "up-right-from-square"], ["sign-in", null, "right-to-bracket"], ["github-square", "fab", "square-github"], ["lemon-o", "far", "lemon"], ["square-o", "far", "square"], ["bookmark-o", "far", "bookmark"], ["twitter", "fab", null], ["facebook", "fab", "facebook-f"], ["facebook-f", "fab", "facebook-f"], ["github", "fab", null], ["credit-card", "far", null], ["feed", null, "rss"], ["hdd-o", "far", "hard-drive"], ["hand-o-right", "far", "hand-point-right"], ["hand-o-left", "far", "hand-point-left"], ["hand-o-up", "far", "hand-point-up"], ["hand-o-down", "far", "hand-point-down"], ["globe", null, "earth-americas"], ["tasks", null, "bars-progress"], ["arrows-alt", null, "maximize"], ["group", null, "users"], ["chain", null, "link"], ["cut", null, "scissors"], ["files-o", "far", "copy"], ["floppy-o", "far", "floppy-disk"], ["save", "far", "floppy-disk"], ["navicon", null, "bars"], ["reorder", null, "bars"], ["magic", null, "wand-magic-sparkles"], ["pinterest", "fab", null], ["pinterest-square", "fab", "square-pinterest"], ["google-plus-square", "fab", "square-google-plus"], ["google-plus", "fab", "google-plus-g"], ["money", null, "money-bill-1"], ["unsorted", null, "sort"], ["sort-desc", null, "sort-down"], ["sort-asc", null, "sort-up"], ["linkedin", "fab", "linkedin-in"], ["rotate-left", null, "arrow-rotate-left"], ["legal", null, "gavel"], ["tachometer", null, "gauge-high"], ["dashboard", null, "gauge-high"], ["comment-o", "far", "comment"], ["comments-o", "far", "comments"], ["flash", null, "bolt"], ["clipboard", null, "paste"], ["lightbulb-o", "far", "lightbulb"], ["exchange", null, "right-left"], ["cloud-download", null, "cloud-arrow-down"], ["cloud-upload", null, "cloud-arrow-up"], ["bell-o", "far", "bell"], ["cutlery", null, "utensils"], ["file-text-o", "far", "file-lines"], ["building-o", "far", "building"], ["hospital-o", "far", "hospital"], ["tablet", null, "tablet-screen-button"], ["mobile", null, "mobile-screen-button"], ["mobile-phone", null, "mobile-screen-button"], ["circle-o", "far", "circle"], ["mail-reply", null, "reply"], ["github-alt", "fab", null], ["folder-o", "far", "folder"], ["folder-open-o", "far", "folder-open"], ["smile-o", "far", "face-smile"], ["frown-o", "far", "face-frown"], ["meh-o", "far", "face-meh"], ["keyboard-o", "far", "keyboard"], ["flag-o", "far", "flag"], ["mail-reply-all", null, "reply-all"], ["star-half-o", "far", "star-half-stroke"], ["star-half-empty", "far", "star-half-stroke"], ["star-half-full", "far", "star-half-stroke"], ["code-fork", null, "code-branch"], ["chain-broken", null, "link-slash"], ["unlink", null, "link-slash"], ["calendar-o", "far", "calendar"], ["maxcdn", "fab", null], ["html5", "fab", null], ["css3", "fab", null], ["unlock-alt", null, "unlock"], ["minus-square-o", "far", "square-minus"], ["level-up", null, "turn-up"], ["level-down", null, "turn-down"], ["pencil-square", null, "square-pen"], ["external-link-square", null, "square-up-right"], ["compass", "far", null], ["caret-square-o-down", "far", "square-caret-down"], ["toggle-down", "far", "square-caret-down"], ["caret-square-o-up", "far", "square-caret-up"], ["toggle-up", "far", "square-caret-up"], ["caret-square-o-right", "far", "square-caret-right"], ["toggle-right", "far", "square-caret-right"], ["eur", null, "euro-sign"], ["euro", null, "euro-sign"], ["gbp", null, "sterling-sign"], ["usd", null, "dollar-sign"], ["dollar", null, "dollar-sign"], ["inr", null, "indian-rupee-sign"], ["rupee", null, "indian-rupee-sign"], ["jpy", null, "yen-sign"], ["cny", null, "yen-sign"], ["rmb", null, "yen-sign"], ["yen", null, "yen-sign"], ["rub", null, "ruble-sign"], ["ruble", null, "ruble-sign"], ["rouble", null, "ruble-sign"], ["krw", null, "won-sign"], ["won", null, "won-sign"], ["btc", "fab", null], ["bitcoin", "fab", "btc"], ["file-text", null, "file-lines"], ["sort-alpha-asc", null, "arrow-down-a-z"], ["sort-alpha-desc", null, "arrow-down-z-a"], ["sort-amount-asc", null, "arrow-down-short-wide"], ["sort-amount-desc", null, "arrow-down-wide-short"], ["sort-numeric-asc", null, "arrow-down-1-9"], ["sort-numeric-desc", null, "arrow-down-9-1"], ["youtube-square", "fab", "square-youtube"], ["youtube", "fab", null], ["xing", "fab", null], ["xing-square", "fab", "square-xing"], ["youtube-play", "fab", "youtube"], ["dropbox", "fab", null], ["stack-overflow", "fab", null], ["instagram", "fab", null], ["flickr", "fab", null], ["adn", "fab", null], ["bitbucket", "fab", null], ["bitbucket-square", "fab", "bitbucket"], ["tumblr", "fab", null], ["tumblr-square", "fab", "square-tumblr"], ["long-arrow-down", null, "down-long"], ["long-arrow-up", null, "up-long"], ["long-arrow-left", null, "left-long"], ["long-arrow-right", null, "right-long"], ["apple", "fab", null], ["windows", "fab", null], ["android", "fab", null], ["linux", "fab", null], ["dribbble", "fab", null], ["skype", "fab", null], ["foursquare", "fab", null], ["trello", "fab", null], ["gratipay", "fab", null], ["gittip", "fab", "gratipay"], ["sun-o", "far", "sun"], ["moon-o", "far", "moon"], ["vk", "fab", null], ["weibo", "fab", null], ["renren", "fab", null], ["pagelines", "fab", null], ["stack-exchange", "fab", null], ["arrow-circle-o-right", "far", "circle-right"], ["arrow-circle-o-left", "far", "circle-left"], ["caret-square-o-left", "far", "square-caret-left"], ["toggle-left", "far", "square-caret-left"], ["dot-circle-o", "far", "circle-dot"], ["vimeo-square", "fab", "square-vimeo"], ["try", null, "turkish-lira-sign"], ["turkish-lira", null, "turkish-lira-sign"], ["plus-square-o", "far", "square-plus"], ["slack", "fab", null], ["wordpress", "fab", null], ["openid", "fab", null], ["institution", null, "building-columns"], ["bank", null, "building-columns"], ["mortar-board", null, "graduation-cap"], ["yahoo", "fab", null], ["google", "fab", null], ["reddit", "fab", null], ["reddit-square", "fab", "square-reddit"], ["stumbleupon-circle", "fab", null], ["stumbleupon", "fab", null], ["delicious", "fab", null], ["digg", "fab", null], ["pied-piper-pp", "fab", null], ["pied-piper-alt", "fab", null], ["drupal", "fab", null], ["joomla", "fab", null], ["behance", "fab", null], ["behance-square", "fab", "square-behance"], ["steam", "fab", null], ["steam-square", "fab", "square-steam"], ["automobile", null, "car"], ["cab", null, "taxi"], ["spotify", "fab", null], ["deviantart", "fab", null], ["soundcloud", "fab", null], ["file-pdf-o", "far", "file-pdf"], ["file-word-o", "far", "file-word"], ["file-excel-o", "far", "file-excel"], ["file-powerpoint-o", "far", "file-powerpoint"], ["file-image-o", "far", "file-image"], ["file-photo-o", "far", "file-image"], ["file-picture-o", "far", "file-image"], ["file-archive-o", "far", "file-zipper"], ["file-zip-o", "far", "file-zipper"], ["file-audio-o", "far", "file-audio"], ["file-sound-o", "far", "file-audio"], ["file-video-o", "far", "file-video"], ["file-movie-o", "far", "file-video"], ["file-code-o", "far", "file-code"], ["vine", "fab", null], ["codepen", "fab", null], ["jsfiddle", "fab", null], ["life-bouy", null, "life-ring"], ["life-buoy", null, "life-ring"], ["life-saver", null, "life-ring"], ["support", null, "life-ring"], ["circle-o-notch", null, "circle-notch"], ["rebel", "fab", null], ["ra", "fab", "rebel"], ["resistance", "fab", "rebel"], ["empire", "fab", null], ["ge", "fab", "empire"], ["git-square", "fab", "square-git"], ["git", "fab", null], ["hacker-news", "fab", null], ["y-combinator-square", "fab", "hacker-news"], ["yc-square", "fab", "hacker-news"], ["tencent-weibo", "fab", null], ["qq", "fab", null], ["weixin", "fab", null], ["wechat", "fab", "weixin"], ["send", null, "paper-plane"], ["paper-plane-o", "far", "paper-plane"], ["send-o", "far", "paper-plane"], ["circle-thin", "far", "circle"], ["header", null, "heading"], ["futbol-o", "far", "futbol"], ["soccer-ball-o", "far", "futbol"], ["slideshare", "fab", null], ["twitch", "fab", null], ["yelp", "fab", null], ["newspaper-o", "far", "newspaper"], ["paypal", "fab", null], ["google-wallet", "fab", null], ["cc-visa", "fab", null], ["cc-mastercard", "fab", null], ["cc-discover", "fab", null], ["cc-amex", "fab", null], ["cc-paypal", "fab", null], ["cc-stripe", "fab", null], ["bell-slash-o", "far", "bell-slash"], ["trash", null, "trash-can"], ["copyright", "far", null], ["eyedropper", null, "eye-dropper"], ["area-chart", null, "chart-area"], ["pie-chart", null, "chart-pie"], ["line-chart", null, "chart-line"], ["lastfm", "fab", null], ["lastfm-square", "fab", "square-lastfm"], ["ioxhost", "fab", null], ["angellist", "fab", null], ["cc", "far", "closed-captioning"], ["ils", null, "shekel-sign"], ["shekel", null, "shekel-sign"], ["sheqel", null, "shekel-sign"], ["buysellads", "fab", null], ["connectdevelop", "fab", null], ["dashcube", "fab", null], ["forumbee", "fab", null], ["leanpub", "fab", null], ["sellsy", "fab", null], ["shirtsinbulk", "fab", null], ["simplybuilt", "fab", null], ["skyatlas", "fab", null], ["diamond", "far", "gem"], ["transgender", null, "mars-and-venus"], ["intersex", null, "mars-and-venus"], ["transgender-alt", null, "transgender"], ["facebook-official", "fab", "facebook"], ["pinterest-p", "fab", null], ["whatsapp", "fab", null], ["hotel", null, "bed"], ["viacoin", "fab", null], ["medium", "fab", null], ["y-combinator", "fab", null], ["yc", "fab", "y-combinator"], ["optin-monster", "fab", null], ["opencart", "fab", null], ["expeditedssl", "fab", null], ["battery-4", null, "battery-full"], ["battery", null, "battery-full"], ["battery-3", null, "battery-three-quarters"], ["battery-2", null, "battery-half"], ["battery-1", null, "battery-quarter"], ["battery-0", null, "battery-empty"], ["object-group", "far", null], ["object-ungroup", "far", null], ["sticky-note-o", "far", "note-sticky"], ["cc-jcb", "fab", null], ["cc-diners-club", "fab", null], ["clone", "far", null], ["hourglass-o", null, "hourglass"], ["hourglass-1", null, "hourglass-start"], ["hourglass-2", null, "hourglass-half"], ["hourglass-3", null, "hourglass-end"], ["hand-rock-o", "far", "hand-back-fist"], ["hand-grab-o", "far", "hand-back-fist"], ["hand-paper-o", "far", "hand"], ["hand-stop-o", "far", "hand"], ["hand-scissors-o", "far", "hand-scissors"], ["hand-lizard-o", "far", "hand-lizard"], ["hand-spock-o", "far", "hand-spock"], ["hand-pointer-o", "far", "hand-pointer"], ["hand-peace-o", "far", "hand-peace"], ["registered", "far", null], ["creative-commons", "fab", null], ["gg", "fab", null], ["gg-circle", "fab", null], ["odnoklassniki", "fab", null], ["odnoklassniki-square", "fab", "square-odnoklassniki"], ["get-pocket", "fab", null], ["wikipedia-w", "fab", null], ["safari", "fab", null], ["chrome", "fab", null], ["firefox", "fab", null], ["opera", "fab", null], ["internet-explorer", "fab", null], ["television", null, "tv"], ["contao", "fab", null], ["500px", "fab", null], ["amazon", "fab", null], ["calendar-plus-o", "far", "calendar-plus"], ["calendar-minus-o", "far", "calendar-minus"], ["calendar-times-o", "far", "calendar-xmark"], ["calendar-check-o", "far", "calendar-check"], ["map-o", "far", "map"], ["commenting", null, "comment-dots"], ["commenting-o", "far", "comment-dots"], ["houzz", "fab", null], ["vimeo", "fab", "vimeo-v"], ["black-tie", "fab", null], ["fonticons", "fab", null], ["reddit-alien", "fab", null], ["edge", "fab", null], ["credit-card-alt", null, "credit-card"], ["codiepie", "fab", null], ["modx", "fab", null], ["fort-awesome", "fab", null], ["usb", "fab", null], ["product-hunt", "fab", null], ["mixcloud", "fab", null], ["scribd", "fab", null], ["pause-circle-o", "far", "circle-pause"], ["stop-circle-o", "far", "circle-stop"], ["bluetooth", "fab", null], ["bluetooth-b", "fab", null], ["gitlab", "fab", null], ["wpbeginner", "fab", null], ["wpforms", "fab", null], ["envira", "fab", null], ["wheelchair-alt", "fab", "accessible-icon"], ["question-circle-o", "far", "circle-question"], ["volume-control-phone", null, "phone-volume"], ["asl-interpreting", null, "hands-asl-interpreting"], ["deafness", null, "ear-deaf"], ["hard-of-hearing", null, "ear-deaf"], ["glide", "fab", null], ["glide-g", "fab", null], ["signing", null, "hands"], ["viadeo", "fab", null], ["viadeo-square", "fab", "square-viadeo"], ["snapchat", "fab", null], ["snapchat-ghost", "fab", "snapchat"], ["snapchat-square", "fab", "square-snapchat"], ["pied-piper", "fab", null], ["first-order", "fab", null], ["yoast", "fab", null], ["themeisle", "fab", null], ["google-plus-official", "fab", "google-plus"], ["google-plus-circle", "fab", "google-plus"], ["font-awesome", "fab", null], ["fa", "fab", "font-awesome"], ["handshake-o", "far", "handshake"], ["envelope-open-o", "far", "envelope-open"], ["linode", "fab", null], ["address-book-o", "far", "address-book"], ["vcard", null, "address-card"], ["address-card-o", "far", "address-card"], ["vcard-o", "far", "address-card"], ["user-circle-o", "far", "circle-user"], ["user-o", "far", "user"], ["id-badge", "far", null], ["drivers-license", null, "id-card"], ["id-card-o", "far", "id-card"], ["drivers-license-o", "far", "id-card"], ["quora", "fab", null], ["free-code-camp", "fab", null], ["telegram", "fab", null], ["thermometer-4", null, "temperature-full"], ["thermometer", null, "temperature-full"], ["thermometer-3", null, "temperature-three-quarters"], ["thermometer-2", null, "temperature-half"], ["thermometer-1", null, "temperature-quarter"], ["thermometer-0", null, "temperature-empty"], ["bathtub", null, "bath"], ["s15", null, "bath"], ["window-maximize", "far", null], ["window-restore", "far", null], ["times-rectangle", null, "rectangle-xmark"], ["window-close-o", "far", "rectangle-xmark"], ["times-rectangle-o", "far", "rectangle-xmark"], ["bandcamp", "fab", null], ["grav", "fab", null], ["etsy", "fab", null], ["imdb", "fab", null], ["ravelry", "fab", null], ["eercast", "fab", "sellcast"], ["snowflake-o", "far", "snowflake"], ["superpowers", "fab", null], ["wpexplorer", "fab", null], ["meetup", "fab", null], [61440, "fas", "martini-glass-empty"], [61443, "far", "envelope"], [61446, "far", "star"], [61460, "far", "trash-can"], [61462, "far", "file"], [61463, "far", "clock"], [61466, "far", "circle-down"], [61467, "far", "circle-up"], [61469, "far", "circle-play"], [61470, "fas", "arrow-rotate-right"], [61474, "far", "rectangle-list"], [61502, "far", "image"], [61505, "fas", "location-dot"], [61508, "far", "pen-to-square"], [61509, "fas", "share-from-square"], [61510, "far", "square-check"], [61511, "fas", "up-down-left-right"], [61532, "far", "circle-xmark"], [61533, "far", "circle-check"], [61541, "fas", "up-right-and-down-left-from-center"], [61542, "fas", "down-left-and-up-right-to-center"], [61550, "far", "eye"], [61552, "far", "eye-slash"], [61555, "fas", "calendar-days"], [61565, "fas", "up-down"], [61566, "fas", "left-right"], [61568, "fas", "chart-column"], [61569, "fab", "square-twitter"], [61570, "fab", "square-facebook"], [61575, "far", "thumbs-up"], [61576, "far", "thumbs-down"], [61578, "far", "heart"], [61579, "fas", "right-from-bracket"], [61580, "fab", "linkedin"], [61582, "fas", "up-right-from-square"], [61584, "fas", "right-to-bracket"], [61586, "fab", "square-github"], [61588, "far", "lemon"], [61590, "far", "square"], [61591, "far", "bookmark"], [61593, "fab", "twitter"], [61594, "fab", "facebook-f"], [61595, "fab", "github"], [61597, "far", "credit-card"], [61600, "far", "hard-drive"], [61604, "far", "hand-point-right"], [61605, "far", "hand-point-left"], [61606, "far", "hand-point-up"], [61607, "far", "hand-point-down"], [61612, "fas", "earth-americas"], [61614, "fas", "bars-progress"], [61618, "fas", "maximize"], [61632, "fas", "users"], [61637, "far", "copy"], [61639, "far", "floppy-disk"], [61641, "fas", "bars"], [61648, "fas", "wand-magic-sparkles"], [61650, "fab", "pinterest"], [61651, "fab", "square-pinterest"], [61652, "fab", "square-google-plus"], [61653, "fab", "google-plus-g"], [61654, "fas", "money-bill-1"], [61665, "fab", "linkedin-in"], [61666, "fas", "arrow-rotate-left"], [61668, "fas", "gauge-high"], [61669, "far", "comment"], [61670, "far", "comments"], [61671, "fas", "bolt"], [61674, "fas", "paste"], [61675, "far", "lightbulb"], [61676, "fas", "right-left"], [61602, "far", "bell"], [61685, "fas", "utensils"], [61686, "far", "file-lines"], [61687, "far", "building"], [61688, "far", "hospital"], [61706, "fas", "tablet-screen-button"], [61707, "fas", "mobile-screen-button"], [61708, "far", "circle"], [61714, "fas", "reply"], [61715, "fab", "github-alt"], [61716, "far", "folder"], [61717, "far", "folder-open"], [61720, "far", "face-smile"], [61721, "far", "face-frown"], [61722, "far", "face-meh"], [61724, "far", "keyboard"], [61725, "far", "flag"], [61731, "far", "star-half-stroke"], [61734, "fas", "code-branch"], [61747, "far", "calendar"], [61750, "fab", "maxcdn"], [61755, "fab", "html5"], [61756, "fab", "css3"], [61758, "fas", "unlock"], [61767, "far", "square-minus"], [61768, "fas", "turn-up"], [61769, "fas", "turn-down"], [61772, "fas", "square-up-right"], [61774, "far", "compass"], [61776, "far", "square-caret-down"], [61777, "far", "square-caret-up"], [61778, "far", "square-caret-right"], [61781, "fas", "dollar-sign"], [61782, "fas", "indian-rupee-sign"], [61786, "fab", "btc"], [61790, "fas", "arrow-down-z-a"], [61792, "fas", "arrow-down-short-wide"], [61793, "fas", "arrow-down-wide-short"], [61795, "fas", "arrow-down-9-1"], [61798, "fab", "square-youtube"], [61799, "fab", "youtube"], [61800, "fab", "xing"], [61801, "fab", "square-xing"], [61802, "fab", "youtube"], [61803, "fab", "dropbox"], [61804, "fab", "stack-overflow"], [61805, "fab", "instagram"], [61806, "fab", "flickr"], [61808, "fab", "adn"], [61809, "fab", "bitbucket"], [61810, "fab", "bitbucket"], [61811, "fab", "tumblr"], [61812, "fab", "square-tumblr"], [61813, "fas", "down-long"], [61814, "fas", "up-long"], [61815, "fas", "left-long"], [61816, "fas", "right-long"], [61817, "fab", "apple"], [61818, "fab", "windows"], [61819, "fab", "android"], [61820, "fab", "linux"], [61821, "fab", "dribbble"], [61822, "fab", "skype"], [61824, "fab", "foursquare"], [61825, "fab", "trello"], [61828, "fab", "gratipay"], [61829, "far", "sun"], [61830, "far", "moon"], [61833, "fab", "vk"], [61834, "fab", "weibo"], [61835, "fab", "renren"], [61836, "fab", "pagelines"], [61837, "fab", "stack-exchange"], [61838, "far", "circle-right"], [61840, "far", "circle-left"], [61841, "far", "square-caret-left"], [61842, "far", "circle-dot"], [61844, "fab", "square-vimeo"], [61845, "fas", "turkish-lira-sign"], [61846, "far", "square-plus"], [61848, "fab", "slack"], [61850, "fab", "wordpress"], [61851, "fab", "openid"], [61854, "fab", "yahoo"], [61856, "fab", "google"], [61857, "fab", "reddit"], [61858, "fab", "square-reddit"], [61859, "fab", "stumbleupon-circle"], [61860, "fab", "stumbleupon"], [61861, "fab", "delicious"], [61862, "fab", "digg"], [61863, "fab", "pied-piper-pp"], [61864, "fab", "pied-piper-alt"], [61865, "fab", "drupal"], [61866, "fab", "joomla"], [61876, "fab", "behance"], [61877, "fab", "square-behance"], [61878, "fab", "steam"], [61879, "fab", "square-steam"], [61884, "fab", "spotify"], [61885, "fab", "deviantart"], [61886, "fab", "soundcloud"], [61889, "far", "file-pdf"], [61890, "far", "file-word"], [61891, "far", "file-excel"], [61892, "far", "file-powerpoint"], [61893, "far", "file-image"], [61894, "far", "file-zipper"], [61895, "far", "file-audio"], [61896, "far", "file-video"], [61897, "far", "file-code"], [61898, "fab", "vine"], [61899, "fab", "codepen"], [61900, "fab", "jsfiddle"], [61901, "fas", "life-ring"], [61902, "fas", "circle-notch"], [61904, "fab", "rebel"], [61905, "fab", "empire"], [61906, "fab", "square-git"], [61907, "fab", "git"], [61908, "fab", "hacker-news"], [61909, "fab", "tencent-weibo"], [61910, "fab", "qq"], [61911, "fab", "weixin"], [61912, "fas", "paper-plane"], [61913, "far", "paper-plane"], [61915, "far", "circle"], [61923, "far", "futbol"], [61927, "fab", "slideshare"], [61928, "fab", "twitch"], [61929, "fab", "yelp"], [61930, "far", "newspaper"], [61933, "fab", "paypal"], [61934, "fab", "google-wallet"], [61936, "fab", "cc-visa"], [61937, "fab", "cc-mastercard"], [61938, "fab", "cc-discover"], [61939, "fab", "cc-amex"], [61940, "fab", "cc-paypal"], [61941, "fab", "cc-stripe"], [61943, "far", "bell-slash"], [61944, "fas", "trash-can"], [61945, "far", "copyright"], [61954, "fab", "lastfm"], [61955, "fab", "square-lastfm"], [61960, "fab", "ioxhost"], [61961, "fab", "angellist"], [61962, "far", "closed-captioning"], [61965, "fab", "buysellads"], [61966, "fab", "connectdevelop"], [61968, "fab", "dashcube"], [61969, "fab", "forumbee"], [61970, "fab", "leanpub"], [61971, "fab", "sellsy"], [61972, "fab", "shirtsinbulk"], [61973, "fab", "simplybuilt"], [61974, "fab", "skyatlas"], [61977, "far", "gem"], [61988, "fas", "mars-and-venus"], [62000, "fab", "facebook"], [62001, "fab", "pinterest-p"], [62002, "fab", "whatsapp"], [62006, "fas", "bed"], [62007, "fab", "viacoin"], [62010, "fab", "medium"], [62011, "fab", "y-combinator"], [62012, "fab", "optin-monster"], [62013, "fab", "opencart"], [62014, "fab", "expeditedssl"], [62016, "fas", "battery-full"], [62017, "fas", "battery-three-quarters"], [62018, "fas", "battery-half"], [62019, "fas", "battery-quarter"], [62023, "far", "object-group"], [62024, "far", "object-ungroup"], [62026, "far", "note-sticky"], [62027, "fab", "cc-jcb"], [62028, "fab", "cc-diners-club"], [62029, "far", "clone"], [62032, "fas", "hourglass"], [62037, "far", "hand-back-fist"], [62038, "far", "hand"], [62039, "far", "hand-scissors"], [62040, "far", "hand-lizard"], [62041, "far", "hand-spock"], [62042, "far", "hand-pointer"], [62043, "far", "hand-peace"], [62045, "far", "registered"], [62046, "fab", "creative-commons"], [62048, "fab", "gg"], [62049, "fab", "gg-circle"], [62051, "fab", "odnoklassniki"], [62052, "fab", "square-odnoklassniki"], [62053, "fab", "get-pocket"], [62054, "fab", "wikipedia-w"], [62055, "fab", "safari"], [62056, "fab", "chrome"], [62057, "fab", "firefox"], [62058, "fab", "opera"], [62059, "fab", "internet-explorer"], [62061, "fab", "contao"], [62062, "fab", "500px"], [62064, "fab", "amazon"], [62065, "far", "calendar-plus"], [62066, "far", "calendar-minus"], [62067, "far", "calendar-xmark"], [62068, "far", "calendar-check"], [62072, "far", "map"], [62074, "fas", "comment-dots"], [62075, "far", "comment-dots"], [62076, "fab", "houzz"], [62077, "fab", "vimeo-v"], [62078, "fab", "black-tie"], [62080, "fab", "fonticons"], [62081, "fab", "reddit-alien"], [62082, "fab", "edge"], [62083, "fas", "credit-card"], [62084, "fab", "codiepie"], [62085, "fab", "modx"], [62086, "fab", "fort-awesome"], [62087, "fab", "usb"], [62088, "fab", "product-hunt"], [62089, "fab", "mixcloud"], [62090, "fab", "scribd"], [62092, "far", "circle-pause"], [62094, "far", "circle-stop"], [62099, "fab", "bluetooth"], [62100, "fab", "bluetooth-b"], [62102, "fab", "gitlab"], [62103, "fab", "wpbeginner"], [62104, "fab", "wpforms"], [62105, "fab", "envira"], [62107, "fab", "accessible-icon"], [62108, "far", "circle-question"], [62117, "fab", "glide"], [62118, "fab", "glide-g"], [62121, "fab", "viadeo"], [62122, "fab", "square-viadeo"], [62123, "fab", "snapchat"], [62124, "fab", "snapchat"], [62125, "fab", "square-snapchat"], [62126, "fab", "pied-piper"], [62128, "fab", "first-order"], [62129, "fab", "yoast"], [62130, "fab", "themeisle"], [62131, "fab", "google-plus"], [62132, "fab", "font-awesome"], [62133, "far", "handshake"], [62135, "far", "envelope-open"], [62136, "fab", "linode"], [62138, "far", "address-book"], [62140, "far", "address-card"], [62142, "far", "circle-user"], [62144, "far", "user"], [62145, "far", "id-badge"], [62147, "far", "id-card"], [62148, "fab", "quora"], [62149, "fab", "free-code-camp"], [62150, "fab", "telegram"], [62151, "fas", "temperature-full"], [62157, "fas", "bath"], [62160, "far", "window-maximize"], [62162, "far", "window-restore"], [62163, "fas", "rectangle-xmark"], [62164, "far", "rectangle-xmark"], [62165, "fab", "bandcamp"], [62166, "fab", "grav"], [62167, "fab", "etsy"], [62168, "fab", "imdb"], [62169, "fab", "ravelry"], [62170, "fab", "sellcast"], [62172, "far", "snowflake"], [62173, "fab", "superpowers"], [62174, "fab", "wpexplorer"], [62176, "fab", "meetup"]];
  bunker(function () {
    if (typeof namespace.hooks.addShims === 'function') {
      namespace.hooks.addShims(shims);
    } else {
      var _namespace$shims;

      (_namespace$shims = namespace.shims).push.apply(_namespace$shims, shims);
    }
  });

  return shims;

})));
