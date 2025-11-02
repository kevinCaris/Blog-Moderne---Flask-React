import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

function LoginPage({ navigate }) {
  const { login } = useContext(AuthContext);
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const success = await login(form.email, form.password);
      if (success) {
        navigate('home');
      } else {
        setError('Email ou mot de passe incorrect.');
      }
    } catch {
      setError('Erreur de connexion au serveur.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-indigo-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-black  bg-clip-text  mb-8 text-center">
          Connexion
        </h1>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded mb-6">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
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
            className="w-full bg-gradient-to-r from-indigo-600 to-indigo-800 text-white font-bold py-3 rounded-xl hover:shadow-lg transition"
          >
            Se connecter
          </button>
        </form>

        <p className="text-center text-gray-600 mt-4">
          Pas de compte ?{' '}
          <button
            type="button"
            onClick={() => navigate('register')}
            className="text-indigo-600 font-bold hover:underline"
          >
            S'inscrire
          </button>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
