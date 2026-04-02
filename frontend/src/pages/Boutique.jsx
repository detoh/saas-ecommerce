import { useState, useEffect } from 'react';
import { boutiqueService } from '../services/api';
import toast, { Toaster } from 'react-hot-toast';
import {
  BuildingStorefrontIcon,
  CameraIcon,
  SwatchIcon,
  DevicePhoneMobileIcon,
} from '@heroicons/react/24/outline';

const Boutique = () => {
  const [boutique, setBoutique] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    nom_boutique: '',
    theme: 'default',
    couleur_primaire: '#000000',
    couleur_secondaire: '#FFFFFF',
    devise: 'XOF',
    whatsapp_numero: '',
  });

  const themes = [
    { value: 'default', label: 'Défaut' },
    { value: 'moderne', label: 'Moderne' },
    { value: 'minimaliste', label: 'Minimaliste' },
    { value: 'colore', label: 'Coloré' },
  ];

  const devises = [
    { value: 'XOF', label: 'FCFA (XOF)' },
    { value: 'EUR', label: 'Euro (EUR)' },
    { value: 'USD', label: 'Dollar (USD)' },
  ];

  useEffect(() => {
    loadBoutique();
  }, []);

  const loadBoutique = async () => {
    try {
      const response = await boutiqueService.getMaBoutique();
      setBoutique(response.data);
      setFormData({
        nom_boutique: response.data.nom_boutique || '',
        theme: response.data.theme || 'default',
        couleur_primaire: response.data.couleur_primaire || '#000000',
        couleur_secondaire: response.data.couleur_secondaire || '#FFFFFF',
        devise: response.data.devise || 'XOF',
        whatsapp_numero: response.data.whatsapp_numero || '',
      });
    } catch (error) {
      console.error('Erreur chargement boutique:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (boutique) {
        await boutiqueService.updateBoutique(boutique.id, formData);
        toast.success('Boutique mise à jour !');
      } else {
        await boutiqueService.createBoutique(formData);
        toast.success('Boutique créée !');
      }
      setEditing(false);
      loadBoutique();
    } catch (error) {
      toast.error(error.response?.data?.error || 'Erreur lors de l\'enregistrement');
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
        <h1 className="text-2xl font-bold text-gray-900">Ma Boutique</h1>
        {!editing ? (
          <button
            onClick={() => setEditing(true)}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Modifier
          </button>
        ) : (
          <button
            onClick={() => {
              setEditing(false);
              loadBoutique();
            }}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            Annuler
          </button>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Statut</p>
              <p className={`text-2xl font-bold ${boutique?.active ? 'text-green-600' : 'text-red-600'}`}>
                {boutique?.active ? '✅ Active' : '❌ Inactive'}
              </p>
            </div>
            <BuildingStorefrontIcon className="w-12 h-12 text-gray-300" />
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Thème</p>
              <p className="text-2xl font-bold text-gray-900 capitalize">{boutique?.theme}</p>
            </div>
            <SwatchIcon className="w-12 h-12 text-gray-300" />
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Devise</p>
              <p className="text-2xl font-bold text-gray-900">{boutique?.devise}</p>
            </div>
            <DevicePhoneMobileIcon className="w-12 h-12 text-gray-300" />
          </div>
        </div>
      </div>

      {/* Formulaire */}
      {editing ? (
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-6">
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Informations Générales</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nom de la boutique *
                </label>
                <input
                  type="text"
                  value={formData.nom_boutique}
                  onChange={(e) => setFormData({ ...formData, nom_boutique: e.target.value })}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Ma Super Boutique"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Thème *
                </label>
                <select
                  value={formData.theme}
                  onChange={(e) => setFormData({ ...formData, theme: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  {themes.map((t) => (
                    <option key={t.value} value={t.value}>{t.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Devise *
                </label>
                <select
                  value={formData.devise}
                  onChange={(e) => setFormData({ ...formData, devise: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  {devises.map((d) => (
                    <option key={d.value} value={d.value}>{d.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Numéro WhatsApp
                </label>
                <input
                  type="tel"
                  value={formData.whatsapp_numero}
                  onChange={(e) => setFormData({ ...formData, whatsapp_numero: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="07070707"
                />
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Apparence</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Couleur Primaire
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="color"
                    value={formData.couleur_primaire}
                    onChange={(e) => setFormData({ ...formData, couleur_primaire: e.target.value })}
                    className="w-12 h-12 rounded-lg border border-gray-300 cursor-pointer"
                  />
                  <input
                    type="text"
                    value={formData.couleur_primaire}
                    onChange={(e) => setFormData({ ...formData, couleur_primaire: e.target.value })}
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    placeholder="#000000"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Couleur Secondaire
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="color"
                    value={formData.couleur_secondaire}
                    onChange={(e) => setFormData({ ...formData, couleur_secondaire: e.target.value })}
                    className="w-12 h-12 rounded-lg border border-gray-300 cursor-pointer"
                  />
                  <input
                    type="text"
                    value={formData.couleur_secondaire}
                    onChange={(e) => setFormData({ ...formData, couleur_secondaire: e.target.value })}
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    placeholder="#FFFFFF"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4 border-t">
            <button
              type="button"
              onClick={() => {
                setEditing(false);
                loadBoutique();
              }}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              Enregistrer
            </button>
          </div>
        </form>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Nom</p>
              <p className="font-medium text-gray-900">{boutique?.nom_boutique}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Thème</p>
              <p className="font-medium text-gray-900 capitalize">{boutique?.theme}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Devise</p>
              <p className="font-medium text-gray-900">{boutique?.devise}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">WhatsApp</p>
              <p className="font-medium text-gray-900">{boutique?.whatsapp_numero || 'Non défini'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Couleur Primaire</p>
              <div className="flex items-center space-x-2">
                <div
                  className="w-6 h-6 rounded border"
                  style={{ backgroundColor: boutique?.couleur_primaire }}
                />
                <span className="font-medium text-gray-900">{boutique?.couleur_primaire}</span>
              </div>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Couleur Secondaire</p>
              <div className="flex items-center space-x-2">
                <div
                  className="w-6 h-6 rounded border"
                  style={{ backgroundColor: boutique?.couleur_secondaire }}
                />
                <span className="font-medium text-gray-900">{boutique?.couleur_secondaire}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Boutique;