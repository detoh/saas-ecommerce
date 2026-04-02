import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Layout
import Layout from './components/Layout';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Produits from './pages/Produits';
import Commandes from './pages/Commandes';
import Boutique from './pages/Boutique';
import Paiements from './pages/Paiements';
import Abonnements from './pages/Abonnements';
import Categories from './pages/Categories';
import Storefront from './pages/Storefront';

// ============================================
// 🛡️ ROUTE PROTÉGÉE
// ============================================
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

// ============================================
// 🎯 CONFIGURATION DES ROUTES
// ============================================
function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* ============================================
              🌐 ROUTES PUBLIQUES (Sans Layout)
              ============================================ */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/store/:lien_site" element={<Storefront />} />
          <Route path="/store/:lien_site/categorie/:categorie_slug" element={<Storefront />} />

          {/* ============================================
              🔒 ROUTES PROTÉGÉES (Avec Layout)
              ============================================ */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="categories" element={<Categories />} />
            <Route path="produits" element={<Produits />} />
            <Route path="commandes" element={<Commandes />} />
            <Route path="boutique" element={<Boutique />} />
            <Route path="paiements" element={<Paiements />} />
            <Route path="abonnements" element={<Abonnements />} />
          </Route>

          {/* ============================================
              ❌ ROUTE 404 (Redirection)
              ============================================ */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;