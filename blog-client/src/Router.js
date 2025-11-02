import React, { useState } from 'react';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ArticleDetailPage from './pages/ArticleDetailPage';
import MyArticlesPage from './pages/MyArticlesPage';
import Header from './components/Header';

function Router() {
  const [currentPage, setCurrentPage] = useState('home');
  const [articleId, setArticleId] = useState(null);

  const navigate = (page, id = null) => {
    setArticleId(id);
    setCurrentPage(page);
  };

  let PageComponent;
  switch (currentPage) {
    case 'home':
      PageComponent = <HomePage navigate={navigate} />;
      break;
    case 'login':
      PageComponent = <LoginPage navigate={navigate} />;
      break;
    case 'register':
      PageComponent = <RegisterPage navigate={navigate} />;
      break;
    case 'article':
      PageComponent = <ArticleDetailPage articleId={articleId} navigate={navigate} />;
      break;
    case 'my-articles':
      PageComponent = <MyArticlesPage navigate={navigate} />;
      break;
    default:
      PageComponent = <HomePage navigate={navigate} />;
  }

  return (
    <>
      <Header navigate={navigate} />
      {PageComponent}
    </>
  );
}

export default Router;
