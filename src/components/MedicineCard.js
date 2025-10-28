import React from 'react';
import { Package, Building2, Pill, Users } from 'lucide-react';

const MedicineCard = ({ medicine }) => {
  const {
    medicine_name,
    salt_composition,
    packagingType,
    pack,
    marketed_by,
    confidence = 85,
    dosage,
    ingredients_count
  } = medicine;

  const getConfidenceColor = (score) => {
    if (score >= 90) return '#28a745';
    if (score >= 75) return '#ffc107';
    return '#dc3545';
  };

  return (
    <div className="medicine-card fade-in">
      <h3 className="medicine-name">{medicine_name}</h3>
      
      {salt_composition && salt_composition !== 'Not specified' && (
        <p className="medicine-composition">
          <strong>Composition:</strong> {salt_composition}
        </p>
      )}

      <div className="medicine-details">
        <div className="detail-item">
          <span className="detail-label">
            <Package size={14} /> Packaging
          </span>
          <span className="detail-value">
            <span className="packaging-type">{packagingType}</span>
          </span>
        </div>

        <div className="detail-item">
          <span className="detail-label">
            <Pill size={14} /> Pack Size
          </span>
          <span className="detail-value">{pack}</span>
        </div>

        <div className="detail-item">
          <span className="detail-label">
            <Building2 size={14} /> Manufacturer
          </span>
          <span className="detail-value manufacturer">{marketed_by}</span>
        </div>

        {ingredients_count && (
          <div className="detail-item">
            <span className="detail-label">
              <Users size={14} /> Ingredients
            </span>
            <span className="detail-value">{ingredients_count} active</span>
          </div>
        )}
      </div>

      <div className="confidence-score">
        <span className="confidence-text">
          Match: {confidence}%
        </span>
        <div className="confidence-bar">
          <div 
            className="confidence-fill"
            style={{ 
              width: `${confidence}%`,
              background: getConfidenceColor(confidence)
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default MedicineCard;