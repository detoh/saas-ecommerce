import { useState, useEffect } from 'react';
import axios from 'axios';
import toast, { Toaster } from 'react-hot-toast';
import { PlusIcon, PencilIcon, TrashIcon, TagIcon, CameraIcon, XCircleIcon } from '@heroicons/react/24/outline';

const API_BASE = 'http://127.0.0.1:8000/api';

const Produits = () => {
  const [produits, setProduits] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showImageModal, setShowImageModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [formData, setFormData] = useState({
    nom: '',
    description: '',
    prix: '',
    prix_promo: '',
    stock: '',
    categorie: '',
    is_visible: true,
  });
  const [images, setImages] = useState([]);
  const [imagePreviews, setImagePreviews] = useState([]);

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    loadProduits();
    loadCategories();
  }, []);

  const loadProduits = async () => {
    try {
      const response = await axios.get(`${API_BASE}/produits/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProduits(response.data);
    } catch (error) {
      toast.error('Erreur de chargement des produits');
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await axios.get(`${API_BASE}/produits/categories/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCategories(response.data);
    } catch (error) {
      console.error('Erreur chargement catégories:', error);
    }
  };

  const handleImageChange = (e) => {
    const files = Array.from(e.target.files);
    
    if (files.length + images.length > 4) {
      toast.error('Maximum 4 images (1 principale + 3 supplémentaires)');
      return;
    }
    
    setImages([...images, ...files]);
    
    // Créer des previews
    const previews = files.map(file => URL.createObjectURL(file));
    setImagePreviews([...imagePreviews, ...previews]);
  };

  const removeImage = (index) => {
    const newImages = images.filter((_, i) => i !== index);
    const newPreviews = imagePreviews.filter((_, i) => i !== index);
    setImages(newImages);
    setImagePreviews(newPreviews);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const data = new FormData();
      data.append('nom', formData.nom);
      data.append('description', formData.description);
      data.append('prix', parseFloat(formData.prix));
      data.append('stock', parseInt(formData.stock));
      if (formData.prix_promo) {
        data.append('prix_promo', parseFloat(formData.prix_promo));
      }
      if (formData.categorie) {
        data.append('categorie', formData.categorie);
      }
      data.append('is_visible', formData.is_visible);
      
      // Image principale
      if (images.length > 0) {
        data.append('image', images[0]);
      }
      
      if (editingProduct) {
        await axios.put(
          `${API_BASE}/produits/${editingProduct.id}/`,
          data,
          { 
            headers: { 
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        toast.success('Produit modifié avec succès');
      } else {
        await axios.post(
          `${API_BASE}/produits/`,
          data,
          { 
            headers: { 
              Authorization: `Bearer ${token}`,
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        toast.success('Produit créé avec succès');
      }
      
      // Upload des images supplémentaires si c'est un nouveau produit
      if (!editingProduct && images.length > 1) {
        // On devra récupérer l'ID du produit créé
      }
      
      setShowModal(false);
      setEditingProduct(null);
      setImages([]);
      setImagePreviews([]);
      resetForm();
      loadProduits();
    } catch (error) {
      toast.error(error.response?.data?.message || 'Erreur lors de l\'enregistrement');
    }
  };

  const handleEdit = (produit) => {
    setEditingProduct(produit);
    setFormData({
      nom: produit.nom,
      description: produit.description || '',
      prix: produit.prix,
      prix_promo: produit.prix_promo || '',
      stock: produit.stock,
      categorie: produit.categorie?.id || produit.categorie || '',
      is_visible: produit.is_visible,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce produit ?')) {
      try {
        await axios.delete(`${API_BASE}/produits/${id}/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Produit supprimé');
        loadProduits();
      } catch (error) {
        toast.error('Erreur lors de la suppression');
      }
    }
  };

  const handleImageUpload = async () => {
    if (!selectedProduct || images.length === 0) return;
    
    try {
      const formData = new FormData();
      images.forEach(image => {
        formData.append('images', image);
      });
      
      await axios.post(
        `${API_BASE}/produits/${selectedProduct.id}/images/`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      toast.success('Images ajoutées avec succès');
      setShowImageModal(false);
      setImages([]);
      setImagePreviews([]);
      loadProduits();
    } catch (error) {
      toast.error('Erreur lors de l\'upload des images');
    }
  };

  const handleDeleteImage = async (produitId, imageIndex) => {
    try {
      await axios.delete(
        `${API_BASE}/produits/${produitId}/images/${imageIndex}/`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      toast.success('Image supprimée');
      loadProduits();
    } catch (error) {
      toast.error('Erreur lors de la suppression de l\'image');
    }
  };

  const openImageModal = (produit) => {
    setSelectedProduct(produit);
    setImages([]);
    setImagePreviews([]);
    setShowImageModal(true);
  };

  const resetForm = () => {
    setFormData({
      nom: '',
      description: '',
      prix: '',
      prix_promo: '',
      stock: '',
      categorie: '',
      is_visible: true,
    });
  };

  const openNewProductModal = () => {
    setEditingProduct(null);
    resetForm();
    setImages([]);
    setImagePreviews([]);
    setShowModal(true);
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
        <h1 className="text-2xl font-bold text-gray-900">Gestion des Produits</h1>
        <button
          onClick={openNewProductModal}
          className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          <PlusIcon className="w-5 h-5 mr-2" />
          Nouveau Produit
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-600">Total Produits</p>
          <p className="text-2xl font-bold text-gray-900">{produits.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-600">En Stock</p>
          <p className="text-2xl font-bold text-green-600">
            {produits.filter(p => p.stock > 0).length}
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-600">Rupture de Stock</p>
          <p className="text-2xl font-bold text-red-600">
            {produits.filter(p => p.stock === 0).length}
          </p>
        </div>
      </div>

      {/* Products Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Produit</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Images</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Catégorie</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prix</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Statut</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {produits.length > 0 ? (
                produits.map((produit) => (
                  <tr key={produit.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        {produit.image && (
                          <img 
                            src={produit.image_url || produit.image} 
                            alt={produit.nom} 
                            className="w-12 h-12 rounded-lg object-cover mr-3"
                          />
                        )}
                        <div>
                          <p className="font-medium text-gray-900">{produit.nom}</p>
                          <p className="text-sm text-gray-500 truncate max-w-xs">
                            {produit.description?.substring(0, 50)}...
                          </p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-600">
                          {1 + (produit.images_supplementaires?.length || 0)} image(s)
                        </span>
                        <button
                          onClick={() => openImageModal(produit)}
                          className="p-1 text-primary-600 hover:bg-primary-50 rounded"
                          title="Gérer les images"
                        >
                          <CameraIcon className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-700 capitalize">
                        {produit.categorie_nom || produit.categorie || 'Autre'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <p className="font-medium text-gray-900">
                        {(produit.prix_actuel || produit.prix).toLocaleString()} FCFA
                      </p>
                      {produit.prix_promo && (
                        <p className="text-sm text-gray-400 line-through">
                          {produit.prix.toLocaleString()} FCFA
                        </p>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`font-medium ${produit.stock > 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {produit.stock}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        produit.is_visible ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'
                      }`}>
                        {produit.is_visible ? 'Visible' : 'Masqué'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleEdit(produit)}
                          className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                          title="Modifier"
                        >
                          <PencilIcon className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(produit.id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                          title="Supprimer"
                        >
                          <TrashIcon className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="px-6 py-12 text-center">
                    <TagIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                    <p className="text-gray-500">Aucun produit</p>
                    <button
                      onClick={openNewProductModal}
                      className="mt-3 text-primary-600 hover:underline"
                    >
                      Créer votre premier produit
                    </button>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Création/Modification Produit */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">
                {editingProduct ? 'Modifier le produit' : 'Nouveau produit'}
              </h2>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nom du produit *
                  </label>
                  <input
                    type="text"
                    value={formData.nom}
                    onChange={(e) => setFormData({ ...formData, nom: e.target.value })}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    placeholder="Ex: Chaussures Nike"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Catégorie
                  </label>
                  <select
                    value={formData.categorie}
                    onChange={(e) => setFormData({ ...formData, categorie: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">-- Sélectionner une catégorie --</option>
                    {categories.map((cat) => (
                      <option key={cat.id} value={cat.id}>
                        {cat.nom} ({cat.nombre_produits} produits)
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows="3"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Décrivez votre produit..."
                />
              </div>

              {/* Upload Images */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Images (1 à 4 photos)
                </label>
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  onChange={handleImageChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Première image = principale, jusqu'à 3 images supplémentaires
                </p>
                
                {/* Previews */}
                {imagePreviews.length > 0 && (
                  <div className="grid grid-cols-4 gap-2 mt-4">
                    {imagePreviews.map((preview, index) => (
                      <div key={index} className="relative">
                        <img 
                          src={preview} 
                          alt={`Preview ${index}`} 
                          className="w-full h-24 object-cover rounded-lg"
                        />
                        <button
                          type="button"
                          onClick={() => removeImage(index)}
                          className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                        >
                          <XCircleIcon className="w-4 h-4" />
                        </button>
                        {index === 0 && (
                          <span className="absolute bottom-1 left-1 bg-primary-600 text-white text-xs px-2 py-1 rounded">
                            Principale
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Prix (FCFA) *
                  </label>
                  <input
                    type="number"
                    value={formData.prix}
                    onChange={(e) => setFormData({ ...formData, prix: e.target.value })}
                    required
                    min="0"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    placeholder="50000"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Prix promo
                  </label>
                  <input
                    type="number"
                    value={formData.prix_promo}
                    onChange={(e) => setFormData({ ...formData, prix_promo: e.target.value })}
                    min="0"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    placeholder="45000"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Stock *
                  </label>
                  <input
                    type="number"
                    value={formData.stock}
                    onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
                    required
                    min="0"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                    placeholder="100"
                  />
                </div>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="is_visible"
                  checked={formData.is_visible}
                  onChange={(e) => setFormData({ ...formData, is_visible: e.target.checked })}
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                />
                <label htmlFor="is_visible" className="ml-2 text-sm text-gray-700">
                  Rendre ce produit visible sur la boutique
                </label>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  {editingProduct ? 'Modifier' : 'Créer'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Gestion Images */}
      {showImageModal && selectedProduct && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">
                Gérer les images - {selectedProduct.nom}
              </h2>
            </div>
            
            <div className="p-6 space-y-4">
              {/* Images existantes */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Images actuelles
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {selectedProduct.image_url && (
                    <div className="relative">
                      <img 
                        src={selectedProduct.image_url} 
                        alt="Image principale" 
                        className="w-full h-32 object-cover rounded-lg"
                      />
                      <span className="absolute bottom-1 left-1 bg-primary-600 text-white text-xs px-2 py-1 rounded">
                        Principale
                      </span>
                    </div>
                  )}
                  {selectedProduct.images_supplementaires?.map((img, index) => (
                    <div key={index} className="relative">
                      <img 
                        src={img} 
                        alt={`Image ${index + 1}`} 
                        className="w-full h-32 object-cover rounded-lg"
                      />
                      <button
                        onClick={() => handleDeleteImage(selectedProduct.id, index)}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                      >
                        <XCircleIcon className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Upload nouvelles images */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ajouter des images (max 3 supplémentaires)
                </label>
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  onChange={handleImageChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg"
                />
                
                {imagePreviews.length > 0 && (
                  <div className="grid grid-cols-3 gap-2 mt-4">
                    {imagePreviews.map((preview, index) => (
                      <div key={index} className="relative">
                        <img 
                          src={preview} 
                          alt={`Preview ${index}`} 
                          className="w-full h-20 object-cover rounded-lg"
                        />
                        <button
                          type="button"
                          onClick={() => removeImage(index)}
                          className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
                        >
                          <XCircleIcon className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t">
                <button
                  type="button"
                  onClick={() => setShowImageModal(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  Fermer
                </button>
                {images.length > 0 && (
                  <button
                    onClick={handleImageUpload}
                    className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                  >
                    Upload ({images.length} image(s))
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

export default Produits;