import React from 'react';

const ScripDropdown = ({ formOptions,scrip,setScrip }) => {
  const scripEntries = formOptions?.scrips ? Object.entries(formOptions.scrips) : [];

  
  return (
    <select value={scrip} onChange={(e) => setScrip(e.target.value)}>
      <option value="" disabled>
          Select an option
        </option>
        
      {scripEntries.map(([key, value]) => (
        <option key={key} value={key}>
          {value.name}
        </option>
      ))}
    </select>
  );
};

export default ScripDropdown;
