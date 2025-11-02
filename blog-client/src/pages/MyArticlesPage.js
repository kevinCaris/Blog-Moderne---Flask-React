import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { getMyPostsAPI, deletePostAPI } from '../api/articlesAPI';

function MyArticlesPage({ navigate }) {
  const [posts, setPosts] = useState([]);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      const data = await getMyPostsAPI();
      if (data.success) setPosts(data.posts || []);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleDelete = async (postId) => {
    try {
      await deletePostAPI(postId);
      await loadPosts();
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <h1 className="text-4xl font-bold mb-8">Mes articles</h1>
      
      <div className="space-y-4">
        {posts.map(post => (
          <div key={post.id} className="bg-white p-6 rounded shadow">
            <h3 className="text-xl font-bold mb-2">{post.title}</h3>
            <p className="text-gray-600 mb-4">{post.body.substring(0, 100)}...</p>
            <div className="flex gap-2">
              <button onClick={() => navigate('article', post.id)} className="bg-blue-600 text-white px-4 py-2 rounded">
                Voir
              </button>
              <button onClick={() => handleDelete(post.id)} className="bg-red-600 text-white px-4 py-2 rounded">
                Supprimer
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MyArticlesPage;