import { useState, useEffect } from 'react';
import { commandeService } from '../services/api';
import toast, { Toaster } from 'react-hot-toast';
import {
  EyeIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClipboardDocumentCheckIcon,
  TruckIcon,
  CubeIcon,
} from '@heroicons/react/24/outline';

const Commandes = () => {
  const [commandes, setCommandes] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [selectedCommande, setSelectedCommande] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    loadCommandes();
    loadStats();
  }, []);

  const loadCommandes = async () => {
    try {
      const response = await commandeService.getAll();
      setCommandes(response.data);
    } catch (error) {
      toast.error('Erreur de chargement des commandes');
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await commandeService.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Erreur stats:', error);
    }
  };

  const updateStatut = async (id, nouveauStatut) => {
    try {
      await commandeService.updateStatut(id, nouveauStatut);
      toast.success(`Commande ${nouveauStatut}`);
      loadCommandes();
      loadStats();
    } catch (error) {
      toast.error('Erreur lors de la mise à jour');
    }
  };

  const viewCommande = (cmd) => {
    setSelectedCommande(cmd);
    setShowModal(true);
  };

  const filteredCommandes = filter === 'all' 
    ? commandes 
    : commandes.filter(cmd => cmd.statut === filter);

  const statutColors = {
    en_attente: 'bg-yellow-100 text-yellow-600',
    validee: 'bg-blue-100 text-blue-600',
    en_preparation: 'bg-purple-100 text-purple-600',
    expediee: 'bg-indigo-100 text-indigo-600',
    livree: 'bg-green-100 text-green-600',
    annulee: 'bg-red-100 text-red-600',
  };

  const statutActions = {
    en_attente: { next: 'validee', icon: CheckCircleIcon, label: 'Valider' },
    validee: { next: 'en_preparation', icon: ClipboardDocumentCheckIcon, label: 'Préparer' },
    en_preparation: { next: 'expediee', icon: TruckIcon, label: 'Expédier' },
    expediee: { next: 'livree', icon: CheckCircleIcon, label: 'Livrer' },
    livree: null,
    annulee: null,
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Toaster position="top-center" />
      
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Commandes</h1>
        <div className="flex space-x-2">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option value="all">Toutes les commandes</option>
            <option value="en_attente">En attente</option>
            <option value="validee">Validées</option>
            <option value="en_preparation">En préparation</option>
            <option value="expediee">Expédiées</option>
            <option value="livree">Livrées</option>
            <option value="annulee">Annulées</option>
          </select>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 text-center">
            <p className="text-2xl font-bold text-gray-900">{stats.total_commandes}</p>
            <p className="text-sm text-gray-600">Total</p>
          </div>
          <div className="bg-yellow-50 rounded-xl shadow-sm border border-yellow-200 p-4 text-center">
            <p className="text-2xl font-bold text-yellow-600">{stats.en_attente}</p>
            <p className="text-sm text-yellow-600">En attente</p>
          </div>
          <div className="bg-blue-50 rounded-xl shadow-sm border border-blue-200 p-4 text-center">
            <p className="text-2xl font-bold text-blue-600">{stats.validees}</p>
            <p className="text-sm text-blue-600">Validées</p>
          </div>
          <div className="bg-purple-50 rounded-xl shadow-sm border border-purple-200 p-4 text-center">
            <p className="text-2xl font-bold text-purple-600">{stats.en_preparation || 0}</p>
            <p className="text-sm text-purple-600">En prép.</p>
          </div>
          <div className="bg-green-50 rounded-xl shadow-sm border border-green-200 p-4 text-center">
            <p className="text-2xl font-bold text-green-600">{stats.livrees}</p>
            <p className="text-sm text-green-600">Livrées</p>
          </div>
          <div className="bg-red-50 rounded-xl shadow-sm border border-red-200 p-4 text-center">
            <p className="text-2xl font-bold text-red-600">{stats.annulees}</p>
            <p className="text-sm text-red-600">Annulées</p>
          </div>
        </div>
      )}

      {/* Commandes Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Référence</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Client</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ville</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Statut</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredCommandes.length > 0 ? (
                filteredCommandes.map((cmd) => {
                  const action = statutActions[cmd.statut];
                  return (
                    <tr key={cmd.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 font-medium text-gray-900">{cmd.reference}</td>
                      <td className="px-6 py-4 text-gray-600">{cmd.client_nom}</td>
                      <td className="px-6 py-4 text-gray-600">{cmd.ville}</td>
                      <td className="px-6 py-4 font-medium text-gray-900">
                        {cmd.total_final?.toLocaleString()} FCFA
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${statutColors[cmd.statut]}`}>
                          {cmd.statut_display || cmd.statut}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {new Date(cmd.date_commande).toLocaleDateString('fr-FR')}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => viewCommande(cmd)}
                            className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                            title="Voir détails"
                          >
                            <EyeIcon className="w-4 h-4" />
                          </button>
                          {action && (
                            <button
                              onClick={() => updateStatut(cmd.id, action.next)}
                              className="p-2 text-green-600 hover:bg-green-50 rounded-lg"
                              title={action.label}
                            >
                              <action.icon className="w-4 h-4" />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan="7" className="px-6 py-12 text-center">
                    <CubeIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                    <p className="text-gray-500">Aucune commande</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Détails */}
      {showModal && selectedCommande && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-900">
                Commande #{selectedCommande.reference}
              </h2>
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <div className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Client</p>
                  <p className="font-medium">{selectedCommande.client_nom}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Téléphone</p>
                  <p className="font-medium">{selectedCommande.telephone_livraison || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Ville</p>
                  <p className="font-medium">{selectedCommande.ville}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Statut</p>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${statutColors[selectedCommande.statut]}`}>
                    {selectedCommande.statut_display || selectedCommande.statut}
                  </span>
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-600 mb-2">Adresse de livraison</p>
                <p className="font-medium">{selectedCommande.adresse_livraison}</p>
              </div>

              {selectedCommande.notes && (
                <div>
                  <p className="text-sm text-gray-600 mb-2">Notes</p>
                  <p className="text-gray-700 bg-gray-50 p-3 rounded-lg">{selectedCommande.notes}</p>
                </div>
              )}

              <div className="border-t pt-4">
                <div className="flex justify-between items-center">
                  <p className="text-lg font-semibold">Total</p>
                  <p className="text-2xl font-bold text-primary-600">
                    {selectedCommande.total_final?.toLocaleString()} FCFA
                  </p>
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t">
                <button
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  Fermer
                </button>
                {statutActions[selectedCommande.statut] && (
                  <button
                    onClick={() => {
                      updateStatut(selectedCommande.id, statutActions[selectedCommande.statut].next);
                      setShowModal(false);
                    }}
                    className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                  >
                    {statutActions[selectedCommande.statut].label}
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Commandes;