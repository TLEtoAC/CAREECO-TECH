import React from 'react';

const SearchFilters = ({ filters, onFiltersChange }) => {
  const handleFilterChange = (key, value) => {
    onFiltersChange({
      ...filters,
      [key]: value
    });
  };

  const packagingTypes = [
    'All Types',
    'strip or blister pack',
    'tablet',
    'capsule',
    'injection',
    'syrup',
    'vial',
    'packet'
  ];

  const manufacturers = [
    'All Manufacturers',
    '3A Pharmaceuticals',
    '3C Health Solution Pvt Ltd',
    '3D Healthcare',
    'GSK Pharmaceuticals',
    'Generic Pharma Ltd',
    '1Mile Healthcare'
  ];

  const sortOptions = [
    { value: 'relevance', label: 'Relevance' },
    { value: 'name', label: 'Name A-Z' },
    { value: 'manufacturer', label: 'Manufacturer' },
    { value: 'packaging', label: 'Packaging Type' }
  ];

  return (
    <div className="filters-section fade-in">
      <div className="filter-group">
        <label className="filter-label">Packaging Type</label>
        <select
          className="filter-select"
          value={filters.packagingType}
          onChange={(e) => handleFilterChange('packagingType', e.target.value)}
        >
          {packagingTypes.map(type => (
            <option key={type} value={type === 'All Types' ? '' : type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">Manufacturer</label>
        <select
          className="filter-select"
          value={filters.manufacturer}
          onChange={(e) => handleFilterChange('manufacturer', e.target.value)}
        >
          {manufacturers.map(manufacturer => (
            <option key={manufacturer} value={manufacturer === 'All Manufacturers' ? '' : manufacturer}>
              {manufacturer}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">Sort By</label>
        <select
          className="filter-select"
          value={filters.sortBy}
          onChange={(e) => handleFilterChange('sortBy', e.target.value)}
        >
          {sortOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default SearchFilters;