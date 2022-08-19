function like(questionId){
    const likeCount = document.getElementById(`like-count/${questionId}`);
    const likeButton = document.getElementById(`like-button/${questionId}`);

    fetch(`/like-post/${questionId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = data["likes"];
      if (data["liked"] === true) {
        likeButton.className = "fas fa-thumbs-up";
      } else {
        likeButton.className = "far fa-thumbs-up";
      }
    })
    .catch((e) => alert("Could not like post."));
}
