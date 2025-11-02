import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { getPostsAPI, deletePostAPI } from '../api/articlesAPI';
import PostCard from '../components/PostCard';
import CreatePostForm from '../components/CreatePostForm';

function HomePage({ navigate }) {
  const [posts, setPosts] = useState([]);
  const [view, setView] = useState(localStorage.getItem('view') || 'grid');
  const { user } = useContext(AuthContext);

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      const data = await getPostsAPI();
      if (data.success) setPosts(data.post || []);
    } catch (error) {
      console.error('Erreur lors du chargement des articles:', error);
    }
  };

  const handleDeletePost = async (postId) => {
    try {
      const data = await deletePostAPI(postId);
      if (data.success) await loadPosts();
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const toggleView = (newView) => {
    setView(newView);
    localStorage.setItem('view', newView);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-10">
        <div className="flex flex-col sm:flex-row items-center justify-between mb-10 gap-4">
          <div className="text-center sm:text-left">
            <h1 className="text-4xl font-bold text-gray-800">Mon Blog</h1>
            <p className="text-gray-500">Partagez vos idées et découvrez de nouveaux articles</p>
          </div>

          <div className="flex gap-2 bg-gray-100 rounded-md p-1">
            <button
              onClick={() => toggleView('grid')}
              className={`px-4 py-1.5 rounded-md text-sm font-medium transition ${
                view === 'grid'
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-600 hover:bg-gray-200'
              }`}
            >
              ⬜ Cartes
            </button>
            <button
              onClick={() => toggleView('list')}
              className={`px-4 py-1.5 rounded-md text-sm font-medium transition ${
                view === 'list'
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-600 hover:bg-gray-200'
              }`}
            >
              ☰ Liste
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {user && (
            <div className="lg:col-span-1">
              <CreatePostForm onPostCreated={loadPosts} />
            </div>
          )}

          <div
            className={`lg:col-span-3 ${
              view === 'grid'
                ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4'
                : 'space-y-3'
            }`}
          >
            {posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                onDelete={handleDeletePost}
                isOwner={user && user.id === post.user_id}
                navigate={navigate}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
