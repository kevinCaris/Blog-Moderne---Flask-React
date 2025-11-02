import React, { useState } from 'react';
import { createPostAPI } from '../api/articlesAPI';

function CreatePostForm({ onPostCreated }) {
    const [title, setTitle] = useState('');
    const [body, setBody] = useState('');
    const [errors, setErrors] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors([]);

        const newErrors = [];
        if (!title || title.length < 3) newErrors.push('Titre minimum 3 caractères');
        if (!body || body.length < 10) newErrors.push('Contenu minimum 10 caractères');

        if (newErrors.length > 0) {
            setErrors(newErrors);
            return;
        }

        try {
            const data = await createPostAPI(title, body);
            if (data.success) {
                setTitle('');
                setBody('');
                onPostCreated();
            } else {
                setErrors([data.message || 'Erreur création article']);
            }
        } catch (error) {
            console.error('Erreur:', error);
            setErrors(['Erreur réseau']);
        }
    };


    return (
        <div className="lg:col-span-1">
            <div className="sticky top-8 bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
                <h2 className="text-2xl font-bold mb-6">✍️ Nouvel article</h2>

                {errors.length > 0 && (
                    <div className="mb-4 space-y-2">
                        {errors.map((error, i) => (
                            <div key={i} className="bg-red-100 border-l-4 border-red-500 text-red-700 px-4 py-2 rounded">
                                ⚠️ {error}
                            </div>
                        ))}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <input
                        type="text"
                        placeholder="Titre..."
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-600"
                    />
                    <textarea
                        placeholder="Contenu..."
                        value={body}
                        onChange={(e) => setBody(e.target.value)}
                        rows="6"
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-600 resize-none"
                    />
                    <button
                        type="submit"
                        className="w-full bg-indigo-600  text-white font-bold py-3 rounded-xl hover:shadow-lg transition"
                    >
                        Publier
                    </button>
                </form>
            </div>
        </div>
    );
}

export default CreatePostForm;