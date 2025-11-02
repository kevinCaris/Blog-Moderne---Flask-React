import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

function Header({ navigate }) {
  const { user, logout } = useContext(AuthContext);

  return (
    <header className="bg-indigo-600 text-white">
      <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
        
        <h1 
          onClick={() => navigate('home')} 
          className="text-xl font-semibold cursor-pointer hover:text-indigo-200 transition"
        >
          📚 Blog
        </h1>

        <nav className="flex items-center gap-4">
          {user ? (
            <>
              <span className="text-sm font-medium">{user.username}</span>
              <button 
                onClick={() => navigate('my-articles')}
                className="text-sm bg-white text-indigo-600 px-3 py-1.5 rounded hover:bg-indigo-50 transition"
              >
                Mes articles
              </button>
              <button 
                onClick={() => { logout(); navigate('home'); }}
                className="text-sm border border-white px-3 py-1.5 rounded hover:bg-indigo-500 transition"
              >
                Déconnexion
              </button>
            </>
          ) : (
            <>
              <button 
                onClick={() => navigate('login')}
                className="text-sm bg-white text-indigo-600 px-3 py-1.5 rounded hover:bg-indigo-50 transition"
              >
                Connexion
              </button>
              <button 
                onClick={() => navigate('register')}
                className="text-sm border border-white px-3 py-1.5 rounded hover:bg-indigo-500 transition"
              >
                Inscription
              </button>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Header;
