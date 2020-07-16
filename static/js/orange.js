
/*
KEY COMPONENTS:
"activeItem" = null until an edit button is clicked. Will contain object of item we are editing
"list_snapshot" = Will contain previous state of list. Used for removing extra rows on list update

PROCESS:
1 - Fetch Data and build rows "buildList()"
2 - Create Item on form submit
3 - Edit Item click - Prefill form and change submit URL
4 - Delete Item - Send item id to delete URL
5 - Cross out completed task - Event handle updated item
NOTES:
-- Add event handlers to "edit", "delete", "title"
-- Render with strike through items completed
-- Remove extra data on re-render
-- CSRF Token
*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
var activeItem = null;


buildList()


function buildList() {
    var wrapper = document.getElementById('list-wrapper')
    wrapper.innerHTML = ''

    var url = "https://rmiaouh.site/api/task-list-orange/"
    fetch(url)
        .then((resp) => resp.json())
        .then(function (data) {
            console.log('Data:', data)

            var list = data
            for (var i in list) {


                var titlespn = `<span class="title">${list[i].message_date}</span>`
                if(list[i].completed == true){
                    titlespn = `<strike class="title">${list[i].message_date}</strike>`
                }
                var item = `
                <div id="data-row-${i}" class="task-wrapper flex-wrapper">
                    <div style="flex:7">
                        ${list[i].output_date}
                    </div>
                    <div style="flex:1">
                        <button class="btn btn-sm btn-outline-danger delete">-</button>
                    </div>
                </div>

            `
                //wrapper.innerHTML += item
                wrapper.insertAdjacentHTML('beforeend', item)
                
                var editBtn = document.getElementsByClassName('edit')[i];
                var deleteBtn = document.getElementsByClassName('delete')[i];
                var titleBtn = document.getElementsByClassName('title')[i];


                deleteBtn.addEventListener('click', (function(item) {
                    return function(){
                        deleteItem(item)

                    }

                })(list[i]))

                
            }
            
        })
        
}

var form = document.getElementById('form-wrapper')
form.addEventListener('submit', function (e) {
    e.preventDefault()
    console.log('Form submitted')
    var url = "https://rmiaouh.site/api/task-orange/"

    if (activeItem != null){
        var url = `https://rmiaouh.site/api/task-update/${activeItem.id}/`
        activeItem = null
    }

    var title = document.getElementById('title').value
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'message_orange': title })
    }).then(function (response) {
        buildList()
        document.getElementById('form').reset()
    })
})


function editItem(item) {
    console.log('item clicked', item)
    activeItem = item
    document.getElementById('title').value = activeItem.title
}


function deleteItem(item) {
    console.log('item click deleted', item)
    fetch(`https://rmiaouh.site/api/task-delete-orange/${item.id}/`, {
        method:'DELETE',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    }).then((response) => {
        buildList()
    })
}


function strikeUnstrike(item){
    console.log('strike clicked')

    item.completed = !item.completed
    fetch(`https://rmiaouh.site/api/task-update/${item.id}/`, {
        method:'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'title': item.title, 'completed': item.completed })
    }).then((response) => {
        buildList()
    })

}