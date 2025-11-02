import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { 
  getCommentsAPI, 
  createCommentAPI, 
  updateCommentAPI, 
  deleteCommentAPI 
} from '../api/commentsAPI';

function CommentSection({ articleId }) {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editingText, setEditingText] = useState('');
  const { user } = useContext(AuthContext);

  useEffect(() => {
    loadComments();
  }, [articleId]);

  const loadComments = async () => {
    try {
      const data = await getCommentsAPI(articleId);
      if (data.success) setComments(data.comments || []);
    } catch (error) {
      console.error('Erreur lors du chargement des commentaires :', error);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    try {
      await createCommentAPI(articleId, newComment);
      setNewComment('');
      await loadComments();
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const handleUpdateComment = async (commentId) => {
    if (!editingText.trim()) return;
    try {
      await updateCommentAPI(commentId, editingText);
      setEditingId(null);
      await loadComments();
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  const handleDeleteComment = async (commentId) => {
    try {
      await deleteCommentAPI(commentId);
      await loadComments();
    } catch (error) {
      console.error('Erreur:', error);
    }
  };

  return (
    <section className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">💬 Commentaires</h2>

      {user ? (
        <form onSubmit={handleAddComment} className="mb-8">
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Écrivez un commentaire..."
            rows="3"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
          />
          <div className="text-right mt-3">
            <button 
              type="submit" 
              className="bg-indigo-600 text-white px-5 py-2 rounded-md hover:bg-indigo-700 transition"
            >
              Envoyer
            </button>
          </div>
        </form>
      ) : (
        <div className="bg-gray-100 text-center py-4 rounded-md text-gray-600 mb-8">
          Connectez-vous pour laisser un commentaire.
        </div>
      )}

      <div className="space-y-4">
        {comments.length === 0 ? (
          <p className="text-gray-500 text-center py-6">Aucun commentaire pour le moment</p>
        ) : (
          comments.map((c) => (
            <div 
              key={c.id} 
              className="border border-gray-200 rounded-md p-4 bg-gray-50"
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="font-medium text-gray-800">{c.username}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(c.creationDate).toLocaleDateString('fr-FR')}
                  </p>
                </div>
                {user && user.id === c.userId && (
                  <span className="text-xs text-gray-500 bg-gray-200 px-2 py-0.5 rounded-md">
                    Vous
                  </span>
                )}
              </div>

              {/* Édition */}
              {editingId === c.id ? (
                <div className="space-y-2">
                  <textarea
                    value={editingText}
                    onChange={(e) => setEditingText(e.target.value)}
                    rows="3"
                    className="w-full px-2 py-1 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 text-sm"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleUpdateComment(c.id)}
                      className="text-sm bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                    >
                      Sauvegarder
                    </button>
                    <button
                      onClick={() => setEditingId(null)}
                      className="text-sm bg-gray-400 text-white px-3 py-1 rounded hover:bg-gray-500"
                    >
                      Annuler
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <p className="text-gray-700">{c.message}</p>
                  {user && user.id === c.userId && (
                    <div className="flex gap-2 mt-2">
                      <button
                        onClick={() => {
                          setEditingId(c.id);
                          setEditingText(c.message);
                        }}
                        className="text-sm text-indigo-600 hover:underline"
                      >
                        Éditer
                      </button>
                      <button
                        onClick={() => handleDeleteComment(c.id)}
                        className="text-sm text-red-600 hover:underline"
                      >
                        Supprimer
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          ))
        )}
      </div>
    </section>
  );
}

export default CommentSection;
