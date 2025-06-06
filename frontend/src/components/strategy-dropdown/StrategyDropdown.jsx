import React from 'react';

const StrategyDropdown = ({ formOptions,strategy,setStrategy }) => {
  const strategyEntries = formOptions?.strategies ? Object.entries(formOptions.strategies) : [];

  
  return (
    <select value={strategy} onChange={(e) => setStrategy(e.target.value)}>
        <option value="" disabled>
          Select an option
        </option>
        
      {strategyEntries.map(([key, value]) => (
        
        <option key={key} value={key}>
          {value}
        </option>
      ))}
    </select>
  );
};

export default StrategyDropdown;
