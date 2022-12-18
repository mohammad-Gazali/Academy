let replyButtons = Array.from(document.querySelectorAll("[data-cid]"));
let hiddenInputComment = document.querySelector('input[name="comment-id"]');
let formRelatedComment = document.querySelector('#form-related-comment');
let formRelatedCommentParagraph = document.querySelector('#form-related-comment p');
let mainCreateCommentForm = document.getElementById("form-create-comment-main")
let closeButton = document.querySelector('.btn-close');


replyButtons.forEach(element => {
    element.onclick = (e) => {
        if (e.target.dataset.cid !== undefined && e.target.dataset.commentText !== undefined) {
            let targetId = e.target.dataset.cid;
            let commentTextString = e.target.dataset.commentText;
            hiddenInputComment.value = targetId;
            formRelatedComment.style.position = "relative";
            formRelatedComment.style.transform = "scale(1)";
            formRelatedCommentParagraph.innerHTML = commentTextString;
            mainCreateCommentForm.scrollIntoView();
        }
    }
});


function sleepTime(ms) {
    return new Promise(
        (resolve, reject) => {
            setTimeout(resolve, ms)
        }
    )
}


closeButton.onclick = async () => {
    hiddenInputComment.value = "";
    formRelatedCommentParagraph.innerHTML = "";
    formRelatedComment.style.transform = "scale(0)";
    await sleepTime(150)
    formRelatedComment.style.position = "absolute";
}
