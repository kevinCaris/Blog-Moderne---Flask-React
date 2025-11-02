import React, { useState } from 'react';
import { registerAPI } from '../api/authAPI';

function RegisterPage({ navigate }) {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await registerAPI(form.username, form.email, form.password);

      if (result.success) {
        navigate('login');
      } else {
        setError(result.message || 'Une erreur est survenue lors de l’inscription.');
      }
    } catch (err) {
      setError('Impossible de se connecter au serveur.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-indigo-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-black  bg-clip-text  mb-8 text-center">
           Créer un compte
        </h1>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded mb-6">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            name="username"
            placeholder="Nom d'utilisateur"
            value={form.username}
            onChange={handleChange}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-indigo-600"
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-indigo-600"
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Mot de passe"
            value={form.password}
            onChange={handleChange}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-indigo-600"
            required
          />

          <button
            type="submit"
            disabled={loading}
            className={`w-full font-bold py-3 rounded-xl transition ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-indigo-600 to-indigo-800 text-white hover:shadow-lg'
            }`}
          >
            {loading ? 'Création du compte...' : 'Créer un compte'}
          </button>
        </form>

        <p className="text-center text-gray-600 mt-4">
          Déjà un compte ?{' '}
          <button
            type="button"
            onClick={() => navigate('login')}
            className="text-indigo-600 font-bold hover:underline"
          >
            Se connecter
          </button>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
