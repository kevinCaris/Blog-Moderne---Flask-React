const API_URL = 'http://localhost:5000';

export const getPostsAPI = async () => {
  const response = await fetch(`${API_URL}/posts`);
  return response.json();
};

export const getPostAPI = async (postId) => {
  const response = await fetch(`${API_URL}/posts/${postId}`);
  return response.json();
};

export const createPostAPI = async (title, body) => {
  const response = await fetch(`${API_URL}/posts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, body })
  });

  const contentType = response.headers.get('content-type');
  if (!contentType || !contentType.includes('application/json')) {
    console.error('Réponse inattendue:', await response.text());
    return { success: false, message: 'Réponse serveur invalide' };
  }

  return response.json();
};

export const updatePostAPI = async (postId, title, body) => {
  const response = await fetch(`${API_URL}/posts/${postId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, body })
  });
  return response.json();
};

export const deletePostAPI = async (postId) => {
  const response = await fetch(`${API_URL}/posts/${postId}`, {
    method: 'DELETE'
  });
  return response.json();
};

export const getMyPostsAPI = async () => {
  const response = await fetch(`${API_URL}/my-posts`);
  return response.json();
};
