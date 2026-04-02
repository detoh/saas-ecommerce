import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { ShoppingBagIcon, StarIcon } from '@heroicons/react/24/outline';

const API_BASE = 'http://127.0.0.1:8000/api';

const Storefront = () => {
  const { lien_site } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState(null);

  useEffect(() => {
    loadStore();
  }, [lien_site]);

  const loadStore = async () => {
    try {
      const response = await axios.get(`${API_BASE}/boutiques/site/${lien_site}/`);
      setData(response.data);
    } catch (error) {
      console.error('Erreur chargement boutique:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Boutique non trouvée</h1>
          <Link to="/" className="text-primary-600 hover:underline">Retour à l'accueil</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Boutique */}
      <header
        className="relative h-64 bg-cover bg-center"
        style={{
          backgroundColor: data.boutique.couleur_primaire || '#667eea'
        }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>
        <div className="relative z-10 container mx-auto px-4 h-full flex items-center">
          <div className="text-white">
            <h1 className="text-4xl font-bold mb-2">{data.boutique.nom_boutique}</h1>
            <p className="text-lg opacity-90">{data.boutique.description || 'Bienvenue dans notre boutique !'}</p>
          </div>
        </div>
      </header>

      {/* Navigation Catégories */}
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4">
          <div className="flex space-x-4 overflow-x-auto py-4">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-4 py-2 rounded-lg whitespace-nowrap ${
                !selectedCategory ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Tous les produits
            </button>
            {data.categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-lg whitespace-nowrap ${
                  selectedCategory?.id === cat.id ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {cat.nom} ({cat.nombre_produits})
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Produits */}
      <main className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {selectedCategory ? selectedCategory.nom : 'Tous les produits'}
          </h2>
          <p className="text-gray-600">{data.produits.length} produits</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {data.produits.map((produit) => (
            <div key={produit.id} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
              <div className="aspect-square bg-gray-100 flex items-center justify-center">
                {produit.image ? (
                  <img src={produit.image} alt={produit.nom} className="w-full h-full object-cover" />
                ) : (
                  <ShoppingBagIcon className="w-16 h-16 text-gray-300" />
                )}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 mb-2 truncate">{produit.nom}</h3>
                <div className="flex items-center justify-between">
                  <div>
                    {produit.prix_promo ? (
                      <>
                        <span className="text-lg font-bold text-primary-600">{produit.prix_actuel} FCFA</span>
                        <span className="text-sm text-gray-400 line-through ml-2">{produit.prix} FCFA</span>
                      </>
                    ) : (
                      <span className="text-lg font-bold text-gray-900">{produit.prix} FCFA</span>
                    )}
                  </div>
                  {produit.en_stock ? (
                    <span className="text-xs text-green-600">En stock</span>
                  ) : (
                    <span className="text-xs text-red-600">Rupture</span>
                  )}
                </div>
                <button className="w-full mt-4 bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700 transition-colors">
                  Ajouter au panier
                </button>
              </div>
            </div>
          ))}
        </div>

        {data.produits.length === 0 && (
          <div className="text-center py-12">
            <ShoppingBagIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">Aucun produit dans cette catégorie</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">© 2026 {data.boutique.nom_boutique}. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
};

export default Storefront;