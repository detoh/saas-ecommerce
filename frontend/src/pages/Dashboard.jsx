import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { dashboardService } from '../services/api';
import toast, { Toaster } from 'react-hot-toast';
import {
  ChartBarIcon,
  ShoppingBagIcon,
  CurrencyDollarIcon,
  UserGroupIcon,
  TagIcon,
} from '@heroicons/react/24/outline';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await dashboardService.getVendeur();
      setData(response.data);
    } catch (error) {
      toast.error('Erreur de chargement du dashboard');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const stats = [
    {
      title: 'Chiffre d\'affaires (30j)',
      value: `${data?.chiffre_affaires?.['30_jours']?.toLocaleString() || 0} FCFA`,
      icon: CurrencyDollarIcon,
      color: 'green',
    },
    {
      title: 'Commandes totales',
      value: data?.commandes?.total || 0,
      icon: ShoppingBagIcon,
      color: 'blue',
    },
    {
      title: 'Produits',
      value: data?.produits?.total || 0,
      icon: TagIcon,
      color: 'purple',
    },
    {
      title: 'Abonnement',
      value: data?.abonnement?.actif ? 'Actif ✅' : 'Inactif ❌',
      icon: UserGroupIcon,
      color: 'yellow',
    },
  ];

  const colorClasses = {
    green: 'bg-green-100 text-green-600',
    blue: 'bg-blue-100 text-blue-600',
    purple: 'bg-purple-100 text-purple-600',
    yellow: 'bg-yellow-100 text-yellow-600',
  };

  return (
    <div className="space-y-6">
      <Toaster position="top-center" />
      
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Tableau de Bord</h1>
        <p className="text-sm text-gray-500">
          Dernière mise à jour: {new Date().toLocaleDateString()}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-lg ${colorClasses[stat.color]}`}>
                  <Icon className="w-6 h-6" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold mb-4 text-gray-900">Ma Boutique</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <p className="text-sm text-gray-600 mb-1">Nom</p>
            <p className="font-medium text-gray-900">{data?.boutique?.nom || 'Non défini'}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Statut</p>
            <p className={`font-medium ${data?.boutique?.active ? 'text-green-600' : 'text-red-600'}`}>
              {data?.boutique?.active ? '✅ Active' : '❌ Inactive'}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600 mb-1">Thème</p>
            <p className="font-medium text-gray-900 capitalize">{data?.boutique?.theme || 'Défaut'}</p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Commandes Récentes</h2>
          <Link to="/commandes" className="text-sm text-primary-600 hover:underline">
            Voir tout →
          </Link>
        </div>
        
        {data?.commandes?.recentes?.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left text-sm text-gray-600 border-b border-gray-200">
                  <th className="pb-3 font-medium">Référence</th>
                  <th className="pb-3 font-medium">Client</th>
                  <th className="pb-3 font-medium">Total</th>
                  <th className="pb-3 font-medium">Statut</th>
                  <th className="pb-3 font-medium">Date</th>
                </tr>
              </thead>
              <tbody>
                {data.commandes.recentes.map((cmd) => (
                  <tr key={cmd.id} className="border-b border-gray-100 last:border-0 hover:bg-gray-50">
                    <td className="py-3 font-medium text-gray-900">{cmd.reference}</td>
                    <td className="py-3 text-gray-600">{cmd.client}</td>
                    <td className="py-3 font-medium text-gray-900">{cmd.total.toLocaleString()} FCFA</td>
                    <td className="py-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        cmd.statut === 'livree' ? 'bg-green-100 text-green-600' :
                        cmd.statut === 'validee' ? 'bg-blue-100 text-blue-600' :
                        cmd.statut === 'en_attente' ? 'bg-yellow-100 text-yellow-600' :
                        'bg-gray-100 text-gray-600'
                      }`}>
                        {cmd.statut}
                      </span>
                    </td>
                    <td className="py-3 text-sm text-gray-600">
                      {new Date(cmd.date).toLocaleDateString('fr-FR')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8">
            <ShoppingBagIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">Aucune commande récente</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;