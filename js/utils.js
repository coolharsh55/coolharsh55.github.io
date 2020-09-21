document.addEventListener('DOMContentLoaded', function () {
    var items = document.getElementsByClassName('timestamp');
    for(var item of items) {
        item.innerHTML = dayjs(item.innerHTML).format("D MMM YY");
    }
}, false);