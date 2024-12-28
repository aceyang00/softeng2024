document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-btn');
    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.dataset.id;
            fetch(`/community/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const likeCount = document.getElementById(`like-count-${postId}`);
                        likeCount.textContent = data.likes;

                        if (data.liked) {
                            this.innerHTML = '❤️ 좋아요';
                            this.classList.add('liked');
                        } else {
                            this.innerHTML = '🤍 좋아요';
                            this.classList.remove('liked');
                        }
                    }
                });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
