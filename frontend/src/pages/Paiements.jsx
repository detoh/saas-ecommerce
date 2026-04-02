import { useState, useEffect } from 'react';
import { paiementService, commandeService } from '../services/api';
import toast, { Toaster } from 'react-hot-toast';
import {
  CreditCardIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';

const Paiements = () => {
  const [paiements, setPaiements] = useState([]);
  const [commandes, setCommandes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadPaiements();
    loadCommandes();
  }, []);

  const loadPaiements = async () => {
    try {
      const response = await commandeService.getAll();
      const cmds = response.data;
      const paiementsList = [];
      
      for (const cmd of cmds) {
        try {
          const response = await paiementService.getById(cmd.id);
          if (response.data) {
            paiementsList.push({ ...response.data, commande: cmd });
          }
        } catch (error) {
          // Pas de paiement pour cette commande
        }
      }
      setPaiements(paiementsList);
    } catch (error) {
      console.error('Erreur chargement paiements:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCommandes = async () => {
    try {
      const response = await commandeService.getAll();
      setCommandes(response.data);
    } catch (error) {
      console.error('Erreur chargement commandes:', error);
    }
  };

  const initierPaiement = async (commandeId) => {
    const methode = prompt('Méthode de paiement (orange_money, wave, mtn_money, moov_money):');
    if (!methode) return;
    
    const telephone = prompt('Numéro de téléphone:');
    if (!telephone) return;

    try {
      await paiementService.initier({
        commande_id: commandeId,
        methode,
        telephone,
      });
      toast.success('Paiement initié !');
      loadPaiements();
    } catch (error) {
      toast.error(error.response?.data?.message || 'Erreur lors du paiement');
    }
  };

  const statutColors = {
    pending: 'bg-yellow-100 text-yellow-600',
    initiated: 'bg-blue-100 text-blue-600',
    success: 'bg-green-100 text-green-600',
    failed: 'bg-red-100 text-red-600',
    cancelled: 'bg-gray-100 text-gray-600',
    refunded: 'bg-purple-100 text-purple-600',
  };

  const statutLabels = {
    pending: 'En attente',
    initiated: 'Initié',
    success: 'Succès',
    failed: 'Échoué',
    cancelled: 'Annulé',
    refunded: 'Remboursé',
  };

  const filteredPaiements = filter === 'all'
    ? paiements
    : paiements.filter(p => p.statut === filter);

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
        <h1 className="text-2xl font-bold text-gray-900">Paiements</h1>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
        >
          <option value="all">Tous les statuts</option>
          <option value="pending">En attente</option>
          <option value="initiated">Initié</option>
          <option value="success">Succès</option>
          <option value="failed">Échoué</option>
        </select>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-600">Total Paiements</p>
          <p className="text-2xl font-bold text-gray-900">{paiements.length}</p>
        </div>
        <div className="bg-green-50 rounded-xl shadow-sm border border-green-200 p-6">
          <p className="text-sm text-green-600">Succès</p>
          <p className="text-2xl font-bold text-green-600">
            {paiements.filter(p => p.statut === 'success').length}
          </p>
        </div>
        <div className="bg-yellow-50 rounded-xl shadow-sm border border-yellow-200 p-6">
          <p className="text-sm text-yellow-600">En attente</p>
          <p className="text-2xl font-bold text-yellow-600">
            {paiements.filter(p => p.statut === 'pending').length}
          </p>
        </div>
        <div className="bg-red-50 rounded-xl shadow-sm border border-red-200 p-6">
          <p className="text-sm text-red-600">Échoués</p>
          <p className="text-2xl font-bold text-red-600">
            {paiements.filter(p => p.statut === 'failed').length}
          </p>
        </div>
      </div>

      {/* Paiements Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Référence</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Commande</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Méthode</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Montant</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Statut</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredPaiements.length > 0 ? (
                filteredPaiements.map((paiement) => (
                  <tr key={paiement.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 font-medium text-gray-900">
                      {paiement.reference_interne}
                    </td>
                    <td className="px-6 py-4 text-gray-600">
                      {paiement.commande?.reference || `CMD-${paiement.commande_id}`}
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-700 capitalize">
                        {paiement.methode?.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-medium text-gray-900">
                      {paiement.montant?.toLocaleString()} FCFA
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${statutColors[paiement.statut]}`}>
                        {statutLabels[paiement.statut] || paiement.statut}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(paiement.date_paiement).toLocaleDateString('fr-FR')}
                    </td>
                    <td className="px-6 py-4">
                      {paiement.statut === 'pending' && (
                        <button
                          onClick={() => initierPaiement(paiement.commande_id)}
                          className="px-3 py-1 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700"
                        >
                          Payer
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="px-6 py-12 text-center">
                    <CreditCardIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                    <p className="text-gray-500">Aucun paiement</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Commandes sans paiement */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Commandes sans Paiement</h2>
        {commandes.filter(cmd => !paiements.find(p => p.commande_id === cmd.id)).length > 0 ? (
          <div className="space-y-2">
            {commandes
              .filter(cmd => !paiements.find(p => p.commande_id === cmd.id))
              .slice(0, 5)
              .map((cmd) => (
                <div
                  key={cmd.id}
                  className="flex justify-between items-center p-4 bg-gray-50 rounded-lg"
                >
                  <div>
                    <p className="font-medium text-gray-900">{cmd.reference}</p>
                    <p className="text-sm text-gray-600">{cmd.client_nom} - {cmd.total_final?.toLocaleString()} FCFA</p>
                  </div>
                  <button
                    onClick={() => initierPaiement(cmd.id)}
                    className="px-4 py-2 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700"
                  >
                    Initier Paiement
                  </button>
                </div>
              ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">Toutes les commandes ont un paiement</p>
        )}
      </div>
    </div>
  );
};

export default Paiements;