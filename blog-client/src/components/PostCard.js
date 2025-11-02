import React from 'react';

function PostCard({ post, onDelete, isOwner, navigate }) {
  return (
    <div className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 overflow-hidden cursor-pointer">
      <div className="h-1 bg-gradient-to-r from-indigo-600 to-indigo-800"></div>
      
      <div className="p-6">
        {isOwner && (
          <div className="inline-block bg-indigo-100 text-indigo-700 text-xs font-bold px-3 py-1 rounded-full mb-3">
            ✍️ C'est toi
          </div>
        )}
        
        <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2 hover:text-indigo-600 transition">
          {post.title}
        </h3>
        
        <p className="text-gray-600 mb-4 line-clamp-3 text-sm">
          {post.body.substring(0, 150)}...
        </p>
        
        <div className="flex justify-between items-center mb-4 pt-4 border-t border-gray-100">
          <small className="text-gray-500 text-xs">📅 {new Date(post.creationDate).toLocaleDateString('fr-FR')}</small>
          <button onClick={() => navigate('article', post.id)} className="text-indigo-600 font-bold text-sm hover:text-indigo-800">
            Lire →
          </button>
        </div>
      </div>
    </div>
  );
}

export default PostCard;