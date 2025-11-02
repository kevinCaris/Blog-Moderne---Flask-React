const API_URL = 'http://localhost:5000';

export const getCommentsAPI = async (postId) => {
  const response = await fetch(`${API_URL}/posts/${postId}/comments`);
  return response.json();
};

export const createCommentAPI = async (articleId, message) => {
  const response = await fetch('/api/comments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ article_id: articleId, message })
  });
  return response.json();
};

export const updateCommentAPI = async (commentId, message) => {
  const response = await fetch(`/api/comments/${commentId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  return response.json();
};

export const deleteCommentAPI = async (commentId) => {
  const response = await fetch(`/api/comments/${commentId}`, {
    method: 'DELETE'
  });
  return response.json();
};