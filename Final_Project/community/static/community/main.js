document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function () {
        const postId = this.dataset.id;  // 블로그 글 ID
        fetch(`/${postId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',  // CSRF 토큰
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked !== undefined) {
                const likeCount = document.getElementById(`like-count-${postId}`);
                likeCount.textContent = data.total_likes;  // 좋아요 개수 업데이트
                this.textContent = data.liked ? '❤️ 좋아요 취소' : '🤍 좋아요';
            } else if (data.error) {
                alert(data.error);  // 오류 메시지 출력
            }
        })
        .catch(error => console.error('Error:', error));  // 오류 로그 출력
    });
});
