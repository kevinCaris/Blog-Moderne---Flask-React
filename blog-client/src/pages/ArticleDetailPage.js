import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { getPostAPI } from '../api/articlesAPI';
import CommentSection from '../components/CommentSection';

function ArticleDetailPage({ articleId, navigate }) {
  const [article, setArticle] = useState(null);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    loadArticle();
  }, );

  const loadArticle = async () => {
    try {
      const data = await getPostAPI(articleId);
      if (data.success) setArticle(data.post);
    } catch (error) {
      console.error('Erreur lors du chargement de l’article :', error);
    }
  };

  if (!article) return <div className="text-center py-12 text-gray-500">Chargement...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-10">
        <article className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-10">
          <h1 className="text-3xl font-bold text-gray-800 mb-3">
            {article.title}
          </h1>

          <div className="flex flex-wrap items-center text-sm text-gray-500 mb-6">
            <span>👤 Auteur</span>
            <span className="mx-2">•</span>
            <span>📅 {new Date(article.creationDate).toLocaleDateString('fr-FR')}</span>
          </div>

          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap mb-8">
            {article.body}
          </p>

          <button
            onClick={() => navigate('home')}
            className="text-indigo-600 font-medium hover:underline"
          >
            ← Retour aux articles
          </button>
        </article>

        <CommentSection articleId={articleId} />
      </div>
    </div>
  );
}

export default ArticleDetailPage;
