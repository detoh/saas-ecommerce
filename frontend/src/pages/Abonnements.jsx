import { useState, useEffect } from 'react';
import { abonnementService } from '../services/api';
import toast, { Toaster } from 'react-hot-toast';
import {
  SparklesIcon,
  CheckCircleIcon,
  ClockIcon,
  BanknotesIcon,
} from '@heroicons/react/24/outline';

const Abonnements = () => {
  const [abonnement, setAbonnement] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState(null);

  const plans = [
    {
      id: 'basic',
      name: 'Basic',
      price: 10000,
      period: 'mois',
      features: [
        '1 Boutique',
        '100 Produits max',
        'Paiements Mobile Money',
        'Support email',
        'Stats de base',
      ],
      color: 'blue',
    },
    {
      id: 'pro',
      name: 'Pro',
      price: 25000,
      period: 'mois',
      features: [
        '1 Boutique',
        'Produits illimités',
        'Paiements Mobile Money',
        'Support prioritaire',
        'Stats avancées',
        'Personnalisation thème',
      ],
      color: 'purple',
      popular: true,
    },
    {
      id: 'premium',
      name: 'Premium',
      price: 50000,
      period: 'mois',
      features: [
        'Boutiques illimitées',
        'Produits illimités',
        'Tous les paiements',
        'Support 24/7',
        'Analytics complet',
        'Personnalisation totale',
        'API accès',
      ],
      color: 'yellow',
    },
  ];

  useEffect(() => {
    loadAbonnement();
    loadStats();
  }, []);

  const loadAbonnement = async () => {
  try {
    const response = await abonnementService.getActif();
    setAbonnement(response.data);
  } catch (error) {
    // 404 = pas d'abonnement actif, c'est normal
    if (error.response?.status !== 404) {
      console.error('Erreur chargement abonnement:', error);
    }
  } finally {
    setLoading(false);
  }
};

  const loadStats = async () => {
    try {
      const response = await abonnementService.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Erreur stats:', error);
    }
  };

  const souscrire = async (plan) => {
    setSelectedPlan(plan);
    setShowModal(true);
  };

  const confirmerSouscription = async (typeAbo) => {
    try {
      await abonnementService.create({
        plan: selectedPlan.id,
        type_abo: typeAbo,
        paiement_auto: false,
      });
      toast.success('Abonnement créé ! Procédez au paiement.');
      setShowModal(false);
      loadAbonnement();
      loadStats();
    } catch (error) {
      toast.error(error.response?.data?.message || 'Erreur lors de la souscription');
    }
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
        <h1 className="text-2xl font-bold text-gray-900">Abonnements</h1>
      </div>

      {/* Abonnement Actuel */}
      {abonnement ? (
        <div className="bg-gradient-to-r from-primary-500 to-primary-700 rounded-xl shadow-lg p-8 text-white">
          <div className="flex justify-between items-start">
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <SparklesIcon className="w-6 h-6" />
                <span className="text-sm font-medium opacity-90">Abonnement Actif</span>
              </div>
              <h2 className="text-3xl font-bold mb-2 capitalize">{abonnement.plan_display || abonnement.plan}</h2>
              <p className="opacity-90">
                Valide jusqu'au {new Date(abonnement.date_fin).toLocaleDateString('fr-FR')}
              </p>
            </div>
            <div className="text-right">
              <p className="text-2xl font-bold">{abonnement.jours_restants} jours</p>
              <p className="text-sm opacity-90">restants</p>
            </div>
          </div>
          
          {abonnement.est_expirable_bientot && (
            <div className="mt-4 bg-white/20 rounded-lg p-4">
              <p className="text-sm font-medium">⚠️ Votre abonnement expire bientôt ! Renouvelez pour éviter l'interruption.</p>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
          <div className="flex items-center space-x-3">
            <ClockIcon className="w-6 h-6 text-yellow-600" />
            <div>
              <p className="font-medium text-yellow-900">Aucun abonnement actif</p>
              <p className="text-sm text-yellow-700">Choisissez un plan ci-dessous pour activer votre boutique</p>
            </div>
          </div>
        </div>
      )}

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-sm text-gray-600">Total Abonnements</p>
            <p className="text-2xl font-bold text-gray-900">{stats.total_abonnements}</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-sm text-gray-600">Jours Restants</p>
            <p className="text-2xl font-bold text-primary-600">{stats.jours_restants}</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <p className="text-sm text-gray-600">Expiration Bientôt</p>
            <p className={`text-2xl font-bold ${stats.expirable_bientot ? 'text-red-600' : 'text-green-600'}`}>
              {stats.expirable_bientot ? 'Oui ⚠️' : 'Non ✅'}
            </p>
          </div>
        </div>
      )}

      {/* Plans */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {plans.map((plan) => {
          const isCurrent = abonnement?.plan === plan.id;
          return (
            <div
              key={plan.id}
              className={`bg-white rounded-xl shadow-sm border-2 p-6 relative ${
                plan.popular ? 'border-primary-500' : 'border-gray-200'
              } ${isCurrent ? 'ring-2 ring-green-500' : ''}`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-primary-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                    POPULAIRE
                  </span>
                </div>
              )}
              
              {isCurrent && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                    ACTUEL
                  </span>
                </div>
              )}

              <div className="text-center mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <div className="flex items-baseline justify-center">
                  <span className="text-4xl font-bold text-gray-900">{plan.price.toLocaleString()}</span>
                  <span className="text-gray-600 ml-2">FCFA/{plan.period}</span>
                </div>
              </div>

              <ul className="space-y-3 mb-6">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-center text-sm text-gray-700">
                    <CheckCircleIcon className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>

              <button
                onClick={() => souscrire(plan)}
                disabled={isCurrent}
                className={`w-full py-3 rounded-lg font-semibold transition-colors ${
                  isCurrent
                    ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                    : `bg-${plan.color}-600 text-white hover:bg-${plan.color}-700`
                }`}
              >
                {isCurrent ? 'Plan Actuel' : 'Choisir ce plan'}
              </button>
            </div>
          );
        })}
      </div>

      {/* Modal de Confirmation */}
      {showModal && selectedPlan && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Choisir {selectedPlan.name}
            </h2>
            
            <p className="text-gray-600 mb-6">
              Sélectionnez la période d'abonnement :
            </p>

            <div className="space-y-3 mb-6">
              <button
                onClick={() => confirmerSouscription('mensuel')}
                className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 transition-colors text-left"
              >
                <p className="font-semibold text-gray-900">Mensuel</p>
                <p className="text-sm text-gray-600">{selectedPlan.price.toLocaleString()} FCFA / mois</p>
              </button>

              <button
                onClick={() => confirmerSouscription('trimestriel')}
                className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 transition-colors text-left"
              >
                <p className="font-semibold text-gray-900">Trimestriel</p>
                <p className="text-sm text-gray-600">
                  {(selectedPlan.price * 3 * 0.9).toLocaleString()} FCFA / 3 mois (-10%)
                </p>
              </button>

              <button
                onClick={() => confirmerSouscription('annuel')}
                className="w-full p-4 border-2 border-green-200 bg-green-50 rounded-lg hover:border-green-500 transition-colors text-left"
              >
                <p className="font-semibold text-green-900">Annuel</p>
                <p className="text-sm text-green-600">
                  {(selectedPlan.price * 12 * 0.8).toLocaleString()} FCFA / an (-20%)
                </p>
              </button>
            </div>

            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Abonnements;