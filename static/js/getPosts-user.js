window.addEventListener("load", function(){
    getPosts();
})

async function getPosts(){
    let response = await fetch('/data')
    let data = await response.json()

    let posts = document.getElementById('posts')
    posts.innerHTML = ""

    for(let post of data){
        var seats = post.seats
        if (seats > 0 ) {
            postsHTML = `<li><div class="list_div"><h1>${post.from_c} - ${post.to_c}</h1><p><b>Travel agency: </b>${post.agency}</p><p><b>Date: </b>${post.start} - ${post.end}</p><p><b>Price: </b>${post.price}€</p><p><b>Total seats: </b>${post.seats}</p></div></li>`
            posts.innerHTML = posts.innerHTML + postsHTML
        } else {
            console.log("")
        }
    }
}