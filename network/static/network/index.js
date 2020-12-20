document.addEventListener('DOMContentLoaded', function() {
    form_post = document.querySelector('#new-post-form');
    if(form_post!=null){
        form_post.onsubmit = () => create_post();
    }

    edit_button = document.querySelectorAll('#edit-button');
    if(edit_button){
        edit_button.forEach(button => {
            button.addEventListener('click', () =>{
                edit_post(button.dataset.post_id);
            } )
        })
    }

    like_button = document.querySelectorAll('#like-button');
    if(like_button){
        like_button.forEach(button => {
            button.addEventListener('click', event=>like_post(event,button.dataset.post_id))
        });
    }

    follow_button = document.querySelector('.follow-button');
    if(follow_button)
        follow_button.addEventListener('click',()=>follow(follow_button.dataset.user_id))

});

function create_post(){
    fetch('/post', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#post-body').value
        })
      })
      .then(response => response.json())
      .then(result => {
          setTimeout(()=>{
              location.reload();
          },500);
     
          document.querySelector(".alert").classList.remove("d-none");
          setTimeout(() => {
            document.querySelector(".alert").classList.add("d-none");

          }, 3000);
      });
      document.querySelector('#post-body').value = "";
      return false;
}

function like_post(event,post_id){
    like = event.target.firstElementChild; 
    if (like.classList.contains("fas"))
        like.classList.replace("fas" , "far");
    else
        like.classList.replace("far" , "fas");

    console.log(event.target.firstElementChild.classList);

    fetch(`/like/${post_id}`,{
        method:'PUT',
        
    })
    .then(response => response.json())
    .then(result => {
        event.target.lastElementChild.innerText = result['count'];

    })
}

function edit_post(post_id){
    post = document.getElementById(`${post_id}`);
    post.querySelector("#edit-button").classList.add("d-none")
    post.querySelector(".card-body").classList.add("d-none");
    post.querySelector(".edit-form").classList.remove("d-none")
    post.querySelector("#save-button").addEventListener('click', () => {
        
        fetch(`/like/${post_id}`,{
            method:'POST',
            body: JSON.stringify({
                body: post.querySelector("#text-body").value
            })
        })
        .then(response => response.json())
        .then(result => {
            post.querySelector(".card-title").innerText = result["body"];
        })
        post.querySelector("#edit-button").classList.remove("d-none")
        post.querySelector(".card-body").classList.remove("d-none");
        post.querySelector(".edit-form").classList.add("d-none")
    })
}

function follow(userId){
    fetch(`/user/${userId}`,{   
        method:'PUT',
    })
    .then(response => response.json())
    
    .then(result => {
        if(result["following"]){
            follow_button.innerText = "Unfollow";
            document.querySelector(".followers").innerText = `${result["count"]} followers`;
        }
        else{
            follow_button.innerText = "Follow";
            document.querySelector(".followers").innerText = `${result["count"]} followers`;
        }        
    })
}

function force_login() {
    document.getElementById('login').click();
}



