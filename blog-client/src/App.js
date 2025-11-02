import { AuthProvider } from './context/AuthContext';
import Router from './Router';
import './App.css';
import { useState } from 'react';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [articleId, setArticleId] = useState(null);

  const navigate = (page, id = null) => {
    setCurrentPage(page);
    if (id) setArticleId(id);
  };

  return (
    <AuthProvider>
      <Router 
        currentPage={currentPage} 
        articleId={articleId}
        navigate={navigate} 
      />
    </AuthProvider>
  );
}

export default App;