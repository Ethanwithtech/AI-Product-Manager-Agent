import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import GuideModal from './components/GuideModal';
import KnowledgeBase from './pages/KnowledgeBase';
import Requirements from './pages/Requirements';
import ProgressBoard from './pages/ProgressBoard';
import Templates from './pages/Templates';
import FeedbackAnalysis from './pages/FeedbackAnalysis';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <GuideModal />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/knowledge" replace />} />
          <Route path="knowledge" element={<KnowledgeBase />} />
          <Route path="requirements" element={<Requirements />} />
          <Route path="progress" element={<ProgressBoard />} />
          <Route path="templates" element={<Templates />} />
          <Route path="feedback" element={<FeedbackAnalysis />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
