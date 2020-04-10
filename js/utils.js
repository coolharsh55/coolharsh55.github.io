document.addEventListener('DOMContentLoaded', function () {
    var items = document.getElementsByClassName('article-timestamp');
    for(var item of items) {
        item.innerHTML = dayjs(item.innerHTML).format("dddd D MMM YYYY");
    }
}, false);